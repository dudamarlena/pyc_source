# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/arg_parser.py
# Compiled at: 2016-05-03 20:54:42
from argparse import ArgumentParser
from fftool import CHANNELS, DEFAULT_CHANNEL

def arg_parser():
    parser = ArgumentParser(prog='ff')
    parser.add_argument('-c', '--channel', choices=CHANNELS, default=DEFAULT_CHANNEL, help='A specific Firefox channel.')
    parser.add_argument('-p', '--profile', help='Name of the Firefox profile to create/use.')
    parser.add_argument('-e', '--env', help='Development environment to use (ie: dev, stage, prod).')
    parser.add_argument('-t', '--test-type', help='Name of the test-type (ie: e2e-test, stack-check).')
    parser.add_argument('-a', '--app', help='Name of the application to test (ie: loop-server).')
    parser.add_argument('--no-launch', action='store_true', help='Whether or not to launch a Firefox instance.')
    parser.add_argument('--no-profile', action='store_true', help='Whether to create a profile. This is used for the daily               refresh job.')
    parser.add_argument('--install-only', action='store_true', help='Whether or not to just download/install Firefox version(s),               or also create a profile and launch a browser.')
    parser.add_argument('--clean-profiles', action='store_true', help='Delete all the fftool.* profile directories in the _temp/profiles              directory')
    return parser.parse_args()