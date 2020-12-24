# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/test/test_benchline.py
# Compiled at: 2014-09-12 18:23:56
__author__ = 'paul'
import unittest, doctest, benchline.args, benchline.command, benchline.date_diff, benchline.files, benchline.new_python_file.new_python_file, benchline.python_deploy, benchline.python_install, benchline.user_input, benchline.hours_seconds_2_hours, benchline.countdown_generator, benchline.sum_timelog, benchline.new_setup_py, benchline.save_line_counts, benchline.http_format, benchline.async, benchline.timer, benchline.binary, benchline.jaxrs_ws_counter

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(benchline.args))
    tests.addTests(doctest.DocTestSuite(benchline.command))
    tests.addTests(doctest.DocTestSuite(benchline.date_diff))
    tests.addTests(doctest.DocTestSuite(benchline.files))
    tests.addTests(doctest.DocTestSuite(benchline.new_python_file.new_python_file))
    tests.addTests(doctest.DocTestSuite(benchline.python_deploy))
    tests.addTests(doctest.DocTestSuite(benchline.python_install))
    tests.addTests(doctest.DocTestSuite(benchline.user_input))
    tests.addTests(doctest.DocTestSuite(benchline.hours_seconds_2_hours))
    tests.addTests(doctest.DocTestSuite(benchline.countdown_generator))
    tests.addTests(doctest.DocTestSuite(benchline.sum_timelog))
    tests.addTests(doctest.DocTestSuite(benchline.new_setup_py))
    tests.addTests(doctest.DocTestSuite(benchline.http_format))
    tests.addTests(doctest.DocTestSuite(benchline.async))
    tests.addTests(doctest.DocTestSuite(benchline.timer))
    tests.addTests(doctest.DocTestSuite(benchline.binary))
    tests.addTests(doctest.DocTestSuite(benchline.jaxrs_ws_counter))
    tests.addTests(doctest.DocTestSuite(benchline.save_line_counts))
    return tests


if __name__ == '__main__':
    unittest.main()