# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/clipon/helper.py
# Compiled at: 2016-06-17 03:52:51
# Size of source mod 2**32: 1862 bytes
from __future__ import absolute_import
import sys, os, re, logging, logging.handlers
from logging import Logger
from xml.dom import minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

INT_MAX = sys.maxsize
LOGGER_NAME = 'clipon'
logger = logging.getLogger(LOGGER_NAME)

def init_log(logfile):
    global logger
    logger.setLevel(logging.DEBUG)
    h = logging.handlers.RotatingFileHandler(logfile, maxBytes=1048576)
    h.setLevel(logging.INFO)
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%Y/%m/%d %H:%M:%S')
    h.setFormatter(formatter)
    logger.addHandler(h)
    logger.info('Initialized logger')


def open_file(dir_path, file_path, mode):
    fd = None
    if not os.path.isfile(file_path):
        try:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path, 448)
            if not os.path.exists(file_path):
                open(file_path, 'x')
        except IOError:
            logger.error('Failed to create file %s' % file_path)
            return

    try:
        fd = open(file_path, mode)
    except IOError:
        logger.error('Failed to open file %s' % file_path)
        return

    return fd


def format_pretty(elem):
    """
    Return a pretty-printed XML string for the given element.
    """
    raw_string = ET.tostring(elem, encoding='utf-8')
    s = raw_string.decode()
    s = re.sub(' *\n *', '', s)
    raw_string = s.encode(encoding='utf-8')
    dom_string = minidom.parseString(raw_string)
    return dom_string.toprettyxml(indent='  ')