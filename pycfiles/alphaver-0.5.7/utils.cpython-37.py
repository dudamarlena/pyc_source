# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\appli\Documents\GitHub\alphaVantageAPI Project\tests\utils.py
# Compiled at: 2020-04-19 19:08:33
# Size of source mod 2**32: 934 bytes
import json
from unittest import mock
from pathlib import Path

class Constant(object):
    TEST_DATA_PATH = Path('./tests/test_data')
    API_KEY_TEST = 'demo'
    API_DATA_TEST = 'MSFT'
    API_DIGITAL_TEST = 'BTC'
    API_FX_TEST = 'EUR'


def load_json(file: str):
    with Path(file).open('r') as (content):
        json_data = json.load(content)
    content.close()
    return json_data


def _mock_response(status=200, text_data=None, json_data=None, raise_for_status=None):
    mock_response = mock.Mock()
    mock_response.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_response.raise_for_status.side_effect = raise_for_status
    mock_response.status_code = status
    if text_data:
        mock_response.text = mock.Mock(return_value=text_data)
    if json_data:
        mock_response.json = mock.Mock(return_value=json_data)
    return mock_response