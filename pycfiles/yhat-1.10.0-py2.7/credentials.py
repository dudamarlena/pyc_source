# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/credentials.py
# Compiled at: 2017-04-26 17:15:42
import json, base64, os, re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from builtins import input

def has():
    """
    Checks if the user has saved their credentials.
    """
    return os.path.isfile(os.path.join(os.environ['HOME'], '.yhat', '.config'))


def setup():
    """
    Prompts the user for their credentials and the saves them to a Yhat "dot"
    file.
    """
    _username = ''
    _apikey = ''
    _server = ' [%s]' % 'http://cloud.yhathq.com'
    if has():
        creds = read()
        _username = ' [%s]' % creds['username']
        _apikey = ' [%s]' % creds['apikey']
        _server = ' [%s]' % creds['server']
    username = input('Yhat username' + _username + ': ')
    apikey = input('Yhat apikey' + _apikey + ': ')
    server = input('Yhat server' + _server + ': ')
    if username == '':
        username = re.search('[^[]*\\[([^]]*)\\]', _username).group(1)
    if apikey == '':
        apikey = re.search('[^[]*\\[([^]]*)\\]', _apikey).group(1)
    if server == '':
        server = re.search('[^[]*\\[([^]]*)\\]', _server).group(1)
    else:
        if 'http://' not in server and 'https://' not in server:
            server = 'http://' + server
        o = urlparse(server)
        server = '%s://%s' % (o.scheme, o.netloc)
    yhat_dir = os.path.join(os.environ['HOME'], '.yhat')
    if not os.path.exists(yhat_dir):
        os.makedirs(yhat_dir)
    with open(os.path.join(yhat_dir, '.config'), 'w') as (f):
        data = json.dumps({'username': username, 'apikey': apikey, 
           'server': server})
        data = base64.encodestring(data)
        f.write(data)


def read():
    """
    Extracts credentials from a "dot" file

    Returns
    =======
    credentials: dict
        your credentials in form:
        {"username": "YOUR USERNAME", "apikey": "YOUR APKIKEY}"
    """
    data = open(os.path.join(os.environ['HOME'], '.yhat', '.config')).read()
    return json.loads(base64.decodestring(data))