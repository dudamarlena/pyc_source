# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/hackmud_chat/hackmud.py
# Compiled at: 2018-10-23 10:27:29
import json, requests

def send(endpoint, data):
    """ send(string, dict) """
    url = ('https://www.hackmud.com/mobile/{}.json').format(endpoint)
    res = requests.post(url, json=data)
    if res.status_code == 200:
        res = res.json()
        if res['ok'] == True:
            return res
        print ('Request Error: {}').format(res['msg'])
    else:
        print ('Error {code}: {text}').format(code=res.status_code, text=res.text)


def get_token(passwd):
    return send('get_token', {'pass': passwd})['chat_token']


def get_account_data(token):
    return send('account_data', {'chat_token': token})


def get_chats(token, usernames, before=None, after=None):
    if before and after:
        return send('chats', {'chat_token': token, 
           'usernames': usernames, 
           'before': before, 
           'after': after})
    else:
        if before:
            return send('chats', {'chat_token': token, 
               'usernames': usernames, 
               'before': before})
        if after:
            return send('chats', {'chat_token': token, 
               'usernames': usernames, 
               'after': after})
        return send('chats', {'chat_token': token, 'usernames': usernames})


def get_history(token, username, before=None, after=None):
    if before and after:
        return send('chat_history', {'chat_token': token, 
           'username': username, 
           'before': before, 
           'after': after})
    else:
        return send('chat_history', {'chat_token': token, 'username': username})


def create_chat(token, username, msg, channel=None, dest=None):
    if channel and dest:
        msg = ('@{}: {}').format(dest, msg)
        return send('create_chat', {'chat_token': token, 
           'username': username, 
           'channel': channel, 
           'msg': msg})
    if channel:
        return send('create_chat', {'chat_token': token, 
           'username': username, 
           'channel': channel, 
           'msg': msg})
    if dest:
        return send('create_chat', {'chat_token': token, 
           'username': username, 
           'tell': dest, 
           'msg': msg})
    print 'I need someone or somewhere to talk...'