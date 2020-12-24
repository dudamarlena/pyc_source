# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/vocabulary.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3526 bytes
"""PyAMS_utils.vocabulary module

This module is used to handle vocabularies.
"""
import logging, venusian
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import getVocabularyRegistry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (utils)')

class vocabulary_config:
    __doc__ = "Class decorator to define a vocabulary\n\n    :param str name: name of the registered vocabulary\n\n    This is, for example, how a vocabulary of registered ZEO connections utilities is created:\n\n    .. code-block:: python\n\n        from pyams_utils.interfaces.zeo import IZEOConnection\n\n        from pyams_utils.registry import get_utilities_for\n        from pyams_utils.vocabulary import vocabulary_config\n        from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary\n\n        @vocabulary_config(name='PyAMS ZEO connections')\n        class ZEOConnectionVocabulary(SimpleVocabulary):\n            '''ZEO connections vocabulary'''\n\n            def __init__(self, context=None):\n                terms = [SimpleTerm(name, title=util.name)\n                         for name, util in get_utilities_for(IZEOConnection)]\n                super(ZEOConnectionVocabulary, self).__init__(terms)\n\n    You can then use such a vocabulary in any schema field:\n\n    .. code-block:: python\n\n        from zope.interface import Interface\n        from zope.schema import Choice\n\n        class MySchema(Interface):\n            '''Custom schema interface'''\n\n            zeo_connection_name = Choice(title='ZEO connection name',\n                                         description='Please select a registered ZEO connection',\n                                         vocabulary='PyAMS ZEO connections',\n                                         required=False)\n    "
    venusian = venusian

    def __init__(self, name, **settings):
        self.name = name
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, obj):
            LOGGER.debug('Registering class {0} as vocabulary with name "{1}"'.format(str(obj), self.name))
            directlyProvides(obj, IVocabularyFactory)
            getVocabularyRegistry().register(self.name, obj)

        info = self.venusian.attach(wrapped, callback, category='pyams_vocabulary', depth=depth + 1)
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped