# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/theme_resource.py
# Compiled at: 2013-04-04 15:36:36
"""A named theme dependent resource."""
from muntjac.terminal.resource import IResource

class ThemeResource(IResource):
    """C{ThemeResource} is a named theme dependent resource
    provided and managed by a theme. The actual resource contents are
    dynamically resolved to comply with the used theme by the terminal
    adapter. This is commonly used to provide static images, flash,
    java-applets, etc for the terminals.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, resourceId):
        """Creates a resource.

        @param resourceId:
                   the Id of the resource.
        """
        self._resourceID = None
        if resourceId is None:
            raise ValueError, 'IResource ID must not be null'
        if len(resourceId) == 0:
            raise ValueError, 'IResource ID can not be empty'
        if resourceId[0] == '/':
            raise ValueError, 'IResource ID must be relative (can not begin with /)'
        self._resourceID = resourceId
        return

    def __eq__(self, obj):
        """Tests if the given object equals this IResource.

        @param obj:
                   the object to be tested for equality.
        @return: C{True} if the given object equals this Icon,
                C{False} if not.
        """
        return isinstance(obj, ThemeResource) and self._resourceID == obj.resourceID

    def __ne__(self, obj):
        return not isinstance(obj, ThemeResource) or self._resourceID != obj.resourceID

    def __hash__(self):
        return hash(self._resourceID)

    def __str__(self):
        return str(self._resourceID)

    def getResourceId(self):
        """Gets the resource id.

        @return: the resource id.
        """
        return self._resourceID

    def getMIMEType(self):
        """@see: L{IResource.getMIMEType}"""
        from muntjac.service.file_type_resolver import FileTypeResolver
        return FileTypeResolver.getMIMEType(self.getResourceId())