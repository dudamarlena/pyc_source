# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trevor/projects/pythonanywhere-cli/source/tests/test_cli.py
# Compiled at: 2017-10-12 17:12:54
# Size of source mod 2**32: 334 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mock import patch
from pythonanywhere_cli.cli import main

@patch('pythonanywhere_cli.cli.Webapps')
@patch('pythonanywhere_cli.cli.docopt')
def test_main(docopt, Webapps):
    docopt.return_value = {'webapps': True}
    main()
    Webapps.assert_called_with({'webapps': True})
    Webapps.return_value.run.assert_called_once()