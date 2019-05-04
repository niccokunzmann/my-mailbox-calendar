import icalendar
import cgi

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
    
    mime_type = "text/calendar"

    def __init__(self):
        """Create a mailbox calendar object."""
        self.events = {}
        
    @staticmethod
    def _get_last_modified(event):
        """Return the last modification date of an event."""
        date = event.get("LAST-MODIFIED")
        if date is not None:
            return date.dt
        return None

    def add_event(self, event):
        """Add an event taking the time into account it was changed."""
        uid = event.get("UID")
        other = self.events.get(uid, None)
        if other:
            for make_comparable in [
                    self._get_last_modified,
                    lambda event: event.get("SEQUENCE")]:
                event_age = make_comparable(event)
                other_age = make_comparable(other)
                if event_age is None or other_age is None:
                    continue
                if event_age > other_age or \
                        event_age == other_age and \
                        event.get(METHOD) in METHODS_TO_DELETE:
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
            if mime_type != self.mime_type or part.is_multipart():
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
            else:
                assert method in METHODS_TO_DELETE, "Invalid method {}".format(method)
        return events

    def as_icalendar(self):
        calendar = icalendar.Calendar()
        for event in self.list_events():
            calendar.add_component(event)
        return calendar

