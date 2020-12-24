# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\slidegen\EngineFileGen.py
# Compiled at: 2012-05-19 05:36:22
import os, sys, cssmin, jsmin
if __name__ == '__main__':
    path = sys.argv[1]
    os.chdir(path)
    map = {}
    for base, dir, files in os.walk('.'):
        for fn in files:
            file_path = base + '/' + fn
            file_content = None
            with open(file_path, 'r') as (f):
                file_content = f.read()
            map[file_path[2:]] = file_content

    print '# *-* coding=utf-8'
    print 'FILES={'
    for k in map:
        if k.find('test') != -1:
            pass
        elif k[-4:len(k)] == '.css':
            print "r'''%s''':r'''%s'''," % (k, cssmin.cssmin(map[k]))
        elif k[-3:len(k)] == '.js':
            print "r'''%s''':r'''%s'''," % (k, jsmin.jsmin(map[k]))

    print '}'