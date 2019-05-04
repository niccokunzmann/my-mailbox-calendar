#!/usr/bin/env python3

import imaplib
import click
from pprint import pprint
import email
from flask import Flask, Response, request, redirect
import mailboxcalendar

# changing the text for a variable here, also change it in the app.json
@click.command(context_settings={"ignore_unknown_options":True})
@click.option("--port", envvar="PORT", type=int, default=5000, help="Port to run the web server on.")
@click.argument("imap_host", envvar="IMAP_HOST", type=str)
@click.argument("imap_user", envvar="IMAP_USER", type=str)
@click.argument("imap_password", envvar="IMAP_PASSWORD", type=str)
@click.argument("args", nargs=-1) # see https://click.palletsprojects.com/en/7.x/arguments/#variadic-arguments
@click.option('--ssl/--no-ssl', envvar="IMAP_SSL", default=True, help="Whether to connect to the IMAP server using SSL encryption. Encryption is used by default.")
@click.option('--debug', '-d', envvar="FLASK_DEBUG", is_flag=True, help="Enable debugging on the server.")
@click.option('--check/--no-check', envvar="IMAP_CHECK", is_flag=True, help="Check whether the app can connect to the IMAP server with the given credentials.")
@click.option('--open-web-calendar', envvar="OPEN_WEB_CALENDAR_URL", default="https://open-web-calendar.herokuapp.com", help="The url of the open web calendar server to display an html page containing the calendar.")
@click.option('--https', envvar="HTTPS", default=False, help="Whether the server uses https.")
@click.option('--start/--no-start', envvar="START", default=True, help="Whether the app should be started.")
def get_app(port, imap_host, imap_user, imap_password, ssl, debug, check, open_web_calendar, https, start, args):
    """Download the messages from a server and create the ICS files.
    
    These arguments can be passed as parameters to the script or as
    environment variables:
    
    IMAP_HOST is the IMAP server to connect to.
    Examples: \"imap.gmail.com\", \"imap.gmail.com:993\"
    
    IMAP_USER is the username on the server for login.
    Example: \"my.mailbox.calendar\x40gmail.com\"
    
    IMAP_PASSWORD is the password for the imap_user.
    """
    connect = (imaplib.IMAP4_SSL if ssl else imaplib.IMAP4)
    imap_port_index = imap_host.rfind(":")
    imap_port = (993 if imap_port_index == -1 else int(imap_host[imap_port_index + 1:]))
    imap_host = (imap_host if imap_port_index == -1 else imap_host[:imap_port_index])
    def get_messages(calendar_name):
        """Iterate over the messages for a calendar_name.
        
        In my.mailbox.calendar\x40gmail.com this looks for messages to
        my.mailbox.calendar+calendar_name\x40gmail.com.
        """
        M = connect(imap_host, imap_port)
        M.login(imap_user, imap_password)
        M.select()
        assert "\"" not in calendar_name
        # imap search cen be optimized, see
        # RFC 3501, Section 6.4.4. http://www.faqs.org/rfcs/rfc3501.html
        typ, data = M.search(None, 'TO', "\"+" + calendar_name + "@\"")
        for num in data[0].split():
            typ, data = M.fetch(num, '(RFC822)')
            message = email.message_from_bytes(data[0][1])
            yield message
        M.close()
        M.logout()
    
    app = Flask(__name__, template_folder="templates")
    
    @app.route("/<calendar_name>.ics")
    def get_ical_calendar(calendar_name):
        calendar = mailboxcalendar.MailboxCalendar()
        for message in get_messages(calendar_name):
            calendar.receive(message)
        icalendar = calendar.as_icalendar()
        icalendar.add("CN", calendar_name)
        response = Response(
            icalendar.to_ical(),
            mimetype=calendar.mime_type)
        response.headers['Access-Control-Allow-Origin'] = '*'
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
        response.headers['Access-Control-Allow-Headers'] = \
            request.headers.get("Access-Control-Request-Headers")
        return response
    
    
    @app.route("/<calendar_name>.html")
    def get_web_page(calendar_name):
        host = request.headers.get("host")
        assert host, "A host is required to show the calendar."
        url = ( open_web_calendar + "/calendar.html?url=" +
            ("https" if https else "http") + "://" + host + "/" +
            calendar_name + ".ics"
        )
        return redirect(url)
        
    @app.route("/")
    def index():
        return redirect("https://github.com/niccokunzmann/my-mailbox-calendar#readme")
        
    if check:
        for message in get_messages("startup"): # check if configured to work later
            pass
    if start:
        app.run(debug=debug, host="0.0.0.0", port=port)
    return app


app = get_app()

