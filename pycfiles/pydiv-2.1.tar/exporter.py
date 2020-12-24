# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/exporter.py
# Compiled at: 2016-11-27 06:27:17
__doc__ = '\nCommon exporter stuff.\n'
import os, shutil
from collections import defaultdict
import pkg_resources as pkg
from jinja2 import Environment, ChoiceLoader, PackageLoader, FileSystemLoader
from .plugin import Plugin, get_plugin, get_plugins
from .config import config, config_path, ConfigSection
from .util import make_directory, timespan
from .files import write_file
from .logger import log
from .pkginfo import __url__
from .version import __version__
from . import flags
exporters = None
archive_suffix = {'.tar': 'tar', '.tar.gz': 'gztar', 
   '.tgz': 'gztar', 
   '.tar.bz2': 'bztar', 
   '.zip': 'zip'}

def get_exporter(name):
    """Get an exporter class given its name."""
    return get_plugin(Exporter, name)


def get_exporters():
    """Yield all available exporters and their descriptions."""
    for cls in get_plugins(Exporter):
        yield (
         cls.name, cls.description)


class Exporter(Plugin):
    """
    Base class for database exporters.

    Args:
        database (DitzDB): Database object.
    """
    category = 'exporter'
    name = None
    description = 'undocumented'
    package = None
    suffix = None
    static_dir = None
    template_dir = None

    def __init__(self, database):
        self.db = database
        self.config = ConfigSection(self.name, 'export', config)
        self.templates = {}
        self.env = None
        self.paths = defaultdict(list)
        for name, dirname in (('static', self.static_dir),
         (
          'templates', self.template_dir)):
            if dirname is not None:
                for dirpath in (self.db.issuedir, config_path()):
                    path = os.path.join(dirpath, name, dirname)
                    self.paths[name].append(path)

        if self.template_dir is not None:
            paths = self.paths['templates']
            templates = os.path.join('templates', self.template_dir)
            package = self.package or __name__
            loaders = [
             FileSystemLoader(paths),
             PackageLoader(package, templates)]
            self.env = Environment(loader=ChoiceLoader(loaders), trim_blocks=True, lstrip_blocks=True)

        @self.add_filter
        def issues(item):
            attr = item.__class__.__name__.lower()
            return [ issue for issue in self.db.issues if getattr(issue, attr) == item.name
                   ]

        rmap = {rel.name:rel for rel in self.db.project.releases}
        cmap = {comp.name:comp for comp in self.db.project.components}
        relmap = self.db.relation_mapping()

        @self.add_filter
        def release(issue):
            return rmap.get(issue.release, None)

        @self.add_filter
        def component(issue):
            return cmap[issue.component]

        @self.add_filter
        def issuetype(issue):
            return flags.TYPE[issue.type]

        @self.add_filter
        def inprogress(issue):
            time = issue.progress_time
            if time > 0:
                return timespan(time)
            return ''

        @self.add_filter
        def related(issue):
            return list(sorted(relmap[issue]))

        @self.add_filter
        def dateformat(value, format='%Y-%m-%d'):
            return value.strftime(format)

        @self.add_filter
        def timeformat(value, format='%Y-%m-%d %H:%M'):
            return value.strftime(format)

        self.setup()
        return

    def export(self, dirname):
        """
        Export the issue database to the given directory.

        Args:
            dirname (str): Directory to write files into.
        """
        archive = None
        for suffix in archive_suffix:
            if dirname.endswith(suffix):
                dirname = dirname.replace(suffix, '')
                archive = archive_suffix[suffix]

        make_directory(dirname, archive)
        if self.template_dir is not None:
            for name in self.env.list_templates():
                self.templates[name] = template = self.env.get_template(name)
                log.info('loaded template from %s' % template.filename)

        self.write(dirname)
        if self.static_dir is not None:
            for path in reversed(self.paths['static']):
                if os.path.exists(path):
                    for name in os.listdir(path):
                        filename = os.path.join(path, name)
                        shutil.copy(filename, dirname)
                        log.info('copied %s to %s' % (filename, dirname))

            static = os.path.join('static', self.static_dir)
            package = self.package or __name__
            if pkg.resource_exists(package, static):
                for name in pkg.resource_listdir(package, static):
                    src = os.path.join(static, name)
                    dst = os.path.join(dirname, name)
                    if not os.path.exists(dst):
                        filename = pkg.resource_filename(package, src)
                        shutil.copy(filename, dirname)
                        log.info('copied %s to %s' % (filename, dirname))

        if archive:
            shutil.make_archive(dirname, archive, root_dir='.', base_dir=dirname, logger=log, verbose=True)
            shutil.rmtree(dirname)
        return

    def setup(self):
        """
        Do exporter-specific setup.

        By default, this does nothing.
        """
        pass

    def add_filter(self, func, name=None):
        """
        Add a custom Jinja filter.

        This returns the original function, so the method can be used as a
        decorator.

        Args:
            func (callable): Filter function.
            name (str, optional): Name to use in templates (same as
                function name, if None).

        Returns:
            func: original function
        """
        if self.env:
            self.env.filters[name or func.__name__] = func
        return func

    def write(self, dirname):
        """
        Write exported files to the given directory.

        This method must be overridden.  If using templates, it should call
        the :func:`render` method.

        Args:
            dirname (str): Directory to write files into.
        """
        raise NotImplementedError

    def render(self, dirname, templatefile, targetfile=None, **kw):
        """
        Render a single file from a template.

        Args:
            dirname (str): Directory to write file into.
            templatefile (str): Jinja template to use.
            targetfile (str, optional): Filename to write (same as
                 *templatefile*, if None).
            kw (dict): Template parameters.
        """
        template = self.templates[templatefile]
        kw.update(version=__version__, url=__url__)
        text = template.render(**kw)
        path = os.path.join(dirname, targetfile or templatefile)
        write_file(path, text)
        log.info("wrote '%s'", path)

    def export_filename(self, item):
        """
        Return a unique export filename for a Ditz item.

        The filename is based on the item's ID (if it's an issue) or its
        name.  Each filename has the exporter suffix appended to it.

        Args:
            item (DitzObject): Ditz item.

        Return:
            Filename string.
        """
        clsname = item.__class__.__name__.lower()
        name = getattr(item, 'id', None) or getattr(item, 'name')
        return '%s-%s.%s' % (clsname, name, self.suffix)