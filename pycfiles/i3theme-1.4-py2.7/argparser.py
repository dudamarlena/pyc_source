# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/i3theme/utils/argparser.py
# Compiled at: 2016-07-14 10:41:16
import argparse
argParser = argparse.ArgumentParser()
argParser.add_argument('-f', '--file', help='Specify a theme to apply.', type=str, default=None)
argParser.add_argument('theme', help='Specify a buid-in theme name.', type=str, nargs='?', default=None)
argParser.add_argument('-l', '--list', help='List build in themes', action='store_true', default=False)
argParser.add_argument('-c', '--clean', help='Remove theme lines from ~/.i3/config', action='store_true', default=False)