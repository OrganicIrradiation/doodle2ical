from datetime import datetime, date
from flask import Flask
from icalendar import Calendar, Event
import json
import pytz
import re
import string
import urllib2
import uuid

import pyDoodleToICS

app = Flask(__name__)

def display(cal):
    return cal.to_ical()

@app.route('/<doodleid>.ical')
def processDoodle(doodleid):
    try:
        outfile = pyDoodleToICS.DoodleToICS(doodleid)
        return outfile
    except pyDoodleToICS.DoodleNotFound:
        return 'Doodle ID #'+doodleid+' not found.', 404

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == '__main__':
    app.run()
