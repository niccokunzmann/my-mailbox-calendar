My Mailbox Calendar
===================

Create an online calendar by inviting this application to your events:
1. Invite the mailbox calendar to your events, replacing TEST with a
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

Heroku uses [gunicorn](http://flask.pocoo.org/docs/dev/deploying/wsgi-standalone/#gunicorn)
to run the server, see the [Procfile](Procfile).


