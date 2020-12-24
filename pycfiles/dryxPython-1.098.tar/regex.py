# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/regex.py
# Compiled at: 2013-08-06 05:22:05
"""
**regex**

Created by David Young on date 2012-10-24
If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
p<Var> = variable formated in the way I want it output to file or screen
xxx = come back here and do some more work

"""
import sys, os, re
raHMS_colon = '^\\+?([0-9]|([0-1][0-9])|([2][0-3]))(:)[0-5][0-9](:)[0-5][0-9]((\\.\\d{1,})?)$'
raHMS_space = '^\\+?([0-9]|([0-1][0-9])|([2][0-3]))( )[0-5][0-9]( )[0-5][0-9]((\\.\\d{1,})?)$'
raHMS_letters = '^\\+?([0-9]|([0-1][0-9])|([2][0-3]))(h )[0-5][0-9](m )[0-5][0-9]((\\.\\d{1,})?s)$'
decDMS_colon = '^([\\+\\-]?([0-9]|[0-8][0-9]))(:)[0-5][0-9](:)[0-5][0-9](\\.\\d{1,})?$'
decDMS_space = '^([\\+\\-]?([0-9]|[0-8][0-9]))( )[0-5][0-9]( )[0-5][0-9](\\.\\d{1,})?$'
decDMS_space = '^([\\+\\-]?([0-9]|[0-8][0-9]))( )[0-5][0-9]( )[0-5][0-9](\\.\\d{1,})?$'