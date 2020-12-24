# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/Storage.py
# Compiled at: 2015-11-05 10:40:17
import calendar, logging, binascii, sqlite3, time, hashlib
from contextlib import GeneratorContextManager
from functools import wraps
from ipaddr import IPAddress
import sys
from bridgedb.Stability import BridgeHistory
import threading
toHex = binascii.b2a_hex
fromHex = binascii.a2b_hex
HEX_ID_LEN = 40

def _escapeValue(v):
    return "'%s'" % v.replace("'", "''")


def timeToStr(t):
    return time.strftime('%Y-%m-%d %H:%M', time.gmtime(t))


def strToTime(t):
    return calendar.timegm(time.strptime(t, '%Y-%m-%d %H:%M'))


SCHEMA2_SCRIPT = "\n CREATE TABLE Config (\n     key PRIMARY KEY NOT NULL,\n     value\n );\n\n CREATE TABLE Bridges (\n     id INTEGER PRIMARY KEY NOT NULL,\n     hex_key,\n     address,\n     or_port,\n     distributor,\n     first_seen,\n     last_seen\n );\n\n CREATE UNIQUE INDEX BridgesKeyIndex ON Bridges ( hex_key );\n\n CREATE TABLE EmailedBridges (\n     email PRIMARY KEY NOT NULL,\n     when_mailed\n );\n\n CREATE INDEX EmailedBridgesWhenMailed on EmailedBridges ( email );\n\n CREATE TABLE BlockedBridges (\n     id INTEGER PRIMARY KEY NOT NULL,\n     hex_key,\n     blocking_country\n );\n\n CREATE INDEX BlockedBridgesBlockingCountry on BlockedBridges(hex_key);\n\n CREATE TABLE WarnedEmails (\n     email PRIMARY KEY NOT NULL,\n     when_warned\n );\n\n CREATE INDEX WarnedEmailsWasWarned on WarnedEmails ( email );\n\n INSERT INTO Config VALUES ( 'schema-version', 2 ); \n"
SCHEMA_2TO3_SCRIPT = "\n CREATE TABLE BridgeHistory (\n     fingerprint PRIMARY KEY NOT NULL,\n     address,\n     port INT,\n     weightedUptime LONG,\n     weightedTime LONG,\n     weightedRunLength LONG,\n     totalRunWeights DOUBLE,\n     lastSeenWithDifferentAddressAndPort LONG,\n     lastSeenWithThisAddressAndPort LONG,\n     lastDiscountedHistoryValues LONG,\n     lastUpdatedWeightedTime LONG\n );\n\n CREATE INDEX BridgeHistoryIndex on BridgeHistory ( fingerprint );\n\n INSERT OR REPLACE INTO Config VALUES ( 'schema-version', 3 ); \n "
SCHEMA3_SCRIPT = SCHEMA2_SCRIPT + SCHEMA_2TO3_SCRIPT

class BridgeData(object):
    """Value class carrying bridge information:
       hex_key      - The unique hex key of the given bridge
       address      - Bridge IP address
       or_port      - Bridge TCP port
       distributor  - The distributor (or pseudo-distributor) through which 
                      this bridge is being announced
       first_seen   - When did we first see this bridge online?
       last_seen    - When was the last time we saw this bridge online?
    """

    def __init__(self, hex_key, address, or_port, distributor='unallocated', first_seen='', last_seen=''):
        self.hex_key = hex_key
        self.address = address
        self.or_port = or_port
        self.distributor = distributor
        self.first_seen = first_seen
        self.last_seen = last_seen


class Database(object):

    def __init__(self, sqlite_fname):
        self._conn = openDatabase(sqlite_fname)
        self._cur = self._conn.cursor()
        self.sqlite_fname = sqlite_fname

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._cur.close()
        self._conn.close()

    def insertBridgeAndGetRing(self, bridge, setRing, seenAt, validRings, defaultPool='unallocated'):
        """Updates info about bridge, setting ring to setRing if none was set.
           Also sets distributor to `defaultPool' if the bridge was found in
           the database, but its distributor isn't valid anymore.

           Returns the name of the distributor the bridge is assigned to.
        """
        cur = self._cur
        t = timeToStr(seenAt)
        h = bridge.fingerprint
        assert len(h) == HEX_ID_LEN
        cur.execute('SELECT id, distributor FROM Bridges WHERE hex_key = ?', (
         h,))
        v = cur.fetchone()
        if v is not None:
            i, ring = v
            if ring not in validRings:
                ring = defaultPool
            cur.execute('UPDATE Bridges SET address = ?, or_port = ?, distributor = ?, last_seen = ? WHERE id = ?', (
             str(bridge.address), bridge.orPort, ring,
             timeToStr(seenAt), i))
            return ring
        else:
            cur.execute('INSERT INTO Bridges (hex_key, address, or_port, distributor, first_seen, last_seen) VALUES (?, ?, ?, ?, ?, ?)', (
             h, str(bridge.address), bridge.orPort, setRing, t, t))
            return setRing
            return

    def cleanEmailedBridges(self, expireBefore):
        cur = self._cur
        t = timeToStr(expireBefore)
        cur.execute('DELETE FROM EmailedBridges WHERE when_mailed < ?', (t,))

    def getEmailTime(self, addr):
        addr = hashlib.sha1(addr).hexdigest()
        cur = self._cur
        cur.execute('SELECT when_mailed FROM EmailedBridges WHERE email = ?', (addr,))
        v = cur.fetchone()
        if v is None:
            return
        else:
            return strToTime(v[0])

    def setEmailTime(self, addr, whenMailed):
        addr = hashlib.sha1(addr).hexdigest()
        cur = self._cur
        t = timeToStr(whenMailed)
        cur.execute('INSERT OR REPLACE INTO EmailedBridges (email,when_mailed) VALUES (?,?)', (
         addr, t))

    def getAllBridges(self):
        """Return a list of BridgeData value classes of all bridges in the
           database
        """
        retBridges = []
        cur = self._cur
        cur.execute('SELECT hex_key, address, or_port, distributor, first_seen, last_seen  FROM Bridges')
        for b in cur.fetchall():
            bridge = BridgeData(b[0], b[1], b[2], b[3], b[4], b[5])
            retBridges.append(bridge)

        return retBridges

    def getBridgesForDistributor(self, distributor):
        """Return a list of BridgeData value classes of all bridges in the
           database that are allocated to distributor 'distributor'
        """
        retBridges = []
        cur = self._cur
        cur.execute('SELECT hex_key, address, or_port, distributor, first_seen, last_seen FROM Bridges WHERE distributor = ?', (
         distributor,))
        for b in cur.fetchall():
            bridge = BridgeData(b[0], b[1], b[2], b[3], b[4], b[5])
            retBridges.append(bridge)

        return retBridges

    def updateDistributorForHexKey(self, distributor, hex_key):
        cur = self._cur
        cur.execute('UPDATE Bridges SET distributor = ? WHERE hex_key = ?', (
         distributor, hex_key))

    def getWarnedEmail(self, addr):
        addr = hashlib.sha1(addr).hexdigest()
        cur = self._cur
        cur.execute('SELECT * FROM WarnedEmails WHERE email = ?', (addr,))
        v = cur.fetchone()
        if v is None:
            return False
        else:
            return True

    def setWarnedEmail(self, addr, warned=True, whenWarned=time.time()):
        addr = hashlib.sha1(addr).hexdigest()
        t = timeToStr(whenWarned)
        cur = self._cur
        if warned == True:
            cur.execute('INSERT INTO WarnedEmails(email,when_warned) VALUES (?,?)', (
             addr, t))
        elif warned == False:
            cur.execute('DELETE FROM WarnedEmails WHERE email = ?', (addr,))

    def cleanWarnedEmails(self, expireBefore):
        cur = self._cur
        t = timeToStr(expireBefore)
        cur.execute('DELETE FROM WarnedEmails WHERE when_warned < ?', (t,))

    def updateIntoBridgeHistory(self, bh):
        cur = self._cur
        cur.execute('INSERT OR REPLACE INTO BridgeHistory values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
         bh.fingerprint, str(bh.ip), bh.port,
         bh.weightedUptime, bh.weightedTime, bh.weightedRunLength,
         bh.totalRunWeights, bh.lastSeenWithDifferentAddressAndPort,
         bh.lastSeenWithThisAddressAndPort, bh.lastDiscountedHistoryValues,
         bh.lastUpdatedWeightedTime))
        return bh

    def delBridgeHistory(self, fp):
        cur = self._cur
        cur.execute('DELETE FROM BridgeHistory WHERE fingerprint = ?', (fp,))

    def getBridgeHistory(self, fp):
        cur = self._cur
        cur.execute('SELECT * FROM BridgeHistory WHERE fingerprint = ?', (fp,))
        h = cur.fetchone()
        if h is None:
            return
        else:
            return BridgeHistory(h[0], IPAddress(h[1]), h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10])

    def getAllBridgeHistory(self):
        cur = self._cur
        v = cur.execute('SELECT * FROM BridgeHistory')
        if v is None:
            return
        else:
            for h in v:
                yield BridgeHistory(h[0], IPAddress(h[1]), h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10])

            return

    def getBridgesLastUpdatedBefore(self, statusPublicationMillis):
        cur = self._cur
        v = cur.execute('SELECT * FROM BridgeHistory WHERE lastUpdatedWeightedTime < ?', (
         statusPublicationMillis,))
        if v is None:
            return
        else:
            for h in v:
                yield BridgeHistory(h[0], IPAddress(h[1]), h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10])

            return


def openDatabase(sqlite_file):
    conn = sqlite3.Connection(sqlite_file)
    cur = conn.cursor()
    try:
        try:
            cur.execute("SELECT value FROM Config WHERE key = 'schema-version'")
            val, = cur.fetchone()
            if val == 2:
                logging.info('Adding new table BridgeHistory')
                cur.executescript(SCHEMA_2TO3_SCRIPT)
            elif val != 3:
                logging.warn('Unknown schema version %s in database.', val)
        except sqlite3.OperationalError:
            logging.warn('No Config table found in DB; creating tables')
            cur.executescript(SCHEMA3_SCRIPT)
            conn.commit()

    finally:
        cur.close()

    return conn


class DBGeneratorContextManager(GeneratorContextManager):
    """Helper for @contextmanager decorator.

    Overload __exit__() so we can call the generator many times
    """

    def __exit__(self, type, value, traceback):
        """Handle exiting a with statement block

        Progress generator or throw exception

        Significantly based on contextlib.py

        :throws: `RuntimeError` if the generator doesn't stop after
            exception is thrown
        """
        if type is None:
            try:
                self.gen.next()
            except StopIteration:
                return

            return
        if value is None:
            value = type()
        try:
            self.gen.throw(type, value, traceback)
            raise RuntimeError("generator didn't stop after throw()")
        except StopIteration as exc:
            return exc is not value
        except:
            if sys.exc_info()[1] is not value:
                raise

        return


def contextmanager(func):
    """Decorator to for :func:`Storage.getDB()`

    Define getDB() for use by with statement content manager
    """

    @wraps(func)
    def helper(*args, **kwds):
        return DBGeneratorContextManager(func(*args, **kwds))

    return helper


_DB_FNAME = None
_LOCK = None
_LOCKED = 0
_OPENED_DB = None
_REFCOUNT = 0

def clearGlobalDB():
    """Start from scratch.

    This is currently only used in unit tests.
    """
    global _DB_FNAME
    global _LOCK
    global _LOCKED
    global _OPENED_DB
    _DB_FNAME = None
    _LOCK = None
    _LOCKED = 0
    _OPENED_DB = None
    _REFCOUNT = 0
    return


def initializeDBLock():
    """Create the lock

    This must be called before the first database query
    """
    global _LOCK
    if not _LOCK:
        _LOCK = threading.RLock()
    assert _LOCK


def setDBFilename(sqlite_fname):
    global _DB_FNAME
    _DB_FNAME = sqlite_fname


@contextmanager
def getDB(block=True):
    """Generator: Return a usable database handler

    Always return a :class:`bridgedb.Storage.Database` that is
    usable within the current thread. If a connection already exists
    and it was created by the current thread, then return the
    associated :class:`bridgedb.Storage.Database` instance. Otherwise,
    create a new instance, blocking until the existing connection
    is closed, if applicable.

    Note: This is a blocking call (by default), be careful about
        deadlocks!

    :rtype: :class:`bridgedb.Storage.Database`
    :returns: An instance of :class:`bridgedb.Storage.Database` used to
        query the database
    """
    global _LOCKED
    global _OPENED_DB
    global _REFCOUNT
    assert _LOCK
    try:
        own_lock = _LOCK.acquire(block)
        if own_lock:
            _LOCKED += 1
            if not (_OPENED_DB or _REFCOUNT == 0):
                raise AssertionError
                _OPENED_DB = Database(_DB_FNAME)
            _REFCOUNT += 1
            yield _OPENED_DB
        else:
            yield False
    finally:
        assert own_lock
        try:
            _REFCOUNT -= 1
            if _REFCOUNT == 0:
                _OPENED_DB.close()
                _OPENED_DB = None
        finally:
            _LOCKED -= 1
            _LOCK.release()

    return


def dbIsLocked():
    return _LOCKED != 0