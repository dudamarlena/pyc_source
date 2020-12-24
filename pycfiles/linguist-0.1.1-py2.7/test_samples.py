# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_samples.py
# Compiled at: 2013-08-31 02:14:09
from framework import LinguistTestBase, main
from libs.samples import DATA

class TestSamples(LinguistTestBase):

    def test_verify(self):
        data = DATA
        assert data['languages_total'] == sum(data['languages'].values())
        assert data['tokens_total'] == sum(data['language_tokens'].values())
        assert data['tokens_total'] == sum(reduce(lambda x, y: x + y, [ token.values() for token in data['tokens'].values() ]))


if __name__ == '__main__':
    main()