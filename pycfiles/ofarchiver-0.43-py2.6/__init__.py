# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ofarchiver/__init__.py
# Compiled at: 2011-11-14 12:32:36
import hashlib, logging, logging.handlers, multiprocessing, os, sys, time, chardet, configobj, HTML, MySQLdb
CONFIG_FILE = 'ofarchiver.ini'
CONFIG_DIRS = ('/usr/local/etc', '/etc', os.environ['HOME'])
SUPPORTED_DBS = ('mysql',)
_ofarchiver = None
_lock = None

class OfArchiver(object):
    """A class for generating an HTML archive of chat rooms on an Openfire
    instant messaging server.

    Public methods:
    get_rooms -- Returns the list of rooms to archive.
    gen_archive -- Generates HTML archives for a chat room.
    """
    _lock = None
    _used_colors = {}

    def __init__(self):
        for config_dir in CONFIG_DIRS:
            config_path = os.path.join(config_dir, CONFIG_FILE)
            if os.path.isfile(config_path):
                self.config = configobj.ConfigObj(config_path)
                break
        else:
            sys.stdout.write('%s not found in either of these directories: %s\n' % (
             CONFIG_FILE, (', ').join(CONFIG_DIRS)))
            sys.exit(1)

        self._set_logging()
        try:
            self._basedir = self.config['main']['basedir']
        except KeyError:
            self.error('Archive base directory not configured')

        if not os.path.isdir(self._basedir):
            self.error("'%s' doesn't exist or isn't a directory" % self._basedir)
        try:
            self._confserver = self.config['main']['confserver']
        except KeyError:
            self.error('Conference server not configured')

        self._dbtype = self.config['main']['db']
        if self._dbtype not in SUPPORTED_DBS:
            self.error("Database type '%s' not supported" % self._dbtype)
        try:
            dbconfig = self.config['db']
        except KeyError:
            self.error('Config for database not found')

        dbvars = ('hostname', 'username', 'password', 'database')
        for dbvar in dbvars:
            try:
                setattr(self, '_db' + dbvar, dbconfig[dbvar])
            except KeyError:
                self.error("Database variable '%s' not defined" % dbvar)

        try:
            colorconfig = self.config['colors']
            if colorconfig['enabled'] == 'true':
                self._colors = colorconfig['names']
            else:
                self._colors = None
        except KeyError:
            self._colors = None

        try:
            self._org = self.config['main']['org']
        except KeyError:
            self._org = None

        try:
            self._rooms = self.config['main']['rooms']
        except KeyError:
            self._rooms = self._get_available_rooms()

        return

    def _set_logging(self):
        self._logger = logging.getLogger('ofarchiver')
        self._logger.setLevel(logging.DEBUG)
        debug = False
        loglevel = logging.ERROR
        try:
            debug = self.config['main']['debug']
            if debug == 'true':
                loglevel = logging.DEBUG
        except KeyError:
            pass

        handler = logging.StreamHandler()
        handler.setLevel(loglevel)
        self._logger.addHandler(handler)
        try:
            logfile = self.config['main']['logfile']
        except KeyError:
            pass
        else:
            if debug == 'true':
                loglevel = logging.DEBUG
            else:
                loglevel = logging.INFO
            handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10485760, backupCount=5)
            handler.setLevel(loglevel)
            logformat = '%(asctime)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(logformat)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def _log(self, msg, level):
        """Log a message with the given level."""
        try:
            loglevel = getattr(logging, level.upper())
        except AttributeError:
            self.error("Log level '%s' not valid" % level)

        if self._lock:
            with self._lock:
                self._logger.log(loglevel, msg)
        else:
            self._logger.log(loglevel, msg)

    def debug(self, msg):
        self._log(msg, level='DEBUG')

    def info(self, msg):
        self._log(msg, level='INFO')

    def warn(self, msg):
        self._log(msg, level='WARNING')

    def error(self, msg):
        self._log(msg, level='ERROR')
        sys.exit(1)

    def get_rooms(self):
        return self._rooms

    def _get_available_rooms(self):
        """Return a list of rooms available to archive."""
        db = self._db_connect()
        cursor = db.cursor()
        sql = "SELECT DISTINCT ToJID from ofMessageArchive\n                 WHERE ToJID LIKE '%%@%s/%%'" % self._confserver
        cursor.execute(sql)
        roomlist = []
        for row in cursor:
            (room, therest) = row[0].split('@', 1)
            roomlist.append(room)

        return set(roomlist)

    def gen_archive(self, room, lock=None):
        """Generate HTML archive for a chat room.

        A lock can also be passed, when using the threading or
        multiprocessing module to improve performance.
        """
        self._lock = lock
        self.debug("Generating HTML for '%s'" % room)
        roomdict = {}
        for msgdict in self._fetch_msgs(room):
            msgmember = msgdict['member']
            msgdate = msgdict['date']
            msgbody = msgdict['body']
            filepath = self._get_file_path(room, msgdate)
            try:
                table = roomdict[filepath]['table']
            except KeyError:
                tabledict = self._init_table(room, msgdate)
                roomdict[filepath] = tabledict
                table = tabledict['table']

            row = self._gen_table_row(msgdate, msgmember, msgbody)
            table.rows.append(row)

        for filepath in sorted(roomdict):
            tabledict = roomdict[filepath]
            html = "\n            <html>\n            <head>\n            <title>%(title)s</title>\n            </head>\n            <body>\n            <h2 style='text-align:center;'>%(title)s</h2>\n            %(table)s\n            </body>\n            </html>\n            " % tabledict
            with open(filepath, 'w') as (htmlfile):
                htmlfile.write(html)
                numentries = len(tabledict['table'].rows)
                self.debug('Wrote %d archive messages to %s' % (
                 numentries, filepath))

        self.info('Wrote %d HTML files for %s' % (len(roomdict), room))

    def _db_connect(self):
        """Return a connection to the database."""
        try:
            db = MySQLdb.connect(self._dbhostname, self._dbusername, self._dbpassword, self._dbdatabase)
        except Exception, exc_info:
            self.error("Couldn't connect to %s on %s: %s" % (
             self._dbtype, self._dbhostname, exc_info))

        return db

    def _fetch_msgs(self, room):
        """Fetch all messages for a room, encoded as UTF-8"""
        db = self._db_connect()
        cursor = db.cursor(MySQLdb.cursors.SSDictCursor)
        sql = "SELECT FromJID, ToJID, sentDate, body\n                from ofMessageArchive WHERE ToJID LIKE '%s@%%'\n                AND body IS NOT NULL ORDER BY sentDate" % room
        cursor.execute(sql)
        for row in cursor:
            msg = {}
            try:
                msg['member'] = row['FromJID'].split('@')[0]
                msg['date'] = row['sentDate'] / 1000
                msg['body'] = row['body']
            except Exception, exc_info:
                self.warn('Expected values for database row not found: %s' % exc_info)
                continue

            try:
                detected = chardet.detect(msg['body'])
            except TypeError, exc_info:
                self.warn("Couldn't detect encoding for '%s': %s" % (
                 msg['body'], exc_info))
            else:
                try:
                    decodedmsg = msg['body'].decode(detected['encoding'])
                except UnicodeDecodeError, exc_info:
                    self.warn("Couldn't decode '%s': %s" % (
                     msg['body'], exc_info))
                else:
                    msg['body'] = decodedmsg.encode('utf8')
                    yield msg

    def _get_file_path(self, room, msgdate):
        """Return a file path based on room and message date."""
        timestruct = time.localtime(msgdate)
        monthsubdir = time.strftime('%Y/%B', timestruct)
        filedir = '%s/%s/%s' % (self._basedir, room, monthsubdir)
        if not os.path.isdir(filedir):
            os.makedirs(filedir)
        msgday = time.strftime('%d', timestruct)
        filepath = '%s/%s.html' % (filedir, msgday)
        return filepath

    def _init_table(self, room, msgdate):
        """Initialize a room table."""
        tabledict = {}
        tabledict['table'] = HTML.Table(header_row=('Time', 'Member', 'Message'))
        timestruct = time.localtime(msgdate)
        titledate = time.strftime('%A, %B %d, %Y', timestruct)
        title = ''
        if self._org:
            title += '%s ' % self._org
        title += '%s archive for %s' % (room, titledate)
        tabledict['title'] = title
        return tabledict

    def _gen_table_row(self, msgdate, msgmember, msgbody):
        """Generate a row for the room table."""
        timestruct = time.localtime(msgdate)
        msgtime = time.strftime('%H:%M:%S %Z', timestruct)
        row = []
        for col in (msgtime, msgmember, msgbody):
            if self._colors and col is msgmember:
                color = self._pick_member_color(msgmember)
                style = 'color: %s' % color
            else:
                style = None
            cell = HTML.TableCell(col, style=style)
            row.append(cell)

        return row

    def _pick_member_color(self, member):
        """Pick a color for a member, unique from the others if possible."""
        colors = self._colors
        if member in self._used_colors:
            return self._used_colors[member]
        index = self._get_dict_index(colors, member)
        color = colors[index]
        reversed_member = member
        while color in self._used_colors.values() and len(self._used_colors) < len(colors):
            reversed_member += reversed_member[::-1]
            index = self._get_dict_index(colors, reversed_member)
            color = colors[index]

        self._used_colors[member] = color
        return color

    def _get_dict_index(self, hdict, hstr):
        """Hash a string and return its corresponding dictionary index."""
        h = hashlib.sha256(hstr)
        d = h.hexdigest()
        i = int(d, 16)
        dindex = i % len(hdict)
        return dindex


def gen_archive(room):
    """Generate HTML archive for a chat room.

    This wrapper function is required to work around this limitation:
    http://stackoverflow.com/questions/1816958/

    """
    global _lock
    global _ofarchiver
    _ofarchiver.gen_archive(room, _lock)


def main():
    global _lock
    global _ofarchiver
    _ofarchiver = OfArchiver()
    rooms = _ofarchiver.get_rooms()
    if len(rooms) > 1:
        manager = multiprocessing.Manager()
        _lock = manager.Lock()
        pool = multiprocessing.Pool()
        pool.map(gen_archive, rooms, 1)
        pool.close()
        pool.join()
    elif rooms:
        _ofarchiver.gen_archive(rooms[0])


if __name__ == '__main__':
    main()
__all__ = ['OfArchiver']