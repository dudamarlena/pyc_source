# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/handle_error.py
# Compiled at: 2004-05-24 13:56:39
import traceback, sys, string, time, socket, os, who_calls
DUMP_DIR = '/tmp/bugs'
Warning = 'handle_error.Warning'
LV_MESSAGE = 'LV_MESSAGE'
LV_WARNING = 'LV_WARNING'
LV_ERROR = 'LV_ERROR'
Count = 0
gErrorCount = 0
DISABLE_DUMP = 0

def exceptionReason():
    return '%s.%s' % (str(sys.exc_type), str(sys.exc_value))


def exceptionString():
    tb_list = traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
    return string.join(tb_list, '')
    import StringIO
    sfp = StringIO.StringIO()
    traceback.print_exc(file=sfp)
    exception = sfp.getvalue()
    sfp.close()
    return exception


def handleException(msg=None, lvl=LV_ERROR, dump=1):
    global gErrorCount
    gErrorCount = gErrorCount + 1
    tb_list = traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
    if msg:
        sys.stderr.write('%s\n' % msg)
    else:
        msg = 'Unhandled Exception'
    sys.stderr.write(string.join(tb_list, ''))
    try:
        if dump:
            dump_bug(lvl, 'handleException', msg, string.join(tb_list, ''))
    except:
        handleException('Unable to dump_bug', dump=0)


def handleWarning(msg=''):
    header = '*** handleWarning: %s\n' % msg
    sys.stderr.write(header)
    tb = who_calls.pretty_who_calls(strip=1) + '\n'
    sys.stderr.write(tb)
    try:
        dump_bug(LV_WARNING, 'handleException', msg, tb)
    except:
        handleException('Unable to dump_bug', dump=0)


def checkPaths():
    paths = (DUMP_DIR, os.path.join(DUMP_DIR, 'tmp'), os.path.join(DUMP_DIR, 'new'))
    for path in paths:
        if not os.path.isdir(path):
            os.mkdir(path, 493)


def dump_bug(level, etype, msg, location=None, nhdf=None):
    global Count
    global DISABLE_DUMP
    if DISABLE_DUMP:
        return
    now = int(time.time())
    pid = os.getpid()
    import neo_cgi, neo_util
    hdf = neo_util.HDF()
    hdf.setValue('Required.Level', level)
    hdf.setValue('Required.When', str(int(time.time())))
    hdf.setValue('Required.Type', etype)
    hdf.setValue('Required.Title', msg)
    hdf.setValue('Optional.Hostname', socket.gethostname())
    if location:
        hdf.setValue('Optional.Location', location)
    for (key, value) in os.environ.items():
        hdf.setValue('Environ.%s' % key, value)

    Count = Count + 1
    fname = '%d.%d_%d.%s' % (now, pid, Count, socket.gethostname())
    checkPaths()
    tpath = os.path.join(DUMP_DIR, 'tmp', fname)
    npath = os.path.join(DUMP_DIR, 'new', fname)
    hdf.writeFile(tpath)
    os.rename(tpath, npath)