# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dhellmann/Devel/rst2blogger/rst2blogger/tests/test_rst2post.py
# Compiled at: 2012-02-12 09:54:25
import tempfile
from rst2blogger.rst2post import format_post, format_post_from_string

def test_find_title():
    title, content = format_post_from_string('\nTitle Goes Here\n===============\n\nthis is the rest of the body\n')
    assert title == 'Title Goes Here'


def test_find_body():
    title, content = format_post_from_string('\nTitle Goes Here\n===============\n\nthis is the rest of the body\n')
    assert 'this is the rest of the body' in content


def test_file():
    f = tempfile.NamedTemporaryFile()
    f.write('\nTitle Goes Here\n===============\n\nthis is the rest of the body\n')
    f.flush()
    title, content = format_post(f.name)
    f.close()
    assert title == 'Title Goes Here'