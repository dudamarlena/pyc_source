# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jake/CRAPtion/craption/utils.py
# Compiled at: 2018-05-18 03:22:54
import craption.settings, datetime, os, pkg_resources, pyperclip, random, re, subprocess, sys, tempfile, time

def set_clipboard(data):
    pyperclip.copy(data)


def screenshot():
    path = tempfile.mktemp('.png')
    if sys.platform.startswith('linux'):
        run(['scrot', '-s', path])
    else:
        run(['screencapture', '-ix', path])
    return path


def get_filename():
    conf = craption.settings.get_conf()
    filename = conf['file']['name']
    now = time.time()
    for match in re.finditer('{r(\\d+)}', filename):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        random_string = ('').join([ random.choice(chars) for _ in range(int(match.group(1))) ])
        filename = filename.replace(match.group(0), random_string)

    filename = filename.replace('{u}', str(int(now)))
    filename = filename.replace('{d}', datetime.datetime.fromtimestamp(now).strftime(conf['file']['datetime_format']))
    return filename + '.png'


def install():
    craption.settings.write_template()
    exit(0)


def run(args):
    devnull = open(os.devnull, 'wb')
    p = subprocess.Popen(args, stdout=devnull, stderr=devnull)
    p.wait()