# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/mobile_agents.py
# Compiled at: 2011-12-23 04:19:50
__author__ = 'KMihajlov'
search_strings = [
 'sony',
 'symbian',
 'nokia',
 'samsung',
 'mobile',
 'windows ce',
 'epoc',
 'opera mini',
 'nitro',
 'j2me',
 'midp-',
 'cldc-',
 'netfront',
 'mot',
 'up.browser',
 'up.link',
 'audiovox',
 'blackberry',
 'ericsson,',
 'panasonic',
 'philips',
 'sanyo',
 'sharp',
 'sie-',
 'portalmmm',
 'blazer',
 'avantgo',
 'danger',
 'palm',
 'series60',
 'palmsource',
 'pocketpc',
 'smartphone',
 'rover',
 'ipaq',
 'au-mic,',
 'alcatel',
 'ericy',
 'up.link',
 'docomo',
 'vodafone/',
 'wap1.',
 'wap2.',
 'plucker',
 '480x640',
 'sec',
 'fennec',
 'android',
 'google wireless transcoder',
 'nintendo',
 'webtv',
 'playstation']

def detect_mobile(request):
    """Adds a "mobile" attribute to the request which is True or False
       depending on whether the request should be considered to come from a
       small-screen device such as a phone or a PDA"""
    if request.headers.environ.has_key('HTTP_X_OPERAMINI_FEATURES'):
        return True
    if request.headers.environ.has_key('HTTP_ACCEPT'):
        s = request.headers.environ['HTTP_ACCEPT'].lower()
        if 'application/vnd.wap.xhtml+xml' in s:
            return True
    if request.headers.environ.has_key('HTTP_USER_AGENT'):
        s = request.headers.environ['HTTP_USER_AGENT'].lower()
        for ua in search_strings:
            if ua in s:
                return True

    return False