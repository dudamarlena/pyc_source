# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/getvps.py
# Compiled at: 2014-07-04 18:13:34
import requests, sys, time, random, re

class Query:

    def __init__(self, sleepTime=30, trycount=1):
        randVal = random.randint(0, 10000)
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.' + str(randVal) + '.52 Safari/537.36'
        url = 'https://noupload.com/'
        sess = requests.session()
        sess.headers.update({'User-Agent': user_agent})
        r = sess.get(url)
        time.sleep(5)
        if 'PHPSESSID' not in r.cookies:
            print 'Not Found Cookie["PHPSESSID"]'
            sys.exit()
        url = 'https://noupload.com/create'
        params = {}
        cookie = {'PHPSESSID': r.cookies['PHPSESSID']}
        sess.headers.update({'referer': 'https://noupload.com/'})
        sess.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        sess.headers.update({'User-Agent': user_agent})
        r2 = sess.post(url, cookies=cookie)
        time.sleep(sleepTime)
        url = 'https://noupload.com/'
        cookie = {'PHPSESSID': r.cookies['PHPSESSID']}
        sess.headers.update({'User-Agent': user_agent})
        r3 = sess.get(url, cookies=cookie)
        rtrnParams = {}
        regex = re.compile('<h3>IP: <span class="label label-info">.+?</span></h3>')
        match = regex.search(r3.text)
        if match:
            ipPassStr = match.group()
            regex = re.compile('\\d+?\\.\\d+?\\.\\d+?\\.\\d+')
            match = regex.search(ipPassStr)
            if match:
                rtrnParams['ipAddr'] = match.group()
            else:
                print 'IP=NO'
            regex = re.compile('Username: <span class="label label-info">.+?</span>')
            match = regex.search(ipPassStr)
            if match:
                userName = match.group()
                userName = userName[41:]
                userName = userName.strip('</span>')
                rtrnParams['userName'] = userName
            else:
                print 'UserName=NO'
            regex = re.compile('Password: <span class="label label-info">.+?</span></h3>')
            match = regex.search(ipPassStr)
            if match:
                pswd = match.group()
                pswd = pswd[41:]
                pswd = pswd.strip('</span></h3>')
                rtrnParams['password'] = pswd
            else:
                print 'Pass=NO'
        else:
            print 'Not Match!'
        self.params = rtrnParams

    def getData(self):
        return self.params