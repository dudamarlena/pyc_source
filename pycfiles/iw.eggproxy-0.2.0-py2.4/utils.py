# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/eggproxy/utils.py
# Compiled at: 2008-09-22 04:57:28
import os, tempfile, shutil
from setuptools.package_index import PackageIndex as BasePackageIndex
from setuptools.package_index import egg_info_for_url
from pkg_resources import Requirement
from iw.eggproxy.config import config
EGGS_DIR = config.get('default', 'eggs_directory')
INDEX_URL = config.get('default', 'index')

class PackageIndex(BasePackageIndex):
    """This class overrides PackageIndex.can_add method to remove filter on
    python major version: we want packages for all versions, all platforms
    """
    __module__ = __name__

    def can_add(self, dist):
        """
        """
        return True


INDEX = PackageIndex(index_url=INDEX_URL)

class PackageNotFound(Exception):
    """
    """
    __module__ = __name__


class IndexProxy(object):
    __module__ = __name__

    def __init__(self):
        self.index = INDEX

    def updateBaseIndex(self):
        """Update base index.html
       """
        file_path = os.path.join(EGGS_DIR, 'index.html')
        self.index.scan_all()
        package_names = self.index.package_pages.keys()
        package_names.sort()
        html = open(file_path, 'w')
        print >> html, '<html><head><title>Simple Index</title></head><body>'
        for pack_name in package_names:
            print >> html, '<a href="%s/">%s</a><br/>' % (pack_name, pack_name)

        print >> html, '</body></html>'
        html.close()
        del html

    def _lookupPackage(self, package_name):
        requirement = Requirement.parse(package_name)
        self.index.find_packages(requirement)

    def updatePackageIndex(self, package_name):
        """Update info for a specific package
        """
        self._lookupPackage(package_name)
        if not self.index[package_name]:
            raise PackageNotFound, "Package '%s' does not exists or has no eggs" % package_name
        package_path = os.path.join(EGGS_DIR, package_name)
        if not os.path.exists(package_path):
            os.mkdir(package_path)
        html_path = os.path.join(package_path, 'index.html')
        html = open(html_path, 'w')
        title = 'Links for %s' % package_name
        print >> html, '<html><head><title>%s</title></head>' % package_name
        print >> html, '<body><h1>%s</h1>' % package_name
        for dist in self.index[package_name]:
            if getattr(dist, 'module_path', None) is not None:
                continue
            (filename, md5) = egg_info_for_url(dist.location)
            print >> html, '<a href="%s#%s" rel="download">%s</a></br>' % (filename, md5, filename)

        print >> html, '</body></html>'
        html.close()
        del html
        return

    def updateEggFor(self, package_name, eggname):
        """Download an egg for package_name
        """
        self._lookupPackage(package_name)
        file_path = os.path.join(EGGS_DIR, package_name, eggname)
        for dist in self.index[package_name]:
            if getattr(dist, 'module_path', None) is not None:
                continue
            (filename, md5) = egg_info_for_url(dist.location)
            if filename == eggname:
                tmp = tempfile.gettempdir()
                tmp_location = self.index.download(dist.location, tmp)
                shutil.move(tmp_location, file_path)
                return

        raise ValueError, "Egg '%s' not found in index" % eggname
        return