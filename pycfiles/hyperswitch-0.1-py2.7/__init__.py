# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperswitch/__init__.py
# Compiled at: 2017-09-16 20:53:13
import hyperswitch.controllers

def main():
    controller = controllers.PySwitchController()
    controller.main()