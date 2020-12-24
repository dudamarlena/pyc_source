# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/CurrencyIndex.py
# Compiled at: 2015-07-18 19:38:10
from types import IntType
import logging
logger = logging.getLogger('UnIndex')
import BTrees.Length
from BTrees.IIBTree import IISet, union, intersection, multiunion
from BTrees.IOBTree import IOBTree
from BTrees.OIBTree import OIBTree
from BTrees.OOBTree import OOBTree
from ZCurrency import CURRENCIES, ZCurrency, UnsupportedCurrency
from App.special_dtml import DTMLFile
from OFS.PropertyManager import PropertyManager
from ZODB.POSException import ConflictError
from zope.interface import implements
from Products.PluginIndexes.common import safe_callable
from Products.PluginIndexes.common.UnIndex import UnIndex
from Products.PluginIndexes.common.util import parseIndexRequest
from Products.BastionBanking.interfaces.ICurrencyIndex import ICurrencyIndex
_marker = []
try:
    import Products.BastionCurrencyTool
    MULTI_CURRENCY_SUPPORT = True
except ImportError:
    MULTI_CURRENCY_SUPPORT = False

class CurrencyIndex(UnIndex, PropertyManager):
    """
    Index for currencies (ie ordered amounts).
    """
    implements(ICurrencyIndex)
    meta_type = 'CurrencyIndex'
    query_options = ['query', 'range']
    base_currency = 'USD'
    convert_to_base = True
    _properties = ({'id': 'base_currency', 'type': 'selection', 'mode': 'w', 'select_variable': 'currencies'}, {'id': 'convert_to_base', 'type': 'boolean', 'mode': 'w'})
    manage = manage_main = DTMLFile('dtml/manageCurrencyIndex', globals())
    manage_browse = DTMLFile('dtml/browseIndex', globals())
    manage_main._setName('manage_main')
    manage_options = (
     {'label': 'Settings', 'action': 'manage_main'},
     {'label': 'Browse', 'action': 'manage_browse'}) + PropertyManager.manage_options

    def __init__(self, id, ignore_ex=None, call_methods=None, extra=None, caller=None):
        UnIndex.__init__(self, id, ignore_ex, call_methods, extra, caller)
        if extra:
            if extra.has_key('base_currency'):
                self.base_currency = extra['base_currency']

    def currencies(self):
        """
        property manager helper
        """
        return CURRENCIES

    def clear(self):
        """ Complete reset """
        self._index = OOBTree()
        self._unindex = IOBTree()
        self._length = BTrees.Length.Length()

    def index_object(self, documentId, obj, threshold=None):
        """index an object, normalizing the indexed value to an integer

           o Normalized value has granularity of one minute.

           o Objects which have 'None' as indexed value are *omitted*,
             by design.
        """
        returnStatus = 0
        try:
            currency_attr = getattr(obj, self.id)
            if safe_callable(currency_attr):
                currency_attr = currency_attr()
            converted = self._convert(value=currency_attr, default=_marker)
        except AttributeError:
            converted = _marker

        old = self._unindex.get(documentId, _marker)
        if converted != old:
            if old is not _marker:
                self.removeForwardIndexEntry(old, documentId)
                if converted is _marker:
                    try:
                        del self._unindex[documentId]
                    except ConflictError:
                        raise
                    except:
                        logger.error("Should not happen: ConvertedDate was there, now it's not, for document with id %s" % documentId)

            if converted is not _marker:
                self.insertForwardIndexEntry(converted, documentId)
                self._unindex[documentId] = converted
            returnStatus = 1
        return returnStatus

    def _apply_index(self, request, cid='', type=type):
        """Apply the index to query parameters given in the argument
        """
        record = parseIndexRequest(request, self.id, self.query_options)
        if record.keys == None:
            return
        else:
            keys = map(self._convert, record.keys)
            index = self._index
            r = None
            opr = None
            operator = record.get('operator', self.useOperator)
            if operator not in self.operators:
                raise RuntimeError, 'operator not valid: %s' % operator
            if operator == 'or':
                set_func = union
            else:
                set_func = intersection
            range_arg = record.get('range', None)
            if range_arg:
                opr = 'range'
                opr_args = []
                if range_arg.find('min') > -1:
                    opr_args.append('min')
                if range_arg.find('max') > -1:
                    opr_args.append('max')
            if record.get('usage', None):
                opr = record.usage.lower().split(':')
                opr, opr_args = opr[0], opr[1:]
            if opr == 'range':
                if 'min' in opr_args:
                    lo = min(keys)
                else:
                    lo = None
                if 'max' in opr_args:
                    hi = max(keys)
                else:
                    hi = None
                if hi:
                    setlist = index.values(lo, hi)
                else:
                    setlist = index.values(lo)
                r = multiunion(setlist)
            else:
                for key in keys:
                    set = index.get(key, None)
                    if set is not None:
                        if type(set) is IntType:
                            set = IISet((set,))
                        r = set_func(r, set)

                if type(r) is IntType:
                    r = IISet((r,))
                if r is None:
                    return (IISet(), (self.id,))
            return (
             r, (self.id,))
            return

    def _convert(self, value, default=None):
        """Convert ZCurrency value to our base currency type so that equality comparisons make
        some sense.  A reindex in effect revalues the """
        if not isinstance(value, ZCurrency):
            value = ZCurrency(value)
        if value.currency() != self.base_currency:
            if not MULTI_CURRENCY_SUPPORT:
                return default
            currency_tool = self.Control_Panel.CurrencyTool
            try:
                rate = currency_tool.getCrossQuote(value.currency(), self.base_currency).mid
            except UnsupportedCurrency:
                return default

            return ZCurrency(self.base_currency, rate * value.amount())
        return value


manage_addCurrencyIndexForm = DTMLFile('dtml/addCurrencyIndex', globals())

def manage_addCurrencyIndex(self, id, REQUEST=None, RESPONSE=None, URL3=None):
    """Add a Date index"""
    return self.manage_addIndex(id, 'CurrencyIndex', extra=None, REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)