# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: updater.py
# Compiled at: 2014-08-24 19:14:50
"""
Detect any changes to the oneline configuration
and restart accordingly.

Changes include new files, updates, and deletes
"""
import hashlib, subprocess, os, re, ctypes

def kill(pid):
    """kill function for Win32"""
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(1, 0, pid)
    return 0 != kernel32.TerminateProcess(handle, 0)


class update(object):

    def start(self):
        prefix = ''
        salt = ''
        _dir = os.getcwd()
        ctimes = dict()
        if os.path.exists('../../modules/'):
            prefix = '../../'
            os.chdir('../../modules')
            files = os.listdir('./')
        else:
            if os.path.exists('../modules/'):
                prefix = '../'
                os.chdir('../modules')
                files = os.listdir('./')
            else:
                if os.path.exists('./modules/'):
                    prefix = './'
                    os.chdir('./modules')
                    files = os.listdir('./')
                else:
                    prefix = '../../'
                    os.chdir('../../modules')
                    files = os.listdir('./')
                for i in files:
                    if len(re.findall('\\.pyc$', i)) > 0:
                        continue
                    if not len(re.findall('\\.py$', i)) > 0:
                        continue
                    salt += '_' + i
                    ctimes[i] = os.path.getmtime(i)

            salt = hashlib.md5(salt).hexdigest()
            while True:
                os.chdir(_dir)
                if os.path.exists('../../modules/'):
                    prefix = '../../'
                    os.chdir('../../modules')
                    files = os.listdir('./')
                else:
                    if os.path.exists('../modules/'):
                        prefix = '../'
                        os.chdir('../modules')
                        files = os.listdir('./')
                    elif os.path.exists('./modules/'):
                        prefix = './'
                        os.chdir('./modules')
                        files = os.listdir('./')
                    else:
                        prefix = '../../'
                        os.chdir('../../modules')
                        files = os.listdir('./')
                    newsalt = ''
                    restart = False
                    for i in files:
                        if len(re.findall('\\.pyc$', i)) > 0:
                            continue
                        if not len(re.findall('\\.py$', i)) > 0:
                            continue
                        if i not in ctimes.keys():
                            ctimes[i] = os.path.getmtime(i)
                        try:
                            if not ctimes[i] == os.path.getmtime(i):
                                restart = True
                                ctimes[i] = os.path.getmtime(i)
                        except:
                            restart = True

                        newsalt += '_' + i

                newsalt = hashlib.md5(newsalt).hexdigest()
                os.chdir(_dir)
                if newsalt != salt or restart:
                    print 'oneline config has changed'
                    if os.path.exists('../../socket/'):
                        prefix = '../../'
                        os.chdir('../../socket')
                    else:
                        if os.path.exists('../socket/'):
                            prefix = '../'
                            os.chdir('../socket')
                        elif os.path.exists('./socket/'):
                            prefix = './'
                            os.chdir('./socket')
                        else:
                            prefix = '../../'
                            os.chdir('../../socket')
                        os.chdir(_dir)
                        try:
                            pid = int(open('./oneline.pid.txt', 'r+').read())
                            os.system('kill ' + str(pid))
                            subprocess.Popen(['python', prefix + 'server.py'])
                        except:
                            print "Coundln't stop process"

                    restart = False
                    salt = newsalt


u = update()
u.start()