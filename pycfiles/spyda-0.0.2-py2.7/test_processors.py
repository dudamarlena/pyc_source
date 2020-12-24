# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/tests/test_processors.py
# Compiled at: 2013-03-25 21:23:33
import pytest
pytest.importorskip('calais')
from os import path
import calais.calais
from spyda.processors import process_calais

@pytest.fixture()
def sample_response(request):
    return open(path.join(path.dirname(__file__), 'sample.json'), 'r').read()


def test_process_calais(monkeypatch, sample_response):

    def rest_POST(self, content):
        return sample_response

    monkeypatch.setattr(calais.calais.Calais, 'rest_POST', rest_POST)
    result = process_calais('blah', key='foobar')
    assert result == {'people': ['Jamil Alayan']}