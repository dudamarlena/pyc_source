# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/transmute/bootstrap.py
# Compiled at: 2014-02-20 19:09:05
__doc__ = "Bootstrap installation of transmute package.\n\nWhen imported (or directly executed), this module will make the latest transmute\npackage available, downloading it from PyPI as needed. Dowloaded packages are\nstored in a local cache and will be reused in subsequent runs.\n\nThis can also be used to bootstrap applications that use the transmute package.\nIn this case, the module becomes the application's main executable. A couple of\ncustomization points are provided to support this use case with minimal effort:\n\n    requirements: global variable listing packages to be fetched from PyPI.\n    main(): placeholder for application specific logic. If the module is\n        executed as __main__ script, this gets called after packages in\n        requirements have been updated and added to sys.path.\n\nAdditionally, bootstrap_starting(), bootstrap_succeeded() and bootstrap_failed()\nare called at specific points in the bootstrapping process.\n\nThe following example could be used to load latest 'foobar' from PyPI and invoke\nthe foobar.cli.main() entry point:\n\n    requirements = [ 'foobar' ]\n    def main():\n        import foobar.cli\n        return foobar.cli.main()\n\n"
requirements = [
 'transmute']

def main():
    """Called when module is '__main__', after successful bootstrap."""
    pass


def bootstrap_starting():
    """Called before attempting to load/download packages."""
    pass


def bootstrap_succeeded():
    """Called after (updated) packages have been added to sys.path."""
    global _bootstrapped_by_transmute
    _bootstrapped_by_transmute = True


def bootstrap_failed():
    """Called when bootstrap fails to download packages from PyPI or load them
    from the local cache.
    """
    raise RuntimeError("Unable to load 'transmute' package.")


import os, os.path, sys

def _chunk_read(file, chunk_size=16384):
    """Read file one chunk at a time."""
    while True:
        chunk = file.read(chunk_size)
        if chunk == '':
            break
        yield chunk


def _md5(filename):
    """Compute MD5 hash of a file."""
    global _chunk_read
    import hashlib
    h = hashlib.md5()
    try:
        with open(filename) as (file):
            for chunk in _chunk_read(file):
                h.update(chunk)

    except:
        pass

    return h.hexdigest()


def _copy(source, destination, chunk_size):
    """Read source into destination, one chunk at a time."""
    for chunk in _chunk_read(source, chunk_size):
        destination.write(chunk)


def _download(source, filename, md5sum):
    """Copy source to filename, verify MD5 hash of content.

    Content is initially saved to a temporary file and the content's MD5 hash is
    verified before the file is atomically renamed to the desired filename.

    This will call source.close().
    """
    global _copy
    global _md5
    global os
    import contextlib, tempfile
    dirname = os.path.dirname(filename)
    dst = tempfile.NamedTemporaryFile(suffix='.download', dir=dirname)
    with contextlib.closing(dst):
        _copy(source, dst, 4096)
        dst.flush()
        if _md5(dst.name) != md5sum:
            raise RuntimeError("MD5 hash of local file doesn't match expected value")
        dst.delete = False
        os.rename(dst.name, filename)


def require(baskets, requirements, entries):
    """Satisfy requirements from given baskets."""
    import pkg_resources, zipimport
    requirements = list(pkg_resources.parse_requirements(requirements))
    environment = pkg_resources.Environment()
    for basket in baskets:
        basket.fill_environment(environment, requirements)

    working_set = pkg_resources.WorkingSet(entries)
    while True:
        needed = working_set.resolve(requirements, env=environment)
        missing = []
        for dist in needed:
            if dist.location in working_set.entries:
                continue
            if hasattr(dist, '_transmute_basket'):
                try:
                    dist._transmute_basket.make_local(dist)
                except:
                    environment.remove(dist)
                    break
                else:
                    dist._provider = pkg_resources.EggMetadata(zipimport.zipimporter(dist.location))
            missing.append(dist)
        else:
            break

    entries[0:0] = [ dist.location for dist in missing ]


class Basket(object):
    """A container for Python Eggs."""
    _cache_dir = os.path.expanduser('~/.python-transmute/cache')

    def __init__(self, url=None, path=None):
        assert (path is None) != (url is None)
        if path is None:
            path = self._prepare_cache(url)
        self.url = url
        self.path = os.path.join(path, '')
        self._projects = set()
        self.distributions = {}
        return

    def _initialize(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        try:
            for filename in os.listdir(self.path):
                self.add_package(filename)

        except:
            pass

        try:
            self.initialize()
        except:
            pass

    def _initialize_project(self, project):
        if project in self._projects:
            return
        self._projects.add(project)
        try:
            self.initialize_project(project)
        except:
            pass

    def _prepare_cache(self, url):
        import urllib
        path = os.path.join(self._cache_dir, urllib.quote(url, ''))
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    @classmethod
    def _is_egg(cls, filename):
        return filename[(-4)] == '.' and filename[-3:].lower() == 'egg'

    def add_package(self, filename, metadata=None):
        if not self._is_egg(filename):
            return
        from pkg_resources import Distribution, EGG_DIST
        dist = Distribution.from_location(self.path + filename, filename)
        dist._transmute_basket = self
        dist._transmute_metadata = metadata
        dist.precedence = EGG_DIST - 0.1
        project_dists = self.distributions.setdefault(dist.project_name, [])
        project_dists.append(dist)

    def fill_environment(self, environment, requirements=None):
        self._initialize()
        for req in requirements:
            project = req.project_name
            self._initialize_project(project)

        for project_dists in self.distributions.itervalues():
            for dist in project_dists:
                environment.add(dist)

    def make_local(self, dist):
        if os.path.isfile(dist.location):
            return
        self.fetch(dist, dist._transmute_metadata)

    def initialize(self):
        """Instance initialization, called once at the end of __init__."""
        pass

    def initialize_project(self, project_name):
        """Called before fulfilling requirements, once per project_name."""
        pass

    def fetch(self, dist, metadata):
        """Called from make_local if local copy does not exist."""
        raise RuntimeError('Unable to fetch: %s' % dist)


class PyPIBasket(Basket):
    """A proxy basket for eggs available in PyPI."""
    pypi_url = 'https://pypi.python.org/pypi'

    def fetch(self, dist, metadata):
        global _download
        import urllib2
        _download(urllib2.urlopen(metadata['url']), dist.location, metadata['md5_digest'])

    def initialize_project(self, project_name):
        global sys
        import json, urllib2
        url = '%s/%s/json' % (self.url, project_name)
        req = urllib2.urlopen(url)
        metadata = json.load(req)
        for package in metadata['urls']:
            if not sys.version.startswith(package['python_version']) or package['packagetype'] != 'bdist_egg':
                continue
            self.add_package(package['filename'], package)


PYPI_BASKET = PyPIBasket(PyPIBasket.pypi_url)

def bootstrap():
    """Bootstrap 'transmute' package, making it available for import.

    Actual packages to be bootstrapped are defined in the global variable
    requirements.

    Latest packages are downloaded from PyPI, if available, and added to
    sys.path.
    """
    global PYPI_BASKET
    global bootstrap_failed
    global bootstrap_starting
    global bootstrap_succeeded
    global require
    global requirements
    import pkg_resources
    bootstrap_starting()
    try:
        require([PYPI_BASKET], requirements, sys.path)
    except:
        bootstrap_failed()
    else:
        reload(pkg_resources)
        bootstrap_succeeded()


def _clean_namespace():
    """Clean module's namespace.

    Used prior to a reload() of the module when the present module is used to
    bootstrap the Real Thing (tm).
    """
    global Basket
    global PYPI_BASKET
    global PyPIBasket
    global __doc__
    global _chunk_read
    global _clean_namespace
    global _copy
    global _download
    global _md5
    global bootstrap
    global bootstrap_failed
    global bootstrap_starting
    global bootstrap_succeeded
    global main
    global os
    global require
    global requirements
    global sys
    del __doc__
    del os
    del sys
    del requirements
    del main
    del bootstrap_starting
    del bootstrap_succeeded
    del bootstrap_failed
    del _chunk_read
    del _md5
    del _copy
    del _download
    del require
    del Basket
    del PyPIBasket
    del PYPI_BASKET
    del bootstrap
    del _clean_namespace


if __name__ in requirements:
    bootstrap()
    _clean_namespace()
    import sys
    reload(sys.modules[__name__])
else:
    import importlib
    try:
        for package in requirements:
            importlib.import_module(package)

    except ImportError:
        bootstrap()

if __name__ == '__main__':
    sys.exit(main())