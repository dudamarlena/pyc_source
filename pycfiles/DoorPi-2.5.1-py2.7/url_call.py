# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/url_call.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi, urllib2, ssl, urlparse

def fire_command(url):
    try:
        if '@' in url:
            nurl = urlparse.urlsplit(url)
            username = nurl.username
            password = nurl.password
            url = url.replace(username + ':' + password + '@', '')
            url = url.replace(' ', '%20')
            logger.debug('url: %s' % url)
            ssl._create_default_https_context = ssl._create_unverified_context
            p = urllib2.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, url, username, password)
            handler = urllib2.HTTPBasicAuthHandler(p)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            url = url.replace(' ', '%20')
            logger.info('url: %s' % url)
            return urllib2.urlopen(url=url, data=None, timeout=1)
    except urllib2.HTTPError as exp:
        logger.error('HTTPError: %s - %s' % (exp.code, exp.reason))
    except urllib2.URLError as exp:
        logger.error('URLError: %s' % exp.reason)

    return False


def get(parameters):
    parsed_parameters = doorpi.DoorPi().parse_string(parameters)
    return UrlCallAction(fire_command, url=parsed_parameters)


class UrlCallAction(SingleAction):
    pass