# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pynestml_frontend_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4192 bytes
import os, pytest, sys, tempfile, unittest
from pynestml.frontend.pynestml_frontend import main
from pynestml.frontend.frontend_configuration import FrontendConfiguration
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

class PyNestMLFrontendTest(unittest.TestCase):
    __doc__ = '\n    Tests if the frontend works as intended and is able to process handed over arguments.\n    '

    def test_codegeneration_for_all_models(self):
        path = str(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join('..', 'models'))))
        params = list()
        params.append('nestml')
        params.append('--input_path')
        params.append(path)
        params.append('--logging_level')
        params.append('INFO')
        params.append('--target_path')
        params.append('target/models')
        params.append('--store_log')
        params.append('--dev')
        exit_code = None
        with patch.object(sys, 'argv', params):
            exit_code = main()
        self.assertTrue(exit_code == 0)

    def test_module_name_parsing_right_module_name_specified(self):
        path = str(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join('..', 'models'))))
        params = list()
        params.append('--input_path')
        params.append(path)
        params.append('--module_name')
        params.append('xyzzymodule')
        FrontendConfiguration.parse_config(params)
        assert FrontendConfiguration.module_name == 'xyzzymodule'

    def test_module_name_parsing_wrong_module_name_specified(self):
        with pytest.raises(Exception):
            path = str(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join('..', 'models'))))
            params = list()
            params.append('--input_path')
            params.append(path)
            params.append('--module_name')
            params.append('xyzzy')
            FrontendConfiguration.parse_config(params)

    def test_module_name_parsing_input_path_is_file(self):
        h, path = tempfile.mkstemp(prefix='nestml')
        basename = os.path.basename(os.path.normpath(path))
        params = list()
        params.append('--input_path')
        params.append(path)
        FrontendConfiguration.parse_config(params)
        assert FrontendConfiguration.module_name == 'nestmlmodule'

    def test_module_name_parsing_input_path_is_dir(self):
        path = tempfile.mkdtemp(prefix='nestml')
        basename = os.path.basename(os.path.normpath(path))
        params = list()
        params.append('--input_path')
        params.append(path)
        params.append('--logging_level')
        params.append('INFO')
        FrontendConfiguration.parse_config(params)
        assert FrontendConfiguration.module_name == basename + 'module'

    def test_module_name_parsing_input_path_is_wrong_dir(self):
        with pytest.raises(Exception):
            path = tempfile.mkdtemp(prefix='nestml-')
            params = list()
            params.append('--input_path')
            params.append(path)
            params.append('--logging_level')
            params.append('INFO')
            FrontendConfiguration.parse_config(params)

    def tearDown(self):
        import shutil
        shutil.rmtree(FrontendConfiguration.target_path)


if __name__ == '__main__':
    unittest.main()