# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_initscript.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.initscript import InitScript, EmptyFileException, NotInitscriptException
from insights.tests import context_wrap
NOTINITSCRIPT_SCRIPT = 'etc/rc.d/init.d/script_notinitscript'
NOTINITSCRIPT_CONTENT = ('\n#! /bin/bash\n\necho script_notinitscript\n').strip()
CHKCONFIG_SCRIPT = 'etc/rc.d/init.d/script_chkconfig'
CHKCONFIG_CONTENT = ('\n#!/bin/sh\n#\n# rhnsd:        Starts the Spacewalk Daemon\n#\n# chkconfig: 345 97 03\n# description:  This is a daemon which handles the task of connecting #               periodically to the Spacewalk servers to #               check for updates, notifications and perform system #               monitoring tasks according to the service level that #               this server is subscribed for\n#\n# processname: rhnsd\n# pidfile: /var/run/rhnsd.pid\n#\n\necho script_chkconfig\n').strip()
LSB_SCRIPT = 'etc/rc.d/init.d/script_lsb'
LSB_CONTENT = ('\n#!/bin/sh\n### BEGIN INIT INFO\n# Provides: rhnsd\n# Required-Start: $local_fs $network $remote_fs $named $time\n# Required-Stop: $local_fs $network $remote_fs $named\n# Default-Start: 2 3 4 5\n# Default-Stop: 0 1 6\n# Short-Description: Starts the Spacewalk Daemon\n# Description: This is a daemon which handles the task of connecting\n#               periodically to the Spacewalk servers to\n#               check for updates, notifications and perform system\n#               monitoring tasks according to the service level that\n#               this server is subscribed for.\n### END INIT INFO\n\necho script_lsb\n').strip()
CHKCONFIG_LSB_SCRIPT = 'etc/rc.d/init.d/script_chkconfig+lsb'
CHKCONFIG_LSB_CONTENT = ('\n#!/bin/sh\n#\n# rhnsd:        Starts the Spacewalk Daemon\n#\n# chkconfig: 345 97 03\n# description:  This is a daemon which handles the task of connecting #               periodically to the Spacewalk servers to #               check for updates, notifications and perform system #               monitoring tasks according to the service level that #               this server is subscribed for\n#\n# processname: rhnsd\n# pidfile: /var/run/rhnsd.pid\n#\n\n### BEGIN INIT INFO\n# Provides: rhnsd\n# Required-Start: $local_fs $network $remote_fs $named $time\n# Required-Stop: $local_fs $network $remote_fs $named\n# Default-Start: 2 3 4 5\n# Default-Stop: 0 1 6\n# Short-Description: Starts the Spacewalk Daemon\n# Description: This is a daemon which handles the task of connecting\n#               periodically to the Spacewalk servers to\n#               check for updates, notifications and perform system\n#               monitoring tasks according to the service level that\n#               this server is subscribed for.\n### END INIT INFO\n\necho script_chkconfig+lsb\n').strip()
EMPTY_SCRIPT = 'etc/rc.d/init.d/script_empty'
EMPTY_CONTENT = ('\n').strip()
HINTSONLY_SCRIPT = 'etc/rc.d/init.d/script_hintsonly'
HINTSONLY_CONTENT = ('\n#!/bin/sh\n#\n\ncase "$1" in\nstart)\n        ;;\nstop)\n        ;;\nesac\n').strip()
COMMENTS_SCRIPT = 'etc/rc.d/init.d/script_comments'
COMMENTS_CONTENT = ('\n#! bin/broken\n#\n#\n#case "$1" in\n#start)\n#        ;;\n#stop)\n#        ;;\n#esac\n').strip()

def test_initscript1():
    context = context_wrap(NOTINITSCRIPT_CONTENT, path=NOTINITSCRIPT_SCRIPT)
    with pytest.raises(NotInitscriptException) as (e_info):
        InitScript(context)
    assert context.path in str(e_info.value)
    assert 'confidence: 1' in str(e_info.value)


def test_initscript2():
    context = context_wrap(CHKCONFIG_CONTENT, path=CHKCONFIG_SCRIPT)
    r = InitScript(context)
    assert r.file_name == 'script_chkconfig'


def test_initscript3():
    context = context_wrap(LSB_CONTENT, path=LSB_SCRIPT)
    r = InitScript(context)
    assert r.file_name == 'script_lsb'


def test_initscript4():
    context = context_wrap(CHKCONFIG_LSB_CONTENT, path=CHKCONFIG_LSB_SCRIPT)
    r = InitScript(context)
    assert r.file_name == 'script_chkconfig+lsb'


def test_initscript5():
    context = context_wrap(HINTSONLY_CONTENT, path=HINTSONLY_SCRIPT)
    r = InitScript(context)
    assert r.file_name == 'script_hintsonly'


def test_initscript6():
    context = context_wrap(EMPTY_CONTENT, path=EMPTY_SCRIPT)
    with pytest.raises(EmptyFileException) as (e_info):
        InitScript(context)
    assert context.path in str(e_info.value)


def test_initscript7():
    context = context_wrap(COMMENTS_CONTENT, path=COMMENTS_SCRIPT)
    with pytest.raises(NotInitscriptException) as (e_info):
        InitScript(context)
    assert context.path in str(e_info.value)
    assert 'confidence: 0' in str(e_info.value)