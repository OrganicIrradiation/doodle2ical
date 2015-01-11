doodle2ical.py
==========================

doodle2ical that takes a Doodle.com administration page for either free or pro accounts and converts the entries into an iCalendar file that can be used in most calendar applications.  The module runs as a web server, so it can be used as a feed for Google Calendar and other calendar applications that accept a feed.

The app scrapes the Doodle calendar page, so it requires the unique identifier from an administration page URL (which includes additional authentication characters, in addition to those in a participation link). For example, a Doodle partcipation link might look something like this:

    https://www.doodle.com/saiou2ofo2nf2e1r

While the administration link would be something like:

    https://www.doodle.com/saiou2ofo2nf2e1rfjgsdgj1/admin#admin

In this case, the "ID" used by doodle2ical is the longer ID from the administration link: `saiou2ofo2nf2e1rfjgsdgj1` (note: this is a fake administration link). Using this administration link and the calendar's "base" timezone, you can use doodle2ical to generate an .ical file.  I have the current code running on a Heroku instance, so you are welcome to try your ID(s); however, I would recommend you run your own instances to avoid any security concerns:

    http://doodle2ical.herokuapp.com/<timezonecontinent>/<timezonecity>/<doodleid_here>.ical
    http://doodle2ical.herokuapp.com/Europe/Berlin/saiou2ofo2nf2e1rfjgsdgj1.ical

doodle2ical currently assumes the following Doodle settings:

  * **Hidden poll** Confidential participation: Only you can see the answers.
  * **Participant can only choose one option** By default all options are selectable. This setting limits the choice to one option per participant.
  * **Limit the number of participants per option** Poll as registration form: As soon as the indicated limit has been reached, the respective option is no longer available. (setting: 1)

## Running doodle2ical locally

Here are some quick instructions to try it out on your own computer. I am doing my development on a Mac so, I installed git and foreman (using Homebrew and Ruby gems):

    brew install git
    sudo gem install foreman

Once you have these, clone the repository into a local folder and install the prerequisites (preferably using a virtualenv):

    git clone https://github.com/OrganicIrradiation/doodle2ical.git
    pip install flask gunicorn icalendar

Try it out on your local machine by loading the Procfile using foreman:

    foreman start

You should get some feedback, for example:

    22:05:39 web.1  | started with pid 39815
    22:05:40 web.1  | [2015-01-06 22:05:40 +0100] [39815] [INFO] Starting gunicorn 19.1.1
    22:05:40 web.1  | [2015-01-06 22:05:40 +0100] [39815] [INFO] Listening at: http://0.0.0.0:5000 (39815)
    22:05:40 web.1  | [2015-01-06 22:05:40 +0100] [39815] [INFO] Using worker: sync
    22:05:40 web.1  | [2015-01-06 22:05:40 +0100] [39818] [INFO] Booting worker with pid: 39818

Then you can simply use your web browser or local calendar application to verify that the calendar file is correctly generated:

    http://localhost:5000/<timezonecontinent>/<timezonecity>/<doodleid_here>.ical

## Installation on Heroku

If you don't already have it, install the Heroku toolbelt and get yourself a Heroku account.

    brew install heroku-toolbelt

If everything seems ok, then you can create a heroku app:

    heroku login
    heroku create

And deploy it to your Heroku instance using:

    git push heroku master

Just make sure to reduce the number of processes:

    heroku ps:scale web=1