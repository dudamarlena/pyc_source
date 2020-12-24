# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_model/test_meta.py
# Compiled at: 2014-09-26 04:50:19
"""

  model meta tests
  ~~~~~~~~~~~~~~~~

  tests metacomponents of canteen's model layer.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
import inspect
from canteen import model
from canteen.model import adapter
from canteen.model import MetaFactory
from canteen.test import FrameworkTest

class MetaFactoryTests(FrameworkTest):
    """ Tests `model.MetaFactory`. """

    def test_abstract_factory(self):
        """ Test that `MetaFactory` is only usable abstractly. """
        self.assertTrue(inspect.isabstract(MetaFactory))
        with self.assertRaises(NotImplementedError):
            MetaFactory()

    def test_abstract_enforcement(self):
        """ Test abstraction enforcement on `MetaFactory` """

        class InsolentClass(MetaFactory):
            """ Look at me! I extend without implementing. The nerve! """
            pass

        with self.assertRaises(TypeError):
            InsolentClass(*(InsolentClass.__name__,
             (
              MetaFactory, type),
             dict([ (k, v) for k, v in InsolentClass.__dict__.items() ])))

    def test_resolve_adapters(self):
        """ Test that `MetaFactory` resolves adapters correctly """
        self.assertTrue(inspect.ismethod(MetaFactory.resolve))
        self.assertIsInstance(MetaFactory.resolve(*(model.Model.__name__,
         model.Model.__bases__,
         model.Model.__dict__,
         False)), tuple)
        self.assertIsInstance(MetaFactory.resolve(*(model.Model.__name__,
         model.Model.__bases__,
         model.Model.__dict__,
         True)), adapter.ModelAdapter)