# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/vocabulary.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3526 bytes
__doc__ = 'PyAMS_utils.vocabulary module\n\nThis module is used to handle vocabularies.\n'
import logging, venusian
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import getVocabularyRegistry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (utils)')

class vocabulary_config:
    """vocabulary_config"""
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