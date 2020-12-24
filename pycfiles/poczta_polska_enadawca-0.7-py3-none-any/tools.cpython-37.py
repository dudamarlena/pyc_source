# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/thirdparty/ifcfg/ifcfg/tools.py
# Compiled at: 2019-04-08 04:14:26
# Size of source mod 2**32: 1543 bytes
from __future__ import unicode_literals
import locale, logging, os
from subprocess import PIPE, Popen
system_encoding = locale.getpreferredencoding()

def minimal_logger(name):
    log = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s IFCFG DEBUG : %(name)s : %(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    if 'IFCFG_DEBUG' in os.environ.keys():
        if os.environ['IFCFG_DEBUG'] == '1':
            log.setLevel(logging.DEBUG)
            log.addHandler(console)
    return log


def exec_cmd(cmd_args):
    proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE, universal_newlines=False, shell=True)
    stdout, stderr = proc.communicate()
    proc.wait()
    stdout = stdout.decode(system_encoding, errors='replace')
    stderr = stderr.decode(system_encoding, errors='replace')
    return (
     stdout, stderr, proc.returncode)


def hex2dotted(hex_num):
    num = hex_num.split('x')[1]
    w = int(num[0:2], 16)
    x = int(num[2:4], 16)
    y = int(num[4:6], 16)
    z = int(num[6:8], 16)
    return '%d.%d.%d.%d' % (w, x, y, z)