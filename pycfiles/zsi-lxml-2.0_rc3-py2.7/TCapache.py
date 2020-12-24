# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/TCapache.py
# Compiled at: 2006-10-25 20:33:30
"""Apache typecodes.
"""
from ZSI import _copyright, _child_elements, _get_idstr
from ZSI.TC import TypeCode, Struct as _Struct, Any as _Any

class Apache:
    NS = 'http://xml.apache.org/xml-soap'


class _Map(TypeCode):
    """Apache's "Map" type.
    """
    parselist = [
     (
      Apache.NS, 'Map')]

    def __init__(self, pname=None, aslist=0, **kw):
        TypeCode.__init__(self, pname, **kw)
        self.aslist = aslist
        self.tc = _Struct(None, [_Any('key'), _Any('value')], inline=1)
        return

    def parse(self, elt, ps):
        self.checkname(elt, ps)
        if self.nilled(elt, ps):
            return None
        else:
            p = self.tc.parse
            if self.aslist:
                v = []
                for c in _child_elements(elt):
                    d = p(c, ps)
                    v.append((d['key'], d['value']))

            else:
                v = {}
                for c in _child_elements(elt):
                    d = p(c, ps)
                    v[d['key']] = d['value']

            return v

    def serialize(self, elt, sw, pyobj, name=None, **kw):
        objid = _get_idstr(pyobj)
        n = name or self.pname or 'E' + objid
        el = elt.createAppendElement(self.nspname, n)
        if self.nillable is True and pyobj is None:
            self.serialize_as_nil(el)
            return
        else:
            self.set_attributes(el, pyobj)
            unique = self.unique or kw.get('unique', False)
            if unique is False and sw.Known(orig or pyobj):
                self.set_attribute_href(el, objid)
                return
            if kw.get('typed', self.typed) is True:
                self.set_attribute_xsi_type(el, **kw)
            if self.unique is False:
                self.set_attribute_id(el, objid)
            if self.aslist:
                for k, v in pyobj:
                    self.tc.serialize(el, sw, {'key': k, 'value': v}, name='item')

            else:
                for k, v in pyobj.items():
                    self.tc.serialize(el, sw, {'key': k, 'value': v}, name='item')

            return


Apache.Map = _Map
if __name__ == '__main__':
    print _copyright