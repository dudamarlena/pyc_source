# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/core/impl/processor/encoder.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 22, 2012\n\n@package: ally core\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nModel encoder testing.\n'
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.api.config import model
from ally.api.type import typeFor, List
from ally.container import ioc
from ally.core.impl.processor.encoder import CreateEncoderHandler
from ally.core.spec.transform.exploit import Resolve
from ally.core.spec.transform.render import RenderToObject
from ally.core.spec.resources import ConverterPath
import unittest

@model(id='Key')
class ModelKey:
    Key = str
    Name = str


@model(id='Id')
class ModelId:
    Id = int
    Name = str
    Flags = List(str)
    ModelKey = ModelKey


class TestModel(unittest.TestCase):

    def testEncode(self):
        transformer = CreateEncoderHandler()
        ioc.initialize(transformer)
        resolve = Resolve(transformer.encoderFor(typeFor(ModelId)))
        render = RenderToObject()
        context = dict(render=render, converter=ConverterPath(), converterId=ConverterPath(), normalizer=ConverterPath())
        model = ModelId()
        model.Id = 12
        render.obj = None
        resolve.request(value=model, **context).doAll()
        self.assertEqual({'Id': '12'}, render.obj)
        model.ModelKey = 'The key'
        render.obj = None
        resolve.request(value=model, **context).doAll()
        self.assertEqual({'Id': '12',  'ModelKey': {'Key': 'The key'}}, render.obj)
        model.Name = 'Uau Name'
        model.Flags = ['1', '2', '3']
        render.obj = None
        resolve.request(value=model, **context).doAll()
        self.assertEqual({'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}, render.obj)
        transformer = CreateEncoderHandler()
        ioc.initialize(transformer)
        resolve = Resolve(transformer.encoderFor(typeFor(List(ModelId))))
        render.obj = None
        resolve.request(value=[model], **context).doAll()
        self.assertEqual({'ModelIdList': [{'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}]}, render.obj)
        render.obj = None
        resolve.request(value=[model, model, model], **context)
        resolve.do()
        self.assertEqual({'ModelIdList': []}, render.obj)
        resolve.do()
        self.assertEqual({'ModelIdList': [{'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}]}, render.obj)
        resolve.do()
        self.assertEqual({'ModelIdList': [{'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}, {'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}]}, render.obj)
        resolve.do()
        self.assertEqual({'ModelIdList': [{'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}, {'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}, {'ModelKey': {'Key': 'The key'},  'Flags': {'Flags': ['1', '2', '3']},  'Id': '12',  'Name': 'Uau Name'}]}, render.obj)
        resolve.do()
        self.assertFalse(resolve.has())
        return


if __name__ == '__main__':
    unittest.main()