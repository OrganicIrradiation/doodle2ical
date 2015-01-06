doodle2ics
==========================

Module that takes a Doodle.com administration page and converts the entries into an iCal file.  It assumes the following Doodle settings:

  * **Hidden poll** Confidential participation: Only you can see the answers.
  * **Participant can only choose one option** By default all options are selectable. This setting limits the choice to one option per participant.
  * **Limit the number of participants per option** Poll as registration form: As soon as the indicated limit has been reached, the respective option is no longer available. (setting: 1)

##Prerequisites
Tested with Python 2.7.8 and the following libraries (tested versions in parentheses):

  * icalendar (3.7)
