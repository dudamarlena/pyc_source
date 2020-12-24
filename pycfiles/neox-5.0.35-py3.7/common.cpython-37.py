# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/common.py
# Compiled at: 2019-03-03 12:52:35
# Size of source mod 2**32: 1615 bytes
import os, sys, subprocess
from re import compile
import unicodedata
import neox.commons.rpc as rpc
from neox import __version__
_slugify_strip_re = compile('[^\\w\\s-]')
_slugify_hyphenate_re = compile('[-\\s]+')

def test_server_version(host, port):
    version = rpc.server_version(host, port)
    if not version:
        return False
    return version.split('.')[:2] == __version__.split('.')[:2]


def slugify(value):
    if not isinstance(value, str):
        value = value.decode('utf-8')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = value.decode('utf-8')
    value = _slugify_strip_re.sub('', value).strip().lower()
    return _slugify_hyphenate_re.sub('-', value)


def file_open(filename, type, direct_print=False):

    def save():
        pass

    name = filename.split('.')
    if 'odt' in name:
        direct_print = False
    if os.name == 'nt':
        operation = 'open'
        if direct_print:
            operation = 'print'
        try:
            os.startfile(os.path.normpath(filename), operation)
        except WindowsError:
            save()

    else:
        if sys.platform == 'darwin':
            try:
                subprocess.Popen(['/usr/bin/open', filename])
            except OSError:
                save()

        else:
            if direct_print:
                try:
                    subprocess.Popen(['lp', filename])
                except:
                    direct_print = False

            if not direct_print:
                try:
                    subprocess.Popen(['xdg-open', filename])
                except OSError:
                    pass