# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/testingbot/install.py
# Compiled at: 2013-12-24 10:20:50
import os, sys

def install():
    api_key = raw_input('Please enter your Testingbot.com API Key: ')
    api_secret = raw_input('Please enter your Testingbot.com API Secret: ')
    write_data(api_key, api_secret)


def write_data(api_key, api_secret):
    path = os.path.expanduser('~/.testingbot')
    f = open(path, 'w')
    f.write(api_key + ':' + api_secret)
    f.close()
    print 'You are now ready to use the testingbot.com Selenium grid'


if len(sys.argv) > 1:
    split_data = sys.argv[1].split(':')
    write_data(split_data[0], split_data[1])