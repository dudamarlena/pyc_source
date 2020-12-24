# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/Datos/devel/hg-repos/scru/scru/clipboard.py
# Compiled at: 2011-06-05 20:34:28
import subprocess

class XclipNotFound(Exception):
    """xclip must be installed"""
    pass


def copy(text):
    """Copy given text into system clipboard."""
    try:
        cmd = [
         'xclip', '-selection', 'clipboard']
        subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(unicode(text))
    except Exception as e:
        raise XclipNotFound


def paste():
    """Returns system clipboard contents."""
    try:
        cmd = [
         'xclip', '-selection', 'clipboard', '-o']
        return unicode(subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0])
    except Exception as e:
        raise XclipNotFound