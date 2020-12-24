# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/remchecker/__init__.py
# Compiled at: 2010-09-09 11:28:27
from __future__ import with_statement
import os, sys, yaml, tweepy
CONSUMER_KEY = 'NMaOvEn0u8QSwhxiGGY0rg'
CONSUMER_SECRET = 'FtY5BbJkaotQQDjUCEutCBk8fL8E8dH67fhKh07dkQ'
CONFIG = os.path.expanduser('~/.remchecker.yml')
MESSAGE = '%s にリムーブされました'

def init(filename):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    print 'Please authorize us: %s' % auth.get_authorization_url()
    verifier = raw_input('PIN: ').strip()
    access_token = auth.get_access_token(verifier)
    api = tweepy.API(auth)
    data = dict(key=access_token.key, secret=access_token.secret, followers=list((str(user.screen_name) for user in tweepy.Cursor(api.followers).items())))
    with open(filename, 'w') as (f):
        yaml.dump(data, f, encoding='utf8')


def update(filename):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    data = {}
    prev = set()
    with open(filename) as (f):
        data = yaml.load(f.read().decode('utf8'))
        auth.set_access_token(data['key'], data['secret'])
        prev = set(data['followers'])
    api = tweepy.API(auth)
    current = set((str(user.screen_name) for user in tweepy.Cursor(api.followers).items()))
    users = []
    diff = prev - current
    for s in diff:
        if users and len(users[(-1)]) + len(s) + 2 + len(MESSAGE) < 140:
            users[(-1)] += ' @' + s
        else:
            users.append('@' + s)

    if diff:
        sys.stderr.write('removed by ' + (', ').join(('@' + u for u in diff)) + '\n')
    myname = api.me().screen_name
    for s in users:
        api.send_direct_message(screen_name=myname, text=MESSAGE.encode('utf8') % s)

    data['followers'] = list(current)
    with open(filename, 'w') as (f):
        yaml.dump(data, f, encoding='utf8')


def main():
    if not os.path.exists(CONFIG):
        init(CONFIG)
    else:
        update(CONFIG)