# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paper_manager/main.py
# Compiled at: 2018-04-14 05:20:12
from paper_manager.mycmd import MyCmd

def main():
    mycmd = MyCmd()
    mycmd.cmdloop()