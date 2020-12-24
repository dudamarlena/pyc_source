# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\BuildDocs.py
# Compiled at: 2006-12-03 00:43:03
__doc__ = '\nMain distutils extensions for generating documentation\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import sys, os, copy, warnings, re, imp, rfc822, time, cStringIO
from distutils import util
from distutils.core import Command, DEBUG
from distutils.errors import *
from Ft import GetConfigVar
from Ft.Lib import Uri, ImportUtil
from Ft.Lib.DistExt import Structures
from Ft.Lib.DistExt.Formatters import *
__zipsafe__ = True

class BuildDocs(Command):
    __module__ = __name__
    command_name = 'build_docs'
    description = 'build documentation files (copy or generate XML sources)'
    user_options = [
     (
      'build-dir=', 'd', 'directory to "build" (generate) to'), ('force', 'f', 'forcibly build everything (ignore file timestamps)')]
    boolean_options = [
     'inplace', 'force']

    def initialize_options(self):
        self.build_dir = None
        self.build_lib = None
        self.force = None
        self.inplace = False
        self.validate = False
        return
        return

    def finalize_options(self):
        self.set_undefined_options('build', (
         'build_docs', 'build_dir'), (
         'build_lib', 'build_lib'), (
         'force', 'force'))
        self.files = [ doc for doc in self.distribution.doc_files if isinstance(doc, Structures.File) ]
        self.static = [ doc for doc in self.distribution.doc_files if isinstance(doc, Structures.Document) ]
        (self.modules, self.module_info) = self.get_modules()
        self.extensions = [ doc for doc in self.distribution.doc_files if isinstance(doc, Structures.ExtensionsDocument) ]
        self.scripts = [ doc for doc in self.distribution.scripts if isinstance(doc, Structures.Script) and doc.application is not None ]
        self._xslt_processor = None
        return
        return

    def get_outputs(self):
        outputs = []
        for name in self.modules:
            xmlfile = self.get_output_filename(name, 'modules')
            outputs.append(xmlfile)

        for ext in self.extensions:
            xmlfile = self.get_output_filename(ext.name, 'extensions')
            outputs.append(xmlfile)

        for script in self.scripts:
            xmlfile = self.get_output_filename(script.name, 'commandline')
            outputs.append(xmlfile)

        index_name = 'index-' + self.distribution.get_name()
        outputs.append(self.get_output_filename(index_name))
        return outputs

    def get_source_files(self):
        sources = []
        for doc in self.distribution.doc_files:
            if isinstance(doc, Structures.File):
                source = util.convert_path(doc.source)
                sources.append(source)
            elif isinstance(doc, Structures.Document):
                source = util.convert_path(doc.source)
                sources.append(source)
                prefix = len(os.getcwd()) + len(os.sep)
                for path in self.find_xml_includes(Uri.OsPathToUri(source)):
                    sources.append(path[prefix:])

        if self.inplace:
            sources.extend(self.get_outputs())
        return sources

    def find_xml_includes(self, uri, _includes=None):
        if _includes is None:
            _includes = {}

        def gather_includes(fullurl):
            if fullurl not in _includes:
                _includes[fullurl] = Uri.UriToOsPath(fullurl)
                self.find_xml_includes(fullurl, _includes)
            return

        ProcessIncludes(uri, gather_includes)
        return _includes.values()
        return

    def run(self):
        if self.modules:
            self.prepare_modules()
        documents = []
        if self.static:
            documents.extend(self.build_static())
        if self.modules:
            documents.extend(self.build_api())
        if self.extensions:
            documents.extend(self.build_extensions())
        if self.scripts:
            documents.extend(self.build_commandline())
        self.build_index(documents)
        return

    def get_modules(self):
        modules = []
        sources = {}
        if self.distribution.has_pure_modules():
            build_py = self.get_finalized_command('build_py')
            for (package, module, filename) in build_py.find_all_modules():
                if module == '__init__':
                    module = package
                    module_type = imp.PKG_DIRECTORY
                elif package:
                    module = package + '.' + module
                    module_type = imp.PY_SOURCE
                modules.append(module)
                package_dir = package.replace('.', os.sep)
                package_dir = os.path.join(build_py.build_lib, package_dir)
                filename = os.path.basename(filename)
                filename = os.path.join(package_dir, filename)
                sources[module] = (filename, module_type)

        if self.distribution.has_ext_modules():
            build_ext = self.get_finalized_command('build_ext')
            for ext in build_ext.extensions:
                module = build_ext.get_ext_fullname(ext.name)
                filename = build_ext.get_ext_filename(module)
                modules.append(module)
                filename = os.path.join(build_ext.build_lib, filename)
                sources[module] = (filename, imp.C_EXTENSION)

        return (
         modules, sources)

    def prepare_modules(self):
        if self.distribution.has_pure_modules():
            self.run_command('build_py')
        if self.distribution.has_ext_modules():
            self.run_command('build_ext')
        if self.distribution.config_module:
            from Ft.Lib.DistExt.InstallConfig import METADATA_KEYS
            if self.distribution.config_module not in sys.modules:
                module = imp.new_module(self.distribution.config_module)
                sys.modules[self.distribution.config_module] = module
            else:
                module = sys.modules[self.distribution.config_module]
            for name in METADATA_KEYS:
                value = getattr(self.distribution, 'get_' + name)()
                setattr(module, name.upper(), value)

        sys.path.insert(0, self.build_lib)
        for package in self.distribution.namespace_packages:
            packages = [
             package]
            while '.' in package:
                package = ('.').join(package.split('.')[:-1])
                packages.insert(0, package)

            for package in packages:
                path = os.path.join(self.build_lib, *package.split('.'))
                if package not in sys.modules:
                    module = sys.modules[package] = imp.new_module(package)
                    module.__path__ = [path]
                else:
                    module = sys.modules[package]
                    try:
                        search_path = module.__path__
                    except AttributeError:
                        raise DistutilsSetupError("namespace package '%s' is not a package" % package)

                    search_path.insert(0, path)

        for name in self.modules:
            if name in sys.modules:
                search_path = getattr(sys.modules[name], '__path__', None)
                if search_path is not None:
                    path = os.path.join(self.build_lib, *name.split('.'))
                    search_path.insert(0, path)

        return
        return

    def build_static(self):
        documents = []
        for document in self.static:
            document = copy.copy(document)
            document.source = util.convert_path(document.source)
            documents.append(document)

        if self.validate:
            from xml.sax.handler import feature_validation
            from Ft.Xml.InputSource import DefaultFactory
            from Ft.Xml.Sax import CreateParser

            class ErrorHandler:
                __module__ = __name__

                def __init__(self, displayhook):
                    self.displayhook = displayhook

                def warning(self, exception):
                    self.displayhook(exception)

                def error(self, exception):
                    self.displayhook(exception)

                def fatalError(self, exception):
                    raise exception

            parser = CreateParser()
            parser.setFeature(feature_validation, True)
            parser.setErrorHandler(ErrorHandler(self.warn))
            for document in documents:
                self.announce('validating %s' % document.source, 2)
                parser.parse(DefaultFactory.fromUri(document.source))

        return documents

    def build_api(self):
        formatter = ApiFormatter.ApiFormatter(self, self.module_info)
        category = 'modules'
        first = min(self.modules)
        last = max(self.modules)
        shortest = min(len(first), len(last))
        for i in xrange(shortest):
            if first[i] != last[i]:
                top_level = first[:i]
                break
        else:
            top_level = first[:shortest]

        if not top_level:
            raise DistutilsInternalError('documenting multiple top-level packages is not supported')
        warnings.filterwarnings('ignore', '', DeprecationWarning, top_level)
        documents = []
        for name in self.modules:
            try:
                module = __import__(name, {}, {}, ['*'])
            except ImportError, error:
                if DEBUG:
                    raise
                self.announce('not documenting %s (%s)' % (name, error), 3)
                continue

            sources = [
             self.module_info[name][0]]
            xmlfile = self.document(category, name, sources, module, formatter)
            if name == top_level:
                title = '%s API Reference' % self.distribution.get_name()
                documents.append(Structures.Document(xmlfile, stylesheet=category, title=title, category='general'))

        return documents

    def build_extensions(self):
        """
        Create XML documentation for XPath/XSLT extensions
        """
        formatter = ExtensionFormatter.ExtensionFormatter(self)
        category = 'extensions'
        extension_attrs = (
         'ExtNamespaces', 'ExtFunctions', 'ExtElements')
        docs = []
        for extension in self.extensions:
            extension_module = imp.new_module(extension.name)
            for attr in extension_attrs:
                setattr(extension_module, attr, {})

            sources = []
            for name in extension.modules:
                try:
                    module = __import__(name, {}, {}, extension_attrs)
                except ImportError, e:
                    raise DistutilsFileError("could not import '%s': %s" % (name, e))

                for attr in extension_attrs:
                    if hasattr(module, attr):
                        attrs = getattr(module, attr)
                        getattr(extension_module, attr).update(attrs)

                sources.append(self.module_info[name][0])

            xmlfile = self.document(category, extension.name, sources, extension_module, formatter)
            docs.append(Structures.Document(xmlfile, stylesheet=category, title=extension.title, category=category))

        return docs

    def build_commandline(self):
        formatter = CommandLineFormatter.CommandLineFormatter(self)
        category = 'commandline'
        docs = []
        for script in self.scripts:
            try:
                module = __import__(script.module, {}, {}, [script.application])
            except ImportError, e:
                raise DistutilsFileError("could not document '%s' script: %s" % (script.name, e))

            app = getattr(module, script.application)()
            sources = [
             self.module_info[script.module][0]]
            for (cmd_name, cmd) in app.get_help_doc_info():
                source = cmd._fileName
                if source is None:
                    module_name = cmd.__class__.__module__
                    source = self.module_info[module_name][0]
                sources.append(source)

            xmlfile = self.document(category, script.name, sources, app, formatter)
            title = script.name + ' - ' + app.description
            docs.append(Structures.Document(xmlfile, stylesheet=category, title=title, category=category))

        return docs
        return

    def build_index(self, documents):
        from Ft.Xml.Xslt.BuiltInExtElements import RESERVED_NAMESPACE
        name = 'index-' + self.distribution.get_name()
        xmlfile = self.get_output_filename(name)
        source_mtime = max(os.path.getmtime(self.distribution.script_name), os.path.getmtime(self.distribution.package_file), ImportUtil.GetLastModified(__name__))
        try:
            target_mtime = os.path.getmtime(xmlfile)
        except OSError:
            target_mtime = -1

        if not (self.force or source_mtime > target_mtime):
            self.announce('not creating index (up-to-date)', 1)
            return
        else:
            self.announce('creating index -> %s' % xmlfile, 2)
        index = {}
        index_uri = Uri.OsPathToUri(xmlfile)
        xmlstr = XmlFormatter.XmlRepr().escape
        for doc in documents:
            if 'noindex' not in doc.flags:
                output = os.path.splitext(doc.source)[0] + '.html'
                source_uri = Uri.OsPathToUri(doc.source)
                output_uri = Uri.OsPathToUri(output)
                category = index.setdefault(doc.category, [])
                category.append({'title': xmlstr(doc.title), 'source': Uri.Relativize(source_uri, index_uri), 'output': Uri.Relativize(output_uri, index_uri), 'stylesheet': xmlstr(doc.stylesheet)})

        sections = []
        for (title, category, sort) in (('General', 'general', False), ('Modules', 'modules', True), ('XPath/XSLT Extensions', 'extensions', False), ('Command-line Applications', 'commandline', True)):
            if category not in index:
                continue
            items = []
            L = index[category]
            if sort:
                L.sort(lambda a, b: cmp(a['title'], b['title']))
            for info in L:
                repl = {'title': info['title'], 'url': info['output']}
                items.append(INDEX_LISTITEM % repl)

            if items:
                items = ('').join(items)
                repl = {'title': xmlstr(title), 'category': xmlstr(category), 'items': items}
                sections.append(INDEX_SECTION % repl)

        sections = ('').join(sections)
        sources = []
        for category in index.values():
            for info in category:
                sources.append(INDEX_SOURCE % info)

        sources = ('').join(sources)
        repl = {'fullname': xmlstr(self.distribution.get_fullname()), 'sections': sections, 'namespace': RESERVED_NAMESPACE, 'sources': sources}
        index = INDEX_TEMPLATE % repl
        if not self.dry_run:
            f = open(xmlfile, 'wb')
            f.write(index)
            f.close()
        return documents

    def document(self, category, name, sources, object, formatter):
        xmlfile = self.get_output_filename(name, category)
        self.mkpath(os.path.dirname(xmlfile))
        formatter_module = formatter.__class__.__module__
        source_mtime = max(ImportUtil.GetLastModified(formatter_module), *map(os.path.getmtime, sources))
        try:
            target_mtime = os.path.getmtime(xmlfile)
        except OSError:
            target_mtime = -1

        if self.force or source_mtime > target_mtime:
            self.announce('documenting %s -> %s' % (name, xmlfile), 2)
            if not self.dry_run:
                try:
                    stream = open(xmlfile, 'w')
                    try:
                        formatter.format(object, stream, encoding='iso-8859-1')
                    finally:
                        stream.close()
                except (KeyboardInterrupt, SystemExit):
                    os.remove(xmlfile)
                    raise
                except Exception, exc:
                    os.remove(xmlfile)
                    if DEBUG:
                        raise
                    raise DistutilsExecError('could not document %s (%s)' % (name, exc))

        else:
            self.announce('not documenting %s (up-to-date)' % name, 1)
        return xmlfile

    def get_output_filename(self, name, category=None):
        dest_dir = self.build_dir
        if category:
            dest_dir = os.path.join(dest_dir, category)
        return os.path.join(dest_dir, name + '.xml')


def FindIncludes(source_uri, _includes=None):
    if _includes is None:
        _includes = {}

    def gather_includes(fullurl):
        if fullurl not in _includes:
            _includes[fullurl] = True
            FindIncludes(fullurl, _includes)
        return

    ProcessIncludes(source, gather_includes)
    return _includes
    return


def ProcessIncludes(source, callback, xslt=False):
    from xml.sax import make_parser, SAXException, SAXNotRecognizedException
    from xml.sax.handler import ContentHandler, feature_namespaces, feature_validation, feature_external_ges, feature_external_pes
    from xml.sax.xmlreader import InputSource

    class InclusionFilter(ContentHandler):
        __module__ = __name__
        XSLT_INCLUDES = [
         (
          'http://www.w3.org/1999/XSL/Transform', 'import'), ('http://www.w3.org/1999/XSL/Transform', 'include')]

        def startDocument(self):
            url = self._locator.getSystemId()
            self._bases = [url]
            self._scheme = Uri.GetScheme(url)
            self._elements = [('http://www.w3.org/2001/XInclude', 'include')]
            if xslt:
                self._elements.extend(self.XSLT_INCLUDES)

        def startElementNS(self, expandedName, tagName, attrs):
            xml_base = ('http://www.w3.org/XML/1998/namespace', 'base')
            baseUri = attrs.get(xml_base, self._bases[(-1)])
            self._bases.append(baseUri)
            if expandedName in self._elements:
                try:
                    href = attrs[(None, 'href')]
                except KeyError:
                    return
                else:
                    if attrs.get((None, 'parse'), 'xml') == 'text':
                        return
                    fullurl = Uri.BaseJoin(baseUri, href)
                    if Uri.GetScheme(fullurl) == self._scheme:
                        callback(fullurl)
            return

        def endElementNS(self, expandedName, tagName):
            del self._bases[-1]

    try:
        parser = make_parser()
        parser.setFeature(feature_namespaces, True)
        for feature in (feature_validation, feature_external_ges, feature_external_pes):
            try:
                parser.setFeature(feature, False)
            except SAXNotRecognizedException:
                pass

    except SAXException, e:
        raise DistutilsModuleError(e.getMessage())

    handler = InclusionFilter()
    parser.setContentHandler(handler)
    if isinstance(source, (str, unicode)):
        try:
            stream = Uri.UrlOpen(source)
        except OSError:
            return
        else:
            source = InputSource(source)
            source.setByteStream(stream)
    elif hasattr(source, 'read'):
        stream = source
        source = InputSource(getattr(stream, 'name', None))
        source.setByteStream(stream)
    parser.parse(source)
    return
    return


INDEX_TEMPLATE = '<?xml version="1.0" encoding="ISO-8859-1"?>\n<!DOCTYPE article PUBLIC "-//OASIS//DTD Simplified DocBook XML V1.1//EN"\n          "http://docbook.org/xml/simple/1.1/sdocbook.dtd">\n<?ftdb-ignore-namespace http://xmlns.4suite.org/reserved?>\n<article>\n  <title>%(fullname)s Document Index</title>\n%(sections)s\n\n  <f:sources xmlns:f="%(namespace)s">\n%(sources)s\n  </f:sources>\n\n</article>\n'
INDEX_SECTION = '\n  <section id="%(category)s">\n    <title>%(title)s</title>\n    <itemizedlist>\n%(items)s\n    </itemizedlist>\n  </section> <!-- %(category)s -->\n'
INDEX_LISTITEM = '      <listitem>\n        <ulink url="%(url)s" type="generate">%(title)s</ulink>\n      </listitem>\n'
INDEX_SOURCE = '    <f:source>\n      <f:title>%(title)s</f:title>\n      <f:src>%(source)s</f:src>\n      <f:dst>%(output)s</f:dst>\n      <f:stylesheet>%(stylesheet)s</f:stylesheet>\n    </f:source>\n'