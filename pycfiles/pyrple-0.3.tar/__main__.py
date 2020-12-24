# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/__main__.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = '\nScript to launch pyrpl from the command line.\n\nType python -m pyrpl [config_file_name] to create\na Pyrpl instance with the config file\n"config_file_name"\n'
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