# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/base_field_factory.py
# Compiled at: 2013-04-04 15:36:35
from warnings import warn
from muntjac.ui.default_field_factory import DefaultFieldFactory
from muntjac.ui.field_factory import IFieldFactory
from muntjac.data.property import IProperty
from muntjac.ui.abstract_component import AbstractComponent

class BaseFieldFactory(IFieldFactory):
    """Default implementation of the the following Field types are used
    by default:

      - B{Boolean}: Button(switchMode:true).
      - B{Date}: DateField(resolution: day).
      - B{Item}: Form.
      - B{default field type}: TextField.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @deprecated: use L{DefaultFieldFactory} or own implementations
                 on L{FormFieldFactory} or L{TableFieldFactory}
                 instead.
    """

    def __init__(self):
        warn('use DefaultFieldFactory', DeprecationWarning)

    def createField(self, *args):
        """Creates the field based on type of data.

        @param args: tuple of the form
            - (type, uiContext)
              1. the type of data presented in field.
              2. the context where the Field is presented.
        @see: L{IFieldFactory.createField}
        """
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[0], IProperty):
                prop, uiContext = args
                if property is not None:
                    return self.createField(prop.getType(), uiContext)
                return
            else:
                typ, uiContext = args
                return DefaultFieldFactory.createFieldByPropertyType(typ)
        elif nargs == 3:
            item, propertyId, uiContext = args
            if item is not None and propertyId is not None:
                f = self.createField(item.getItemProperty(propertyId), uiContext)
                if isinstance(f, AbstractComponent):
                    name = DefaultFieldFactory.createCaptionByPropertyId(propertyId)
                    f.setCaption(name)
                return f
            return
        else:
            if nargs == 4:
                container, itemId, propertyId, uiContext = args
                prop = container.getContainerProperty(itemId, propertyId)
                return self.createField(prop, uiContext)
            raise ValueError, 'invalid number of arguments'
        return