import icalendar
import cgi

MIME_TYPE_CALENDAR = "text/calendar"
METHOD = "X-METHOD"
METHODS_TO_ADD = ["REQUEST"]
METHODS_TO_DELETE = ["CANCEL"]

def is_event(component):
    """Return whether a component is a calendar event."""
    return isinstance(component, icalendar.cal.Event)

def iter_events(calendar_content):
    """Iterate over all the events of a calendar."""
    calendar = icalendar.Calendar.from_ical(calendar_content)
    for event in calendar.walk():
        if is_event(event):
            yield event


class MailboxCalendar:
    """A calendar which is nutured by emails."""

    def __init__(self):
        """Create a mailbox calendar object."""
        self.events = {}

    def add_event(self, event):
        """Add an event taking the time into account it was changed."""
        uid = event.get("UID")
        other = self.events.get(uid, None)
        if other:
            event_last_modified = event.get("LAST-MODIFIED")
            other_last_modified = other.get("LAST-MODIFIED")
            if event_last_modified and other_last_modified and \
                (   event_last_modified.dt > other_last_modified.dt or
                    event_last_modified.dt == other_last_modified.dt and
                    event.get(METHOD) in METHODS_TO_DELETE):
                self.events[uid] = event
        else:
            self.events[uid] = event

    def receive(self, email):
        """Receive an email.
        
        email is from the email module. (import email)
        """
        for part in email.walk():
            content_type = part.get("Content-Type", "")
            # parse header, see https://stackoverflow.com/a/36627725
            mime_type, arguments = cgi.parse_header(content_type)
            method = arguments.get("method", None)
            if mime_type != MIME_TYPE_CALENDAR or part.is_multipart():
                continue
            for event in iter_events(part.get_payload()):
                event.add(METHOD, method)
                self.add_event(event)


    def list_events(self):
        """Return a list of all events so far received."""
        events = []
        for event in self.events.values():
            method = event.get(METHOD)
            if method in METHODS_TO_ADD:
                events.append(event)
        return events
