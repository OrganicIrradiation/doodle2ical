#!/usr/bin/python
# Filename: doodle2ics.py

from datetime import datetime
from flask import Flask
import HTMLParser
from icalendar import Calendar, Event
import json
import re
import string
import urllib2
import uuid

app = Flask(__name__)

class DoodleNotFound(Exception):
    pass

def doodle2ics(doodleid):
    try:
        doodleid = re.findall(r'http.*?doodle\.com\/(.*?)\/', doodleid)[0]
    except IndexError:
        pass
    url = 'https://doodle.com/'+doodleid+'/admin#table'

    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError, error:
        if error.code == 404:
            raise DoodleNotFound()

    data = page.read()
    poll_data = json.loads(re.findall(r"data.poll\s*=\s*(.*);", data)[0])
    poll_desc = HTMLParser.HTMLParser().unescape(poll_data['descriptionHTML'])
    poll_desc = poll_desc.replace('<br/>', ' -- ')

    cal = Calendar()
    cal.add('prodid', '-//doodle2ics//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'Doodle: {0}'.format(poll_data['title']))
    cal.add('x-wr-caldesc', poll_desc)
    for entry in poll_data['participants']:
        try:
            time_id = string.find(entry[u'preferences'], u'y')
            time_start = [v for v in poll_data['fcOptions'] if v[u'id'] == time_id][0][u'start']
            time_end = [v for v in poll_data['fcOptions'] if v[u'id'] == time_id][0][u'end']
            time_start = datetime.utcfromtimestamp(time_start)
            time_end = datetime.utcfromtimestamp(time_end)

            event = Event()
            event.add('summary', entry[u'name'])
            event.add('dtstamp', datetime.now())
            event.add('dtstart', time_start)
            event.add('dtend', time_end)
            event.add('uid', str(uuid.uuid4()))

            cal.add_component(event)
        except IndexError:
            # 'Could not find timeID for '+entry[u'name']
            pass

    return cal.to_ical()

@app.route('/<doodleid>.ical')
def process_doodle(doodleid):
    try:
        outfile = doodle2ics(doodleid)
        return outfile
    except DoodleNotFound:
        return 'Doodle ID #'+doodleid+' not found.', 404

@app.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
