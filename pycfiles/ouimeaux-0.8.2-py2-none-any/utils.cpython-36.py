# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/utils.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 2252 bytes
from functools import wraps
import re, socket, struct, time, gevent, requests

def tz_hours():
    delta = time.localtime().tm_hour - time.gmtime().tm_hour
    sign = '-' if delta < 0 else ''
    return '%s%02d.00' % (sign, abs(delta))


def is_dst():
    if time.localtime().tm_isdst:
        return 1
    else:
        return 0


def get_timesync():
    timesync = '\n<?xml version="1.0" encoding="utf-8"?>\n<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n <s:Body>\n  <u:TimeSync xmlns:u="urn:Belkin:service:timesync:1">\n   <UTC>{utc}</UTC>\n   <TimeZone>{tz}</TimeZone>\n   <dst>{dst}</dst>\n   <DstSupported>{dstsupported}</DstSupported>\n  </u:TimeSync>\n </s:Body>\n</s:Envelope>'.format(utc=(int(time.time())),
      tz=(tz_hours()),
      dst=(is_dst()),
      dstsupported=(is_dst())).strip()
    return timesync


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        try:
            s.connect(('1.2.3.4', 9))
            return s.getsockname()[0]
        except socket.error:
            return

    finally:
        del s


def matcher(match_string):
    pattern = re.compile('.*?'.join(re.escape(c) for c in match_string.lower()))

    def matches(s):
        return pattern.search(s.lower()) is not None

    return matches


_RETRIES = 30.016666666666666

def get_retries():
    return _RETRIES


def retry_with_delay(f, delay=60):
    """
    Retry the wrapped requests.request function in case of ConnectionError.
    Optionally limit the number of retries or set the delay between retries.
    """

    @wraps(f)
    def inner(*args, **kwargs):
        kwargs['timeout'] = 5
        remaining = get_retries() + 1
        while remaining:
            remaining -= 1
            try:
                return f(*args, **kwargs)
            except (requests.ConnectionError, requests.Timeout):
                if not remaining:
                    raise
                gevent.sleep(delay)

    return inner


requests_get = retry_with_delay(requests.get)
requests_post = retry_with_delay(requests.post)
requests_request = retry_with_delay(requests.request)