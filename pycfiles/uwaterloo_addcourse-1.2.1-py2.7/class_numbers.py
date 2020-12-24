# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/class_numbers.py
# Compiled at: 2015-04-26 10:52:15
import urllib, urllib2, re, time, bs4

def nearest_term(t=time.time()):
    """Return the number for the nearest term."""
    t = time.localtime(t)
    y = t.tm_year % 100
    m = int((t.tm_mon + 2) / 4) * 4 + 1
    return 1000 + y * 10 + m


def numbers(course):
    """Return a list of class numbers corresponding to course."""
    subject, number = re.findall('[a-zA-Z]+|[0-9]+', course)
    query = {'level': 'under', 'sess': nearest_term(), 
       'subject': subject.upper(), 
       'cournum': number}
    f = urllib2.urlopen(course_query_url, urllib.urlencode(query))
    a = bs4.BeautifulSoup(f.read())
    f.close()
    return [ int(n.parent.previous) for n in a.findAll(text=re.compile('LEC'))
           ]


course_query_url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'