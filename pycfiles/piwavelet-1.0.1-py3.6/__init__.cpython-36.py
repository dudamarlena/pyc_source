# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/piwavelet/__init__.py
# Compiled at: 2020-03-19 11:26:12
# Size of source mod 2**32: 2287 bytes
__authors = 'Eduardo dos Santos Pereira, Regla D. Somoza'
__data = '13/03/2013'
__email = 'pereira.somoza@gmail.com,duthit@gmail.com'
import sys, os, piwavelet, shutil
from .wcoherence import *
from .smooth import *
from .piwavelet import *
from .motherWavelets import *
HOME = os.path.expanduser('~')
if not os.path.exists(HOME + '/.piwavelet'):
    local = os.path.dirname(piwavelet.__file__)
    print('Creating .piwavelet cache diretory in %s' % HOME)
    os.makedirs(HOME + '/.piwavelet')
    shutil.copytree(local + '/wtc', HOME + '/.piwavelet/wtc')
__all__ = ['waveletCC', 'Morlet', 'Paul', 'DOG',
 'Mexican_hat']