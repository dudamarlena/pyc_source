# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/collection_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1246 bytes
from unittest import TestCase
from firestore.errors import ValidationError
from firestore import Collection, String, Array, Reference, Integer

class RefDoc(Collection):
    __collection__ = 'testref'
    name = String(required=True)

    def to_dict(self):
        return {'name': self.name}


class SomeDocument(Collection):
    __collection__ = 'testdoc'
    name = String(default='alexis')
    age = Integer(default=10)
    references = Array((Reference(RefDoc)), maximum=1)


class CollectionTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_collection_instantiation(self):
        refdoc = RefDoc()
        refdoc.name = 'mocked'
        refdoc.__loaded__ = True
        ewargs = {'name':'instantiator', 
         'age':50, 
         'references':[
          refdoc, refdoc, refdoc]}
        with self.assertRaises(ValidationError):
            errordoc = SomeDocument(**ewargs)
        kwargs = {'name':'instantiator', 
         'age':50, 
         'references':[
          refdoc]}
        somedoc = SomeDocument(**kwargs)
        self.assertEqual(somedoc.name, 'instantiator')
        self.assertEquals(somedoc.references, [refdoc])