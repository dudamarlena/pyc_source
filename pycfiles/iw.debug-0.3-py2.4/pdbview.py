# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/debug/pdbview.py
# Compiled at: 2008-05-28 11:11:31
"""
Contains the PDB view. It will start the python debugger or the ipython python
debugger if available.
It will only start if the zope instance is in debug mode.
"""
import zope.component, zope.interface
from ipdb import set_trace
try:
    from Products.Five import BrowserView
    from App.config import getConfiguration
    debug_mode = getConfiguration().debug_mode
except:
    from zope.publisher.browser import BrowserView
    debug_mode = True

valid_keys = ('v', 'view')

class PdbView(BrowserView):
    __module__ = __name__

    def pdb(self):
        context = self.context
        request = self.request
        try:
            portal = context.portal_url.getPortalObject()
        except AttributeError:
            portal = None

        def getView(name):
            return zope.component.queryMultiAdapter((context, request), name=name)

        view_name = None
        kwargs = self.request.form
        for k in valid_keys:
            if k in kwargs:
                view_name = kwargs.get(k, None)
                del kwargs[k]

        if view_name:
            view = getView(view_name)
        else:
            view = None
        if view_name and view is None:
            meth = getattr(context, view_name, None)
        else:
            meth = None
        if debug_mode:
            ll = locals().copy()
            for k in ('getView', 'kwargs', 'ipdb', 'self', 'view_name', 'k'):
                try:
                    del ll[k]
                except KeyError:
                    pass

            if callable(view):
                fn = view
            elif callable(meth):
                fn = meth
            else:
                fn = None
            if callable(fn):
                if kwargs:
                    set_trace()
                    fn(**kwargs)
                else:
                    set_trace()
                    fn()
            else:
                set_trace()
        return