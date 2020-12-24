# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_substitute.py
# Compiled at: 2020-05-09 20:18:22
# Size of source mod 2**32: 4284 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import os, pytest, tempfile
here = os.path.abspath(os.path.dirname(__file__))

def test_expand_args():
    """Test generating arguments from a gridtest lookup
    """
    from gridtest.main.expand import expand_args
    assert expand_args({}) == {}
    assert len(expand_args({'two': 2})) == 1
    assert len(expand_args({'two': [2, 1]})) == 1


def test_substitute_args():
    """Test that argument substitution works
    """
    from gridtest.main.substitute import substitute_args
    assert substitute_args('{{ name }}') == ''
    assert substitute_args('echo hello {{ name }}') == 'echo hello '
    assert substitute_args('{{ name }}', {'name': 'vanessa'}) == 'vanessa'
    assert substitute_args('echo hello {{ name }}', {'name': 'vanessa'}) == 'echo hello vanessa'


def test_substitute_func(tmp_path):
    """Run a test that checks gridtest provided substitution functions"""
    from gridtest.main.substitute import substitute_func
    tmpdir = os.path.join(str(tmp_path))
    assert substitute_func('{% tmp_path %}').startswith(tempfile.gettempdir())
    assert 'pancakes' in substitute_func('{% tmp_path prefix=pancakes %}')
    assert tmpdir in substitute_func('{% tmp_path requested_tmpdir=' + tmpdir + '%}')
    assert os.path.exists(substitute_func('{% tmp_dir %}'))
    assert not os.path.exists(substitute_func('{% tmp_dir create=False %}'))
    assert tmpdir in substitute_func('{% tmp_dir requested_tmpdir=' + tmpdir + ' create=False%}')


def test_substitute_func_custom(tmp_path):
    """Test that any module (and function) substitution works"""
    from gridtest.main.substitute import substitute_func

    def get_name(name='dinosauria'):
        return name

    with pytest.raises(SystemExit):
        assert substitute_func('{% get_name %}')
    assert substitute_func('{% get_name %}', {'get_name': get_name}) == 'dinosauria'
    assert substitute_func('{% get_name name=weeble %}', {'get_name': get_name}) == 'weeble'


def test_substitute_gridtest():
    """Test that the gridtest (test instantiation) performs the substitution.
    """
    from gridtest.main.test import GridRunner
    test_file = os.path.join(here, 'modules', 'temp-tests.yml')
    runner = GridRunner(test_file)
    assert '{% tmp_dir %}' in runner.config['temp']['tests']['temp.create_directory'][0]['args']['dirname']
    assert '{% tmp_path %}' in runner.config['temp']['tests']['temp.write_file'][0]['args']['filename']
    tests = runner.get_tests()
    assert '{% tmp_dir %}' not in tests['temp.create_directory.0'].params['args']['dirname']
    assert '{% tmp_path %}' not in tests['temp.write_file.0'].params['args']['filename']
    assert os.path.exists(tests['temp.create_directory.0'].params['args']['dirname'])
    assert not os.path.exists(tests['temp.write_file.0'].params['args']['filename'])
    for name, test in tests.items():
        test.run(cleanup=False)

    assert os.path.exists(tests['temp.create_directory.0'].params['args']['dirname'])
    assert os.path.exists(tests['temp.write_file.0'].params['args']['filename'])
    for name, test in tests.items():
        test.run(cleanup=True)