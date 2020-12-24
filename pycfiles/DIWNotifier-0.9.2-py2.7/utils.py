# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/utils/utils.py
# Compiled at: 2014-02-05 13:45:29
import sys, os, logging
logging.basicConfig()
module_logger = logging.getLogger('utils.utils')
module_logger.setLevel('INFO')
import threading

class Thread(threading.Thread):

    def __init__(self, t, *args):
        self.handled = False
        threading.Thread.__init__(self, target=t, args=args)
        self.setDaemon(True)
        self.start()


import ConfigParser

class MyConfigParser(object):

    def __init__(self, path):
        self.config = ConfigParser.RawConfigParser()
        self.path = path
        self.report_bug_at = 'foo@bar.com'
        self.logger = logging.getLogger('utils.utils.MyconfigParser')
        self.logger.debug('creating an instance of utils.utils.MyconfigParser')

    def read_field(self, section, field):
        try:
            self.config.read(self.path)
            field_value = self.config.get(section, field)
        except ConfigParser.Error:
            module_logger.error('Error reading config file ' + self.path + ', please report bug at ' + self.report_bug_at)
            sys.exit(1)
        else:
            return field_value


import subprocess

def download_avatar(link, uri):
    flag = False
    if link.find('gravatar.com') != -1 and not link.find('default_large.png'):
        waldo = link.split('/')
        waldo = waldo[4].split('&')
        waldo = waldo[0]
        flag = True
    elif link.find('clandiw.it/uploads/') != -1:
        waldo = link.split('/')
        waldo = waldo[5]
        flag = True
    else:
        waldo = 'default_large.png'
    if flag:
        if not os.path.exists(uri + '' + waldo):
            p = subprocess.Popen(['wget', '-P', uri, link])
            p.communicate()
    return uri + '' + waldo


def bool_print(string, function, *args):
    if hasattr(function, '__call__'):
        flag = True if function(*args) else False
    else:
        flag = True if function else False
    module_logger.info(string) if flag else module_logger.error(string)
    return flag


def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (
).
    """
    return reduce(lambda line, word, w=width: '%s%s%s' % (
     line,
     ' \n'[(len(line) - line.rfind('\n') - 1 + len(word.split('\n', 1)[0]) >= w)],
     word), text.split(' '))


import re

def get_desktop_environment():
    if sys.platform in ('win32', 'cygwin'):
        return 'windows'
    else:
        if sys.platform == 'darwin':
            return 'mac'
        desktop_session = os.environ.get('DESKTOP_SESSION')
        if desktop_session is not None:
            desktop_session = desktop_session.lower()
            if desktop_session in ('gnome', 'unity', 'cinnamon', 'mate', 'xfce4', 'lxde',
                                   'fluxbox', 'blackbox', 'openbox', 'icewm', 'jwm',
                                   'afterstep', 'trinity', 'kde'):
                return desktop_session
            if 'xfce' in desktop_session or desktop_session.startswith('xubuntu'):
                return 'xfce4'
            if desktop_session.startswith('ubuntu'):
                return 'unity'
            if desktop_session.startswith('lubuntu'):
                return 'lxde'
            if desktop_session.startswith('kubuntu'):
                return 'kde'
            if desktop_session.startswith('razor'):
                return 'razor-qt'
            if desktop_session.startswith('wmaker'):
                return 'windowmaker'
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            return 'kde'
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if 'deprecated' not in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                return 'gnome2'
        else:
            if is_running('openbox'):
                return 'openbox'
            if is_running('xfce-mcs-manage'):
                return 'xfce4'
            if is_running('ksmserver'):
                return 'kde'
        return 'unknown'


def is_running(process):
    try:
        s = subprocess.Popen(['ps', 'axw'], stdout=subprocess.PIPE)
    except:
        s = subprocess.Popen(['tasklist', '/v'], stdout=subprocess.PIPE)

    for x in s.stdout:
        if re.search(process, x):
            return True

    return False


def check_notification_daemon():
    daemons = [
     'dunst', 'notify-osd', 'xfce4-notifyd', 'plasma-widgets-workspace', 'notification-daemon']
    for daemon in daemons:
        if is_running(daemon):
            return daemon

    return False


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return