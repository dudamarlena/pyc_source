# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/http/handler.py
# Compiled at: 2011-11-24 06:30:42
import mimetypes, threading, Queue, copy
from Cookie import SimpleCookie
from cgi import parse_qs, escape
import pypoly, pypoly.session
request = None
response = None
session = None

def pypolyauth():
    action = pypoly.http.request.params.get('_pypoly_action', None)
    if action == None:
        return
    else:
        action = action.lower()
        pypoly.log.debug('PyPoly-Action: %s' % action)
        if action == 'login':
            username = pypoly.http.request.params.get('username', None)
            password = pypoly.http.request.params.get('password', None)
            if username == None or password == None:
                return
            pypoly.http.auth.login(username, password)
            del pypoly.http.request.params['username']
            del pypoly.http.request.params['password']
        elif action == 'logout':
            pypoly.http.auth.logout()
        del pypoly.http.request.params['_pypoly_action']
        return


def set_lang():
    """
    Set the language for the system

    :ToDo: check if the language exists
    """
    lang = pypoly.http.request.params.get('_pypoly_lang', None)
    if lang == None:
        return
    else:
        pypoly.session.set_pypoly('user.lang', lang)
        return


def set_template():
    """
    Set the Webpage Template
    """
    tpl = pypoly.http.request.params.get('_pypoly_template', None)
    if tpl == None or tpl not in pypoly.template.templates:
        return
    else:
        pypoly.session.set_pypoly('template.name', pypoly.http.request.params['_pypoly_template'])
        del pypoly.http.request.params['_pypoly_template']
        return