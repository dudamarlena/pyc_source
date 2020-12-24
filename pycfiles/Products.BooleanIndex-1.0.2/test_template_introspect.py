# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/tests/test_template_introspect.py
# Compiled at: 2012-02-27 07:41:53
import os
from paste.script import templates
tmpl_dir = os.path.join(os.path.dirname(__file__), 'sample_templates')

def test_find():
    vars = templates.find_args_in_dir(tmpl_dir, True)
    assert 'a' in vars
    assert vars['a'].default is templates.NoDefault
    assert 'b' in vars
    assert vars['b'].default == 1
    assert len(vars) == 2