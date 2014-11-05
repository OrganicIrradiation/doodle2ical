#!/usr/bin/python
# Filename: pyDoodleToICS.py

from datetime import datetime, date
from icalendar import Calendar, Event
import json
import re
import string
import urllib2
import uuid

class DoodleNotFound(Exception):
    pass

def DoodleToICS(doodleid):
    doodleid = 'ystm2g294htfxzn942suqpup'
    url = 'http://doodle.com/'+doodleid+'/admin#table'
    
    try:
        page=urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        if e.code == 404:
            raise DoodleNotFound()
        
    data = page.read()
    pollTitle = re.search(r'<title>Doodle: (.*)',data).group(1)
    pollData = re.search(r"doodleJS.data.poll\s*=\s*(.*);", data).group(1)
    pollDatesAndTimes = json.loads(re.search(r"\"fcOptions\"\:(\[\{.*?\}\])", pollData).group(1))
    pollParticipants = json.loads(re.search(r"\"participants\"\:(\[\{.*?\}\])", pollData).group(1))
    
    cal = Calendar()
    cal.add('prodid', '-//pyDoodleToICSFlaskServer//')
    cal.add('version', '2.0')
    for entry in pollParticipants:
        try:
            timeID = string.find(entry[u'preferences'],u'y')
            timeStart = [value for value in pollDatesAndTimes if value[u'id']==timeID][0][u'start']
            timeEnd = [value for value in pollDatesAndTimes if value[u'id']==timeID][0][u'end']
            timeStart = datetime.fromtimestamp(timeStart)
            timeEnd = datetime.fromtimestamp(timeEnd)
            
            event = Event()
            event.add('summary', entry[u'name'])
            event.add('dtstart', timeStart)
            event.add('duration', timeEnd-timeStart)
            event.add('dtstamp', date.today())
            event.add('uid', str(uuid.uuid4()))
            
            cal.add_component(event)
        except IndexError:
            # 'Could not find timeID for '+entry[u'name']
            pass

    return cal.to_ical()
