# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/training/tokenTools.py
# Compiled at: 2018-07-12 08:05:01
renewtokens = True

def renew_token_process():
    if not renewtokens:
        return
    import subprocess, time
    while True:
        logstr = ''
        try:
            logstr = subprocess.check_call(['kinit', '-R'])
            logstr += subprocess.check_call(['aklog'])
        except:
            print logstr

        time.sleep(3600)


def checkTokens(cutofftime_hours=48):
    if not renewtokens:
        return True
    import subprocess
    klist = ''
    try:
        klist = str(subprocess.check_output(['klist'], stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as inst:
        print 'klist failed - no token?'
        klist = ''
        del inst

    if 'renew' not in klist:
        print 'did not find renew option in kerberos token. Starting kinit'
        subprocess.check_call(['kinit', '-l 96h'])
        subprocess.check_call(['aklog'])
        return True
    klist = str(klist).split()
    firstrenewapp = klist.index('renew')
    kdate = klist[(firstrenewapp + 2)]
    ktime = klist[(firstrenewapp + 3)]
    import datetime
    thistime = datetime.datetime.now()
    day, month, year = kdate.split('/')
    hour, minu, sec = ktime.split(':')
    tokentime = datetime.datetime(2000 + int(year), int(month), int(day), int(hour))
    diff = tokentime - thistime
    diff = diff.total_seconds()
    if diff < cutofftime_hours * 3600:
        print 'token will expire soon. Starting kinit'
        subprocess.check_call(['kinit', '-l 96h'])
        subprocess.check_call(['aklog'])
    return True