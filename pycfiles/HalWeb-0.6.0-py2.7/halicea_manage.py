# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/halicea_manage.py
# Compiled at: 2012-01-04 16:27:54
import sys, logging
try:
    from halicea import hal
except:
    print 'Hal web is not located in your python path'
    print 'accessing halweb thru path {{hal_path}}'
    sys.path.append('{{hal_path}}')
    import hal

if __name__ == '__main__':
    hal.main_safe(*sys.argv)