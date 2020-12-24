# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/lib/textguard/antimat.py
# Compiled at: 2008-10-21 04:34:39
"""Antimat class for the textguard package

$Id: antimat.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
__credits__ = 'Ilya Soldatkin, arc <at> tcen.ru -- original Perl module Lingua::RU::Antimat, http://www.tcen.ru/antimat'
import re, os.path
from inspect import isfunction
_ANTI_FILE = os.path.join(os.path.dirname(__file__), 'antiutf8')
anti = re.compile('(?:\\b|(?<=_))(?:%s)(?:\\b|(?=_))' % open(_ANTI_FILE).read().decode('utf-8'), flags=re.U | re.I)

def remove_slang(repl, slang, count=0):
    if isfunction(repl):
        real_repl = lambda m: repl(m.group(0))
    else:
        real_repl = repl
    return anti.sub(real_repl, string, count)


def detect_slang(slang):
    return anti.match(slang)