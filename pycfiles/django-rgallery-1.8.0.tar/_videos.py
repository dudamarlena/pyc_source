# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/_videos.py
# Compiled at: 2014-11-03 11:26:00
import os, errno, re, sys, time, datetime, gzip, glob
from datetime import datetime
from pprint import pprint
from shutil import copyfile
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset

def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    filename = fn
    filename, realname = unicodeFilename(filename), filename
    parser = createParser(filename, realname)
    if not parser:
        print '[EEE] No puedo parsear %s' % filename
        exit(1)
    try:
        metadata = extractMetadata(parser)
    except HachoirError as err:
        print '[EEE] Metadata extraction error: %s' % unicode(err)
        metadata = None

    if not metadata:
        print '[EEE] Unable to extract metadata'
        exit(1)
    text = metadata.exportPlaintext()
    charset = getTerminalCharset()
    for line in text:
        mes = makePrintable(line, charset)
        if 'Creation date' in mes:
            return mes.split(': ')[1]

    return