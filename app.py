#!/usr/bin/env python3

import imaplib
import click
from pprint import pprint
import email

def download_mails():
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login(user, password)
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print('Message %s\n%s\n' % (num, data[0][1]))
    M.close()
    M.logout()


@click.command()
@click.argument("imap_host", envvar="IMAP_HOST", type=str)
@click.argument("user", envvar="IMAP_USER", type=str)
@click.argument("password", envvar="IMAP_PASSWORD", type=str)
@click.option('--ssl/--no-ssl', default=True, help="Whether to connect using SSL encryption. Encryption is used by default.")
def download(imap_host, user, password, ssl):
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
    port_index = imap_host.rfind(":")
    port = (993 if port_index == -1 else int(imap_host[port_index + 1:]))
    host = (imap_host if port_index == -1 else imap_host[:port_index])
    M = connect(host, port)
    print(user, password)
    M.login(user, password)
    M.select()
    # imap search cen be optimized, see
    # RFC 3501, Section 6.4.4. http://www.faqs.org/rfcs/rfc3501.html
    typ, data = M.search(None, 'ALL')
    pprint((typ, data))
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        m = email.message_from_bytes(data[0][1])
        for header, value in m.items():
            print(header, value)
        #print('Message %s\n%s\n' % (num, data[0][1]))
    M.close()
    M.logout()

if __name__ == '__main__':
    download()
