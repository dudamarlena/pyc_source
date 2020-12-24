# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/download/_fetch.py
# Compiled at: 2020-04-17 06:44:40
"""
*Retrieve an HTML document or file from the web at a given URL*

:Author:
    David Young
"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def _fetch(url):
    """
    *Retrieve an HTML document or file from the web at a given URL*

    **Key Arguments**

    
      - ``url`` -- the URL of the document or file

    **Return**

    
      - ``url`` -- the URL of the document or file, or None if an error occured
      - ``body`` -- the text content of the HTML document.
    """
    import logging as log, socket
    from eventlet import Timeout
    import urllib, sys
    tries = 10
    count = 1
    downloaded = False
    while count < tries and downloaded == False:
        try:
            log.debug('downloading ' + url.get_full_url())
            body = urllib.request.urlopen(url).read()
            downloaded = True
        except socket.timeout as e:
            print('timeout on URL, trying again')
            count += 1
        except Exception as e:
            if '[Errno 60]' in str(e):
                log.warning('timeout on URL, trying again' % locals())
                count += 1
            if 'Error 502' in str(e):
                log.warning('proxy error on URL, trying again' % locals())
                count += 1
            else:
                log.warning('could not download ' + url.get_full_url() + ' : ' + str(e) + '\n')
                url = None
                body = None
                downloaded = True

    return (
     url, body)