# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_toolkit/kotti_toolkit/util.py
# Compiled at: 2018-09-19 01:20:41
import time, uuid, json, re, subprocess
from uuid import UUID
from datetime import datetime, date
from unicodedata import normalize
from kotti.resources import Content
_punct_re = re.compile('[\\t !"#$%&\\\'()*\\-/<=>?@\\[\\\\\\]^_`{|},.:]+')

def uuid_factory():
    return uuid.uuid4()


def format_email_username(user):
    return ('"{}" <{}>').format(user.title, user.email)


def file_endswith(string, *args):
    extensions = ('|').join(args)
    return re.match('.*\\.(' + extensions + ')$', string)


def chunk_list(ls, n):
    return [ ls[i:i + n] for i in xrange(0, len(ls), n) ]


def slugify(text, delim='-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    text = unicode(text)
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)

    return unicode(delim.join(result))


def unslugify(text, delim='-'):
    return text.replace(delim, ' ')


def list_to_tuple(ls):
    return [ (v, v) for v in ls ]


def dict_to_tuple(dt):
    return [ (k, v) for k, v in dt.items() ]


def to_int(value, default=None, ceiling=True):
    try:
        if ceiling:
            return int(round(value))
        else:
            return int(value)

    except TypeError:
        return default


def json_value(value):
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [ json_value(v) for v in value ]
    if isinstance(value, long):
        if value > 9007199254740992 or value < -9007199254740992:
            return str(value)
    if isinstance(value, UUID):
        return str(value)
    return value


def find_key(d, val):
    return d.keys()[d.values().index(val)]


def remove_duplicates(list1):
    return reduce(lambda r, v: v in r and r or r + [v], list1, [])


def merge_list(list1, list2):
    """Remove duplicate values after merging the two lists"""
    return remove_duplicates((list1 or []) + (list2 or []))


def append_to_list(lst, val):
    """Append and return lists"""
    lst2 = lst[:]
    lst2.append(val)
    return lst2


def dateformat_momentize(date):
    if date is None:
        return ''
    else:
        return date.strftime('%Y-%m-%d %H:%M')


def to_timestamp(date):
    if date is None:
        return 0
    else:
        return time.mktime(date.timetuple()) * 1000


def get_system_timezone():
    tz = subprocess.check_output(['date', '+%Z'])
    return tz.replace('\n', '')