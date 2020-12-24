# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/gacontext/adapters.py
# Compiled at: 2008-05-20 05:21:26
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60982 $'
__version__ = '$Revision: 60982 $'[11:-2]
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from collective.gacontext.interfaces import IGACode

class GACode(object):
    """ Adapter for the metadata annotations """
    __module__ = __name__
    implements(IGACode)
    _KEY = 'collective.gacontext'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.metadata = annotations.get(self._KEY, None)
        if self.metadata is None:
            annotations[self._KEY] = PersistentDict()
            self.metadata = annotations[self._KEY]
        return

    def _get_ga_code(self):
        """ Get the GA code """
        return self.metadata.get('ga_code', None)

    def _set_ga_code(self, ga_code):
        """ Set the GA Code """
        self.metadata['ga_code'] = ga_code

    ga_code = property(_get_ga_code, _set_ga_code)