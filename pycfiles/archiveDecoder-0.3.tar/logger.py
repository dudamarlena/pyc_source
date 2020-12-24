# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/archivedb/logger.py
# Compiled at: 2011-12-26 01:48:04
import os, sys, logging, logging.handlers, traceback, platform, pymysql
from archivedb import __author__, __version__
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from archivedb.config import args

def get_logger(log_path):
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FORMAT = '%(asctime)s :: %(levelname)-8s :: %(filename)s:%(lineno)s :: %(funcName)s :: %(message)s'
    CONSOLE_FORMAT = '%(asctime)s %(levelname)-8s: %(message)s'
    if not os.path.isdir(os.path.dirname(log_path)):
        os.mkdir(os.path.dirname(log_path))
    log_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_formatter = logging.Formatter(CONSOLE_FORMAT, datefmt=DATE_FORMAT)
    log = logging.getLogger('archivedb')
    log.setLevel(logging.DEBUG)
    rotator = logging.handlers.RotatingFileHandler(filename=log_path, maxBytes=20000000, backupCount=5)
    rotator.setLevel(logging.DEBUG)
    rotator.setFormatter(log_formatter)
    log.addHandler(rotator)
    console = logging.StreamHandler()
    if args['debug']:
        console_level = logging.DEBUG
    else:
        console_level = logging.INFO
    console.setLevel(console_level)
    console.setFormatter(console_formatter)
    log.addHandler(console)
    return log


def log_traceback(exc_info, header=None):
    """log traceback
    Args
    exc_info: tuple returned by sys.exc_info()
    header: info to be logged before the exception
    """
    s = StringIO()
    if header is not None:
        s.write(header + '\n')
    s.write('*** There has been an error, please contact the developer\n\n')
    traceback.print_exception(exc_info[0], exc_info[1], exc_info[2], file=s)
    s.write('\n')
    s.write('*** Copy this message in the email.\n')
    s.write(('*** archivedb: {0}\n').format(__version__))
    s.write(('*** Python: {0}\n').format(platform.python_version()))
    s.write(('*** PyMySQL: {0}\n').format(pymysql.__version__))
    s.write(('*** Platform: {0}\n').format(platform.platform()))
    s.write(('*** Contact Info: {0}\n').format(__author__))
    s.write(('*** Please attach log file(s) (they can be found here: {0})\n').format(args['log_path']))
    s.seek(0)
    log.critical(s.read())
    s.close()
    return


if __name__ == 'archivedb.logger':
    log = get_logger(args['log_path'])