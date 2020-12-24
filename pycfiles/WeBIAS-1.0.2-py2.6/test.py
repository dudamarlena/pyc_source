# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/data/examples/programs/test.py
# Compiled at: 2015-04-13 16:10:38
from optparse import OptionParser
import tempfile, os, re, sys
parser = OptionParser()
parser.add_option('--name', dest='name')
parser.add_option('--mood', type=int, dest='mood')
(options, args) = parser.parse_args()
mresp = {0: "that's great", 
   1: 'nice to meet you', 
   2: 'please discuss this matter with ELIZA', 
   3: 'CowboyNeal likes you too'}
response = 'Hello %s, %s.' % (options.name, mresp[options.mood])
print '<TestResult><response>%s</response></TestResult>' % response