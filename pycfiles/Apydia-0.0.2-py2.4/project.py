# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/project.py
# Compiled at: 2007-12-05 07:06:46
"""
    Project
    =======
    
    The ``Project``-class represents the whole API-documentation project.
    It loads themes and parsers, invokes a ``Generator``-object to render
    all HTML and runs plugins and hooks.
"""
import sys, warnings, logging
from os.path import abspath, join
from operator import attrgetter
from datetime import datetime
from pkg_resources import iter_entry_points, DistributionNotFound
from genshi import Markup, HTML
from apydia.generator import Generator
from apydia.descriptors import create_desc, ModuleDesc
from apydia import helpers
from apydia.theme import Theme
import apydia.release
log = logging.getLogger(__name__)
DEFAULT_DOCFORMAT = 'reStructuredText'

class Project(object):
    """
        The documentation ``Project`` class.
    """
    __module__ = __name__
    apydia_version = apydia.release.version

    def __init__(self, options):
        self.options = options
        self.modules = set()
        self.name = options.title
        module_names = options.modules
        self.theme = Theme.load(options.theme)
        self._parsers = dict()
        self._loaded_parsers = dict()
        if options.trac_browser_url:
            options.trac_browser_url = options.trac_browser_url.rstrip('/')
        for entrypoint in iter_entry_points('apydia.docrenderers'):
            try:
                self._parsers[entrypoint.name.lower()] = entrypoint
            except DistributionNotFound, msg:
                warnings.warn('DistributionNotFound: %s' % msg)

        module_names = sorted(filter(None, module_names))
        for module_name in module_names:
            __import__(module_name)

        for module_name in module_names:
            desc = create_desc(sys.modules[module_name])
            self.modules.add(desc)
            for module in desc.module_tree():
                if helpers.is_included(module.pathname, self.options):
                    self.modules.add(module)

        self.modules = filter(None, sorted(list(self.modules), key=attrgetter('pathname')))
        return

    @property
    def startpage(self):
        """ Try to find the root module's page and return it. """
        module = self.modules[0]
        while module.parent:
            module = module.parent

        return abspath(join(self.options.destination, module.href))

    def generate(self):
        """
            Create a ``Generator``-object and make it create all requested
            pages for each module recursively.
        """
        generator = Generator(self)
        generator.create_dirs()
        for module in self.modules:
            generator.generate(module)

        log.debug('running post-project hooks')
        generator.copy_resources()
        generator.generate_resources()

    @property
    def date(self):
        """ Just the current date and time. """
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def _get_parser(self, name):
        if name not in self._loaded_parsers:
            if name not in self._parsers:
                log.warn('%s not in %r', name, self._parsers.keys())
            parser_class = self._parsers[name].load()
            self._loaded_parsers[name] = parser_class()
        return self._loaded_parsers[name]

    def parser(self, desc):
        """
            Returns the docstring-parser for the descriptor
            given in ``desc``.
        """
        docformat = desc.docformat
        if not docformat:
            docformat = self.options.docformat or DEFAULT_DOCFORMAT
        return self._get_parser(docformat.lower())

    def render_description(self, desc):
        """
            Returns the rendered docstring for the descriptor given in
            ``desc`` as a Genshi-HTML-object.
        """
        return HTML(self.parser(desc).render_description(desc))

    def render_short_desc(self, desc):
        """
            Returns the first paragraph from a rendered docstring for the
            descriptor given in ``desc`` as a Genshi-HTML-object.
        """
        return HTML(self.parser(desc).render_short_desc(desc))

    def render_title(self, desc):
        """
            Returns the title (``<h1>`` or ``<h2>``) of a rendered docstring
            for the descriptor given in ``desc`` as a Genshi-HTML-object.
        """
        return Markup(self.parser(desc).render_title(desc))

    def renderer_id(self, desc):
        """
            The ``Parser``'s id for the descriptor given
            in ``desc``.
        """
        return self.parser(desc).parser_id

    def open_in_browser(self):
        """
            Open the generated root module's page in the system's default
            Webbrowser.
        """
        import webbrowser
        from urllib import pathname2url
        webbrowser.open(pathname2url(self.startpage))