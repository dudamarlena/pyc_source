# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/table_field_factory.py
# Compiled at: 2013-04-04 15:36:35


class ITableFieldFactory(object):
    """Factory interface for creating new Field-instances based on Container
    (datasource), item id, property id and uiContext (the component responsible
    for displaying fields). Currently this interface is used by L{Table},
    but might later be used by some other components for L{Field}
    generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @see: FormFieldFactory
    """

    def createField(self, container, itemId, propertyId, uiContext):
        """Creates a field based on the Container, item id, property id and
        the component responsible for displaying the field (most commonly
        L{Table}).

        @param container:
                   the Container where the property belongs to.
        @param itemId:
                   the item Id.
        @param propertyId:
                   the Id of the property.
        @param uiContext:
                   the component where the field is presented.
        @return: A field suitable for editing the specified data or null if the
                property should not be editable.
        """
        raise NotImplementedError