# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build\bdist.win32\egg\xurrency\tests\test_pep8.py
# Compiled at: 2011-02-28 20:31:54
import os, pep8
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

def test_pep8():
    arglist = [
     '--statistics',
     '--filename=*.py',
     '--show-source',
     '--repeat',
     BASE_DIR]
    (options, args) = pep8.process_options(arglist)
    runner = pep8.input_file
    for path in args:
        if os.path.isdir(path):
            pep8.input_dir(path, runner=runner)
        elif not pep8.excluded(path):
            options.counters['files'] += 1
            runner(path)

    pep8.print_statistics()
    errors = pep8.get_count('E')
    warnings = pep8.get_count('W')
    message = 'pep8: %d errors / %d warnings' % (errors, warnings)
    print message
    assert errors + warnings == 0, message