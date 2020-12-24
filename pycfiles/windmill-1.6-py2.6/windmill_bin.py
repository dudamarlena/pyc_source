# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/bin/windmill_bin.py
# Compiled at: 2011-01-13 01:48:00
import os, sys, time, windmill

def main():
    if len(sys.argv) is 0 or len(sys.argv) is 1 or sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == '-help':
        from windmill.bin import admin_options
        if len(sys.argv) > 0:
            admin_options.help(sys.argv[0])
        else:
            admin_options.help()
        sys.exit()
    from windmill.bin import admin_lib
    admin_lib.command_line_startup()


if __name__ == '__main__':
    main()