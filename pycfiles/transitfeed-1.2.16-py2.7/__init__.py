# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/__init__.py
# Compiled at: 2018-01-24 00:52:58
"""This module is a library to help you create, read and write Google
Transit Feed files. Refer to the feed specification, available at
https://developers.google.com/transit/gtfs/, for a
complete description how the transit feed represents a transit schedule. This
library supports all required parts of the specification but does not yet
support all optional parts. Patches welcome!

Before transitfeed version 1.2.4 all our library code was distributed in a
one file module, transitfeed.py, and could be used as

  import transitfeed
  schedule = transitfeed.Schedule()

At that time the module (one file, transitfeed.py) was converted into a
package (a directory named transitfeed containing __init__.py and multiple .py
files). Classes and attributes exposed by the old module may still be imported
in the same way. Indeed, code that depends on the library <em>should</em>
continue to use import commands such as the above and ignore _transitfeed.

To import the transitfeed module you should do something like:

  import transitfeed
  schedule = transitfeed.Schedule()
  ...

The specification describes several tables such as stops, routes and trips.
In a feed file these are stored as comma separeted value files. This library
represents each row of these tables with a single Python object. This object has
attributes for each value on the row. For example, schedule.AddStop returns a
Stop object which has attributes such as stop_lat and stop_name.

  Schedule: Central object of the parser
  GenericGTFSObject: A base class for each of the objects below
  Route: Represents a single route
  Trip: Represents a single trip
  Stop: Represents a single stop
  ServicePeriod: Represents a single service, a set of dates
  Agency: Represents the agency in this feed
  Transfer: Represents a single transfer rule
  TimeToSecondsSinceMidnight(): Convert HH:MM:SS into seconds since midnight.
  FormatSecondsSinceMidnight(s): Formats number of seconds past midnight into a string
"""
from util import *
from agency import *
from fareattribute import *
from farerule import *
from frequency import *
from gtfsfactory import *
from gtfsfactoryuser import *
from gtfsobjectbase import *
from loader import *
from problems import *
from route import *
from schedule import *
from serviceperiod import *
from shape import *
from shapelib import *
from shapeloader import *
from shapepoint import *
from stop import *
from stoptime import *
from transfer import *
from trip import *
from transitfeed.version import __version__