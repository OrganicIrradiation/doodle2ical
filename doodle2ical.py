#!/usr/bin/python
# Filename: doodle2ical.py

from flask import Flask
import HTMLParser
from icalendar import Calendar, Event
import arrow
import json
import re
import string
import urllib2
import uuid

app = Flask(__name__)

class DoodleNotFound(Exception):
    pass

def get_poll_data(doodleid):
    try:
        doodleid = re.findall(r'http.*?doodle\.com\/(.*?)\/', doodleid)[0]
    except IndexError:
        pass
    url = 'https://doodle.com/'+doodleid+'/admin#table'

    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError as error:
        if error.code == 404:
            raise DoodleNotFound()

    data = page.read()
    poll_data = json.loads(re.findall(r"doodleJS\.data\,\ (.*)\);\n", data)[0])
    return poll_data['poll']

def doodle2ical(doodleid, doodletz):
    poll_data = get_poll_data(doodleid)
    poll_desc = HTMLParser.HTMLParser().unescape(poll_data['descriptionHTML'])
    poll_desc = poll_desc.replace('<br/>', ' -- ')

    cal = Calendar()
    cal.add('prodid', '-//doodle2ical//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'Doodle: {0}'.format(poll_data['title']))
    cal.add('x-wr-caldesc', poll_desc)
    cal.add('x-wr-timezone', doodletz)
    for entry in poll_data['participants']:
        try:
            time_id = string.find(entry[u'preferences'], u'y')
            time_start = [v for v in poll_data['fcOptions'] if v[u'id'] == time_id][0][u'start']
            time_end = [v for v in poll_data['fcOptions'] if v[u'id'] == time_id][0][u'end']
            time_start = arrow.get(time_start)
            time_end = arrow.get(time_end)
            # Add time zone
            time_start = arrow.get(time_start.datetime, doodletz)
            time_end = arrow.get(time_end.datetime, doodletz)
            # Need to shift time 12 hours:
            time_start = time_start.replace(hours=-12)
            time_end = time_end.replace(hours=-12)

            event = Event()
            event.add('summary', entry[u'name'])
            event.add('dtstamp', arrow.now().datetime)
            event.add('dtstart', time_start.datetime)
            event.add('dtend', time_end.datetime)
            event.add('uid', str(uuid.uuid4()))

            cal.add_component(event)
        except IndexError:
            # 'Could not find timeID for '+entry[u'name']
            pass

    return cal.to_ical()

@app.route('/<contintent>/<city>/<doodleid>.ical')
def process_doodle(contintent, city, doodleid):
    """Make sure URL is formatted: server/<contintent>/<city>/<doodlid>.ical"""
    try:
        doodletz = '{0}/{1}'.format(contintent, city)
        data = doodle2ical(doodleid, doodletz)
        outfile = app.make_response(data)
        outfile.mimetype = 'text/calendar'
        return outfile
    except DoodleNotFound:
        return 'Doodle ID #'+doodleid+' not found.', 404

@app.route('/')
def front_page():
	"""Return an empty front page"""
	return '', 204

@app.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == "__main__":
    app.run(debug=True)
