# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/TestConsole.py
# Compiled at: 2019-12-11 16:38:02
"""This module launches an interactive console.

   Its purpose is to provide an easy means to
   test the environment created by a py2exe build.
   """
if __name__ == '__main__':
    import code
    console = code.InteractiveConsole()
    console.interact()