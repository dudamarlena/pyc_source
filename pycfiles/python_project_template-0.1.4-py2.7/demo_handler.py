# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/demo/demo_handler.py
# Compiled at: 2015-03-20 11:24:22
"""Module for to demo python project
"""
import requests

class DemoHandler(object):
    """Placeholder class"""

    def __init__(self):
        print 'Hallo, Welt.'

    def do_nothing(self):
        pass

    def do_something(self):
        return "Ain't that something?"

    def some_bool(self):
        return True

    def remote_data(self):
        response = requests.get('http://httpbin.org/get')
        return response.text


def main():
    demo = DemoHandler()
    print demo.do_something()
    print demo.remote_data()


if __name__ == '__main__':
    main()