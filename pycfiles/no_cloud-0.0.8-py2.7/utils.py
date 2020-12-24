# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/no_cloud/utils.py
# Compiled at: 2017-01-01 16:24:15
import re, fnmatch, getpass, pyperclip
TIME_UNITS = {'m': 60, 
   'h': 3600, 
   'd': 86400, 
   'w': 604800}

def human_timedelta(time):
    match = re.match('^(\\d+)([mhdw])$', time)
    assert match, 'unknown time format `%s`' % time
    value = match.group(1)
    unit = match.group(2)
    return int(value) * TIME_UNITS[unit]


def get_password(prompt='Password', confirm=False):
    password = getpass.getpass(prompt + ': ')
    if confirm:
        confirmation = getpass.getpass('Confirmation: ')
        assert password == confirmation, 'password and confirmation must match'
    return password


def nth(generator, i):
    for current_iteration, data in enumerate(generator, 0):
        if current_iteration == i:
            return data


def first(generator):
    return nth(generator, 0)


def ignored(filename):
    patterns = [
     '.hg',
     '.git',
     '.env',
     '.DS_Store',
     '.localized']
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True


def cleanup_path(path, keep_leading=False):
    path = path.replace('//', '/').rstrip('/')
    if not keep_leading:
        path = path.lstrip('/')
    return path


def copy_to_clipboard(value):
    pyperclip.copy(value)
    if pyperclip.paste() == value:
        return '*copied to clipboard*'
    return value