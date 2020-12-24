# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_rst.py
# Compiled at: 2006-03-14 17:35:23
__doc__ = 'pudge.rst unit tests'

def test_rst_to_html():
    from pudge.rst import to_html
    expected = '<p>A single <em>emphasized</em> paragraph.</p>\n'
    actual = to_html('A single *emphasized* paragraph.')
    assert actual == expected