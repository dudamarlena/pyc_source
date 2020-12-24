# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/form_field_factory.py
# Compiled at: 2013-04-04 15:36:35


class IFormFieldFactory(object):
    """Factory interface for creating new Field-instances based on
    L{Item}, property id and uiContext (the component responsible for
    displaying fields). Currently this interface is used by L{Form}, but
    might later be used by some other components for L{Field} generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @see: L{TableFieldFactory}
    """

    def createField(self, item, propertyId, uiContext):
        """Creates a field based on the item, property id and the component
        (most commonly L{Form}) where the Field will be presented.

        @param item:
                   the item where the property belongs to.
        @param propertyId:
                   the Id of the property.
        @param uiContext:
                   the component where the field is presented, most commonly
                   this is L{Form}. uiContext will not necessary be the
                   parent component of the field, but the one that is
                   responsible for creating it.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError