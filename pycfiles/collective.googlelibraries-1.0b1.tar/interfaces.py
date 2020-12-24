# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/interfaces.py
# Compiled at: 2010-12-01 16:10:29
from zope import interface
from zope import schema
from collective.googlelibraries import messageFactory as _

class IGoogleLibrariesLayer(interface.Interface):
    """Browser layer"""
    pass


class ILibrary(interface.Interface):
    """ """
    id = schema.ASCIILine(title=_('label_id', default='id'))
    title = schema.TextLine(title=_('label_title', default='Title'))
    version = schema.ASCIILine(title=_('label_version', default='Version'))
    url = schema.URI(title=_('label_url', default='URL minified'))
    optionalSettings = schema.Dict(title=_('label_optionalSettings', default='Optional settings'))


class ILibraryField(schema.interfaces.IASCIILine):
    """Field for Library"""
    pass


class LibraryField(schema.ASCIILine):
    __doc__ = ILibraryField.__doc__
    interface.implements(ILibraryField)


class ILibraryManager(interface.Interface):
    """The library manager. manage CRUD on Library"""
    libraries = schema.Tuple(title=_('label_libraries', default='Google Libraries'), description=_('help_libraires', default='Add Google Libraries.'), unique=True, value_type=LibraryField(title=_('Library')))


class IGoogleAPIKey(schema.interfaces.IASCIILine):
    """Field for a google api key."""
    pass


class GoogleAPIKey(schema.ASCIILine):
    __doc__ = IGoogleAPIKey.__doc__
    interface.implements(IGoogleAPIKey)


class IAPIKeyManager(interface.Interface):
    google_keys = schema.Tuple(title=_('label_google_keys', default='Google Libraries API Keys'), description=_('help_google_keys', default='Add Google Libraries API keys. You have to use the client side url at which your site is visible.'), unique=True, value_type=GoogleAPIKey(title=_('Key')))

    def api_key(request):
        """Return the key associated to the host. The host is extracted
        from the request object"""
        pass