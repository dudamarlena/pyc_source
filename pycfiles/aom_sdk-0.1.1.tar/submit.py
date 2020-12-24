# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aojtools/submit.py
# Compiled at: 2014-11-04 09:55:25
import urllib, time, socket, generated as api

def submit_noresult(info, timeout=None):
    assert sorted(info.keys()) == sorted(['user_id', 'code', 'problem_id', 'lang', 'password']), 'first argument must have keys ["user_id", "code", "problem_id", "lang", "password"]'
    assert timeout is None or isinstance(timeout, int) and timeout > 0, 'timout must be a positive integer'
    if isinstance(info['problem_id'], int):
        info['problem_id'] = '%04d' % info['problem_id']
    assert info['lang'] in ('C', 'C++', 'JAVA'), 'lang must be "C", "C++" or "JAVA"'
    url = 'http://judge.u-aizu.ac.jp/onlinejudge/servlet/Submit'
    info = {'userID': info['user_id'], 
       'sourceCode': info['code'], 
       'problemNO': info['problem_id'], 
       'language': info['lang'].upper(), 
       'password': info['password']}
    postdata = urllib.urlencode(info)
    if timeout is not None:
        socket.setefaulttimeout(timeout)
    resp = urllib.urlopen(url, postdata).read()
    return resp


def tryntimes(fun, nmax=10, interval=2, timeout=10):
    try:
        return fun()
    except Exception as e:
        if nmax:
            time.sleep(interval)
            return tryntimes(fun, nmax - 1, interval, timeout)
        raise Exception('maximum try times exceed')


def lastrunid(info):
    resp = api.StatusLogSearchAPI(user_id=info['user_id'])
    return (
     resp.status[0], resp.status[0].run_id)


def submit(info, timeout=None, waittime=2, maxtry=10):
    """
    usage:
        info = {
            'user_id': (user id),
            'password': (password),
            'code': (source code),
            'problem_id': (problem id, integer or string),
            'lang': (language "C","C++",or"JAVA")
        }
        submit(info)
        #submit(info, timeout=3) # seconds
    """
    resp, rid = lastrunid(info)
    try:
        submit_noresult(info, timeout)
    except Exception as e:
        raise e

    if 'UserID or Password is Wrong.' in resp:
        raise Exception('userid or password is wrong.')

    def fun():
        resp, new_rid = lastrunid(info)
        if new_rid > rid:
            return resp
        raise Exception('fun')

    return tryntimes(fun, maxtry, waittime, timeout)