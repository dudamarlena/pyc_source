# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: __init__.py
# Compiled at: 2016-04-08 04:32:28
from __future__ import unicode_literals, division, absolute_import, print_function
import base64, string, requests, datetime
from pyramid.httpexceptions import HTTPFound

def NDict(request, d):
    for i in d:
        if not d[i]:
            d[i] = b''

    return d


def ReqPost(request, url, data, headers=None):
    req = requests.post(url, data, verify=False, headers=headers)
    req.close()
    return req


def ReqGet(request, url, headers=None):
    req = requests.get(url, verify=False, headers=headers)
    req.close()
    return req


def ReqGetUser(request):
    hdr = {b'User-Agent': b'Mozilla/5.0 (X11; Linux x86_64)      AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
       b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
       b'Accept-Charset': b'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
       b'Accept-Encoding': b'none', 
       b'Accept-Language': b'en-US,en;q=0.8', 
       b'Referer': request.registry.settings[b'login_url'], 
       b'Connection': b'keep-alive'}
    req = request.rget(request.registry.settings[b'sso_user'].format(request.session[b'token']), headers=hdr)
    req.close()
    return req.text


def userinfo(request, username=None):
    req = request.rpost(request.registry.settings[b'sso_userinfo'] + b'user=' + base64.decodestring(request.registry.settings[b'secret'][4:] + b'\n') + b'&password=' + base64.decodestring(request.registry.settings[b'key'][4:] + b'\n'), {b'username': username})
    try:
        user = request.dict(req.json()[0])
    except:
        return

    try:
        string.atoi(user[b'username'][(-1)], 10)
        try:
            string.atoi(user[b'username'][(-2)], 10)
            try:
                string.atoi(user[b'username'][(-3)], 10)
                user[b'cnname'] = user[b'cnname'] + b'%s%s%s' % tuple(user[b'username'][-3:])
            except:
                user[b'cnname'] = user[b'cnname'] + b'%s%s' % tuple(user[b'username'][-2:])

        except:
            user[b'cnname'] = user[b'cnname'] + b'%s' % tuple(user[b'username'][-1:])

    except:
        user[b'cnname'] = user[b'cnname']

    return user


def clean(request, url=b'/login'):
    del request.session[b'token']
    del request.session[b'expires']
    del request.session[b'username']
    del request.session[b'user']


def initialized(request):
    request.session[b'token'] = request.params.get(b't')
    request.session[b'expires'] = datetime.datetime.now() + datetime.timedelta(seconds=86400)
    request.session[b'username'] = request.rget_user()
    if not request.session[b'username']:
        clean(request)
    request.session[b'user'] = request.userinfo(request.session[b'username'])
    if not request.session[b'user'] and datetime.datetime.now().month >= 6:
        clean(request)


def token(request):
    if request.session.get(b'token', None):
        if request.session.get(b'expires', datetime.datetime.now()) < datetime.datetime.now():
            clean(request)
        if request.path == b'/login':
            raise HTTPFound(b'/')
        if request.path == b'/logout':
            clean(request, request.registry.settings[b'sso_logout'])
        request.session[b'expires'] = datetime.datetime.now() + datetime.timedelta(seconds=86400)
    elif request.path == b'/login':
        if request.params.get(b't', None):
            initialized(request)
            raise HTTPFound(b'/')
        else:
            raise HTTPFound(request.registry.settings[b'sso_login'])
    else:
        if b'_items' in request.POST.__dict__:
            return True
        raise HTTPFound(b'/login')
    return


def init(config):
    config.add_request_method(token, b'token')
    config.add_request_method(ReqPost, b'rpost')
    config.add_request_method(ReqGet, b'rget')
    config.add_request_method(ReqGetUser, b'rget_user')
    config.add_request_method(userinfo, b'userinfo')
    config.add_request_method(NDict, b'dict')