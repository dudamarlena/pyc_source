# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/wtforms/tests/test_wtforms_tool.py
# Compiled at: 2020-02-07 17:32:44
# Size of source mod 2**32: 423 bytes
from unittest import TestCase
from wtforms import Form
from wtforms.fields.html5 import EmailField
from foxylib.tools.wtforms.wtforms_tool import WTFormsTool

class TestWTFormsTool(TestCase):

    def test_01(self):

        class TestForm(Form):
            email = EmailField()

        form = TestForm()
        hyp = WTFormsTool.boundfield2name(form.email)
        ref = 'email'
        self.assertEqual(hyp, ref)