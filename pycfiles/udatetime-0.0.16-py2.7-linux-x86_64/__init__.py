# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/udatetime/__init__.py
# Compiled at: 2017-12-04 07:36:12
try:
    import __pypy__
except ImportError:
    __pypy__ = None

if __pypy__:
    from udatetime._pure import utcnow, now, from_rfc3339_string as from_string, to_rfc3339_string as to_string, utcnow_to_string, now_to_string, from_timestamp as fromtimestamp, from_utctimestamp as utcfromtimestamp, TZFixedOffset
else:
    from udatetime.rfc3339 import utcnow, now, from_rfc3339_string as from_string, to_rfc3339_string as to_string, utcnow_to_string, now_to_string, from_timestamp as fromtimestamp, from_utctimestamp as utcfromtimestamp, TZFixedOffset
__all__ = [
 'utcnow', 'now', 'from_string', 'to_string', 'utcnow_to_string',
 'now_to_string', 'fromtimestamp', 'utcfromtimestamp', 'TZFixedOffset']