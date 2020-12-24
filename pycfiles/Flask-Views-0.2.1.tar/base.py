# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brocaar/Work/Projects/Brocaar/Flask/flask-views/flask_views/tests/functional/db/mongoengine/base.py
# Compiled at: 2012-02-19 15:02:16
from mongoengine import connect, fields
from mongoengine.document import Document
from wtforms import fields as form_fields, validators
from wtforms.form import Form
from flask_views.tests.functional.base import BaseTestCase

class BaseMongoTestCase(BaseTestCase):
    """
    Base test-case class for MongoDB tests.
    """

    def setUp(self):
        super(BaseMongoTestCase, self).setUp()
        self.db = connect('brocaar_flask_views_test')

        class TestDocument(Document):
            username = fields.StringField(verbose_name='Username', required=True)
            name = fields.StringField(verbose_name='Name', required=True)

        class TestForm(Form):
            username = form_fields.TextField('Username', [validators.required()])
            name = form_fields.TextField('Name', [validators.required()])

        self.TestDocument = TestDocument
        self.TestForm = TestForm

    def tearDown(self):
        for collection in self.db.collection_names():
            if collection.split('.')[0] != 'system':
                self.db.drop_collection(collection)