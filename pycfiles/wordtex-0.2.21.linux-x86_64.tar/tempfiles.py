# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/tempfiles.py
# Compiled at: 2013-11-12 16:48:22
"""
This module is created to extend the module tempfile. It handles things better
than tempfile, automatically deleting previous processes files if they have
not been used for a long time.

It will also be eventually extended to a new type of data, harddata. This data
type will automatically store it's variable if it hasn't been used in a while.

It uses the threading module after the first call of get_temp_file. If your
applicationc cannot support threading, then:
    Define your own THREAD_LOCK object to handle locking, make sure to set
        the global variable to the object you are using.
    set THREAD_HANDLED = True
    call create_temp_directory
    call THREAD_manage_harddata about every .5 seconds
    
"""
import sys, os, pdb, dbe, cPickle, time, shutil, re, tempfile, errors, system, textools
THREAD_HANDLED = False
THREAD_LOCK = None
THREAD_PERIOD = 30
DELETE_TMP_AFTER = 3600
ga = object.__getattribute__
sa = object.__setattr__
TIMER_FILE = 'pytimer.time'
TEMP_DIRECTORY = None
_HARDDATA = []
STR_TEMP_PREFIX = 'pyhdd08234'
STR_TEMP_SUFIX = '.hd'
tmp_regexp = ('^{0}(.*?){1}$').format(textools.convert_to_regexp(STR_TEMP_PREFIX), textools.convert_to_regexp(STR_TEMP_SUFIX))
tmp_regexp = re.compile(tmp_regexp)

def get_temp_file():
    global TEMP_DIRECTORY
    if not TEMP_DIRECTORY:
        create_temp_directory()
    tempfile.mkstemp(suffix=STR_TEMP_SUFIX, prefix=STR_TEMP_PREFIX, dir=TEMP_DIRECTORY)


def create_harddata_thread():
    global THREAD_HANDLED
    global THREAD_harddata
    global THREAD_lock
    assert not THREAD_HANDLED
    from errors import ModuleError
    try:
        THREAD_harddata
        raise ModuleError('Thread already started')
    except NameError:
        pass

    from threading import Thread, Lock

    class harddata_thread(Thread):

        def __init__(self, harddata, lock):
            print 'intializing thread'
            self.harddata = harddata
            self.lock = lock
            Thread.__init__(self)

        def run(self):
            while True:
                print 'running thread'
                start_time = time.time()
                THREAD_manage_harddata()
                if time.time() - start_time > THREAD_PERIOD:
                    assert 0
                else:
                    print 'thread sleeping'
                    time.sleep(self.last_run - start_time)

    THREAD_lock = Lock()
    THREAD_harddata = harddata_thread(_HARDDATA, THREAD_lock)
    THREAD_HANDLED = True
    THREAD_harddata.run()


def create_temp_directory():
    global TEMP_DIRECTORY
    TEMP_DIRECTORY = tempfile.mkdtemp(suffix='.hd', prefix=STR_TEMP_PREFIX, dir=tempfile.gettempdir())
    THREAD_manage_harddata()
    if not THREAD_HANDLED:
        create_harddata_thread()


def THREAD_manage_harddata():
    THREAD_LOCK.acquire()
    for hd in _HARDDATA:
        hd._check(time.time())

    _manage_temp_dirs()
    THREAD_LOCK.release()


def _manage_temp_dirs():
    update_timer_file()
    temp_folders = (tmpf for tmpf in os.listdir(tempfile.gettempdir()) if os.path.isdir(tmpf) and tmp_regexp.match(tmpf, len(tmpf)))
    for tmpfold in temp_folders:
        tpath = os.path.join(tmpfold)
        if not check_timer(tpath):
            shutil.rmtree(tpath)


def update_timer_file():
    """updates the file timer so that external python processes don't
    delete the temp data"""
    with open(os.path.join(TEMP_DIRECTORY, TIMER_FILE), 'w') as (f):
        f.write(time.ctime(time.time()))


def check_timer(folder_path):
    """returns whether the data should be kept (True) or deleted (False)"""
    timer_path = os.path.join(TEMP_DIRECTORY, TIMER_FILE)
    if time.time() - os.path.getatime(timer_path) > DELETE_TMP_AFTER:
        return False
    return True


if __name__ == '__main__':
    pass