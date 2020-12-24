# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/projects/firelet/test/test_local.py
# Compiled at: 2011-05-24 16:52:02
from firelet import flssh
import shutil
from nose.tools import assert_raises, with_setup

def test_sshconnector_getconf():
    t = {'localhost': ['127.0.0.1']}
    sx = flssh.SSHConnector(targets=t, username='root')
    confs = sx.get_confs()
    print repr(confs)
    assert 'localhost' in confs