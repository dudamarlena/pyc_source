# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/subscribers/variants.py
# Compiled at: 2008-09-03 11:14:28
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.component import adapter
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IProperty
from easyshop.core.interfaces import IPropertyOption

@adapter(IProperty, IObjectRemovedEvent)
def deleteProperty(property, event):
    """Removes property from all existing product variants.
    """
    product = property.aq_inner.aq_parent
    pvm = IProductVariantsManagement(product)
    if pvm.hasVariants() == False:
        return
    to_delete_property_id = property.getId()
    for variant in pvm.getVariants():
        new_properties = []
        for variant_property in variant.getForProperties():
            variant_property_id = variant_property.split(':')[0]
            if variant_property_id != to_delete_property_id:
                new_properties.append(variant_property)

        new_properties.sort()
        variant.setForProperties(new_properties)


@adapter(IPropertyOption, IObjectRemovedEvent)
def deleteProperty(option, event):
    """Removes property from all existing product variants.
    """
    property = option.aq_inner.aq_parent
    if property.getOptions() == 0:
        deleteProperty(property, event)