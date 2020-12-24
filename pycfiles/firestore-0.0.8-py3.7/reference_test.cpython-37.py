# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/reference_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1969 bytes
from unittest import TestCase
from pytest import mark
from firestore import Connection
from firestore import Collection, Reference, String
from tests import online, FIREBASE_PATH

class AnotherDocument(Collection):
    __collection__ = 'testdoc'
    first_name = String(pk=True)


class ReferenceDocument(Collection):
    __collection__ = 'testref'
    reference = Reference(AnotherDocument)


class UnrelatedDocument(Collection):
    ref = Reference(ReferenceDocument)


@online
class TestReference(TestCase):

    def setUp(self):
        self.ad = AnotherDocument()
        self.ad.first_name = 'temp-doc'
        self.rd = ReferenceDocument()
        self.urd = UnrelatedDocument()
        self.connection = Connection(FIREBASE_PATH)
        self.ad = self.ad.save()
        self.rd = self.rd.save()

    def tearDown(self):
        self.ad.delete()
        self.rd.delete()

    def test_reference_must_receive_document(self):
        with self.assertRaises(ValueError):
            Reference('Not a document')

    def test_reference_assignment_error(self):
        with self.assertRaises(AttributeError):
            self.rd.reference = UnrelatedDocument()

    def test_reference_assignment(self):
        with self.assertRaises(ValueError):
            self.rd.reference = 'temp-docs'
        self.rd.reference = 'temp-doc'
        self.assertEqual(self.rd.reference, self.ad)

    def test_fetched_reference_assignment(self):
        fetched = AnotherDocument.get(self.ad.pk).first()
        referenced = ReferenceDocument.get(self.rd.pk).first()
        referenced.reference = fetched
        referenced = referenced.save()
        self.assertEqual(referenced.reference, fetched)
        self.assertTrue(referenced.__loaded__)

    def test_reference_document_string(self):
        pass