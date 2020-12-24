# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/batch.py
# Compiled at: 2018-08-13 08:58:37
"""
Functions related to the RediBatch database
"""
import datetime, hashlib, logging, os, sqlite3 as lite, stat, sys, time
from lxml import etree
from utils import redi_email
from utils.rawxml import RawXml
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
BATCH_STATUS_STARTED = 'Started'
BATCH_STATUS_COMPLETED = 'Completed'

def create_empty_md5_database(db_path):
    if os.path.exists(db_path):
        logger.warn('The file with name ' + db_path + ' already exists')
    try:
        logger.info('Opening the file:' + db_path)
        fresh_file = open(db_path, 'w')
        fresh_file.close()
        os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)
        time.sleep(5)
    except IOError as e:
        logger.error('I/O error: ' + e.strerror + ' for file: ' + db_path)
        return False

    success = create_empty_table(db_path)
    return success


def create_empty_table(db_path):
    logger.info('exec create_empty_table')
    db = None
    try:
        try:
            db = lite.connect(db_path)
            cur = db.cursor()
            sql = 'CREATE TABLE RediBatch (\n    rbID INTEGER PRIMARY KEY AUTOINCREMENT,\n    rbCreateTime DATETIME DEFAULT CURRENT_TIMESTAMP,\n    rbStartTime DATETIME,\n    rbEndTime DATETIME,\n    rbStatus TEXT,\n    rbMd5Sum TEXT NOT NULL\n)\n        '
            cur.execute(sql)
        except lite.Error as e:
            logger.error('SQLite error in create_empty_table(): ' + e.args[0])
            return False

    finally:
        if db:
            db.close()

    logger.info('success create_empty_table')
    return True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def check_input_file(batch_warning_days, db_path, email_settings, raw_xml_file, project, start_time):
    batch = None
    if not os.path.exists(db_path):
        create_empty_md5_database(db_path)
    new_md5ive = get_md5_input_file(raw_xml_file)
    new_msg = 'Using SQLite file: %s to store input file: %s md5 sum: %s' % (
     db_path, raw_xml_file, new_md5ive)
    logger.info(new_msg)
    old_batch = get_last_batch(db_path)
    old_md5ive = None
    if old_batch:
        old_md5ive = old_batch['rbMd5Sum']
        logger.info('Old md5 sum for the input file is: ' + old_md5ive)
    else:
        logger.info('There is no old md5 recorded yet for the input file. Continue data import...')
        batch = add_batch_entry(db_path, new_md5ive)
        record_msg = 'Added batch (rbID= %s, rbCreateTime= %s, rbMd5Sum= %s' % (
         batch['rbID'], batch['rbCreateTime'], batch['rbMd5Sum'])
        logger.info(record_msg)
        return batch
    if old_md5ive != new_md5ive:
        batch = add_batch_entry(db_path, new_md5ive)
        record_msg = 'Added batch (rbID= %s, rbCreateTime= %s, rbMd5Sum= %s' % (
         batch['rbID'], batch['rbCreateTime'], batch['rbMd5Sum'])
        logger.info(record_msg)
        return batch
    else:
        days_since_today = get_days_since_today(old_batch['rbCreateTime'])
        if days_since_today > int(batch_warning_days):
            raw_xml = RawXml(project, raw_xml_file)
            msg_file_details = '\nXML file details: ' + raw_xml.get_info()
            logger.info('Last import was started on: %s which is more than  the limit of %s' % (
             old_batch['rbStartTime'], batch_warning_days))
            if -1 == int(batch_warning_days):
                msg_continue = '\n                The configuration `batch_warning_days = -1` indicates that we want to continue\n                execution even if the input file did not change\n                ' + msg_file_details
                logger.info(msg_continue)
            else:
                msg_quit = 'The input file did not change in the past: %s days.' % days_since_today
                logger.critical(msg_quit + msg_file_details)
                redi_email.send_email_input_data_unchanged(email_settings, raw_xml)
                sys.exit()
        else:
            logger.info('Reusing md5 entry: ' + str(old_batch['rbID']))
        return old_batch


def get_last_batch(db_path):
    batch = None
    try:
        try:
            db = lite.connect(db_path)
            db.row_factory = dict_factory
            cur = db.cursor()
            sql = '\nSELECT\n    rbID, rbCreateTime, rbStartTime, rbEndTime, rbMd5Sum\nFROM\n    RediBatch\nORDER BY rbID DESC\nLIMIT 1\n'
            cur.execute(sql)
            batch = cur.fetchone()
        except lite.Error as e:
            logger.error('SQLite error in get_last_batch() for file %s - %s' % (db_path, e.args[0]))
            return

    finally:
        if db:
            db.close()

    return batch


def get_batch_by_id(db_path, batch_id):
    db = None
    try:
        try:
            db = lite.connect(db_path)
            db.row_factory = dict_factory
            cur = db.cursor()
            sql = '\nSELECT\n    rbID, rbCreateTime, rbStartTime, rbEndTime, rbMd5Sum\nFROM\n    RediBatch\nWHERE\n    rbID = ?\nLIMIT 1\n'
            cur.execute(sql, (str(batch_id),))
            batch = cur.fetchone()
        except lite.Error as e:
            logger.exception('SQLite error in get_batch_by_id(): %s:' % e.args[0])
            raise

    finally:
        if db:
            db.close()

    return batch


def get_md5_input_file(input_file):
    """
    @see #check_input_file()
    @see https://docs.python.org/2/library/hashlib.html
    @see https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory

    Returns the md5 sum for the redi input file
    """
    if not os.path.exists(input_file):
        raise Exception('Input file not found at: ' + input_file)
    logger.info('Computing md5 sum for: ' + input_file)
    f = open(input_file, 'rb')
    chunk_size = 1048576
    md5 = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        md5.update(chunk)

    return md5.hexdigest()


def add_batch_entry(db_path, md5):
    """
    Inserts a row into RediBatch table
    @see #check_input_file()
    Parameters
    ----------
    db_path : string
        The SQLite database file name
    md5 : string
        The md5 sum to be inserted
    create_time : string
        The batch start time
    """
    try:
        try:
            db = lite.connect(db_path)
            db.row_factory = dict_factory
            cur = db.cursor()
            sql = '\nINSERT INTO RediBatch\n    (rbCreateTime,rbStartTime, rbEndTime, rbStatus, rbMd5Sum)\nVALUES\n    ( ?, NULL, NULL, ?, ?)\n'
            create_time = get_db_friendly_date_time()
            cur.execute(sql, (create_time, BATCH_STATUS_STARTED, md5))
            rbID = cur.lastrowid
            db.commit()
            batch = get_batch_by_id(db_path, rbID)
        except lite.Error as e:
            logger.error('SQLite error in add_batch_entry() for file %s - %s' % (db_path, e.args[0]))
            return

    finally:
        if db:
            db.close()

    return batch


def update_batch_entry(db_path, id, status, start_time, end_time):
    """
    Update the status and the start/end time of a specified batch entry
    Return True if update succeeded, False otherwise

    Parameters
    ----------
    db_path : string
    id : integer
    status : string
    start_time : datetime string
    end_time : datetime string
    """
    try:
        try:
            db = lite.connect(db_path)
            cur = db.cursor()
            sql = '\nUPDATE\n    RediBatch\nSET\n    rbStartTime = ?\n    , rbEndTime = ?\n    , rbStatus = ?\nWHERE\n    rbID = ?\n'
            cur.execute(sql, (start_time, end_time, status, id))
            db.commit()
            success = True
        except lite.Error as e:
            logger.exception('SQLite error in update_batch_entry(): %s:' % e.args[0])
            success = False

    finally:
        if db:
            db.close()

    return success


def get_db_friendly_date_time():
    """
    @return string in format: "2014-06-24 01:23:24"
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_db_friendly_date():
    """
    @return string in format: 2014-06-24
    """
    return datetime.date.today()


def get_days_since_today(date_string):
    """
    @return the number of days passed since the specified date
    """
    num = None
    other = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    delta = now - other
    return delta.days


def printxml(tree):
    """
    Helper function for debugging xml content
    """
    print etree.tostring(tree, pretty_print=True)