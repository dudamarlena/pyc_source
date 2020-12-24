# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_utils/utils.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 5033 bytes
import shutil, os, glob, math

def format_bytes(n):
    """
    Given a float number (bytes) returns size output
    strings human readable, e.g.
    out = format_bytes(9909043.20)
    It return a string digit with metric suffix
    """
    unit = [
     'B', 'KiB', 'MiB', 'GiB', 'TiB',
     'PiB', 'EiB', 'ZiB', 'YiB']
    const = 1024.0
    if n == 0.0:
        exponent = 0
    else:
        exponent = int(math.log(n, const))
    suffix = unit[exponent]
    output_value = n / const ** exponent
    return '%.2f%s' % (output_value, suffix)


def to_bytes(string):
    """
    Convert given size string to bytes, e.g.
    out = to_bytes('9.45MiB')
    It return a number 'float'
    """
    value = 0.0
    unit = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    const = 1024.0
    for index, metric in enumerate(reversed(unit)):
        if metric in string:
            value = float(string.split(metric)[0])
            break

    exponent = index * -1 + (len(unit) - 1)
    return round(value * const ** exponent, 2)


def time_seconds(time):
    """
    convert time human to seconds e.g. time_seconds('00:02:00')
    """
    if time == 'N/A':
        return int('0')
    pos = time.split(':')
    h, m, s = pos[0], pos[1], pos[2]
    duration = int(h) * 3600 + int(m) * 60 + float(s)
    return duration


def time_human(seconds):
    """
    Convert from seconds to time human. Accept integear only e.g.
    time_human(2300)
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%d:%02d:%02d' % (h, m, s)


def copy_restore(src, dest):
    """
    Restore file. File name is owner choice and can be an preset
    or not. If file exist overwrite it.
    """
    try:
        shutil.copyfile(src, '%s' % dest)
    except FileNotFoundError as err:
        try:
            return err
        finally:
            err = None
            del err


def copy_backup(src, dest):
    """
    function for file backup. File name is owner choice.
    """
    shutil.copyfile('%s' % src, dest)


def makedir_move(ext, name_dir):
    """
    this function make directory and move-in file
    (ext, name_dir: extension, directory name)
    """
    try:
        os.mkdir('%s' % name_dir)
    except OSError as err:
        try:
            return err
        finally:
            err = None
            del err

    move_on(ext, name_dir)


def move_on(ext, name_dir):
    """
    Cycling on name extension file and move-on in other directory
    """
    files = glob.glob('*%s' % ext)
    for sposta in files:
        print('%s   %s' % (sposta, name_dir))


def copy_on(ext, name_dir, path_confdir):
    """
    Cycling on path and file extension name for copy files in other directory
    ARGUMENTS:
    ext: files extension with no dot
    name_dir: path name with no basename
    """
    files = glob.glob('%s/*.%s' % (name_dir, ext))
    for copia in files:
        shutil.copy(copia, '%s' % path_confdir)


def delete(ext):
    """
    function for file group delete with same extension
    """
    files = glob.glob('*%s' % ext)
    for rimuovi in files:
        os.remove(rimuovi)