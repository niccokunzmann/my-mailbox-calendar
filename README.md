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
When a request is made, the emails are filtered for the name of the calendar
and are downloaded.
Each event e-mail is processed for ICAL-entries.

Tested with:

- Thunderbird
- Lotus Notes

If you like to have it tested with other applications, 

1. Create an event and invite my.mailbox.calendar+APPLICATION@gmail.com
2. Edit this event and send the changes - see if it changed.
3. Create a new event and delete it - see if it disappeares.
4. Open an issue for this application and mention the events you created.
5. In a pull request, add the sent/received emails and add them to the tests.

Development
-----------

This application uses Python3.

1. Get the source code
    ```shell
    git clone https://github.com/niccokunzmann/my-mailbox-calendar.git
    ```
2. (Optional) Install virtualenv  
    ```shell
    pip install virtualenv
    virtualenv -p python3 ENV
    source ENV/bin/activate # do this each time you open a new console
    ```
3. Install the packages  
    ```shell
    python3 -m pip install -r requirements.txt -r test-requirements.in
    ```
4. Run the tests  
    ```
    pytest
    ```
5. Launch the application  
    For environment variables and command line arguments, run
    ```shell
    python3 app.py --help
    ```
    To launch the application with the correct credentials, use
    ```shell
    IMAP_HOST=imap.gmail.com:993 IMAP_USER='...@googlemail.com' IMAP_PASSWORD='...' ./app.py --debug
    ```

Related Projects
----------------

- [Open Web Calendar](https://github.com/niccokunzmann/open-web-calendar/)
