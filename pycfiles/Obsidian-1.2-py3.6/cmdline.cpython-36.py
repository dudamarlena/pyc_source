# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/Obsidian/cmdline.py
# Compiled at: 2018-01-07 09:08:12
# Size of source mod 2**32: 1205 bytes
import os, sys, scrapy.cmdline
base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

def execute():
    if len(sys.argv) <= 1:
        print('usage: %s [config file]' % sys.argv[0])
        sys.exit(0)
    else:
        filename = sys.argv[1]
        output = os.path.join(os.getcwd(), 'obsidian_output.json')
        if len(sys.argv) > 2:
            output = sys.argv[2]
        if not output.startswith('/'):
            output = os.path.join(os.getcwd(), output)
        if not filename.startswith('/'):
            filename = os.path.join(os.getcwd(), filename)
        if not os.path.isfile(filename):
            print('file not exist: %s' % sys.argv[1])
            sys.exit(0)
    os.chdir(os.path.join(base, 'spiders'))
    scrapy.cmdline.execute(('scrapy runspider jsonspider.py -a path=%s -o %s' % (filename, output)).split())


if __name__ == '__main__':
    execute()