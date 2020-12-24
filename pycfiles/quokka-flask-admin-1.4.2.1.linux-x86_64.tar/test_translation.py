# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/tests/sqla/test_translation.py
# Compiled at: 2016-06-26 14:14:34
import json
from nose.tools import eq_, ok_, raises, assert_true
from speaklater import make_lazy_string
from . import setup
from .test_basic import CustomModelView, create_models

class Translator:
    translate = False

    def __call__(self, string):
        if self.translate:
            return ('Translated: "{0}"').format(string)
        else:
            return string


def test_column_label_translation():
    app, db, admin = setup()
    Model1, _ = create_models(db)
    translated = Translator()
    label = make_lazy_string(translated, 'Column1')
    view = CustomModelView(Model1, db.session, column_list=[
     'test1', 'test3'], column_labels=dict(test1=label), column_filters=('test1', ))
    admin.add_view(view)
    translated.translate = True
    non_lazy_groups = view._get_filter_groups()
    json.dumps(non_lazy_groups)
    ok_(translated('Column1') in non_lazy_groups)
    client = app.test_client()
    rv = client.get('/admin/model1/?flt1_0=test')
    eq_(rv.status_code, 200)