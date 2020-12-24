# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/_toggle_tests.py
# Compiled at: 2016-09-19 13:27:02
"""This executable toggles all nosetests in the onlinelinguisticdatabase/tests
directory on or off.

Usage:

Turn all of the tests in all of the test scripts on:

    $ ./_toggle_tests.py on

Turn all of the tests in all of the test scripts off:

    $ ./_toggle_tests.py off

Turn all of the tests in 'test_forms.py' and 'test_formsearches.py' off/on (note
that the .py extensions is optional):

    $ ./_toggle_tests.py on/off test_forms test_formsearches.py
"""
import os, sys, re
try:
    on_off = sys.argv[1]
    if on_off not in ('on', 'off'):
        on_off = None
except IndexError:
    on_off = None

tests_dir_path = os.path.dirname(os.path.realpath(__file__))

def add_py_suffix(fn):
    if fn.split('.')[(-1)] == 'py':
        return fn
    else:
        return '%s.py' % fn


def get_test_scripts():
    ignore_patt = re.compile('^(\\.|_|setup\\.py$)')
    scripts = os.listdir(tests_dir_path)
    return [ s for s in scripts if not ignore_patt.search(s) ]


files = [ add_py_suffix(fn) for fn in sys.argv[2:] ]

def toggle_tests_in_script(on_off, script):
    script_path = os.path.join(tests_dir_path, script)
    new_script_path = os.path.join(tests_dir_path, '%s.tmp' % script)
    script_file = open(script_path, 'r')
    new_script_file = open(new_script_path, 'w')
    test_me_patt = re.compile('^    #@nottest(\n| )')
    test_me_not_patt = re.compile('^    @nottest(\n| )')
    i = 1
    messages = []
    for line in script_file:
        if test_me_not_patt.search(line) and on_off == 'on':
            messages.append('Turned on test at line %d of %s.' % (i, script))
            new_script_file.write('    #@nottest\n')
        elif test_me_patt.search(line) and on_off == 'off':
            messages.append('Turned off test at line %d of %s.' % (i, script))
            new_script_file.write('    @nottest\n')
        else:
            new_script_file.write(line)
        i = i + 1

    new_script_file.close()
    script_file.close()
    if messages:
        os.rename(new_script_path, script_path)
    else:
        os.remove(new_script_path)
    return messages


if on_off is not None:
    test_scripts = get_test_scripts()
    if files == []:
        scripts_to_toggle = test_scripts
    else:
        scripts_to_toggle = list(set(test_scripts) & set(files))
    messages = [ toggle_tests_in_script(on_off, script) for script in scripts_to_toggle ]
    if sum([ len(ms) for ms in messages ]) == 0:
        print 'No tests were turned %s.' % on_off
    else:
        print ('\n').join([ ('\n').join([ m for m in ms ]) for ms in messages if ms ])
else:
    print 'You must specify "on" or "off" as the first argument.'