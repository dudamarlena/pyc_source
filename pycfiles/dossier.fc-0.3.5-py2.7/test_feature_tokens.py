# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/test_feature_tokens.py
# Compiled at: 2015-09-05 21:22:50
from __future__ import absolute_import, division, print_function
from dossier.fc import FeatureCollection, FeatureTokens
import streamcorpus

def test_ft_fcdefault():
    fc = FeatureCollection()
    assert isinstance(fc['@NAME'], FeatureTokens)


def test_ft_default():
    fo = FeatureTokens()
    assert fo['foo'] == []


def test_ft_roundtrip():
    fc = FeatureCollection()
    fc['@NAME']['foo'].append([
     ('nltk', 5, 2)])
    fc2 = FeatureCollection.loads(fc.dumps())
    assert fc['@NAME'] == fc2['@NAME']


def test_ft_with_stream_item():
    si = streamcorpus.make_stream_item('2005-01-01T05:06:07.0Z', 'abc')
    tokens = [
     streamcorpus.Token(offsets={streamcorpus.OffsetType.XPATH_CHARS: streamcorpus.Offset(type=streamcorpus.OffsetType.XPATH_CHARS, xpath='/html[1]/body[1]/p[1]/b[1]/text()[1]', first=0, xpath_end='/html[1]/body[1]/p[1]/text()[1]', xpath_end_offset=2)}),
     streamcorpus.Token(offsets={streamcorpus.OffsetType.XPATH_CHARS: streamcorpus.Offset(type=streamcorpus.OffsetType.XPATH_CHARS, xpath='/html[1]/body[1]/p[1]/b[2]/text()[1]', first=0, xpath_end='/html[1]/body[1]/p[1]/text()[2]', xpath_end_offset=4)})]
    si.body.sentences = {'test': [streamcorpus.Sentence(tokens=tokens)]}
    si.body.clean_html = '<html><body><p><b>T</b>om <b>B</b>rady</p></body></html>'
    ft = FeatureTokens()
    ft['tom brady'].append([('test', 0, 0), ('test', 0, 1)])
    assert next(ft.xpath_slices(si, 'tom brady')) == 'Tom Brady'