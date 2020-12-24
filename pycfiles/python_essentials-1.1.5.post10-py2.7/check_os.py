# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/check_os.py
# Compiled at: 2015-12-24 21:24:55
import subprocess as sp, re, os, sys, platform
ARCHITECTURE_X86_64 = 'x86_64'
ARCHITECTURE_I386 = 'i386'
ARCHITECTURE_I686 = 'i686'
ARCHITECTURE_ARMV7L = 'armv7l'
INSTRUCTION_SET_AMD64 = 'amd64'
INSTRUCTION_SET_I386 = 'i386'
ARCHITECTURE_INSTRUCTION_SET_DICT = {ARCHITECTURE_X86_64: INSTRUCTION_SET_AMD64, 
   ARCHITECTURE_I386: INSTRUCTION_SET_I386, 
   ARCHITECTURE_I686: INSTRUCTION_SET_I386}
lsb_release = 'lsb_release'

def check_linux():
    if not check_python3():
        ret_value = sys.platform == 'linux2'
        return ret_value
    else:
        ret_value = sys.platform == 'linux'
        return ret_value


def check_opensuse():
    try:
        lsb_release_id_short = sp.check_output([lsb_release, '-d', '-s'])
        return 'openSUSE' in lsb_release_id_short
    except Exception:
        return False


def check_ubuntu():
    try:
        lsb_release_id_short = sp.check_output([lsb_release, '-d', '-s']).strip().decode('utf-8')
        ret_value = 'Ubuntu' in lsb_release_id_short
        return ret_value
    except Exception:
        return False


def check_debian():
    try:
        lsb_release_id_short = sp.check_output([lsb_release, '-d', '-s']).strip().decode('utf-8')
        ret_value = 'Debian' in lsb_release_id_short
        return ret_value
    except Exception:
        return False


def check_linuxmint():
    try:
        lsb_release_id_short = sp.check_output([lsb_release, '-d', '-s']).strip().decode('utf-8')
        ret_value = 'Linux Mint' in lsb_release_id_short
        return ret_value
    except Exception:
        return False


def check_freebsd():
    return platform.system() == 'FreeBSD'


def check_root():
    uid = sp.check_output(['id', '-u']).strip()
    ret_value = int(uid) == 0
    return ret_value


def check_python3():
    ret_value = sys.version_info >= (3, 0)
    return ret_value


def findout_architecture():
    architecture = sp.check_output(['uname', '-m']).strip()
    return architecture


def findout_instruction_set():
    architecture = findout_architecture()
    instruction_set = ARCHITECTURE_INSTRUCTION_SET_DICT[architecture]
    return instruction_set


def findout_release_ubuntu():
    while not os.path.isfile('/usr/bin/python2.6') and not os.path.isfile('/usr/bin/python2.7'):
        print "Neither python2.6 nor python 2.7 could be found in /usr/bin/. It's necessary to determine your distribution release"
        confirm('proceed', 'Install python 2.6 or 2.7 and make it available at /usr/bin/python2.6 or /usr/lib/python2.7')

    release = sp.check_output([lsb_release, '-cs']).strip().decode('utf-8')
    return release


def findout_release_debian():
    return findout_release_ubuntu()


def findout_release_ubuntu_tuple():
    while not os.path.isfile('/usr/bin/python2.6') and not os.path.isfile('/usr/bin/python2.7'):
        print "Neither python2.6 nor python 2.7 could be found in /usr/bin/. It's necessary to determine your distribution release"
        confirm('proceed', 'Install python 2.6 or 2.7 and make it available at /usr/bin/python2.6 or /usr/lib/python2.7')

    release_number = sp.check_output([lsb_release, '-rs']).strip().decode('utf-8')
    release_tuple = tuple([ int(x) for x in release_number.split('.') ])
    return release_tuple


def findout_release_linuxmint():
    ret_value = sp.check_output([lsb_release, '-r', '-s']).decode('utf-8').strip()
    return int(ret_value)