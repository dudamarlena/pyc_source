# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/library.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
import weakref
from random import choice
import logging, re
from fs.errors import FSError
from fs.opener import open_fs
from fs import walk
from fs import wrap
from collections import defaultdict
from . import errors
from .parser import Parser
from . import xmlreport
from .settings import SettingContainer, SettingsContainer, SettingsSectionContainer
from .importer import fs_import
from .elements import ElementBase
from . import pyversion
from .tools import textual_list, split_commas
from . import translations
from .versioning import Version, VersionSpec
from .compat import iteritems, implements_to_string, string_types, text_type, xrange, PY2
from .context import Context
log = logging.getLogger(b'moya')
startup_log = logging.getLogger(b'moya.startup')
tests_log = logging.getLogger(b'moya.tests')

def _make_id():
    """A random token to make default libnames unique"""
    _ID_CHARS = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return (b'').join(choice(_ID_CHARS) for _ in xrange(6))


class FailedDocument(object):

    def __init__(self, path, code, line, col, msg, diagnosis=None):
        self.path = path
        self.code = code
        self.line = line
        self.col = col
        self.msg = msg
        self.diagnosis = diagnosis
        super(FailedDocument, self).__init__()

    def __repr__(self):
        return (b"<faileddocument '{}', line {} ({})>").format(self.path, self.line, self.msg)

    def render(self):
        error = xmlreport.render_error(self.code, self.line, col=None, col_text=b'here')
        return b'[Error parsing %s]\n%s:\n\n%s\n' % (self.path, self.msg, error)


@implements_to_string
class Library(object):
    """A collection of documents"""

    def __init__(self, archive, fs=None, settings_path=None, long_name=None, namespace=None, rebuild=False):
        self._archive = weakref.ref(archive)
        self.documents = []
        self.elements_by_name = {}
        self.elements_by_type = defaultdict(list)
        self.long_name = long_name
        self.no_py = rebuild
        self.namespace = namespace
        self.settings = SettingsSectionContainer()
        self.system_settings = {}
        self.templates_info = {}
        self.data_info = {}
        self.data_fs = None
        self.media = {}
        self.author = {}
        self.libinfo = {}
        self.version = None
        self.load_fs = None
        self.loaded_ini = None
        self.failed_documents = []
        self._libnames = defaultdict(int)
        self.replace_nodes = defaultdict(list)
        self.py = {}
        self.filters = {}
        self.loaded = False
        self.imported_documents = False
        self.documentation_location = None
        self.translations_location = None
        self.default_language = b'en'
        self.languages = []
        self.translations = translations.Translations()
        self.priority = 0
        self.template_priority = 0
        self.data_priority = None
        self.built = False
        self.finalized = False
        self.imported_tests = False
        self._cfg = None
        if fs:
            self.load(fs, settings_path=settings_path)
        return

    @property
    def archive(self):
        return self._archive()

    @property
    def enum(self):
        return self.archive.get_lib_enums(self.long_name)

    @property
    def install_location(self):
        try:
            return self.load_fs.getsyspath(b'/')
        except FSError:
            return

        return

    @property
    def cfg(self):
        return self._cfg

    @property
    def version_spec(self):
        """Get a version spec for precisely this version"""
        return VersionSpec((b'{}=={}').format(self.long_name, self.version))

    @property
    def version_name(self):
        return (b'{} {}').format(self.long_name, self.version)

    def __str__(self):
        return (b'<library {}>').format(self.long_name)

    def __repr__(self):
        return (b'<library {}>').format(self.long_name)

    def add_replacement_node(self, element):
        self.replace_nodes[element.libname].append(element)

    def get_element(self, element_ref, app=None):
        return self.archive.get_element(element_ref, app=app, lib=self.lib)

    def allocate_libname(self, docid):
        """Allocates a name, unique to the library"""
        new_libname = docid
        while new_libname in self.elements_by_name:
            new_libname = (b'{}.{}').format(docid, _make_id())

        return new_libname
        if docid not in self.elements_by_name:
            return docid

    def qualify_libname(self, libname):
        """Qualifies the libname to identify the container library (if it isn't already qualified)"""
        if b'#' not in libname:
            return b'%s#%s' % (self.long_name, libname)
        else:
            if libname.startswith(b'#'):
                return self.long_name + libname
            return libname

    def import_document(self, fs, path):
        """Import a single document"""
        return self.import_documents(fs, files=(path,))

    def import_documents(self, fs, wildcard=b'*.xml', recurse=False, files=None):
        """Imports a number of documents in to the library"""
        if isinstance(fs, string_types):
            fs = open_fs(fs)
        if files is None:
            if recurse:
                files = sorted(fs.walk.files(filter=[wildcard]))
            else:
                files = sorted(info.name for info in fs.filterdir(files=[
                 wildcard], exclude_dirs=[
                 b'*']))
        else:
            files = sorted(files)
        import_count = 0
        for filepath in files:
            parser = Parser(self.archive, fs, filepath, library=self)
            try:
                document = parser.parse()
                if document is not None:
                    self.documents.append(document)
                    import_count += 1
            except errors.ParseError as parse_error:
                line, col = parse_error.position
                if fs.hassyspath(filepath):
                    path = fs.getsyspath(filepath)
                else:
                    path = fs.desc(filepath)
                failed_doc = FailedDocument(path=path, code=parser.xml, line=line, col=col, msg=text_type(parse_error))
                self.failed_documents.append(failed_doc)
            except (errors.ElementError, errors.UnknownElementError) as element_error:
                line = element_error.source_line
                col = 0
                if fs.hassyspath(filepath):
                    path = fs.getsyspath(filepath)
                else:
                    path = fs.desc(filepath)
                failed_doc = FailedDocument(path=path, code=parser.xml, line=line, col=col, msg=text_type(element_error))
                self.failed_documents.append(failed_doc)

        return import_count

    def finalize(self, ignore_errors=False):
        if self.finalized:
            return
        context = Context({b'_ignore_finalize_errors': ignore_errors})
        context.root[b'_lib_long_name'] = self.long_name
        context.root[b'lib'] = self
        for doc in self.documents:
            doc.document_finalize(context)

        for doc in self.documents:
            doc.lib_finalize(context)

        self.built = True
        self.finalized = True
        for doc in self.documents:
            del doc.structure

    def on_archive_finalize(self):
        for libname, elements in iteritems(self.replace_nodes):
            winner = sorted(elements, key=lambda e: e.lib.priority)[(-1)]
            existing = self.get_named_element(libname)
            if existing and existing.lib.priority < winner.lib.priority:
                existing.replace(winner)
                self.elements_by_name[existing.libname] = winner
                element_type = (existing.xmlns, existing._tag_name)
                by_type = self.elements_by_type[element_type]
                by_type[by_type.index(existing)] = winner

        self.replace_nodes.clear()

    def load(self, fs, settings_path=None):
        self.loaded = True
        self.load_fs = fs
        self.loaded_ini = fs.desc(b'lib.ini')
        try:
            self._cfg = cfg = SettingsContainer.read(fs, b'lib.ini')
        except FSError as e:
            raise errors.LibraryLoadError(b'failed to load lib.ini from "{path}" ({exc})', path=fs.desc(b'lib.ini'), exc=e, lib=self)

        def cfgget(section, key, bool=False, default=Ellipsis):
            try:
                if bool:
                    value = cfg[section][key].strip().lower() in ('yes', 'true')
                else:
                    value = cfg[section][key]
            except KeyError:
                if default is Ellipsis:
                    raise errors.LibraryLoadError((b'required key [{}]/{} not found in lib.ini').format(section, key), lib=self)
                return default

            return value

        self.long_name = cfgget(b'lib', b'name')
        if self.long_name in self.archive.libs:
            raise errors.LibraryLoadError((b"already loaded this library from '{}'").format(self.loaded_ini), lib=self, diagnosis=b'Check for a previous <import> that loads this library')
        py_requires = cfgget(b'lib', b'pyrequires', default=None)
        if py_requires:
            try:
                version_ok = pyversion.check(py_requires)
            except ValueError as e:
                raise errors.LibraryLoadError((b'bad Py version specification in [lib]/pyrequires ({})').format(text_type(e)), lib=self)

            if not version_ok:
                versions = (b', ').join((b'Python {}.{}').format(*v) for v in pyversion.list_compatible(py_requires))
                raise errors.LibraryLoadError(b'one of the following Python versions required: {versions}', lib=self.long_name, versions=versions)
        self.title = cfgget(b'lib', b'title', default=None)
        self.url = cfgget(b'lib', b'url', default=None)
        try:
            self.version = Version(cfgget(b'lib', b'version'))
        except ValueError as e:
            raise errors.LibraryLoadError(text_type(e), lib=self.long_name)

        self.namespace = cfgget(b'lib', b'namespace')
        self.docs_location = cfgget(b'lib', b'location', default=None)
        self.tests_location = cfgget(b'tests', b'location', default=None)
        self.system_settings = {b'templates_directory': self.long_name or b'', b'data_directory': self.long_name or b''}
        project_cfg = self.archive.cfg
        settings = SettingsSectionContainer()

        def update_settings(section):
            settings.update((k, SettingContainer(v)) for k, v in iteritems(cfg[section]))

        if b'author' in cfg:
            self.author.update(cfg[b'author'])
        if b'lib' in cfg:
            self.libinfo.update(cfg[b'lib'])
        if b'settings' in cfg:
            update_settings(b'settings')
        if b'templates' in cfg:
            self.templates_info = cfg[b'templates']
        if b'data' in cfg:
            self.data_info = cfg[b'data']
            location = cfgget(b'data', b'location')
            try:
                self.data_fs = fs.opendir(location)
            except FSError as e:
                raise errors.LibraryLoadError(b'Unable to read data from {path} ({exc})', path=location, exc=e, lib=self)

        if b'documentation' in cfg:
            self.documentation_location = cfg[b'documentation'].get(b'location', b'./docs')
        if b'translations' in cfg:
            i18n = cfg[b'translations']
            self.translations_location = i18n.get(b'location', b'./translations')
            self.default_language = i18n.get(b'default_language', b'en')
            self.languages = split_commas(i18n.get(b'languages', b'en'))
            self._localedir = self.load_fs.getsyspath(self.translations_location)
            if self.languages:
                startup_log.debug(b'%s reading translations %s', self, textual_list(self.languages, b'and'))
                self.translations.read(b'messages', self._localedir, self.languages)
        if project_cfg and b'lib:' + self.long_name in project_cfg:
            update_settings(b'lib:' + self.long_name)
        self.settings = settings
        for section_name, section in iteritems(cfg):
            if b':' in section_name:
                what, name = section_name.split(b':', 1)
            else:
                continue
            if what.startswith(b'py'):
                if self.no_py:
                    continue
                try:
                    version_ok = pyversion.check(what)
                except ValueError as e:
                    raise errors.LibraryLoadError((b'Bad Py version specification ({})').format(text_type(e)), lib=self)

                if version_ok:
                    location = cfgget(section_name, b'location')
                    py_fs = fs.opendir(location)
                    try:
                        fs_import(self, py_fs, name or self.long_name)
                    except errors.StartupFailedError as e:
                        raise errors.LibraryLoadError(text_type(e), exc=e, lib=self)
                    except Exception as e:
                        raise
                        raise errors.LibraryLoadError(b'Error in Python extension', py_exception=e, lib=self)

            elif what == b'media':
                location = cfgget(section_name, b'location')
                try:
                    media_fs = fs.opendir(location)
                except FSError as e:
                    raise errors.LibraryLoadError(b'Unable to read media from {path} ({exc})', path=location, exc=e, lib=self)

                if media_fs.hassyspath(b'/'):
                    self.media[name] = open_fs(media_fs.getsyspath(b'/'))
                else:
                    self.media[name] = media_fs

        if self.docs_location:
            with self.load_fs.opendir(self.docs_location) as (docs_fs):
                self.import_documents(docs_fs, recurse=True)
        return

    def load_tests(self):
        if not self.tests_location:
            return False
        tests_log.info((b'{} importing tests').format(self))
        self.built = False
        self.finalized = False
        if not self.imported_tests and self.tests_location:
            with self.load_fs.opendir(self.tests_location) as (tests_fs):
                self.import_documents(tests_fs, recurse=True)
        self.imported_tests = True
        return True

    def register_element(self, element):
        """Called by parser to register an element"""
        element_type = (
         element.xmlns, element._tag_name)
        self.elements_by_type[element_type].append(element)

    def unregister_element(self, element):
        element_type = (
         element.xmlns, element._tag_name)
        self.elements_by_type[element_type].remove(element)

    def register_named_element(self, name, element, priority=0):
        """Called by parser to register a named element"""
        self.elements_by_name[name] = element
        self.register_element(element)

    def register_filter(self, name, _filter):
        self.filters[name] = _filter

    def get_named_element(self, name, default=None):
        """Get an element with the given name, or return a default"""
        return self.elements_by_name.get(name, default)

    def get_elements_by_type(self, element_type):
        """Get all elements of a given type"""
        if not isinstance(element_type, tuple):
            element_type = (
             ElementBase.xmlns, element_type)
        return self.elements_by_type[element_type]

    def get_element_by_type_and_attribute(self, element_type, attrib, value):
        """Get the first element of a given type containing a given attribute"""
        for element in self.get_elements_by_type(element_type):
            if hasattr(element, attrib) and getattr(element, attrib) == value:
                return element

        raise errors.ElementNotFoundError(b'%s %s=%s' % (element_type, attrib, value))

    _whitespace_padding_sub = re.compile(b'^\\s*(.*?)\\s*$').sub
    if PY2:

        def translate(self, context, text):
            return self._whitespace_padding_sub(lambda m: self.translations.get(context[b'.languages']).ugettext(m.group(0)), text, 1)

    else:

        def translate(self, context, text):
            return self._whitespace_padding_sub(lambda m: self.translations.get(context[b'.languages']).gettext(m.group(0)), text, 1)