# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/testpackage/pbr_testpackage/_setup_hooks.py
# Compiled at: 2017-12-04 07:19:32
from distutils.command import build_py

def test_hook_1(config):
    print 'test_hook_1'


def test_hook_2(config):
    print 'test_hook_2'


class test_command(build_py.build_py):
    command_name = 'build_py'

    def run(self):
        print 'Running custom build_py command.'
        return build_py.build_py.run(self)


def test_pre_hook(cmdobj):
    print 'build_ext pre-hook'


def test_post_hook(cmdobj):
    print 'build_ext post-hook'