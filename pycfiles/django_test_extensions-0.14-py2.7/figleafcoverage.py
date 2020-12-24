# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/testrunners/figleafcoverage.py
# Compiled at: 2010-03-28 18:09:43
import os, commands
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.simple import run_tests as django_test_runner
import figleaf

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    setup_test_environment()
    figleaf.start()
    test_results = django_test_runner(test_labels, verbosity, interactive, extra_tests)
    figleaf.stop()
    if not os.path.isdir(os.path.join('temp', 'figleaf')):
        os.makedirs(os.path.join('temp', 'figleaf'))
    file_name = 'temp/figleaf/test_output.figleaf'
    figleaf.write_coverage(file_name)
    output = commands.getoutput('figleaf2html ' + file_name + ' --output-directory=temp/figleaf')
    print output
    return test_results