"""
This module contains all the interaction with the mailbox online.
"""
import imaplib
import email

class MailboxInteraction:    

    def __init__(self, calendar_name, imap_host, imap_port, imap_user, imap_password, use_ssl=True):
        self.calendar_name = calendar_name
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.imap_user = imap_user
        self.imap_password = imap_password
        self.connect = (imaplib.IMAP4_SSL if use_ssl else imaplib.IMAP4)
        assert "\"" not in calendar_name
        
    def get_messages(self):
        """Iterate over the messages for a calendar_name.
        
        In my.mailbox.calendar\x40gmail.com this looks for messages to
        my.mailbox.calendar+calendar_name\x40gmail.com.
        """
        M = self.connect(self.imap_host, self.imap_port)
        M.login(self.imap_user, self.imap_password)
        try:
            M.select()
            # imap search can be optimized, see
            # RFC 3501, Section 6.4.4. http://www.faqs.org/rfcs/rfc3501.html
            typ, data = M.search(None, 'TO', "\"+" + self.calendar_name + "@\"")
            email_ids = data[0].split()
            # fetching several mails at once
            # see https://stackoverflow.com/a/3581682
            status, data = M.fetch(b','.join(email_ids), '(RFC822)')
            if status != "OK":
                raise ValueError("Could not fetch messages for {}".format(self.calendar_name))
            messages = []
            for i in range(len(email_ids)):
                message = email.message_from_bytes(data[i * 2][1])
                messages.append(message)
        finally:
            M.close()
            M.logout()
        return messages
        
