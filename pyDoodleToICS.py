from datetime import datetime, date
from icalendar import Calendar, Event
import json
import pytz
import re
import string
import urllib2
import uuid

url = raw_input('Doodle Administration URL: ')
timezone = raw_input('Time Zone (defaults to \'Europe/Berlin\'): ')

if not timezone:
    timezone = 'Europe/Berlin'

page=urllib2.urlopen(url)
data = page.read()
pollTitle = re.search(r'<title>Doodle: (.*)',data).group(1)
pollData = re.search(r"doodleJS.data.poll\s*=\s*(.*);", data).group(1)
pollDatesAndTimes = json.loads(re.search(r"\"fcOptions\"\:(\[.*?\])", pollData).group(1))
pollParticipants = json.loads(re.search(r"\"participants\"\:(\[.*?\])", pollData).group(1))

cal = Calendar()
cal.add('prodid', '-//pyDoodleToICS//')
cal.add('version', '2.0')
for entry in pollParticipants:
    try:
        timeID = string.find(entry[u'preferences'],u'y')
        timeStart = [value for value in pollDatesAndTimes if value[u'id']==timeID][0][u'start']
        timeEnd = [value for value in pollDatesAndTimes if value[u'id']==timeID][0][u'end']
        timeStart = datetime.fromtimestamp(timeStart,tz=pytz.timezone(timezone))
        timeEnd = datetime.fromtimestamp(timeEnd,tz=pytz.timezone(timezone))
        
        event = Event()
        event.add('summary', entry[u'name'])
        event.add('dtstart', timeStart)
        event.add('dtend', timeStart)
        event.add('duration', timeEnd-timeStart)
        event.add('dtstamp', date.today())
        event.add('uid', str(uuid.uuid4()))
        
        cal.add_component(event)
        
    except IndexError:
        print 'Could not find timeID for '+entry[u'name']

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
filename = ''.join(c for c in pollTitle+'.ics' if c in valid_chars)
f = open(filename, 'wb')
f.write(cal.to_ical())
f.close()
