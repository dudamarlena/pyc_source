# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/log.py
# Compiled at: 2020-04-10 09:12:00
# Size of source mod 2**32: 1222 bytes
import logging
l = logging.getLogger('')

def info(message):
    """Log helper function for jinja2 tasks"""
    l.info(message)
    return ''


def warn(message):
    """Log helper function for jinja2 tasks"""
    l.warning(message)
    return ''


def warning(message):
    """Log helper function for jinja2 tasks"""
    l.warning(message)
    return ''


def error(message):
    """Log helper function for jinja2 tasks"""
    l.error(message)
    return ''


def debug(message):
    """Log helper function for jinja2 tasks"""
    l.debug(message)
    return ''


def console(message):
    print(message)
    l.debug(f"console log: {message}")