# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tramline/simplefilter.py
# Compiled at: 2006-11-08 05:39:19
import os, shutil

def log(text):
    f = open('/tmp/tramline.log', 'a')
    f.write(text)
    f.write('\n')
    f.close()


def inputfilter(filter):
    if filter.req.method != 'POST':
        filter.disable()
        return
    f = open('/tmp/filtertest.txt', 'ab')
    log('first read')
    s = filter.read()
    while s:
        log('writing (%s)' % len(s))
        f.write(s)
        f.flush()
        filter.write(s)
        log('loop read')
        s = filter.read()

    if s is None:
        log('closing')
        filter.close()
        raise 'error'
    f.close()
    return


def requesthandler(req):
    fs = util.FieldStorage(req)
    for key in fs.keys():
        value = fs[key]
        if isinstance(value, util.Field):
            f = open(os.path.join('/tmp/dumpingground', value.filename), 'wb')
            shutil.copyfileobj(value.file, f)
            f.close()

    return apache.DECLINED