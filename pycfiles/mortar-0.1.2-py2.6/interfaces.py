# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/interfaces.py
# Compiled at: 2008-12-19 12:41:15
from zope.interface import Interface, Attribute
marker = object()

class IContent(Interface):
    """
    All content must implement this interface.
    Security should be checked for each operation.
    """
    id = Attribute('\n       A unique identifier, that must be representable as a string,\n       for this object across the whole system.\n\n       This may also be None, indicating that it has not yet been\n       stored anywhere.\n       ')
    type = Attribute('\n       The type of this IContent. \n       ')
    names = Attribute('\n       The names of the fields currently available in this IContent.\n       This sequence will always be alphabetically ordered.\n       ')

    def __getitem__(name):
        """
        Get a field of the specified name.
        Returns an object implementing IField.
        """
        pass

    def __setitem__(name, value):
        """
        Set a field of the specified name.
        The value may implement IField or be of a type for which a
        converter to IFieldType has been registered.  
        """
        pass

    def view(name=None):
        """
        returns the view object or the default view if no name is specified.

        A KeyError is raised if the named view cannot be found or if
        there is no default view available for this IContent.
        """
        pass

    def dimension(name, id=None):
        """
        Return the dimension of the specified name with the provided identity.

        eg: c.dimension('revision',1).dimension('language','french')
        """
        pass


class IField(Interface):
    """A single field of a piece of content"""

    def get(default=marker, type=None):
        """
        Return the value of the field in the type specified.
        If the IContent does not have a value, return the default
        specified or, if the default is the marker, the default value
        specified in the content type. If this IContent has no content
        type, return None.
        The type specified must implement IFieldType.
        """
        pass

    def set(value, type=None):
        """
        Set this field to the supplied value. The value stored will be
        converted to IIf a type is supplied,
        the value will be converted to this type before being
        stored. Any type supplied must implement IFieldType.
        """
        pass

    type = Attribute('\n       The IFieldType of the data in this field. \n       ')

    def canSet(user=None):
        """
        returns boolean saying whether this field can be set by the current
        user.
        """
        pass

    def canGet(user=None):
        """
        returns boolean saying whether this field can be accessed by the current
        user.
        """
        pass

    def delete():
        """
        Deletes this field from the IContent containing it.
        If a field cannot be deleted, it should be reset to its default value.
        """
        pass


empty = object()

class IFieldType(Interface):
    """
    A marker interface indicating that this is a 'mortar-native'
    value.

    Subclasses of this interface are used to indicate particular types
    of value. The full list of these is provided in mortar.types.

    Registering adapters to these interfaces will allow you to set a
    field value to any object where an adapter to the appropriate
    interface is provided. The adapter does the conversion.
    """

    def __call__(self, *args, **kw):
        raise NotImplementedError
        r = Interface.__call__(*args, **kw)
        if r is empty:
            return None
        else:
            return r


class ICollection(Interface):
    """
    The result of a search
    """

    def __len__():
        """
        The number of results in this set
        """
        pass

    def __getitem__(i):
        """
        Return the i'th item in this sequence
        """
        pass

    def filter(*args, **kw):
        """
        Filter this result set.
        """
        pass

    def sort(*args, **kw):
        """
        Sort this result set.
        """
        pass

    def add(value):
        """
        value can be an id or an IContent.
        """
        pass

    def remove(value):
        """
        value can be an id or an IContent.
        """
        pass


class IStorage(Interface):
    """
    A physical storage for content objects.
    This could be a relational, file system or zodb storage.
    """

    def save(content):
        """
        This should store the supplied content in the current
        storage.
        If the content is already contained within this storage, then
        any changes made to it should be saved.

        If this storage does not support changing of its content or if
        the supplied content cannot be stored (eg: because it contains
        fields that do not map to a relational table) then a
        mortar.exceptions.NotSupported exception should be raised
        giving appropriate details.
        """
        pass

    def load(id):
        """
        This should load the content related to the supplied id.

        If the content does not exist in this storage, a
        mortar.exeptions.NotFound exception should be raised giving
        appropriate details.
        """
        pass


class ISearch(Interface):
    """
    """

    def search(query):
        """
        """
        pass


class IQueryAtom(Interface):
    """
    """
    pass


class IView(Interface):
    """
    A view control, for accumulating other controls
    """

    def __call__(self):
        """
        """
        pass


class IControl(Interface):
    """
    A control for inserting into things.

    Namespace isolation?

    Form processing?

    Urls?
    """

    def getUrl():
        """
        url for control interaction
        """
        pass

    def render():
        """
        """
        pass