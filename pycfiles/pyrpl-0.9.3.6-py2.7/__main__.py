# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/__main__.py
# Compiled at: 2017-08-29 09:44:06
"""
Script to launch pyrpl from the command line.

Type python -m pyrpl [config_file_name] to create
a Pyrpl instance with the config file
"config_file_name"
"""
import sys
try:
    from pyrpl import Pyrpl, APP
except:
    from . import Pyrpl, APP

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print 'usage: python run_pyrpl.py [[config]=config_file_name] [source=config_file_template] [hostname=hostname/ip]'
    kwargs = dict()
    for i, arg in enumerate(sys.argv):
        print (
         i, arg)
        if i == 0:
            continue
        try:
            k, v = arg.split('=', 1)
        except ValueError:
            k, v = arg, ''

        if v == '':
            if i == 1:
                kwargs['config'] = k
        else:
            kwargs[k] = v

    print 'Calling Pyrpl(**%s)' % str(kwargs)
    PYRPL = Pyrpl(**kwargs)
    APP.exec_()