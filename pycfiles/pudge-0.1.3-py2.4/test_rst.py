# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_rst.py
# Compiled at: 2006-03-14 16:35:23
"""pudge.rst unit tests"""

def test_rst_to_html():
    from pudge.rst import to_html
    expected = '<p>A single <em>emphasized</em> paragraph.</p>\n'
    actual = to_html('A single *emphasized* paragraph.')
    assert actual == expected