# from https://docs.python.org/3.7/library/imaplib.html
import getpass, imaplib, sys

M = imaplib.IMAP4_SSL("imap.gmail.com")
user = sys.argv[1]
password = sys.argv[2]
M.login(user, password)
M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
M.close()
M.logout()
