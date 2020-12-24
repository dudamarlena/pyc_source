# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/nosetty/test/nosepassthru.py
# Compiled at: 2007-03-19 23:48:50
"""a decoy python script that can be run like `python nosepassthru.py` to test using an executable chain"""
if __name__ == '__main__':
    from nose.core import main
    main()