# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/utils.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 2238 bytes
from __future__ import absolute_import, division
import hashlib, logging
from django.core.cache import get_cache, InvalidCacheBackendError
logger = logging.getLogger('django-pegasus-cms')
try:
    cache = get_cache('decorated')
except InvalidCacheBackendError:
    cache = get_cache('default')

def get_func_cache_key(f, *args, **kwargs):
    serialize = [
     unicode(f.__name__)]
    for arg in args:
        try:
            serialize.append(unicode(arg))
        except UnicodeDecodeError as e1:
            try:
                serialize.append(str(arg))
            except UnicodeEncodeError as e2:
                return

        except Exception as e3:
            return

    for k, v in kwargs.iteritems():
        serialize.append(unicode(k) + '=' + unicode(v))

    try:
        key = hashlib.sha1(unicode('/'.join(serialize)).encode('utf-8')).hexdigest()
    except:
        return

    return key


class cache_for(object):

    def __init__(self, seconds=0, minutes=None, hours=None):
        if hours and minutes and seconds:
            self.seconds = hours * 60 * 60 + minutes * 60 + seconds
        else:
            if hours and minutes:
                self.seconds = hours * 60 * 60 + minutes * 60
            else:
                if hours and seconds:
                    self.seconds = hours * 60 * 60 + seconds
                else:
                    if minutes and seconds:
                        self.seconds = minutes * 60 + seconds
                    else:
                        if hours:
                            self.seconds = hours * 60 * 60
                        else:
                            if minutes:
                                self.seconds = minutes * 60
                            elif seconds:
                                self.seconds = seconds

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            cached_val = None
            cache_key = get_func_cache_key(f, *args, **kwargs)
            if cache_key:
                cached_val = cache.get(cache_key)
            if cached_val:
                return cached_val
            else:
                ret_val = f(*args, **kwargs)
                cache.set(cache_key, ret_val, self.seconds)
                return ret_val

        return wrapped_f