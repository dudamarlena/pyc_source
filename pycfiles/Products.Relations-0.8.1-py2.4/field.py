# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/field.py
# Compiled at: 2008-09-11 19:48:09
from types import ListType, TupleType, StringTypes
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import ReferenceField
from Products.Archetypes.Registry import registerField
from Products.Archetypes.utils import DisplayList
from Products.Archetypes import config as atconfig
try:
    from Products.generator import i18n
except ImportError:
    from Products.Archetypes.generator import i18n

from config import RELATIONS_LIBRARY
import processor, utils

class RelationField(ReferenceField):
    """
        This field is interface compatible to the normal reference field,
        but uses the Relations engine instead of the basic referece engine.
        it can be used with the Reference Widget and also provides 
        the usual get and set methods for the relation. 
    
    """
    __module__ = __name__
    _properties = ReferenceField._properties.copy()
    _properties.update({'type': 'relation'})
    security = ClassSecurityInfo()
    security.declarePrivate('set')

    def set(self, instance, value, **kwargs):
        """Mutator.

        ``value`` is a list of UIDs or one UID string to which I will add a
        relation to. None and [] are equal.
        """
        rc = getToolByName(instance, atconfig.REFERENCE_CATALOG)
        relationslib = getToolByName(instance, RELATIONS_LIBRARY)
        targetUIDs = [ ref.targetUID for ref in rc.getReferences(instance, self.relationship) ]
        if not self.multiValued and value and type(value) not in (ListType, TupleType):
            value = (value,)
        if not value:
            value = ()
        uids = []
        for v in value:
            if type(v) in StringTypes:
                uids.append(v)
            else:
                uids.append(v.UID())

        add = [ v for v in uids if v if v not in targetUIDs ]
        sub = [ t for t in targetUIDs if t not in uids ]
        sUid = instance.UID()
        addtriples = []
        subtriples = []
        for tUid in add:
            addtriples.append((sUid, tUid, self.relationship))

        for tUid in sub:
            subtriples.append((sUid, tUid, self.relationship))

        processor.process(relationslib, connect=addtriples, disconnect=subtriples)
        if self.callStorageOnSet:
            ObjectField.set(self, instance, self.getRaw(instance), **kwargs)

    def _Vocabulary(self, content_instance):
        rel_vocab = utils.adddeleteVocab(content_instance, ruleset_ids=[self.relationship])
        if rel_vocab:
            tuples = rel_vocab[0]['tuples']
        else:
            tuples = []
        brains = [ t[0] for t in tuples ]
        pairs = [ (t[0].UID, t[0].Title) for t in tuples ]
        if i18n and not self.required and not self.multiValued:
            no_reference = i18n.translate(domain='archetypes', msgid='label_no_reference', context=content_instance, default='<no reference>')
            pairs.insert(0, ('', no_reference))
        __traceback_info__ = (content_instance, self.getName(), pairs)
        return DisplayList(pairs)


registerField(RelationField, title='Relations', description='Used for storing references through Relations.')