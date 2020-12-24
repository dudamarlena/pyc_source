# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jluker/projects/pytest-ghostinspector/tests/conftest.py
# Compiled at: 2016-02-23 10:49:39
import re, pytest
from pytest_gi.plugin import API_URL
pytest_plugins = 'pytester'

@pytest.fixture()
def gi_api_suite_tests_re():
    return re.compile(API_URL + 'suites/\\w+/tests/')


@pytest.fixture()
def gi_api_test_re():
    return re.compile(API_URL + 'tests/\\w+/$')


@pytest.fixture()
def gi_api_test_exec_re():
    return re.compile(API_URL + 'tests/\\w+/execute/')


@pytest.fixture
def suite_resp():
    return '\n        {\n            "data": [\n                { "_id": 1, "name": "test 1", "suite": { "name": "ABC Suite" } },\n                { "_id": 2, "name": "test 2", "suite": { "name": "ABC Suite" } }\n            ]\n        }'


@pytest.fixture
def test_resp():
    return '\n        {\n            "data": {\n                "_id": "xyz789",\n                "name": "test xyz789",\n                "suite": { "name": "ABC Suite" }\n            }\n        }'