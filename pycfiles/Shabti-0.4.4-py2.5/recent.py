# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/pyblosxom/data/blog/plugins/recent.py
# Compiled at: 2009-09-05 11:34:12
from Pyblosxom import tools, entries
import time, os

def cb_filelist(args):
    request = args['request']
    data = request.getData()
    config = request.getConfiguration()
    allentries = tools.Walk(request, config['datadir'])
    i = 0
    recent = []
    x = {}
    for a in allentries:
        timetuple = tools.filestat(request, a)
        entrystamp = time.mktime(timetuple)
        tstamp = entrystamp
        a_path = a[len(config['datadir']):a.rfind(os.sep)]
        fn = a[a.rfind(os.sep) + 1:a.rfind('.')]
        x[tstamp] = a

    e = x.keys()
    e.sort()
    e.reverse()
    f = e[0:16]
    for g in f:
        fn = x[g]
        e = entries.fileentry.FileEntry(request, fn, data['root_datadir'])
        url = '%s/%s/%s' % (config.get('base_url'), e.get('absolute_path'), e.get('fn'))
        title = e.get('title')
        recent.append('<a href="%s" title="%s, posted %s">%s</a>' % (url, title, e.getMetadata('date'), title))

    data['recent'] = ('<br/>').join(recent)