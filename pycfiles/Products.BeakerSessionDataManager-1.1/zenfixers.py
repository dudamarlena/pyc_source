# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/browser/zenfixers.py
# Compiled at: 2011-01-11 16:22:56
from Acquisition import aq_base, aq_inner
from Products.Five.browser import BrowserView

def delObject(context, id, tp=1, suppress_events=False):
    """
    strong medicine to overcome all these f**ked relation objects
    """
    ob = context._getOb(id)
    if getattr(aq_base(ob), '_objects', None):
        ob._objects = ()
        try:
            ob._v__object_deleted__ = 1
        except:
            pass

    context._objects = tuple([ i for i in context._objects if i['id'] != id ])
    context._delOb(id)
    return


class FixerMethods(BrowserView):
    __module__ = __name__

    def fixZenPackManager(self):
        """
        packs with missing/broken objects get left in the packs Relation
        """
        context = aq_inner(self.context)
        packs = context.zport.dmd.packs
        for id in packs.objectIds():
            pack = packs._getOb(id)
            if pack.getId() != id:
                delObject(packs, id)

        self.request.RESPONSE.redirect('manage_main')

    def deletePacks(self):
        """
        packs has actually been moved to ZenPackManger
        """
        context = aq_inner(self.context)
        dmd = context.zport.dmd
        if getattr(aq_base(dmd), 'packs', None):
            delObject(dmd, 'packs')
        self.request.RESPONSE.redirect('manage_main')
        return