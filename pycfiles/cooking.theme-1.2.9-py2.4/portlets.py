# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cooking/theme/browser/portlets.py
# Compiled at: 2010-08-12 16:17:02
from plone.portlet.collection import collection
from zope.formlib import form
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.portlet.collection import PloneMessageFactory as _

class ICollectionListPortlet(collection.ICollectionPortlet):
    """Collection portlet that handles collection as a list"""
    __module__ = __name__


class AddForm(collection.AddForm):
    """Portlet add form.
    
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(ICollectionListPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    label = _('Add Collection List Portlet')
    description = _('This portlet display a listing of items from a Collection in a list.')