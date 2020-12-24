# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/opendir.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 2740 bytes
import subprocess, os

def browse(OS, pathname):
    """
    open file browser in a specific location with
    file manager of the OS
    """
    status = 'Unrecognized error'
    if OS == 'Windows':
        cmd = ' '.join(['cmd', '/c', 'start', pathname])
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        if OS == 'Darwin':
            cmd = [
             'open', pathname]
            info = None
        else:
            cmd = [
             'xdg-open', pathname]
            info = None
    try:
        p = subprocess.Popen(cmd, stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT),
          universal_newlines=True,
          startupinfo=info)
        out = p.communicate()
    except (OSError, FileNotFoundError) as oserr:
        try:
            status = '%s' % oserr
        finally:
            oserr = None
            del oserr

    else:
        if p.returncode:
            status = out[0]
        else:
            status = None