# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jabbercracky/jabbercracky.py
# Compiled at: 2010-07-31 08:24:08
import MySQLdb, os
from multiprocessing import Pool
import time, ConfigParser, sys, traceback, logging, pipes
state_NEW = 0
state_RUNNING = 20
state_P1WON = 30
state_P1LOST = 40
state_P2WON = 50
state_P2LOST = 60

def formatExceptionInfo(maxTBlevel=5):
    (cla, exc, trbk) = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__['args']
    except KeyError:
        excArgs = '<no args>'

    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


def connectDB():
    global conn
    if conn:
        try:
            conn.ping()
        except MySQLdb.OperationalError:
            conn = None

    if not conn:
        logging.debug('Connecting to MySQL')
        conn = MySQLdb.connect(host=config.get('db', 'host'), user=config.get('db', 'user'), passwd=config.get('db', 'passwd'), db=config.get('db', 'database'))
    return


def crackWorker(id, hash, type):
    filename = str(id) + '.txt'
    s = config.get('fs', 'rcracki') + ' -h ' + hash + ' -o ' + filename + ' -t ' + config.get('tune', 'threads_per_proc') + ' ' + config.get('fs', 'rainbow_tables') + '/' + type
    logging.debug('crackWorker CWD is ' + os.getcwd())
    logging.debug('crackWorker CMD is ' + s)
    fd = os.popen(s)
    fd.read()
    fd.close()
    try:
        f = open(filename, 'r')
        for line in f.readlines():
            words = line.split(':')
            setClearStateByHash(words[0], words[1], state_P1WON)

        f.close()
    except:
        logging.debug(formatExceptionInfo())
        setStateById(id, state_P1LOST)


def setRunningById(id):
    bq = '\n        UPDATE queue SET state=20,started=now(),maxcpu={0!s},threads={1!s} WHERE id={2!s}\n        '
    maxProcs = int(config.get('tune', 'max_procs'))
    connectDB()
    c = conn.cursor()
    c.execute('SET AUTOCOMMIT=1')
    c.execute(bq.format(maxProcs, config.get('tune', 'threads_per_proc'), id))
    c.close()


def setStateById(id, state, lastpw=''):
    bq = "\n        UPDATE queue SET state={0!s},lastpw='{2!s}' WHERE id={1!s}\n        "
    connectDB()
    c = conn.cursor()
    c.execute('SET AUTOCOMMIT=1')
    logging.debug('lastpw in setstate: ' + lastpw)
    c.execute(bq.format(state, id, lastpw))
    c.close()


def setClearStateByHash(hash, clear, state):
    aq = "\n        UPDATE queue SET state={0!s},clear='{1!s}',cracked=now() WHERE hash='{2!s}'\n        "
    connectDB()
    c = conn.cursor()
    c.execute('SET AUTOCOMMIT=1')
    c.execute(aq.format(state, clear, hash))
    c.close()


def getByState(state):
    bq = '\n        SELECT * FROM queue WHERE state={0!s}\n        '
    connectDB()
    c = conn.cursor()
    c.execute('SET AUTOCOMMIT=1')
    c.execute(bq.format(state))
    rows = c.fetchall()
    c.close()
    return rows


def gpuWorker(id, hash, start_pw=''):
    try:
        s = config.get('fs', 'gpucrack') + ' -c 7 -h ' + hash
        if len(start_pw) > 0:
            s = s + ' -s ' + pipes.quote(start_pw)
        logging.debug('gpuWorker CWD is ' + os.getcwd())
        logging.debug('gpuWorker CMD is ' + s)
        (fdin, fdouterr) = os.popen4(s)
        output = fdouterr.read()
        errStr = 'Init Bruteforce error'
        loseStr = 'no password found'
        lastPwStr = 'End Pwd:'
        winStr = 'MD5 Cracked pwd='
        if output.rfind(errStr) > -1:
            logging.error(output)
        elif output.rfind(loseStr) > -1:
            logging.debug('GPU Crack Failed')
            a = output.rfind(lastPwStr) + len(lastPwStr)
            z = output.find('\n', a)
            lastPw = output[a:z]
            logging.debug('lastPw: ' + lastPw)
            setStateById(id, state_P2LOST, lastPw)
        else:
            logging.debug('GPU Crack Succeeded')
            a = output.rfind(winStr) + len(winStr)
            z = output.find(' ', a)
            crackedPw = output[a:z].strip()
            logging.debug('crackedPw: ' + crackedPw)
            setClearStateByHash(hash, crackedPw, state_P2WON)
        fdouterr.close()
        fdin.close()
    except:
        logging.debug(formatExceptionInfo())


def jabbercrackyMain():
    global config
    global conn
    config = ConfigParser.RawConfigParser()
    config.read('/etc/jabbercracky.conf')
    conn = None
    maxProcs = int(config.get('tune', 'max_procs'))
    pool = Pool(processes=maxProcs)
    logging.debug('Starting Thread Pool')
    while 1:
        try:
            rows = getByState(state_NEW)
            for r in rows:
                pool.apply_async(crackWorker, [r[0], r[4], r[2]])
                setRunningById(r[0])

            grows = getByState(state_P1LOST)
            for t in grows:
                if t[2] == 'md5':
                    pool.apply_async(gpuWorker, [t[0], t[4]])
                    setRunningById(t[0])

            frows = getByState(state_P2LOST)
            for f in frows:
                if f[2] == 'md5':
                    pool.apply_async(gpuWorker, [f[0], f[4], f[11]])
                    setRunningById(f[0])

            time.sleep(10)
        except:
            logging.debug(formatExceptionInfo())
            exit()

    return


if __name__ == '__main__':
    jabbercrackyMain()