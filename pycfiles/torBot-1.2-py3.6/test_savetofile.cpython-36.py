# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_savetofile.py
# Compiled at: 2018-07-01 06:51:02
# Size of source mod 2**32: 1137 bytes
import sys, os, json
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from modules import savefile

def test_save_links_successful():
    mock_data = [
     'http://aff.ironsocket.com/SH7L',
     'http://aff.ironsocket.com/SH7L',
     'http://wsrs.net/',
     'http://cmsgear.com/']
    try:
        file_name = savefile.saveJson('Links', mock_data)
        mock_output = {'Links': mock_data}
        with open('test_file.json', 'w+') as (test_file):
            json.dump(mock_output, test_file, indent=2)
        os.chdir(os.getcwd())
        assert os.path.isfile(file_name) is True
        mock_file = open(file_name, 'r')
        test_file = open('test_file.json', 'r')
        mock_data = mock_file.read()
        test_data = test_file.read()
    finally:
        os.remove(file_name)
        os.remove('test_file.json')

    assert mock_data == test_data


if __name__ == '__main__':
    test_save_links_successful()