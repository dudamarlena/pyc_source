# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Admin/Desktop/Code/Git/school-app/lib/utils.py
# Compiled at: 2014-02-08 12:44:29
import re, cgi, hmac, random, string, urllib, hashlib, datetime

def html(jinja_env, filename, **params):
    """Get the parsed html of a template."""
    return jinja_env.get_template(filename).render(params)


def escape(s):
    """Get an html-safe version of a string or list."""
    return cgi.escape(s, quote=True)


def newlines(txt):
    """Replace the string's newlines with html newlines."""
    return txt.replace('\n', '<br>')


def contains_word(a, b):
    """Check if a string contains a given word."""
    return ' %s ' % b in ' %s ' % a


def is_num(n):
    """Check if the input is a number."""
    return re.match(str(n), '^[0-9]+$')


def valid_date(d, m, y):
    """Check if the date set is valid."""
    try:
        return datetime.date(y, m, d)
    except:
        return False


def lowercase(s):
    """Convert class-like names to varliable-like names."""
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', s)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()


def uppercase(s):
    """Opposite function to lowercase()."""
    return filter(str.isalnum, s.title())


def file_size(num):
    """Get the human-readable file size (from bytes)."""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.1f %s' % (num, x)
        num /= 1024.0


def gravatar(email, size=None):
    """Given an email, get its gravatar url."""
    url = 'http://www.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest()
    if size:
        url += '?'
        return url + urllib.urlencode({'s': str(size)})
    return url


def random_string(length=16):
    s = string.lowercase + string.digits + string.uppercase
    return ('').join(random.sample(s, length))