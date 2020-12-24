# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_gridtest.py
# Compiled at: 2020-05-03 17:03:16
# Size of source mod 2**32: 6745 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import os, pytest
here = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture
def runner():
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'basic-tests.yml')
    return GridRunner(test_file)


def test_gridrunner(runner):
    """Load a gridtest runner and test for a basic file.
    """
    assert 'basic' in runner.config
    assert len(runner.config['basic']) >= 6
    assert runner.run() == 0
    assert runner.run(parallel=False) == 0
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'temp-tests.yml')
    runner = GridRunner(test_file)
    assert 'temp' in runner.config
    assert len(runner.config['temp']) >= 2
    assert runner.run() == 0
    assert runner.run(parallel=False) == 0


def test_returns(runner):
    """Run a test that checks for a return value"""
    tests = runner.get_tests()
    returns_test = tests['basic.add.0']
    assert not returns_test.result
    assert not returns_test.success
    assert 'returns' in returns_test.params
    returns_test.run()
    assert returns_test.result == returns_test.params['returns']
    assert returns_test.success
    returns_test.params['returns'] = 2
    returns_test.run()
    assert returns_test.result != returns_test.params['returns']
    assert not returns_test.success


def test_runs(runner):
    """Run a test that does not checks (other than working)"""
    tests = runner.get_tests()
    returns_test = tests['basic.add.1']
    assert not returns_test.result
    assert not returns_test.success
    returns_test.run()
    assert returns_test.success


def test_broken_func():
    """Run a test for a broken function"""
    from gridtest.main.test import GridTestFunc

    def broken():
        print(1 + 'string')

    test = GridTestFunc(broken)
    assert not test.success
    test.run()
    assert not test.success
    assert test.raises == 'TypeError'
    assert len(test.err) >= 1


def test_broken_func():
    """Run a test for a broken function"""
    from gridtest.main.test import GridTestFunc

    def broken():
        print(1 + 'string')

    test = GridTestFunc(broken)
    assert not test.success
    test.run()
    assert not test.success
    assert len(test.err) >= 1


def test_return_type():
    """test that a function with typing honors returning that type
    """
    from gridtest.main.test import GridTestFunc

    def return_int(one: int, two: int) -> int:
        return one + two

    test = GridTestFunc(return_int, params={'args': {'one':1,  'two':2}})
    assert not test.success
    test.run()
    assert test.success
    assert test.result == 3
    test = GridTestFunc(return_int, params={'args': {'one':1,  'two':'two'}})
    assert not test.success
    test.run()
    assert not test.success
    assert test.raises == 'TypeError'


def test_raises():
    """test that a function that should raise an error raises is
    """
    from gridtest.main.test import GridTestFunc

    def raises_error():
        raise Exception

    test = GridTestFunc(raises_error)
    assert not test.success
    assert not test.raises
    test.run()
    assert not test.success
    assert test.raises == 'Exception'
    assert len(test.err) == 1
    test = GridTestFunc(raises_error, params={'raises': 'Exception'})
    assert not test.success
    assert not test.raises
    test.run()
    assert test.success
    assert test.raises == 'Exception'
    assert len(test.err) == 0
    assert len(test.out) == 1


def test_exists(tmp_path):
    """test that a file is generated (exists)
    """
    from gridtest.main.test import GridTestFunc

    def write_file(output_file):
        with open(output_file, 'w') as (filey):
            filey.writelines('cheezypasta')

    output_file = os.path.join(str(tmp_path), 'pasta.txt')
    test = GridTestFunc(write_file,
      params={'args':{'output_file': output_file},  'exists':output_file})
    assert not test.success
    assert not os.path.exists(output_file)
    test.run()
    assert test.success
    assert os.path.exists(output_file)


def test_istrue_isfalse():
    """Test that the gridtest istrue, isfalse, exists, works as expected.
    """
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'truefalse-tests.yml')
    runner = GridRunner(test_file)
    tests = runner.get_tests()
    test = tests['truefalse.add.0']
    for result in ('istrue', 'isfalse'):
        assert result in test.params

    assert test.params['istrue'] == 'isinstance({{ result }}, float)'
    assert test.params['isfalse'] == 'isinstance({{ result }}, int)'
    test.run()
    assert test.result == 3.0
    assert test.params['istrue'] == 'isinstance(3.0, float)'
    assert test.params['isfalse'] == 'isinstance(3.0, int)'


def test_classes():
    """Test that gridtest can load classes
    """
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'car-tests.yml')
    runner = GridRunner(test_file)
    tests = runner.get_tests()
    test = tests['car.Car.1']
    assert not test.result
    assert 'isinstance' in test.params
    test.run()
    assert type(test.result).__name__ == test.params['isinstance']


def test_metrics():
    """Test that gridtest can load metrics specifications
    """
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'metrics.yml')
    runner = GridRunner(test_file)
    tests = runner.get_tests()
    assert len([x for x in tests.keys() if 'gotosleep' in x]) == 6
    runner.run()
    runner = GridRunner(test_file)
    runner.config['metrics']['metrics.gotosleep'][0]['grid']['seconds']['invalid'] = 1
    with pytest.raises(SystemExit):
        tests = runner.get_tests()