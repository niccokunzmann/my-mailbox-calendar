My Mailbox Calendar
===================

Create an online calendar by inviting this application to your events:
1. Invite the mailbox calendar to your events, replacing "test" with a
   name of your liking:
   [my.mailbox.calendar+test@gmail.com](mailto:my.mailbox.calendar+test@gmail.com).
2. View that the event is actually being processed. Here, also replace
   "test" with the name you chose before:  
   https://my-mailbox-calendar.herokuapp.com/test.html
3. Subscribe to the calendar with any application using ICS.  
   https://my-mailbox-calendar.herokuapp.com/test.ics

## Deployment

You can deploy the app using Heroku.
There is a free plan.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## How it works

This service uses an IMAP connection to the mailbox.
When a request is made, the calendar is filtered for the name of the calendar
and the e-mails are downloaded.
Each event e-mail is processed for ICAL-entries.

Tested with:

- Thunderbird
- Lotus Notes

If you like to have it tested with other applications, 

1. Create an event and invite my.mailbox.calendar+APPLICATION@gmail.com
2. Edit this event and send the changed - see if it changed.
3. Delete this event - see if it disappeared.
4. Open an issue for this application and mention the events you created.
5. In a pull request, add the sent/received emails and add them to the tests.

Related Projects
----------------

- [Open Web Calendar](https://github.com/niccokunzmann/open-web-calendar/)
