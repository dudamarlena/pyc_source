# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/utils.py
# Compiled at: 2008-05-07 15:44:29
"""
Purpose: Utility methods 
Author: kapil thangavelu <pluto@objectrealms.net>
$Id: utils.py 2205 2008-05-07 19:44:27Z hazmat $
"""
import time
from datetime import datetime
from svn import core

def make_aprtime(dt, pool):
    if not isinstance(dt, datetime):
        raise SyntaxError('must pass a valid date time')
    try:
        (parsed, aprtime) = core.svn_parse_date(dt.isoformat(), pool)
    except AttributeError:
        parsed = False

    if not parsed:
        raise SyntaxError('could not parse %r' % dt)
    return aprtime


def make_time(aprtime):
    return datetime.fromtimestamp(aprtime / 1000000)


def svn_path_id(svnpath):
    idx = svnpath.rfind('/')
    if not idx and svnpath.startswith('/'):
        id = svnpath[1:].strip()
    else:
        id = svnpath[idx + 1:]
    return id


def svn_path_parent(svnpath):
    idx = svnpath.rfind('/')
    if idx == 0:
        return '/'
    parent, name = svnpath[:idx], svnpath[idx:]
    if name == '/':
        return svn_path_parent(svnpath[:idx])
    return parent


def svn_path_join(*args):
    return '/%s' % ('/').join(filter(None, ('/').join(args).split('/')))


class charbuffer:

    def __init__(self):
        self.data = []

    def write(self, d):
        self.data.append(d)

    def getvalue(self):
        return ('').join(self.data)


class wrap:

    def __init__(self, o):
        self.o = o

    def __call__(self, v):
        return v.__of__(self.o)


def sort_by_id(obj1, obj2):
    return cmp(obj1.getId(), obj2.getId())


def format_size(size):
    """
    format size for display
    """
    KBSize = 1024
    MBSize = 1048576
    if size < KBSize:
        return '%d bytes' % size
    elif size < MBSize:
        return '%d kb' % (size / KBSize)
    else:
        return '%d mb' % (size / MBSize)


def format_date(date):
    """
    format date for display
    """
    units = (
     (31536000, 'year', 'years'),
     (2592000, 'month', 'months'),
     (604800, 'week', 'weeks'),
     (86400, 'day', 'days'),
     (3600, 'hour', 'hours'),
     (60, 'minute', 'minutes'))
    then = time.mktime(date.timetuple())
    now = time.time()
    t_delta = int(now - then)
    for (u, unit, unit_plural) in units:
        r = int(t_delta / u)
        if r:
            return '%i %s' % (r, r == 1 and unit or unit_plural)

    return ''


def merge_object_models(target_klass, target_fti, source_klass, source_fti, order=-1):
    bases = list(target_klass.__bases__)
    bases.insert(order, source_klass)
    target_klass.__bases__ = tuple(bases)
    bases = list(target_fti.__bases__)
    bases.insert(0, source_fti)
    target_fti.__bases__ = tuple(bases)


def klassify_type_info(ti=None, **kw):

    class kti:
        pass

    if ti is None:
        ti = kw
    return kti().__dict__.update(ti)


def initialize_type_info(klass):
    ti = {}
    bases = klass.__bases__
    bases.reverse()
    bases.append(klass)
    for b in bases:
        ti.update(b.__dict__)

    return ti