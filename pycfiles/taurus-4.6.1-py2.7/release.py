# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/release.py
# Compiled at: 2019-08-19 15:09:29
"""
Release data for the taurus project. It contains the following members:

    - version : (str) version string
    - description : (str) brief description
    - long_description : (str) a long description
    - license : (str) license
    - authors : (dict<str, tuple<str,str>>) the list of authors
    - url : (str) the project url
    - download_url : (str) the project download url
    - platforms : list<str> list of supported platforms
    - keywords : list<str> list of keywords
"""
__docformat__ = 'restructuredtext'
name = 'taurus'
version = '4.6.1'
if '-' in version:
    _v, _rel = version.split('-')
else:
    _v, _rel = version, ''
_v = tuple([ int(n) for n in _v.split('.') ])
version_info = _v + (_rel, 0)
revision = str(version_info[4])
description = 'A framework for scientific/industrial CLIs and GUIs'
long_description = 'Taurus is a python framework for control and data\nacquisition CLIs and GUIs in scientific/industrial environments.\nIt supports multiple control systems or data sources: Tango, EPICS,...\nNew control system libraries can be integrated through plugins.'
license = 'LGPL'
authors = {'Tiago_et_al': ('Tiago Coutinho et al.', ''), 'Community': ('Taurus Community', 'tauruslib-devel@lists.sourceforge.net')}
url = 'http://www.taurus-scada.org'
download_url = 'http://pypi.python.org/packages/source/t/taurus'
platforms = [
 'Linux', 'Windows']
keywords = [
 'CLI', 'GUI', 'PyTango', 'Tango', 'Shell', 'Epics']