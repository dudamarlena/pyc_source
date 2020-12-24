# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/__init__.py
# Compiled at: 2011-01-27 14:39:21
"""Main cifit library code."""
from cifitlib.classes import classes
import cifitlib.appadm, cifitlib.files, cifitlib.network, cifitlib.pkgs, cifitlib.procs, cifitlib.state
sysadm = cifitlib.appadm.SysADM()
mysql = cifitlib.appadm.MysqlADM()
mailman = cifitlib.appadm.MailmanADM()
pg = cifitlib.appadm.PostgresADM()
cifitlib.pear = cifitlib.pkgs.pearPKG()
cifitlib.state = cifitlib.state.State
cifitlib.runs = cifitlib.state('cifit_runs')
try:
    import setuptools
    __version__ = setuptools.pkg_resources.get_distribution('cifitlib').version
except:
    import version
    __version__ = version.version

cifitlib.runs.add(__version__)