# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/BugReport.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 602 bytes


def report(saved_files):
    print('Apologies. Vai has crashed.')
    print('---------------------------')
    with open('vai_crashreport.out') as (f):
        print(f.read())
    print('---------------------------')
    if len(saved_files) != 0:
        print('Your buffers have been dumped to the following files')
        print('')
        for f in saved_files:
            print('  ' + str(f))

    print('')
    print('The traceback has been saved in vai_crashreport.out')


def yes():
    y_or_n = input('[y/N]> ')
    if y_or_n.strip().lower() in ('y', 'yes'):
        return True
    return False