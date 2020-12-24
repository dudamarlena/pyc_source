# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/zcml.py
# Compiled at: 2010-03-12 11:12:03
from zif.headincludes.resourcelibrary import LibraryInfo, library_info
from zope.app import zapi
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.metadirectives import IBasicResourceInformation
from zope.app.publisher.browser.resourcemeta import allowed_names
from zope.configuration.exceptions import ConfigurationError
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.security.checker import CheckerPublic, NamesChecker
import os.path, zope.configuration.fields

class IResourceLibraryDirective(IBasicResourceInformation):
    """
    Defines a resource library
    """
    name = zope.schema.TextLine(title='The name of the resource library', description='        This is the name used to disambiguate resource libraries.  No two\n        libraries can be active with the same name.', required=True)
    require = zope.configuration.fields.Tokens(title='Require', description='The resource libraries on which this library depends.', required=False, value_type=zope.schema.Text())


class IDirectoryDirective(Interface):
    """
    Identifies a directory to be included in a resource library
    """
    source = zope.configuration.fields.Path(title='Source', description='The directory containing the files to add.', required=True)
    include = zope.configuration.fields.Tokens(title='Include', description='The files which should be included in HTML pages which reference this resource library.', required=False, value_type=zope.schema.Text())


def handler(name, dependencies, required, provided, adapter_name, factory, info=''):
    if dependencies:
        for dep in dependencies:
            if dep not in library_info:
                raise ConfigurationError('Resource library "%s" has unsatisfied dependency on "%s".' % (
                 name, dep))

    zapi.getGlobalSiteManager().registerAdapter(factory, required, provided, adapter_name, info)


INCLUDABLE_EXTENTIONS = ('.js', '.css')

class ResourceLibrary(object):

    def __init__(self, _context, name, require=(), layer=IDefaultBrowserLayer, permission='zope.Public'):
        self.name = name
        self.layer = layer
        if permission == 'zope.Public':
            permission = CheckerPublic
        self.checker = NamesChecker(allowed_names, permission)
        library_info[name] = LibraryInfo()
        library_info[name].required.extend(require)

    def directory(self, _context, source, include=()):
        if not os.path.isdir(source):
            raise ConfigurationError('Directory %r does not exist' % source)
        for file_name in include:
            ext = os.path.splitext(file_name)[1]
            if ext not in INCLUDABLE_EXTENTIONS:
                raise ConfigurationError('Resource library doesn\'t know how to include this file: "%s".' % file_name)

        library_info[self.name].included.extend(include)
        factory = directoryresource.DirectoryResourceFactory(source, self.checker, self.name)
        _context.action(discriminator=(
         'resource', self.name, IBrowserRequest, self.layer), callable=handler, args=(
         self.name, library_info[self.name].required, (self.layer,),
         Interface, self.name, factory, _context.info))