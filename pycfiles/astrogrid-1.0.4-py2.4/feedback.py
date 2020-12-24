# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/feedback.py
# Compiled at: 2007-11-30 08:02:11
import os, tempfile, base64, urllib, urllib2, datetime
try:
    ed = os.environ['EDITOR']
except KeyError:
    if os.name == 'posix':
        ed = 'vi'
    else:
        ed = 'notepad'

text = 'Your email:\nSubject:\n\ntext\n\n'

def calleditor(filename):
    os.system('%s %s' % (ed, filename))


def submit():
    print 'Please complete the next form using the editor (%s)' % ed
    print 'Press [Return]'
    raw_input()
    fname = tempfile.mktemp()
    open(fname, 'w').write(text)
    calleditor(fname)
    feedback = open(fname).read()
    now = datetime.datetime.now()
    feedback = 'Date: ' + now.strftime('%Y%m%dT%H:%M:%S') + '\n' + feedback
    os.unlink(fname)
    try:
        urllib2.urlopen('http://casu.ast.cam.ac.uk/ag/portal/server.py/feedback', urllib.urlencode({'data': feedback})).read()
        print 'Thanks for your feedback'
    except:
        pass