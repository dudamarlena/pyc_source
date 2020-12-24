# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/mini_main.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nRun the example application with a reduced main window\n'
import main

def main():
    from camelot.view.main import main
    from camelot_example.application_admin import MiniApplicationAdmin
    main(MiniApplicationAdmin())


if __name__ == '__main__':
    main()