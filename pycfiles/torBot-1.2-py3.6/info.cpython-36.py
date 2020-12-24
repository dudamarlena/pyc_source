# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/info.py
# Compiled at: 2018-07-01 06:51:02
# Size of source mod 2**32: 2680 bytes
import requests
from urllib.parse import urlsplit
from termcolor import cprint

def executeAll(target, soup, response):
    try:
        get_robots_txt(target)
    except Exception:
        cprint('No robots.txt file Found!blue')

    try:
        get_dot_git(target)
    except Exception:
        cprint('Error !red')

    try:
        get_dot_svn(target)
    except Exception:
        cprint('Errorred')

    try:
        get_dot_htaccess(target)
    except Exception:
        cprint('Errorred')

    try:
        get_webpage_description(soup)
    except Exception:
        cprint('Errorred')

    try:
        get_headers(response)
    except Exception:
        cprint('Errorred')


def get_headers(response):
    print('\n          RESPONSE HEADERS\n          __________________\n          ')
    for key, val in response.headers.items():
        print('*', key, ':', val)


def get_robots_txt(target):
    cprint('[*]Checking for Robots.txtyellow')
    url = target
    target = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
    requests.get(target + '/robots.txt')
    cprint('blue')


def get_dot_git(target):
    cprint('[*]Checking for .git folderyellow')
    url = target
    target = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
    req = requests.get(target + '/.git/')
    r = req.status_code
    if r == 200:
        cprint('Alert!red')
        cprint('.git folder exposed publiclyred')
    else:
        print('NO .git folder foundblue')


def get_dot_svn(target):
    cprint('[*]Checking for .svn folderyellow')
    url = target
    target = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
    req = requests.get(target + '/.svn/entries')
    r = req.status_code
    if r == 200:
        cprint('Alert!red')
        cprint('.SVN folder exposed publiclyred')
    else:
        cprint('NO .SVN folder foundblue')


def get_dot_htaccess(target):
    cprint('[*]Checking for .htaccessyellow')
    url = target
    target = '{0.scheme}://{0.netloc}/'.format(urlsplit(url))
    req = requests.get(target + '/.htaccess')
    statcode = req.status_code
    if statcode == 403:
        cprint('403 Forbiddenblue')
    else:
        if statcode == 200:
            cprint('Alert!!blue')
            cprint('.htaccess file found!blue')
        else:
            cprint('Status codeblue')
            cprint(statcode)


def get_webpage_description(soup):
    cprint('[*]Checking for description meta tagyellow')
    metatags = soup.find_all('meta')
    for meta in metatags:
        if meta.has_attr('name'):
            attributes = meta.attrs
            if attributes['name'] == 'description':
                cprint('Page description: ' + attributes['content'])