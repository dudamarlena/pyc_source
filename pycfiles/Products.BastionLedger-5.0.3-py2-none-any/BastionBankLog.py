# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/BastionBankLog.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl, string
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view_management_screens
from Acquisition import aq_base
from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
try:
    from Products.ZCTextIndex.ZCTextIndex import PLexicon
    from Products.ZCTextIndex.Lexicon import Splitter, CaseNormalizer
    from Products.ZCTextIndex.Lexicon import StopWordRemover
    have_zctextindex = 1
except ImportError:
    have_zctextindex = 0

from ZReturnCode import ZReturnCode

class TextIndexExtra:

    def __init__(self, lexicon_id, index_type):
        self.lexicon_id = lexicon_id
        self.index_type = index_type


def _generateEventId(btreefolder2):
    """ Generate an ID for Events """
    ob_count = btreefolder2._count()
    if ob_count == 0:
        return 'event_000000001'
    else:
        good_id = None
        found_ob = None
        while good_id is None:
            try_id = 'event_%s' % string.zfill(str(ob_count), 9)
            if btreefolder2._getOb(try_id, None) is None and btreefolder2._getOb('event_%i' % ob_count, None) is None:
                if found_ob is not None:
                    good_id = try_id
                elif try_id == 'event_000000001':
                    good_id = try_id
                else:
                    ob_count -= 1
            else:
                found_ob = 1
                ob_count += 1

        return good_id


class BastionBankServiceLogEvent(SimpleItem):
    """
    This is simply any loggable event.  It has the following attributes:
        o  date (DateTime)
        o  level (int)
        o  subject (string)
        o  message (string)
        
    A level of zero is OK, less than zero is an
    informational/peripheral message, and greater than zero is indicates a failure.
    """
    meta_type = 'BastionBankServiceLogEvent'
    _security = ClassSecurityInfo()
    __ac_permissions__ = (
     (
      view_management_screens, ('manage_tabs', 'manage_main')),)
    manage_options = ({'label': 'Message', 'action': 'manage_main'},)
    manage_main = PageTemplateFile('zpt/log_event', globals())

    def __init__(self, id, level, subject, message):
        self.id = id
        self.date = DateTime()
        self.level = level
        self.subject = subject
        self.message = message

    _security.declarePrivate('manage_afterAdd')

    def manage_afterAdd(self, item, container):
        self.aq_parent.catalog.catalog_object(self)


AccessControl.class_init.InitializeClass(BastionBankServiceLogEvent)

class BastionBankServiceLog(BTreeFolder2):
    """
    A bank transaction audit trail/logging mechanism.

    A ZCatalog instance is incorporated in the log to allow for a sophisticated searching
    engine.

    This stuff is designed to be around forever - hence the use of a BTree and hiding of
    delete features.
    """
    meta_type = 'BastionBankServiceLog'
    _security = ClassSecurityInfo()
    manage_options = (
     BTreeFolder2.manage_options[0],) + BTreeFolder2.manage_options[2:4]
    manage_main = PageTemplateFile('zpt/log', globals())

    def __init__(self, id, title):
        BTreeFolder2.__init__(self, id)
        self.title = title

    def manage_afterAdd(self, item, container):
        if hasattr(aq_base(self), 'catalog'):
            return
        self.manage_addProduct['ZCatalog'].manage_addZCatalog('catalog', 'Catalog')
        cat = getattr(self, 'catalog')
        if have_zctextindex:
            lexicon = PLexicon('lexicon', 'Lexicon', Splitter(), CaseNormalizer(), StopWordRemover())
            cat._setObject('lexicon', lexicon)
            ti_extra = TextIndexExtra('lexicon', 'Okapi BM25 Rank')
            cat.addIndex('SearchableText', 'ZCTextIndex', ti_extra)
        else:
            cat.addIndex('SearchableText', 'TextIndex')
        cat.addIndex('date', 'FieldIndex')
        cat.addIndex('level', 'FieldIndex')
        for name in ('id', 'date', 'level', 'subject'):
            cat.addColumn(name)

    _security.declarePrivate('log')

    def log(self, level, subject, message=''):
        if not ZReturnCode._codes.has_key(level):
            raise AssertionError, 'Unsupported Log Level: %i' % level
        id = _generateEventId(self)
        self._setObject(id, BastionBankServiceLogEvent(id, ZReturnCode._codes[level], subject, message))

    _security.declareProtected(view_management_screens, 'saveSearch')

    def saveSearch(self, REQUEST):
        """ Save a search for possible later re-execution """
        if REQUEST.has_key('SESSION'):
            bbl_data = REQUEST.SESSION.set('bbl', REQUEST.form)


AccessControl.class_init.InitializeClass(BastionBankServiceLog)