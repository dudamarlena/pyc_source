# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/underlay/pages/HelpOnInstalling(2f)ApacheOnLinuxFtp/attachments/explore.py
# Compiled at: 2010-04-25 12:11:22
import os.path, os, sys
try:
    __file__
except NameError:
    __file__ = '?'

print 'Content-type: text/html\n\n<html>\n<head>\n <title>Python Exploration</title>\n</head>\n<body>\n <table border=1>\n <tr><th colspan=2>1. System Information</th></tr>\n <tr><td>Python</td><td>%s</td></tr>\n <tr><td>Platform</td><td>%s</td></tr>\n <tr><td>Absolute path of this script</td><td>%s</td></tr>\n <tr><td>Filename</td><td>%s</td></tr>\n' % (sys.version,
 sys.platform,
 os.path.abspath('.'),
 __file__)
print '<th colspan=2>2. Environment Variables</th>'
for variable in os.environ:
    print '<tr><td>%s</td><td>%s</td></tr>\n' % (variable, os.environ[variable])

print '\n</table>\n</body>\n</html>\n'