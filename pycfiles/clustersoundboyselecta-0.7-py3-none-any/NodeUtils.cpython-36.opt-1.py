# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/NodeUtils.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 25226 bytes
__doc__ = '\nCluster nodes utility module\n\nThe NodeUtils module is a ClusterShell helper module that provides\nsupplementary services to manage nodes in a cluster. It is primarily\ndesigned to enhance the NodeSet module providing some binding support\nto external node groups sources in separate namespaces (example of\ngroup sources are: files, jobs scheduler, custom scripts, etc.).\n'
try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError

import errno
from functools import wraps
import glob, logging, os, shlex, time
from string import Template
from subprocess import Popen, PIPE
try:
    basestring
except NameError:
    basestring = str

LOGGER = logging.getLogger(__name__)

class GroupSourceError(Exception):
    """GroupSourceError"""

    def __init__(self, message, group_source):
        Exception.__init__(self, message)
        self.group_source = group_source


class GroupSourceNoUpcall(GroupSourceError):
    """GroupSourceNoUpcall"""
    pass


class GroupSourceQueryFailed(GroupSourceError):
    """GroupSourceQueryFailed"""
    pass


class GroupResolverError(Exception):
    """GroupResolverError"""
    pass


class GroupResolverSourceError(GroupResolverError):
    """GroupResolverSourceError"""
    pass


class GroupResolverIllegalCharError(GroupResolverError):
    """GroupResolverIllegalCharError"""
    pass


class GroupResolverConfigError(GroupResolverError):
    """GroupResolverConfigError"""
    pass


_DEFAULT_CACHE_TIME = 3600

class GroupSource(object):
    """GroupSource"""

    def __init__(self, name, groups=None, allgroups=None):
        """Initialize GroupSource

        :param name: group source name
        :param groups: group to nodes dict
        :param allgroups: optional _all groups_ result (string)
        """
        self.name = name
        self.groups = groups or {}
        self.allgroups = allgroups
        self.has_reverse = False

    def resolv_map(self, group):
        """Get nodes from group `group`"""
        return self.groups.get(group, '')

    def resolv_list(self):
        """Return a list of all group names for this group source"""
        return list(self.groups)

    def resolv_all(self):
        """Return the content of all groups as defined by this GroupSource"""
        if self.allgroups is None:
            raise GroupSourceNoUpcall('All groups info not available', self)
        return self.allgroups

    def resolv_reverse(self, node):
        """
        Return the group name matching the provided node.
        """
        raise GroupSourceNoUpcall('Not implemented', self)


class FileGroupSource(GroupSource):
    """FileGroupSource"""

    def __init__(self, name, loader):
        """
        Initialize FileGroupSource object.

        :param name: group source name (eg. key name of yaml root dict)
        :param loader: associated content loader (eg. YAMLGroupLoader object)
        """
        self.name = name
        self.loader = loader
        self.has_reverse = False

    @property
    def groups(self):
        """groups property (dict)"""
        return self.loader.groups(self.name)

    @property
    def allgroups(self):
        """allgroups property (string)"""
        return self.groups.get('all')


class UpcallGroupSource(GroupSource):
    """UpcallGroupSource"""

    def __init__(self, name, map_upcall, all_upcall=None, list_upcall=None, reverse_upcall=None, cfgdir=None, cache_time=None):
        GroupSource.__init__(self, name)
        self.verbosity = 0
        self.cfgdir = cfgdir
        self.logger = logging.getLogger(__name__)
        self.upcalls = {}
        self.upcalls['map'] = map_upcall
        if all_upcall:
            self.upcalls['all'] = all_upcall
        else:
            if list_upcall:
                self.upcalls['list'] = list_upcall
            if reverse_upcall:
                self.upcalls['reverse'] = reverse_upcall
                self.has_reverse = True
            if cache_time is None:
                self.cache_time = _DEFAULT_CACHE_TIME
            else:
                self.cache_time = cache_time
        self._cache = {}
        self.clear_cache()

    def clear_cache(self):
        """
        Remove all previously cached upcall results whatever their lifetime is.
        """
        self._cache = {'map':{},  'reverse':{}}

    def _upcall_read(self, cmdtpl, args=dict()):
        """
        Invoke the specified upcall command, raise an Exception if
        something goes wrong and return the command output otherwise.
        """
        cmdline = Template(self.upcalls[cmdtpl]).safe_substitute(args)
        self.logger.debug("EXEC '%s'", cmdline)
        proc = Popen(cmdline, stdout=PIPE, shell=True, cwd=(self.cfgdir), universal_newlines=True)
        output = proc.communicate()[0].strip()
        self.logger.debug("READ '%s'", output)
        if proc.returncode != 0:
            self.logger.debug("ERROR '%s' returned %d", cmdline, proc.returncode)
            raise GroupSourceQueryFailed(cmdline, self)
        return output

    def _upcall_cache(self, upcall, cache, key, **args):
        """
        Look for `key' in provided `cache'. If not found, call the
        corresponding `upcall'.

        If `key' is missing, it is added to provided `cache'. Each entry in a
        cache is kept only for a limited time equal to self.cache_time .
        """
        if not self.upcalls.get(upcall):
            raise GroupSourceNoUpcall(upcall, self)
        else:
            if key in cache:
                if cache[key][1] < time.time():
                    self.logger.debug("PURGE EXPIRED (%d)'%s'", cache[key][1], key)
                    del cache[key]
            if key not in cache:
                cache_expiry = time.time() + self.cache_time
                args['CFGDIR'] = self.cfgdir
                args['SOURCE'] = self.name
                cache[key] = (self._upcall_read(upcall, args), cache_expiry)
        return cache[key][0]

    def resolv_map(self, group):
        """
        Get nodes from group 'group', using the cached value if
        available.
        """
        return self._upcall_cache('map', (self._cache['map']), group, GROUP=group)

    def resolv_list(self):
        """
        Return a list of all group names for this group source, using
        the cached value if available.
        """
        return self._upcall_cache('list', self._cache, 'list')

    def resolv_all(self):
        """
        Return the content of special group ALL, using the cached value
        if available.
        """
        return self._upcall_cache('all', self._cache, 'all')

    def resolv_reverse(self, node):
        """
        Return the group name matching the provided node, using the
        cached value if available.
        """
        node_str = str(node)
        return self._upcall_cache('reverse', (self._cache['reverse']), node_str, NODE=node_str)


class YAMLGroupLoader(object):
    """YAMLGroupLoader"""

    def __init__(self, filename, cache_time=None):
        """
        Initialize YAMLGroupLoader and load file.

        :param filename: YAML file path
        :param cache_time: cache time (seconds)
        """
        if cache_time is None:
            self.cache_time = _DEFAULT_CACHE_TIME
        else:
            self.cache_time = cache_time
        self.cache_expiry = 0
        self.filename = filename
        self.sources = {}
        self._groups = {}
        self._load()

    def _load(self):
        """Load or reload YAML group file to create GroupSource objects."""
        with open(self.filename) as (yamlfile):
            try:
                import yaml
                sources = yaml.safe_load(yamlfile)
            except ImportError as exc:
                msg = 'Disable autodir or install PyYAML!'
                raise GroupResolverConfigError('%s (%s)' % (str(exc), msg))
            except yaml.YAMLError as exc:
                raise GroupResolverConfigError('%s: %s' % (self.filename, exc))

        if not isinstance(sources, dict):
            fmt = '%s: invalid content (base is not a dict)'
            raise GroupResolverConfigError(fmt % self.filename)
        first = not self.sources
        for srcname, groups in sources.items():
            if not isinstance(srcname, basestring):
                fmt = '%s: group source %s not a string (add quotes?)'
                raise GroupResolverConfigError(fmt % (self.filename, srcname))
            if not isinstance(groups, dict):
                fmt = "%s: invalid content (group source '%s' is not a dict)"
                raise GroupResolverConfigError(fmt % (self.filename, srcname))
            for grp in groups:
                if not isinstance(grp, basestring):
                    fmt = '%s: %s: group name %s not a string (add quotes?)'
                    raise GroupResolverConfigError(fmt % (self.filename,
                     srcname, grp))

            if first:
                self._groups[srcname] = groups
                self.sources[srcname] = FileGroupSource(srcname, self)
            else:
                if srcname in self.sources:
                    self._groups[srcname] = groups

        self.cache_expiry = time.time() + self.cache_time

    def __iter__(self):
        """Iterate over GroupSource objects."""
        return iter(self.sources.values())

    def groups(self, sourcename):
        """
        Groups dict accessor for sourcename.

        This method is called by associated FileGroupSource objects and simply
        returns dict content, after reloading file if cache_time has expired.
        """
        if self.cache_expiry < time.time():
            self._load()
        return self._groups[sourcename]


class GroupResolver(object):
    """GroupResolver"""

    def __init__(self, default_source=None, illegal_chars=None):
        """Lazy initialization of a new GroupResolver object."""
        self._sources = {}
        self._default_source = default_source
        self._initialized = False
        self.illegal_chars = illegal_chars or set()

    def _late_init(self):
        """Override method to initialize object just before it is needed."""
        if self._default_source:
            self._sources[self._default_source.name] = self._default_source
        self._initialized = True

    def init(func):

        @wraps(func)
        def wrapper(self, *args):
            if not self._initialized:
                self._late_init()
            return func(self, *args)

        return wrapper

    @init
    def set_verbosity(self, value):
        """Set debugging verbosity value (DEPRECATED: use logging.DEBUG)."""
        for source in self._sources.values():
            source.verbosity = value

    @init
    def add_source(self, group_source):
        """Add a GroupSource to this resolver."""
        if group_source.name in self._sources:
            raise ValueError("GroupSource '%s': name collision" % group_source.name)
        self._sources[group_source.name] = group_source

    @init
    def sources(self):
        """Get the list of all resolver source names. """
        srcs = list(self._sources)
        if srcs:
            if srcs[0] is not self._default_source:
                srcs.remove(self._default_source.name)
                srcs.insert(0, self._default_source.name)
        return srcs

    @init
    def _get_default_source_name(self):
        """Get default source name of resolver."""
        if self._default_source is None:
            return
        else:
            return self._default_source.name

    @init
    def _set_default_source_name(self, sourcename):
        """Set default source of resolver (by name)."""
        try:
            self._default_source = self._sources[sourcename]
        except KeyError:
            raise GroupResolverSourceError(sourcename)

    default_source_name = property(_get_default_source_name, _set_default_source_name)

    def _list_nodes(self, source, what, *args):
        """Helper method that returns a list of results (nodes) when
        the source is defined."""
        result = []
        assert source
        raw = (getattr(source, 'resolv_%s' % what))(*args)
        for line in raw.splitlines():
            [result.append(x) for x in line.strip().split()]

        return result

    def _list_groups(self, source, what, *args):
        """Helper method that returns a list of results (groups) when
        the source is defined."""
        result = []
        assert source
        raw = (getattr(source, 'resolv_%s' % what))(*args)
        try:
            grpiter = raw.splitlines()
        except AttributeError:
            grpiter = raw

        for line in grpiter:
            for grpstr in line.strip().split():
                if self.illegal_chars.intersection(grpstr):
                    errmsg = ' '.join(self.illegal_chars.intersection(grpstr))
                    raise GroupResolverIllegalCharError(errmsg)
                result.append(grpstr)

        return result

    @init
    def _source(self, namespace):
        """Helper method that returns the source by namespace name."""
        if not namespace:
            source = self._default_source
        else:
            source = self._sources.get(namespace)
        if not source:
            raise GroupResolverSourceError(namespace or '<default>')
        return source

    def group_nodes(self, group, namespace=None):
        """
        Find nodes for specified group name and optional namespace.
        """
        source = self._source(namespace)
        return self._list_nodes(source, 'map', group)

    def all_nodes(self, namespace=None):
        """
        Find all nodes. You may specify an optional namespace.
        """
        source = self._source(namespace)
        return self._list_nodes(source, 'all')

    def grouplist(self, namespace=None):
        """
        Get full group list. You may specify an optional
        namespace.
        """
        source = self._source(namespace)
        return self._list_groups(source, 'list')

    def has_node_groups(self, namespace=None):
        """
        Return whether finding group list for a specified node is
        supported by the resolver (in optional namespace).
        """
        try:
            return self._source(namespace).has_reverse
        except GroupResolverSourceError:
            return False

    def node_groups(self, node, namespace=None):
        """
        Find group list for specified node and optional namespace.
        """
        source = self._source(namespace)
        return self._list_groups(source, 'reverse', node)


class GroupResolverConfig(GroupResolver):
    """GroupResolverConfig"""
    SECTION_MAIN = 'Main'

    def __init__(self, filenames, illegal_chars=None):
        """
        Lazy init GroupResolverConfig object from filenames.
        """
        GroupResolver.__init__(self, illegal_chars=illegal_chars)
        self.filenames = filenames
        self.config = None

    def _late_init(self):
        """
        Initialize object when needed. Only the first accessible config
        filename is loaded.
        """
        GroupResolver._late_init(self)
        self.config = ConfigParser()
        parsed = self.config.read(self.filenames)
        if parsed:
            self._parse_config(os.path.dirname(parsed[(-1)]))

    def _parse_config(self, cfg_dirname):
        """parse config using relative dir cfg_dirname"""
        try:
            if self.config.has_option(self.SECTION_MAIN, 'groupsdir'):
                opt_confdir = 'groupsdir'
            else:
                opt_confdir = 'confdir'
            loaded_confdirs = set()
            confdirstr = self.config.get(self.SECTION_MAIN, opt_confdir)
            for confdir in shlex.split(confdirstr):
                confdir = Template(confdir).safe_substitute(CFGDIR=cfg_dirname)
                confdir = os.path.normpath(confdir)
                if confdir in loaded_confdirs:
                    pass
                else:
                    loaded_confdirs.add(confdir)
                    if not os.path.isdir(confdir):
                        if not os.path.exists(confdir):
                            pass
                        else:
                            raise GroupResolverConfigError('Defined confdir %s is not a directory' % confdir)
                    for groupsfn in sorted(glob.glob('%s/*.conf' % confdir)):
                        grpcfg = ConfigParser()
                        grpcfg.read(groupsfn)
                        self._sources_from_cfg(grpcfg, confdir)

        except (NoSectionError, NoOptionError):
            pass

        try:
            loaded_autodirs = set()
            autodirstr = self.config.get(self.SECTION_MAIN, 'autodir')
            for autodir in shlex.split(autodirstr):
                autodir = Template(autodir).safe_substitute(CFGDIR=cfg_dirname)
                autodir = os.path.normpath(autodir)
                if autodir in loaded_autodirs:
                    continue
                loaded_autodirs.add(autodir)
                if not os.path.isdir(autodir):
                    if not os.path.exists(autodir):
                        pass
                    else:
                        raise GroupResolverConfigError('Defined autodir %s is not a directory' % autodir)
                for autosfn in sorted(glob.glob('%s/*.yaml' % autodir)):
                    try:
                        self._sources_from_yaml(autosfn)
                    except IOError as exc:
                        if exc.errno in (errno.EACCES, errno.EPERM):
                            LOGGER.debug(exc)
                            continue

        except (NoSectionError, NoOptionError):
            pass

        self._sources_from_cfg(self.config, cfg_dirname)
        try:
            def_sourcename = self.config.get('Main', 'default')
            self.default_source_name = def_sourcename
        except (NoSectionError, NoOptionError):
            pass
        except GroupResolverSourceError:
            if def_sourcename:
                fmt = 'Default group source not found: "%s"'
                raise GroupResolverConfigError(fmt % self.config.get('Main', 'default'))

        if not self.default_source_name:
            if self._sources:
                self.default_source_name = list(self._sources)[0]

    def _sources_from_cfg(self, cfg, cfgdir):
        """
        Instantiate as many UpcallGroupSources needed from cfg object,
        cfgdir (CWD for callbacks) and cfg filename.
        """
        try:
            for section in cfg.sections():
                for srcname in section.split(','):
                    if srcname != self.SECTION_MAIN:
                        map_upcall = cfg.get(section, 'map', raw=True)
                        all_upcall = list_upcall = reverse_upcall = ctime = None
                        if cfg.has_option(section, 'all'):
                            all_upcall = cfg.get(section, 'all', raw=True)
                        if cfg.has_option(section, 'list'):
                            list_upcall = cfg.get(section, 'list', raw=True)
                        if cfg.has_option(section, 'reverse'):
                            reverse_upcall = cfg.get(section, 'reverse', raw=True)
                        if cfg.has_option(section, 'cache_time'):
                            ctime = float(cfg.get(section, 'cache_time', raw=True))
                        self.add_source(UpcallGroupSource(srcname, map_upcall, all_upcall, list_upcall, reverse_upcall, cfgdir, ctime))

        except (NoSectionError, NoOptionError, ValueError) as exc:
            raise GroupResolverConfigError(str(exc))

    def _sources_from_yaml(self, filepath):
        """Load source(s) from YAML file."""
        for source in YAMLGroupLoader(filepath):
            self.add_source(source)