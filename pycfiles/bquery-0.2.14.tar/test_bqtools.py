# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mike/PycharmProjects/bqtools/bqtools/tests/test_bqtools.py
# Compiled at: 2020-04-21 16:52:00
__doc__ = b'\nThis modules purpose is to test bqtools-json\n\n'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import copy, difflib, json, logging, pprint, unittest
from deepdiff import DeepDiff
from google.cloud import bigquery, storage, exceptions
import bqtools

class TestScannerMethods(unittest.TestCase):

    def load_data(self, file_name):
        with open(file_name) as (json_file):
            return json.load(json_file)

    def setUp(self):
        logging.basicConfig()
        self.pp = pprint.PrettyPrinter(indent=4)
        self.schemaTest1 = self.load_data(b'bqtools/tests/schemaTest1.json')
        self.schemaTest2 = self.load_data(b'bqtools/tests/schemaTest2.json')
        self.schema2startnobare = self.load_data(b'bqtools/tests/schema2startnobare.json')
        self.schemaTest2bare = self.load_data(b'bqtools/tests/schemaTest2bare.json')
        self.schemaTest2nonbare = self.load_data(b'bqtools/tests/schemaTest2nonbare.json')
        self.schemaTest4 = self.load_data(b'bqtools/tests/schemaTest4.json')
        self.schemaTest3 = self.load_data(b'bqtools/tests/schemaTest3.json')
        self.monsterSchema = self.load_data(b'bqtools/tests/monsterSchema.json')

    def test_toDict(self):
        schema2Dict = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'float', b'FLOAT'),
         bigquery.SchemaField(b'boolean', b'BOOLEAN'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'integer2', b'INTEGER'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'))))
        expectedResult = [
         {b'name': b'string', 
            b'type': b'STRING', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'integer', 
            b'type': b'INTEGER', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'float', 
            b'type': b'FLOAT', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'boolean', 
            b'type': b'BOOLEAN', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'record', 
            b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': [
                      {b'name': b'string2', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'float', 
                         b'type': b'FLOAT', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'integer2', 
                         b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'boolean2', 
                         b'type': b'BOOLEAN', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []}]},
         {b'name': b'array', 
            b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'REPEATED', 
            b'fields': [
                      {b'name': b'string3', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'integer3', 
                         b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []}]}]
        sa = []
        for bqi in schema2Dict:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(expectedResult, sa, ignore_order=True)
        self.assertEqual(diff, {}, (b'Unexpected result in toDict expected nothing insteadest got {}').format(self.pp.pprint(diff)))
        return

    def test_createschema(self):
        bqSchema = bqtools.create_schema(self.schemaTest1)
        expectedSchema = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'float', b'FLOAT'),
         bigquery.SchemaField(b'boolean', b'BOOLEAN'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'integer2', b'INTEGER'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'))))
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        isa = sa
        sa = []
        for bqi in expectedSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(isa, sa, ignore_order=True)
        a = (b'Schema test1 schema does not match target {}').format(len(diff))
        self.assertEqual(diff, {}, a)

    def test_createschema2(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        sa2 = []
        for bqi in bqSchema2:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        expectedSchema2 = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'),
          bigquery.SchemaField(b'appended1', b'STRING'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'),
          bigquery.SchemaField(b'foo', b'FLOAT'))),
         bigquery.SchemaField(b'anotherarray', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'test1', b'INTEGER'),
          bigquery.SchemaField(b'test2', b'BOOLEAN'))))
        sa = []
        for bqi in expectedSchema2:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        a = (b'Schema test1 schema does not match target {}').format(diff)
        self.assertEqual(diff, {}, a)
        logger = logging.getLogger(b'testBQTools')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello'}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 1')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 2')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 3')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2'}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 4')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 6')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': []}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 7')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [{b'string3': b'hello'}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 8')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [{b'string3': b'hello', b'integer3': 42}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 9')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 10')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 11')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False}, {b'test1': 52, b'test2': True}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 12')
        copyoforigschema = list(expectedSchema2)
        savedSchema = copy.deepcopy(copyoforigschema)
        sa = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False},
                           {b'test1': 52, b'test2': True, b'fred': b'I am an evolved string', 
                              b'iamanotherevolve': 32}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 13')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        diff = dict(diff)
        print(b'============================================ evolve test 1 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 1 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolve', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False}, {b'test1': 52, b'test2': True}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 2 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 2 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'fred': b'I am same previous evolution'}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 3 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 3 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 4 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 4 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'bill': [
                                      b'hello', b'fred', b'break this']}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 5 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 5 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [
                                                                        {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                           b'name': b'value', 
                                                                           b'type': b'STRING'}], 
                                                              b'mode': b'REPEATED', 
                                                              b'name': b'bill', 
                                                              b'type': b'RECORD'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'bill': {}}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 6 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 6 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [
                                                                        {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                           b'name': b'xxxDummySchemaAsNoneDefinedxxx', 
                                                                           b'type': b'STRING'}], 
                                                              b'mode': b'NULLABLE', 
                                                              b'name': b'bill', 
                                                              b'type': b'RECORD'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        return

    def test_patchbare(self):
        startschema = bqtools.create_schema(self.schema2startnobare)
        resultschema = bqtools.create_schema(self.schemaTest2nonbare)
        origobject = copy.deepcopy(self.schemaTest2bare)
        evolved = bqtools.match_and_addtoschema(self.schemaTest2bare, startschema)
        self.assertEqual(evolved, True, b'Bare llist and multi dict evolution has not happened as expected')
        diff = DeepDiff(resultschema, startschema, ignore_order=True)
        print(b'============================================ mixed arrays added  diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ mixed arrays added  diff end  ====================================')

    def test_patch(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        bqSchema = bqtools.create_schema(self.schemaTest1)
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        osa = copy.deepcopy(sa)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema2, sa)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        expectedDiff = {b'iterable_item_added': {b'root[2]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'integer2', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'float', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'string2', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'boolean2', 
                                                              b'type': b'BOOLEAN'}], 
                                                 b'mode': b'NULLABLE', 
                                                 b'name': b'record', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'integer3', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'string3', 
                                                              b'type': b'STRING'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'array', 
                                                 b'type': b'RECORD'}}, 
           b'iterable_item_removed': {b'root[2]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'integer2', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'float', 
                                                                b'type': b'FLOAT'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'string2', 
                                                                b'type': b'STRING'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'boolean2', 
                                                                b'type': b'BOOLEAN'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'appended1', 
                                                                b'type': b'STRING'}], 
                                                   b'mode': b'NULLABLE', 
                                                   b'name': b'record', 
                                                   b'type': b'RECORD'}, 
                                      b'root[5]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'integer3', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'string3', 
                                                                b'type': b'STRING'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'foo', 
                                                                b'type': b'FLOAT'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'array', 
                                                   b'type': b'RECORD'}, 
                                      b'root[6]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}
        self.assertEqual(diff, expectedDiff, (b'Patch diff is not what is expected {}').format(self.pp.pformat(diff)))
        self.assertEqual(change, True, (b'Patch diff change result {} is not what is expected {}').format(change, self.pp.pformat(diff)))
        bqSchema3 = bqtools.create_schema(self.schemaTest3)
        bqSchema4 = bqtools.create_schema(self.schemaTest4)
        sa2 = []
        for bqi in bqSchema3:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        osa = copy.deepcopy(sa2)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema4, sa2)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), change))
        return

    def test_patch2(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        bqSchema = bqtools.create_schema(self.schemaTest2)
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        osa = copy.deepcopy(sa)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema2, sa)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        expectedDiff = {}
        self.assertEqual(diff, expectedDiff, (b'Patch diff is not what is expected {}').format(self.pp.pformat(diff)))
        self.assertEqual(change, False, (b'Patch diff change result {} is not what is expected {}').format(change, self.pp.pformat(diff)))
        self.schemaTest2nonbare = self.load_data(b'bqtools/tests/schemaTest2nonbare.json')
        self.schemaTest4 = self.load_data(b'bqtools/tests/schemaTest4.json')
        self.schemaTest3 = self.load_data(b'bqtools/tests/schemaTest3.json')
        self.monsterSchema = self.load_data(b'bqtools/tests/monsterSchema.json')

    def test_toDict(self):
        schema2Dict = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'float', b'FLOAT'),
         bigquery.SchemaField(b'boolean', b'BOOLEAN'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'integer2', b'INTEGER'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'))))
        expectedResult = [
         {b'name': b'string', 
            b'type': b'STRING', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'integer', 
            b'type': b'INTEGER', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'float', 
            b'type': b'FLOAT', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'boolean', 
            b'type': b'BOOLEAN', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': []},
         {b'name': b'record', 
            b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': [
                      {b'name': b'string2', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'float', 
                         b'type': b'FLOAT', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'integer2', 
                         b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'boolean2', 
                         b'type': b'BOOLEAN', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []}]},
         {b'name': b'array', 
            b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'REPEATED', 
            b'fields': [
                      {b'name': b'string3', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []},
                      {b'name': b'integer3', 
                         b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': []}]}]
        sa = []
        for bqi in schema2Dict:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(expectedResult, sa, ignore_order=True)
        self.assertEqual(diff, {}, (b'Unexpected result in toDict expected nothing insteadest got {}').format(self.pp.pprint(diff)))
        return

    def test_createschema(self):
        bqSchema = bqtools.create_schema(self.schemaTest1)
        expectedSchema = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'float', b'FLOAT'),
         bigquery.SchemaField(b'boolean', b'BOOLEAN'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'integer2', b'INTEGER'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'))))
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        isa = sa
        sa = []
        for bqi in expectedSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(isa, sa, ignore_order=True)
        a = (b'Schema test1 schema does not match target {}').format(len(diff))
        self.assertEqual(diff, {}, a)

    def test_createschema2(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        sa2 = []
        for bqi in bqSchema2:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        expectedSchema2 = (
         bigquery.SchemaField(b'string', b'STRING'),
         bigquery.SchemaField(b'integer', b'INTEGER'),
         bigquery.SchemaField(b'record', b'RECORD', fields=(
          bigquery.SchemaField(b'string2', b'STRING'),
          bigquery.SchemaField(b'float', b'FLOAT'),
          bigquery.SchemaField(b'boolean2', b'BOOLEAN'),
          bigquery.SchemaField(b'appended1', b'STRING'))),
         bigquery.SchemaField(b'array', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'string3', b'STRING'),
          bigquery.SchemaField(b'integer3', b'INTEGER'),
          bigquery.SchemaField(b'foo', b'FLOAT'))),
         bigquery.SchemaField(b'anotherarray', b'RECORD', mode=b'REPEATED', fields=(
          bigquery.SchemaField(b'test1', b'INTEGER'),
          bigquery.SchemaField(b'test2', b'BOOLEAN'))))
        sa = []
        for bqi in expectedSchema2:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        a = (b'Schema test1 schema does not match target {}').format(diff)
        self.assertEqual(diff, {}, a)
        logger = logging.getLogger(b'testBQTools')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello'}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 1')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 2')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 3')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2'}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 4')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 6')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': []}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 7')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [{b'string3': b'hello'}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 8')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [{b'string3': b'hello', b'integer3': 42}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 9')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 10')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 11')
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False}, {b'test1': 52, b'test2': True}]}, expectedSchema2, logger=logger)
        self.assertEqual(evolved, False, b'Expected no evolve but got evolve true evolve test 12')
        copyoforigschema = list(expectedSchema2)
        savedSchema = copy.deepcopy(copyoforigschema)
        sa = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False},
                           {b'test1': 52, b'test2': True, b'fred': b'I am an evolved string', 
                              b'iamanotherevolve': 32}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 13')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        diff = dict(diff)
        print(b'============================================ evolve test 1 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 1 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolve', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [{b'test1': 52, b'test2': False}, {b'test1': 52, b'test2': True}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 2 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 2 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'fred': b'I am same previous evolution'}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 3 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 3 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, (b'Schema evolution not as expected {}').format(self.pp.pformat(diff)))
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 4 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 4 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'bill': [
                                      b'hello', b'fred', b'break this']}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 5 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 5 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [
                                                                        {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                           b'name': b'value', 
                                                                           b'type': b'STRING'}], 
                                                              b'mode': b'REPEATED', 
                                                              b'name': b'bill', 
                                                              b'type': b'RECORD'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        copyoforigschema = copy.deepcopy(savedSchema)
        evolved = bqtools.match_and_addtoschema({b'string': b'hello', b'integer': 52, b'hellomike': 3.1415926, 
           b'record': {b'string2': b'hello2', b'float': 1.3, b'boolean2': False, 
                       b'appended1': b'another string'}, 
           b'array': [
                    {b'string3': b'hello', b'integer3': 42, b'foo': 3.141}, {b'integer3': 42, b'foo': 3.141}], 
           b'anotherarray': [
                           {b'test1': 52, b'test2': False, b'fred': b'I am an evolution'},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3},
                           {b'test1': 52, b'test2': True, b'iamanotherevolution': 1.3, 
                              b'bill': {}}]}, copyoforigschema, logger=logger)
        self.assertEqual(evolved, True, b'Expected evolve but got no evolve False for evolve test 14')
        sa2 = []
        for bqi in copyoforigschema:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        diff = DeepDiff(sa, sa2, ignore_order=True)
        print(b'============================================ evolve test 6 diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ evolve test 6 diff end  ====================================')
        self.assertEqual({b'iterable_item_added': {b'root[4]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test1', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'test2', 
                                                              b'type': b'BOOLEAN'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'fred', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'iamanotherevolution', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [
                                                                        {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                           b'name': b'xxxDummySchemaAsNoneDefinedxxx', 
                                                                           b'type': b'STRING'}], 
                                                              b'mode': b'NULLABLE', 
                                                              b'name': b'bill', 
                                                              b'type': b'RECORD'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'anotherarray', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                 b'name': b'hellomike', 
                                                 b'type': b'FLOAT'}}, 
           b'iterable_item_removed': {b'root[4]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}, diff, b'Schema evolution not as expected')
        return

    def test_patchbare(self):
        startschema = bqtools.create_schema(self.schema2startnobare)
        resultschema = bqtools.create_schema(self.schemaTest2nonbare)
        origobject = copy.deepcopy(self.schemaTest2bare)
        evolved = bqtools.match_and_addtoschema(self.schemaTest2bare, startschema)
        self.assertEqual(evolved, True, b'Bare llist and multi dict evolution has not happened as expected')
        diff = DeepDiff(resultschema, startschema, ignore_order=True)
        print(b'============================================ mixed arrays added  diff start  ====================================')
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), evolved))
        print(b'============================================ mixed arrays added  diff end  ====================================')

    def test_patch(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        bqSchema = bqtools.create_schema(self.schemaTest1)
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        osa = copy.deepcopy(sa)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema2, sa)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        expectedDiff = {b'iterable_item_added': {b'root[2]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'integer2', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'float', 
                                                              b'type': b'FLOAT'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'string2', 
                                                              b'type': b'STRING'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'boolean2', 
                                                              b'type': b'BOOLEAN'}], 
                                                 b'mode': b'NULLABLE', 
                                                 b'name': b'record', 
                                                 b'type': b'RECORD'}, 
                                    b'root[5]': {b'description': None, b'fields': [
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'integer3', 
                                                              b'type': b'INTEGER'},
                                                           {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                              b'name': b'string3', 
                                                              b'type': b'STRING'}], 
                                                 b'mode': b'REPEATED', 
                                                 b'name': b'array', 
                                                 b'type': b'RECORD'}}, 
           b'iterable_item_removed': {b'root[2]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'integer2', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'float', 
                                                                b'type': b'FLOAT'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'string2', 
                                                                b'type': b'STRING'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'boolean2', 
                                                                b'type': b'BOOLEAN'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'appended1', 
                                                                b'type': b'STRING'}], 
                                                   b'mode': b'NULLABLE', 
                                                   b'name': b'record', 
                                                   b'type': b'RECORD'}, 
                                      b'root[5]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'integer3', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'string3', 
                                                                b'type': b'STRING'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'foo', 
                                                                b'type': b'FLOAT'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'array', 
                                                   b'type': b'RECORD'}, 
                                      b'root[6]': {b'description': None, b'fields': [
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test1', 
                                                                b'type': b'INTEGER'},
                                                             {b'description': None, b'fields': [], b'mode': b'NULLABLE', 
                                                                b'name': b'test2', 
                                                                b'type': b'BOOLEAN'}], 
                                                   b'mode': b'REPEATED', 
                                                   b'name': b'anotherarray', 
                                                   b'type': b'RECORD'}}}
        self.assertEqual(diff, expectedDiff, (b'Patch diff is not what is expected {}').format(self.pp.pformat(diff)))
        self.assertEqual(change, True, (b'Patch diff change result {} is not what is expected {}').format(change, self.pp.pformat(diff)))
        bqSchema3 = bqtools.create_schema(self.schemaTest3)
        bqSchema4 = bqtools.create_schema(self.schemaTest4)
        sa2 = []
        for bqi in bqSchema3:
            i = bqtools.to_dict(bqi)
            sa2.append(i)

        osa = copy.deepcopy(sa2)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema4, sa2)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        print((b'Patched schema diff {} change{}').format(self.pp.pformat(diff), change))
        return

    def test_patch2(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        bqSchema = bqtools.create_schema(self.schemaTest2)
        sa = []
        for bqi in bqSchema:
            i = bqtools.to_dict(bqi)
            sa.append(i)

        osa = copy.deepcopy(sa)
        change, pschema = bqtools.recurse_and_add_to_schema(bqSchema2, sa)
        diff = DeepDiff(pschema, osa, ignore_order=True)
        expectedDiff = {}
        self.assertEqual(diff, expectedDiff, (b'Patch diff is not what is expected {}').format(self.pp.pformat(diff)))
        self.assertEqual(change, False, (b'Patch diff change result {} is not what is expected {}').format(change, self.pp.pformat(diff)))

    def test_sync(self):
        logging.basicConfig(level=logging.INFO)
        bqclient = bigquery.Client()
        stclient = storage.Client()
        destination_project = bqclient.project
        test_buckets = []
        usbucket = (b'bqsynctest_{}_us').format(destination_project)
        test_buckets.append({b'name': usbucket, b'region': b'us'})
        eubucket = (b'bqsynctest_{}_eu').format(destination_project)
        test_buckets.append({b'name': eubucket, b'region': b'eu'})
        eu2bucket = (b'bqsynctest_{}_europe-west-2').format(destination_project)
        test_buckets.append({b'name': eu2bucket, b'region': b'europe-west2'})
        logging.info(b'Checking buckets for bqsync tests exist in right regions and with lifecycle rules...')
        for bucket_dict in test_buckets:
            bucket = None
            try:
                bucket = stclient.get_bucket(bucket_dict[b'name'])
            except exceptions.NotFound:
                bucket_ref = storage.Bucket(stclient, name=bucket_dict[b'name'])
                bucket_ref.location = bucket_dict[b'region']
                storage.Bucket.create(bucket_ref, stclient)
                bucket = stclient.get_bucket(bucket_dict[b'name'])

            rules = bucket.lifecycle_rules
            nrules = []
            found1daydeletrule = False
            for rule in rules:
                if isinstance(rule, dict):
                    if b'condition' in rule and b'age' in rule[b'condition'] and rule[b'condition'][b'age'] == 1 and b'isLive' in rule[b'condition'] and rule[b'condition'][b'isLive']:
                        found1daydeletrule = True
                nrules.append(rule)

            if not found1daydeletrule:
                nrules.append({b'action': {b'type': b'Delete'}, b'condition': {b'age': 1, b'isLive': True}})
            bucket.lifecycle_rules = nrules
            bucket.update(stclient)

        test_source_configs = []
        test_source_configs.append({b'description': b'small dataset good to start tests basic types', 
           b'dataset_name': b'fcc_political_ads', 
           b'table_filter_regexp': [
                                  b'broadcast_tv_radio_station',
                                  b'content_info',
                                  b'file_history',
                                  b'file_record'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'date partitioned 1 date type field', 
           b'dataset_name': b'wikipedia', 
           b'table_filter_regexp': [
                                  b'wikidata'], 
           b'max_last_days': None})
        test_source_configs.append({b'description': b'a table with geography data type', 
           b'dataset_name': b'faa', 
           b'table_filter_regexp': [
                                  b'us_airports'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'a dataset with a day partitioned table with  clustering not using a specific partition column name so  just ingest time', 
           b'dataset_name': b'new_york_subway', 
           b'table_filter_regexp': [
                                  b'geo_nyc_borough_boundaries'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'a dataset with view referencing it self to demo simple view copying', 
           b'dataset_name': b'noaa_goes16', 
           b'table_filter_regexp': [
                                  b'.*'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'a dataset with functions only', 
           b'dataset_name': b'persistent_udfs', 
           b'table_filter_regexp': [
                                  b'.*'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'a dataset with nested table example and a model', 
           b'dataset_name': b'samples', 
           b'table_filter_regexp': [
                                  b'github_nested', b'model'], 
           b'max_last_days': 365})
        test_source_configs.append({b'description': b'a dataset with day partioned no clustering using natural load time', 
           b'dataset_name': b'sec_quarterly_financials', 
           b'table_filter_regexp': [
                                  b'.*'], 
           b'max_last_days': 1095})
        test_source_configs.append({b'description': b'a dataset with a day partitioned table with clustering using a specific partition column name so not just ingest time', 
           b'dataset_name': b'human_genome_variants', 
           b'table_filter_regexp': [
                                  b'platinum_genomes_deepvariant_variants_20180823'], 
           b'max_last_days': None})
        test_destination_datasets_list = []
        for src_destination in test_source_configs:
            tests = []
            destdatset = (b'bqsynctest_{}_{}').format(b'US', src_destination[b'dataset_name']).replace(b'-', b'_')
            tests.append({b'subtest': b'us intra region', 
               b'destdataset': destdatset, 
               b'destregion': b'US'})
            test_destination_datasets_list.append(destdatset)
            destdatset = (b'bqsynctest_{}_{}').format(b'EU', src_destination[b'dataset_name']).replace(b'-', b'_')
            tests.append({b'subtest': b'us to eu cross region', 
               b'destdataset': destdatset, 
               b'destregion': b'EU', 
               b'dstbucket': eubucket})
            test_destination_datasets_list.append(destdatset)
            destdatset = (b'bqsynctest_{}_{}').format(b'europe-west2', src_destination[b'dataset_name']).replace(b'-', b'_')
            tests.append({b'subtest': b'us to eu cross region', 
               b'destdataset': destdatset, 
               b'destregion': b'europe-west2', 
               b'dstbucket': eu2bucket})
            test_destination_datasets_list.append(destdatset)
            src_destination[b'tests'] = tests

        logging.info(b'Checking daatsets for bqsync tests exist in right regions and if exist empty them i.e. delete and recreate them...')
        for datasetname in test_destination_datasets_list:
            dataset_ref = bqclient.dataset(datasetname)
            if bqtools.dataset_exists(bqclient, dataset_ref):
                bqclient.delete_dataset(bqclient.get_dataset(dataset_ref), delete_contents=True)

        logging.info(b'Staring tests...')
        test_source_configs = []
        for test_config in test_source_configs:
            for dstconfig in test_config[b'tests']:
                dataset_ref = bqclient.dataset(dstconfig[b'destdataset'])
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = dstconfig[b'destregion']
                dataset = bqclient.create_dataset(dataset)
                synctest = None
                if dstconfig[b'destregion'] == b'US':
                    synctest = bqtools.MultiBQSyncCoordinator([(b'bigquery-public-data.{}').format(test_config[b'dataset_name'])], [
                     (b'{}.{}').format(destination_project, dstconfig[b'destdataset'])], remove_deleted_tables=True, copy_data=True, copy_types=[
                     b'TABLE', b'VIEW', b'ROUTINE', b'MODEL'], check_depth=0, table_view_filter=test_config[b'table_filter_regexp'], table_or_views_to_exclude=[], latest_date=None, days_before_latest_day=test_config[b'max_last_days'], day_partition_deep_check=False, analysis_project=destination_project)
                else:
                    synctest = bqtools.MultiBQSyncCoordinator([
                     (b'bigquery-public-data.{}').format(test_config[b'dataset_name'])], [
                     (b'{}.{}').format(destination_project, dstconfig[b'destdataset'])], srcbucket=usbucket, dstbucket=dstconfig[b'dstbucket'], remove_deleted_tables=True, copy_data=True, copy_types=[
                     b'TABLE', b'VIEW', b'ROUTINE', b'MODEL'], check_depth=0, table_view_filter=test_config[b'table_filter_regexp'], table_or_views_to_exclude=[], latest_date=None, days_before_latest_day=test_config[b'max_last_days'], day_partition_deep_check=False, analysis_project=destination_project)
                synctest.sync()
                self.assertEqual(True, True, (b'Initial Sync {} {} from bigquery-public-data..{} with {}.{}  completed').format(test_config[b'description'], dstconfig[b'subtest'], test_config[b'dataset_name'], destination_project, dstconfig[b'destdataset']))
                synctest.reset_stats()
                synctest.sync()
                self.assertEqual(synctest.tables_avoided, synctest.tables_synced, (b'Second Sync {} {} from bigquery-public-data..{} with {}.{}  completed').format(test_config[b'description'], dstconfig[b'subtest'], test_config[b'dataset_name'], destination_project, dstconfig[b'destdataset']))

            eutest = bqtools.MultiBQSyncCoordinator([
             (b'{}.{}').format(destination_project, test_config[b'tests'][1][b'destdataset'])], [
             (b'{}.{}').format(destination_project, test_config[b'tests'][2][b'destdataset'])], srcbucket=eubucket, dstbucket=eu2bucket, remove_deleted_tables=True, copy_data=True, copy_types=[
             b'TABLE', b'VIEW', b'ROUTINE', b'MODEL'], check_depth=0, table_view_filter=[
             b'.*'], table_or_views_to_exclude=[], latest_date=None, days_before_latest_day=None, day_partition_deep_check=False, analysis_project=destination_project)
            eutest.sync()
            self.assertEqual(eutest.tables_avoided + eutest.view_avoided + eutest.routines_avoided, eutest.tables_synced + eutest.views_synced + eutest.routines_synced, (b'Inter europe Sync {} {} from {}.{} with {}.{}completed').format(test_config[b'description'], b'EU to europe-west2', destination_project, test_config[b'tests'][1][b'destdataset'], destination_project, test_config[b'tests'][2][b'destdataset']))

        return

    def test_gendiff(self):
        bqSchema2 = bqtools.create_schema(self.schemaTest2)
        views = bqtools.gen_diff_views(b'foo', b'ar', b'bob', bqSchema2, description=b'A test schema')
        vexpected = {b'bobdb': {b'query': b'#standardSQL\nSELECT\n    _PARTITIONTIME AS scantime,\n    xxrownumbering.partRowNumber,\n    ifnull(tabob.integer,0) as integer,\n    ifnull(A1.integer3,0) as arrayinteger3,\n    ifnull(A1.foo,0.0) as arrayfoo,\n    ifnull(A1.string3,"None") as arraystring3,\n    ifnull(A2.test1,0) as anotherarraytest1,\n    ifnull(A2.test2,False) as anotherarraytest2,\n    ifnull(tabob.string,"None") as string,\n    ifnull(tabob.record.appended1,"None") as recordappended1,\n    ifnull(tabob.record.float,0.0) as recordfloat,\n    ifnull(tabob.record.string2,"None") as recordstring2,\n    ifnull(tabob.record.boolean2,False) as recordboolean2\nfrom `foo.ar.bob` as tabob\nLEFT JOIN UNNEST(tabob.array) as A1\nLEFT JOIN UNNEST(tabob.anotherarray) as A2\n    JOIN (\n      SELECT\n        scantime,\n        ROW_NUMBER() OVER(ORDER BY scantime) AS partRowNumber\n      FROM (\n        SELECT\n          DISTINCT _PARTITIONTIME AS scantime,\n        FROM\n          `foo.ar.bob`)) AS xxrownumbering\n    ON\n      _PARTITIONTIME = xxrownumbering.scantime\n    ', 
                      b'description': b'View used as basis for diffview:A test schema'}, 
           b'bobdiff': {b'query': b'#standardSQL\nSELECT\n  *\nFROM (\n  SELECT\n    ifnull(earlier.scantime,\n      later.scantime) AS scantime,\n    CASE\n      WHEN earlier.scantime IS NULL AND later.scantime IS NOT NULL THEN 1\n      WHEN earlier.scantime IS NOT NULL\n    AND later.scantime IS NULL THEN -1\n    ELSE\n    0\n  END\n    AS action,\n    ARRAY((\n      SELECT\n        field\n      FROM (\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "integer"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "arrayinteger3"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "arrayfoo"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "arraystring3"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "anotherarraytest1"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "anotherarraytest2"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "string"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "recordappended1"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "recordfloat"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "recordstring2"\n             ELSE CAST(null as string) END as field\n\n     UNION ALL\n         SELECT \n           CASE \n              WHEN earlier.scantime IS NULL or later.scantime IS NULL then "recordboolean2"\n             ELSE CAST(null as string) END as field\n\n            \n            )\n      WHERE\n        field IS NOT NULL) ) AS updatedFields,\n    ifnull(later.integer,\n      earlier.integer) AS integer,\nifnull(later.arrayinteger3,\n      earlier.arrayinteger3) AS arrayinteger3,\nifnull(later.arrayfoo,\n      earlier.arrayfoo) AS arrayfoo,\nifnull(later.arraystring3,\n      earlier.arraystring3) AS arraystring3,\nifnull(later.anotherarraytest1,\n      earlier.anotherarraytest1) AS anotherarraytest1,\nifnull(later.anotherarraytest2,\n      earlier.anotherarraytest2) AS anotherarraytest2,\nifnull(later.string,\n      earlier.string) AS string,\nifnull(later.recordappended1,\n      earlier.recordappended1) AS recordappended1,\nifnull(later.recordfloat,\n      earlier.recordfloat) AS recordfloat,\nifnull(later.recordstring2,\n      earlier.recordstring2) AS recordstring2,\nifnull(later.recordboolean2,\n      earlier.recordboolean2) AS recordboolean2\n  FROM \n     (#standardSQL\nSELECT\n    _PARTITIONTIME AS scantime,\n    xxrownumbering.partRowNumber,\n    ifnull(tabob.integer,0) as integer,\n    ifnull(A1.integer3,0) as arrayinteger3,\n    ifnull(A1.foo,0.0) as arrayfoo,\n    ifnull(A1.string3,"None") as arraystring3,\n    ifnull(A2.test1,0) as anotherarraytest1,\n    ifnull(A2.test2,False) as anotherarraytest2,\n    ifnull(tabob.string,"None") as string,\n    ifnull(tabob.record.appended1,"None") as recordappended1,\n    ifnull(tabob.record.float,0.0) as recordfloat,\n    ifnull(tabob.record.string2,"None") as recordstring2,\n    ifnull(tabob.record.boolean2,False) as recordboolean2\nfrom `foo.ar.bob` as tabob\nLEFT JOIN UNNEST(tabob.array) as A1\nLEFT JOIN UNNEST(tabob.anotherarray) as A2\n    JOIN (\n      SELECT\n        scantime,\n        ROW_NUMBER() OVER(ORDER BY scantime) AS partRowNumber\n      FROM (\n        SELECT\n          DISTINCT _PARTITIONTIME AS scantime,\n        FROM\n          `foo.ar.bob`)) AS xxrownumbering\n    ON\n      _PARTITIONTIME = xxrownumbering.scantime\n    ) as later \n  FULL OUTER JOIN \n     (#standardSQL\nSELECT\n    _PARTITIONTIME AS scantime,\n    xxrownumbering.partRowNumber,\n    ifnull(tabob.integer,0) as integer,\n    ifnull(A1.integer3,0) as arrayinteger3,\n    ifnull(A1.foo,0.0) as arrayfoo,\n    ifnull(A1.string3,"None") as arraystring3,\n    ifnull(A2.test1,0) as anotherarraytest1,\n    ifnull(A2.test2,False) as anotherarraytest2,\n    ifnull(tabob.string,"None") as string,\n    ifnull(tabob.record.appended1,"None") as recordappended1,\n    ifnull(tabob.record.float,0.0) as recordfloat,\n    ifnull(tabob.record.string2,"None") as recordstring2,\n    ifnull(tabob.record.boolean2,False) as recordboolean2\nfrom `foo.ar.bob` as tabob\nLEFT JOIN UNNEST(tabob.array) as A1\nLEFT JOIN UNNEST(tabob.anotherarray) as A2\n    JOIN (\n      SELECT\n        scantime,\n        ROW_NUMBER() OVER(ORDER BY scantime) AS partRowNumber\n      FROM (\n        SELECT\n          DISTINCT _PARTITIONTIME AS scantime,\n        FROM\n          `foo.ar.bob`)) AS xxrownumbering\n    ON\n      _PARTITIONTIME = xxrownumbering.scantime\n    \n     -- avoid last row as full outer join this will attempt to find a row later\n     -- that won\'t exist showing as a false delete\n     WHERE \n    partRowNumber < (SELECT \n        MAX(partRowNumber)\n    FROM (\n      SELECT\n        scantime,\n        ROW_NUMBER() OVER(ORDER BY scantime) AS partRowNumber\n      FROM (\n        SELECT\n          DISTINCT _PARTITIONTIME AS scantime,\n        FROM\n          `foo.ar.bob`)\n    ))\n) as earlier\n  ON\n    earlier.partRowNumber = later.partRowNumber -1\n    AND earlier.integer = later.integer\nAND earlier.arrayinteger3 = later.arrayinteger3\nAND earlier.arrayfoo = later.arrayfoo\nAND earlier.arraystring3 = later.arraystring3\nAND earlier.anotherarraytest1 = later.anotherarraytest1\nAND earlier.anotherarraytest2 = later.anotherarraytest2\nAND earlier.string = later.string\nAND earlier.recordappended1 = later.recordappended1\nAND earlier.recordfloat = later.recordfloat\nAND earlier.recordstring2 = later.recordstring2\nAND earlier.recordboolean2 = later.recordboolean2\n)\nWHERE\n  (action != 0 or array_length(updatedFields) > 0)\n', 
                        b'description': b'View calculates what has changed at what time:A test schema'}, 
           b'bobdiffday': {b'query': b"#standardSQL\nSELECT\n    o.scantime as origscantime,\n    l.scantime as laterscantime,\n    CASE\n    WHEN o.integer IS NULL THEN 'Added'\n    WHEN l.integer IS NULL THEN 'Deleted'\n    WHEN o.integer = l.integer AND o.arrayinteger3 = l.arrayinteger3 AND o.arrayfoo = l.arrayfoo AND o.arraystring3 = l.arraystring3 AND o.anotherarraytest1 = l.anotherarraytest1 AND o.anotherarraytest2 = l.anotherarraytest2 AND o.string = l.string AND o.recordappended1 = l.recordappended1 AND o.recordfloat = l.recordfloat AND o.recordstring2 = l.recordstring2 AND o.recordboolean2 = l.recordboolean2 THEN 'Same'\n    ELSE 'Updated'\n  END AS action,\n    o.integer as originteger,\n    l.integer as laterinteger,\n    case when o.integer = l.integer then 0 else 1 end as diffinteger,\n    o.arrayinteger3 as origarrayinteger3,\n    l.arrayinteger3 as laterarrayinteger3,\n    case when o.arrayinteger3 = l.arrayinteger3 then 0 else 1 end as diffarrayinteger3,\n    o.arrayfoo as origarrayfoo,\n    l.arrayfoo as laterarrayfoo,\n    case when o.arrayfoo = l.arrayfoo then 0 else 1 end as diffarrayfoo,\n    o.arraystring3 as origarraystring3,\n    l.arraystring3 as laterarraystring3,\n    case when o.arraystring3 = l.arraystring3 then 0 else 1 end as diffarraystring3,\n    o.anotherarraytest1 as origanotherarraytest1,\n    l.anotherarraytest1 as lateranotherarraytest1,\n    case when o.anotherarraytest1 = l.anotherarraytest1 then 0 else 1 end as diffanotherarraytest1,\n    o.anotherarraytest2 as origanotherarraytest2,\n    l.anotherarraytest2 as lateranotherarraytest2,\n    case when o.anotherarraytest2 = l.anotherarraytest2 then 0 else 1 end as diffanotherarraytest2,\n    o.string as origstring,\n    l.string as laterstring,\n    case when o.string = l.string then 0 else 1 end as diffstring,\n    o.recordappended1 as origrecordappended1,\n    l.recordappended1 as laterrecordappended1,\n    case when o.recordappended1 = l.recordappended1 then 0 else 1 end as diffrecordappended1,\n    o.recordfloat as origrecordfloat,\n    l.recordfloat as laterrecordfloat,\n    case when o.recordfloat = l.recordfloat then 0 else 1 end as diffrecordfloat,\n    o.recordstring2 as origrecordstring2,\n    l.recordstring2 as laterrecordstring2,\n    case when o.recordstring2 = l.recordstring2 then 0 else 1 end as diffrecordstring2,\n    o.recordboolean2 as origrecordboolean2,\n    l.recordboolean2 as laterrecordboolean2,\n    case when o.recordboolean2 = l.recordboolean2 then 0 else 1 end as diffrecordboolean2\n  FROM (SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime = (\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob`\n    WHERE\n      _PARTITIONTIME < (\n      SELECT\n        MAX(_PARTITIONTIME)\n      FROM\n        `foo.ar.bob`)\n      AND\n      _PARTITIONTIME < TIMESTAMP_SUB(CURRENT_TIMESTAMP(),INTERVAL 1 DAY) ) ) o\nFULL OUTER JOIN (\n  SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime =(\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob` )) l\nON\n    l.integer = o.integer\n    AND l.arrayinteger3=o.arrayinteger3\n    AND l.arrayfoo=o.arrayfoo\n    AND l.arraystring3=o.arraystring3\n    AND l.anotherarraytest1=o.anotherarraytest1\n    AND l.anotherarraytest2=o.anotherarraytest2\n    AND l.string=o.string\n    AND l.recordappended1=o.recordappended1\n    AND l.recordfloat=o.recordfloat\n    AND l.recordstring2=o.recordstring2\n    AND l.recordboolean2=o.recordboolean2", 
                           b'description': b'Diff of day of underlying table bob description: A test schema'}, 
           b'bobdiffweek': {b'query': b"#standardSQL\nSELECT\n    o.scantime as origscantime,\n    l.scantime as laterscantime,\n    CASE\n    WHEN o.integer IS NULL THEN 'Added'\n    WHEN l.integer IS NULL THEN 'Deleted'\n    WHEN o.integer = l.integer AND o.arrayinteger3 = l.arrayinteger3 AND o.arrayfoo = l.arrayfoo AND o.arraystring3 = l.arraystring3 AND o.anotherarraytest1 = l.anotherarraytest1 AND o.anotherarraytest2 = l.anotherarraytest2 AND o.string = l.string AND o.recordappended1 = l.recordappended1 AND o.recordfloat = l.recordfloat AND o.recordstring2 = l.recordstring2 AND o.recordboolean2 = l.recordboolean2 THEN 'Same'\n    ELSE 'Updated'\n  END AS action,\n    o.integer as originteger,\n    l.integer as laterinteger,\n    case when o.integer = l.integer then 0 else 1 end as diffinteger,\n    o.arrayinteger3 as origarrayinteger3,\n    l.arrayinteger3 as laterarrayinteger3,\n    case when o.arrayinteger3 = l.arrayinteger3 then 0 else 1 end as diffarrayinteger3,\n    o.arrayfoo as origarrayfoo,\n    l.arrayfoo as laterarrayfoo,\n    case when o.arrayfoo = l.arrayfoo then 0 else 1 end as diffarrayfoo,\n    o.arraystring3 as origarraystring3,\n    l.arraystring3 as laterarraystring3,\n    case when o.arraystring3 = l.arraystring3 then 0 else 1 end as diffarraystring3,\n    o.anotherarraytest1 as origanotherarraytest1,\n    l.anotherarraytest1 as lateranotherarraytest1,\n    case when o.anotherarraytest1 = l.anotherarraytest1 then 0 else 1 end as diffanotherarraytest1,\n    o.anotherarraytest2 as origanotherarraytest2,\n    l.anotherarraytest2 as lateranotherarraytest2,\n    case when o.anotherarraytest2 = l.anotherarraytest2 then 0 else 1 end as diffanotherarraytest2,\n    o.string as origstring,\n    l.string as laterstring,\n    case when o.string = l.string then 0 else 1 end as diffstring,\n    o.recordappended1 as origrecordappended1,\n    l.recordappended1 as laterrecordappended1,\n    case when o.recordappended1 = l.recordappended1 then 0 else 1 end as diffrecordappended1,\n    o.recordfloat as origrecordfloat,\n    l.recordfloat as laterrecordfloat,\n    case when o.recordfloat = l.recordfloat then 0 else 1 end as diffrecordfloat,\n    o.recordstring2 as origrecordstring2,\n    l.recordstring2 as laterrecordstring2,\n    case when o.recordstring2 = l.recordstring2 then 0 else 1 end as diffrecordstring2,\n    o.recordboolean2 as origrecordboolean2,\n    l.recordboolean2 as laterrecordboolean2,\n    case when o.recordboolean2 = l.recordboolean2 then 0 else 1 end as diffrecordboolean2\n  FROM (SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime = (\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob`\n    WHERE\n      _PARTITIONTIME < (\n      SELECT\n        MAX(_PARTITIONTIME)\n      FROM\n        `foo.ar.bob`)\n      AND\n      _PARTITIONTIME < TIMESTAMP_SUB(CURRENT_TIMESTAMP(),INTERVAL 7 DAY) ) ) o\nFULL OUTER JOIN (\n  SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime =(\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob` )) l\nON\n    l.integer = o.integer\n    AND l.arrayinteger3=o.arrayinteger3\n    AND l.arrayfoo=o.arrayfoo\n    AND l.arraystring3=o.arraystring3\n    AND l.anotherarraytest1=o.anotherarraytest1\n    AND l.anotherarraytest2=o.anotherarraytest2\n    AND l.string=o.string\n    AND l.recordappended1=o.recordappended1\n    AND l.recordfloat=o.recordfloat\n    AND l.recordstring2=o.recordstring2\n    AND l.recordboolean2=o.recordboolean2", 
                            b'description': b'Diff of week of underlying table bob description: A test schema'}, 
           b'bobdiffmonth': {b'query': b"#standardSQL\nSELECT\n    o.scantime as origscantime,\n    l.scantime as laterscantime,\n    CASE\n    WHEN o.integer IS NULL THEN 'Added'\n    WHEN l.integer IS NULL THEN 'Deleted'\n    WHEN o.integer = l.integer AND o.arrayinteger3 = l.arrayinteger3 AND o.arrayfoo = l.arrayfoo AND o.arraystring3 = l.arraystring3 AND o.anotherarraytest1 = l.anotherarraytest1 AND o.anotherarraytest2 = l.anotherarraytest2 AND o.string = l.string AND o.recordappended1 = l.recordappended1 AND o.recordfloat = l.recordfloat AND o.recordstring2 = l.recordstring2 AND o.recordboolean2 = l.recordboolean2 THEN 'Same'\n    ELSE 'Updated'\n  END AS action,\n    o.integer as originteger,\n    l.integer as laterinteger,\n    case when o.integer = l.integer then 0 else 1 end as diffinteger,\n    o.arrayinteger3 as origarrayinteger3,\n    l.arrayinteger3 as laterarrayinteger3,\n    case when o.arrayinteger3 = l.arrayinteger3 then 0 else 1 end as diffarrayinteger3,\n    o.arrayfoo as origarrayfoo,\n    l.arrayfoo as laterarrayfoo,\n    case when o.arrayfoo = l.arrayfoo then 0 else 1 end as diffarrayfoo,\n    o.arraystring3 as origarraystring3,\n    l.arraystring3 as laterarraystring3,\n    case when o.arraystring3 = l.arraystring3 then 0 else 1 end as diffarraystring3,\n    o.anotherarraytest1 as origanotherarraytest1,\n    l.anotherarraytest1 as lateranotherarraytest1,\n    case when o.anotherarraytest1 = l.anotherarraytest1 then 0 else 1 end as diffanotherarraytest1,\n    o.anotherarraytest2 as origanotherarraytest2,\n    l.anotherarraytest2 as lateranotherarraytest2,\n    case when o.anotherarraytest2 = l.anotherarraytest2 then 0 else 1 end as diffanotherarraytest2,\n    o.string as origstring,\n    l.string as laterstring,\n    case when o.string = l.string then 0 else 1 end as diffstring,\n    o.recordappended1 as origrecordappended1,\n    l.recordappended1 as laterrecordappended1,\n    case when o.recordappended1 = l.recordappended1 then 0 else 1 end as diffrecordappended1,\n    o.recordfloat as origrecordfloat,\n    l.recordfloat as laterrecordfloat,\n    case when o.recordfloat = l.recordfloat then 0 else 1 end as diffrecordfloat,\n    o.recordstring2 as origrecordstring2,\n    l.recordstring2 as laterrecordstring2,\n    case when o.recordstring2 = l.recordstring2 then 0 else 1 end as diffrecordstring2,\n    o.recordboolean2 as origrecordboolean2,\n    l.recordboolean2 as laterrecordboolean2,\n    case when o.recordboolean2 = l.recordboolean2 then 0 else 1 end as diffrecordboolean2\n  FROM (SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime = (\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob`\n    WHERE\n      _PARTITIONTIME < (\n      SELECT\n        MAX(_PARTITIONTIME)\n      FROM\n        `foo.ar.bob`)\n      AND\n      _PARTITIONTIME < TIMESTAMP_SUB(CURRENT_TIMESTAMP(),INTERVAL 30 DAY) ) ) o\nFULL OUTER JOIN (\n  SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime =(\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob` )) l\nON\n    l.integer = o.integer\n    AND l.arrayinteger3=o.arrayinteger3\n    AND l.arrayfoo=o.arrayfoo\n    AND l.arraystring3=o.arraystring3\n    AND l.anotherarraytest1=o.anotherarraytest1\n    AND l.anotherarraytest2=o.anotherarraytest2\n    AND l.string=o.string\n    AND l.recordappended1=o.recordappended1\n    AND l.recordfloat=o.recordfloat\n    AND l.recordstring2=o.recordstring2\n    AND l.recordboolean2=o.recordboolean2", 
                             b'description': b'Diff of month of underlying table bob description: A test schema'}, 
           b'bobdifffortnight': {b'query': b"#standardSQL\nSELECT\n    o.scantime as origscantime,\n    l.scantime as laterscantime,\n    CASE\n    WHEN o.integer IS NULL THEN 'Added'\n    WHEN l.integer IS NULL THEN 'Deleted'\n    WHEN o.integer = l.integer AND o.arrayinteger3 = l.arrayinteger3 AND o.arrayfoo = l.arrayfoo AND o.arraystring3 = l.arraystring3 AND o.anotherarraytest1 = l.anotherarraytest1 AND o.anotherarraytest2 = l.anotherarraytest2 AND o.string = l.string AND o.recordappended1 = l.recordappended1 AND o.recordfloat = l.recordfloat AND o.recordstring2 = l.recordstring2 AND o.recordboolean2 = l.recordboolean2 THEN 'Same'\n    ELSE 'Updated'\n  END AS action,\n    o.integer as originteger,\n    l.integer as laterinteger,\n    case when o.integer = l.integer then 0 else 1 end as diffinteger,\n    o.arrayinteger3 as origarrayinteger3,\n    l.arrayinteger3 as laterarrayinteger3,\n    case when o.arrayinteger3 = l.arrayinteger3 then 0 else 1 end as diffarrayinteger3,\n    o.arrayfoo as origarrayfoo,\n    l.arrayfoo as laterarrayfoo,\n    case when o.arrayfoo = l.arrayfoo then 0 else 1 end as diffarrayfoo,\n    o.arraystring3 as origarraystring3,\n    l.arraystring3 as laterarraystring3,\n    case when o.arraystring3 = l.arraystring3 then 0 else 1 end as diffarraystring3,\n    o.anotherarraytest1 as origanotherarraytest1,\n    l.anotherarraytest1 as lateranotherarraytest1,\n    case when o.anotherarraytest1 = l.anotherarraytest1 then 0 else 1 end as diffanotherarraytest1,\n    o.anotherarraytest2 as origanotherarraytest2,\n    l.anotherarraytest2 as lateranotherarraytest2,\n    case when o.anotherarraytest2 = l.anotherarraytest2 then 0 else 1 end as diffanotherarraytest2,\n    o.string as origstring,\n    l.string as laterstring,\n    case when o.string = l.string then 0 else 1 end as diffstring,\n    o.recordappended1 as origrecordappended1,\n    l.recordappended1 as laterrecordappended1,\n    case when o.recordappended1 = l.recordappended1 then 0 else 1 end as diffrecordappended1,\n    o.recordfloat as origrecordfloat,\n    l.recordfloat as laterrecordfloat,\n    case when o.recordfloat = l.recordfloat then 0 else 1 end as diffrecordfloat,\n    o.recordstring2 as origrecordstring2,\n    l.recordstring2 as laterrecordstring2,\n    case when o.recordstring2 = l.recordstring2 then 0 else 1 end as diffrecordstring2,\n    o.recordboolean2 as origrecordboolean2,\n    l.recordboolean2 as laterrecordboolean2,\n    case when o.recordboolean2 = l.recordboolean2 then 0 else 1 end as diffrecordboolean2\n  FROM (SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime = (\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob`\n    WHERE\n      _PARTITIONTIME < (\n      SELECT\n        MAX(_PARTITIONTIME)\n      FROM\n        `foo.ar.bob`)\n      AND\n      _PARTITIONTIME < TIMESTAMP_SUB(CURRENT_TIMESTAMP(),INTERVAL 14 DAY) ) ) o\nFULL OUTER JOIN (\n  SELECT\n     *\n  FROM\n    `foo.ar.bobdb`\n  WHERE\n    scantime =(\n    SELECT\n      MAX(_PARTITIONTIME)\n    FROM\n      `foo.ar.bob` )) l\nON\n    l.integer = o.integer\n    AND l.arrayinteger3=o.arrayinteger3\n    AND l.arrayfoo=o.arrayfoo\n    AND l.arraystring3=o.arraystring3\n    AND l.anotherarraytest1=o.anotherarraytest1\n    AND l.anotherarraytest2=o.anotherarraytest2\n    AND l.string=o.string\n    AND l.recordappended1=o.recordappended1\n    AND l.recordfloat=o.recordfloat\n    AND l.recordstring2=o.recordstring2\n    AND l.recordboolean2=o.recordboolean2", 
                                 b'description': b'Diff of fortnight of underlying table bob description: A test schema'}}
        for vi in views:
            expected = vexpected[vi[b'name']][b'query'].splitlines(1)
            actual = vi[b'query'].splitlines(1)
            diff = difflib.unified_diff(expected, actual)
            print((b'').join(diff))
            self.assertEqual(len(vi[b'query']), len(vexpected[vi[b'name']][b'query']), (b'Query len for view {} is not equal to what is expected\n:{}:\n:{}:').format(vi[b'name'], vi[b'query'], vexpected[vi[b'name']][b'query']))
            self.assertEqual(vi[b'query'], vexpected[vi[b'name']][b'query'], (b'Query for view {} is not equal to what is expected\n:{}:\n:{}:').format(vi[b'name'], vi[b'query'], vexpected[vi[b'name']][b'query']))
            self.assertEqual(vi[b'description'], vexpected[vi[b'name']][b'description'], (b'Description for view {} is not equal to what is expected\n:{}:\n:{}:').format(vi[b'name'], vi[b'description'], vexpected[vi[b'name']][b'description']))

    def test_calc_field_depth(self):
        toTest = [
         {b'name': b'string', b'type': b'STRING', 
            b'description': None, 
            b'mode': b'NULLABLE'},
         {b'name': b'integer', b'type': b'INTEGER', 
            b'description': None, 
            b'mode': b'NULLABLE'},
         {b'name': b'float', b'type': b'FLOAT', 
            b'description': None, 
            b'mode': b'NULLABLE'},
         {b'name': b'boolean', b'type': b'BOOLEAN', 
            b'description': None, 
            b'mode': b'NULLABLE'},
         {b'name': b'record', b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'NULLABLE', 
            b'fields': [
                      {b'name': b'string2', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE'},
                      {b'name': b'float', b'type': b'FLOAT', 
                         b'description': None, 
                         b'mode': b'NULLABLE'},
                      {b'name': b'integer2', b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE'},
                      {b'name': b'boolean2', b'type': b'BOOLEAN', 
                         b'description': None, 
                         b'mode': b'NULLABLE'},
                      {b'name': b'record', b'type': b'RECORD', 
                         b'description': None, 
                         b'mode': b'NULLABLE', 
                         b'fields': [
                                   {b'name': b'string2', b'type': b'STRING', 
                                      b'description': None, 
                                      b'mode': b'NULLABLE'},
                                   {b'name': b'record', b'type': b'RECORD', 
                                      b'description': None, 
                                      b'mode': b'NULLABLE', 
                                      b'fields': [
                                                {b'name': b'string2', b'type': b'STRING', 
                                                   b'description': None, 
                                                   b'mode': b'NULLABLE'}]}]}]},
         {b'name': b'array', b'type': b'RECORD', 
            b'description': None, 
            b'mode': b'REPEATED', 
            b'fields': [
                      {b'name': b'string3', b'type': b'STRING', 
                         b'description': None, 
                         b'mode': b'NULLABLE'},
                      {b'name': b'integer3', b'type': b'INTEGER', 
                         b'description': None, 
                         b'mode': b'NULLABLE'}]}]
        depth = bqtools.calc_field_depth(toTest)
        self.assertEqual(depth, 3, b'measured field depth should be 3')
        bqtools.trunc_field_depth(toTest, 2)
        depth = bqtools.calc_field_depth(toTest)
        self.assertEqual(depth, 2, (b'measured field depth should be 2 is {}').format(depth))
        depth = bqtools.calc_field_depth(self.monsterSchema[b'schema'][b'fields'])
        self.assertEqual(depth, 13, (b'measured field depth should be 13 is {}').format(depth))
        newMonster = copy.deepcopy(self.monsterSchema)
        yamonster = bqtools.trunc_field_depth(newMonster[b'schema'][b'fields'], 10)
        depth = bqtools.calc_field_depth(newMonster[b'schema'][b'fields'])
        self.assertEqual(depth, 10, (b'measured field depth should be 10 is {}').format(depth))
        depth = bqtools.calc_field_depth(yamonster)
        self.assertEqual(depth, 10, (b'measured field depth should be 10 is {}').format(depth))
        return


def main(argv):
    unittest.main()


if __name__ == b'__main__':
    main(sys.argv)