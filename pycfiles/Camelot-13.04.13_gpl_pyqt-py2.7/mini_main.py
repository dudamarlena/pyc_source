# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/mini_main.py
# Compiled at: 2013-04-11 17:47:52
"""
Run the example application with a reduced main window
"""
import main

def main():
    from camelot.view.main import main
    from camelot_example.application_admin import MiniApplicationAdmin
    main(MiniApplicationAdmin())


if __name__ == '__main__':
    main()