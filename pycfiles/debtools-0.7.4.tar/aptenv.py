# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/DebTools/debtools/aptenv.py
# Compiled at: 2016-09-11 06:49:03
from __future__ import unicode_literals, print_function, absolute_import
import argparse, codecs, sys, re
from distutils.version import LooseVersion
from pip import get_installed_distributions
from pip._vendor import requests
from pip._vendor.pkg_resources import Distribution
from pip.download import PipSession
from pip.req import parse_requirements
from pip.req.req_install import InstallRequirement
from stdeb.util import debianize_name
__author__ = b'Matthieu Gallet'
ubuntu_distribs = {
 b'precise', b'precise-updates', b'trusty', b'trusty-updates', b'wily', b'wily-updates', b'xenial',
 b'xenial-updates', b'yakkety'}
debian_distribs = {b'wheezy', b'wheezy-backports', b'jessie', b'jessie-backports', b'stretch', b'sid'}
default_map = {b'ansible': b'ansible', b'Fabric': b'fabric', b'PyYAML': b'python-yaml', b'ipython': b'ipython', 
   b'pybtex': b'pybtex', b'pylint': b'pylint', b'pytz': b'python-tz'}

class EnvironmentBuilder(object):

    def __init__(self, base_urls, python_version=b'3', package_mapping=None, required_packages=None):
        self.base_urls = base_urls
        self.python_version = python_version
        self.package_mapping = package_mapping or {}
        self.required_packages = required_packages or []

    def get_debian_package(self, python_package):
        if python_package in self.package_mapping:
            return self.package_mapping[python_package]
        debian_name = debianize_name(python_package)
        if debian_name.startswith(b'python-'):
            debian_name = debian_name.partition(b'-')[2]
        if self.python_version == b'3':
            return b'python3-' + debian_name
        return b'python-' + debian_name

    def get_available_package_version_in_url(self, base_url, python_package):
        debian_package = self.get_debian_package(python_package)
        url = base_url + debian_package
        title = self._extract_title(url)
        if title is None:
            return
        else:
            title = title.replace(b'\xa0', b' ').partition(b' [')[0]
            matcher = re.match(b'^\\w+\\s*:[^(]*\\((\\d:|)(.*)-.*\\).*$', title)
            if not matcher:
                return
            version_info = matcher.groups()[1].partition(b'+')[0]
            return version_info

    def _extract_title(self, url):
        title = None
        r = requests.get(url)
        if r.status_code == 200:
            content = r.text
            start_pos = content.find(b'<h1>')
            end_pos = content.find(b'</h1>')
            if 0 < start_pos < end_pos:
                title = content[start_pos + 4:end_pos].strip()
        return title

    def get_best_available_package_version(self, python_package, descending=True):
        versions = [ self.get_available_package_version_in_url(base_url, python_package) for base_url in self.base_urls ]
        loose_versions = [ LooseVersion(x) for x in versions if x ]
        loose_versions.sort(reverse=descending)
        if not loose_versions:
            return None
        else:
            return loose_versions[0]

    def print_requirements(self):
        for python_package in self.required_packages:
            if python_package in self.package_mapping and not self.package_mapping[python_package]:
                continue
            version = self.get_best_available_package_version(python_package)
            if not version:
                sys.stderr.write(b'Unable to find any version for %s\n' % python_package)
            else:
                print(b'%s==%s' % (python_package, version))


def main():
    parser = argparse.ArgumentParser(description=b'Build a Python virtual env using the versions also available as official Debian or Ubuntu packages')
    parser.add_argument(b'-u', b'--URL', help=b'"wheezy", "xenial-updates", other distrib name or any URL like https://packages.debian.org/stretch/', default=[], action=b'append')
    parser.add_argument(b'-M', b'--defaultmap', help=b'Use name mapping for well-known packages', action=b'store_true', default=False)
    parser.add_argument(b'-m', b'--mapfile', help=b'mapping file between Python package names and Debian ones: each line is like "python-package-name=debian-package-name".Otherwise, use the default Debianized name ("python[3]-package-name"). Add"python-package-name=" to ignore this package', default=None)
    parser.add_argument(b'-p', b'--python', help=b'Python version: "2" or "3" (default: "%s")' % sys.version_info[0], default=str(sys.version_info[0]))
    parser.add_argument(b'-r', b'--requirements', help=b'Requirements file (otherwise use "pip list")', default=None)
    args = parser.parse_args()
    base_urls = []
    for url in args.URL:
        if url in ubuntu_distribs:
            base_urls.append(b'http://packages.ubuntu.com/%s/' % url)
        elif url in debian_distribs:
            base_urls.append(b'https://packages.debian.org/%s/' % url)
        elif url.startswith(b'http'):
            base_urls.append(url)
        else:
            print(b'Invalid URL: %s' % url)
            print(b'Known default values: %s, %s' % ((b', ').join(ubuntu_distribs), (b', ').join(debian_distribs)))

    package_mapping = {}
    if args.defaultmap:
        package_mapping.update(default_map)
    if args.mapfile:
        with codecs.open(args.mapfile, b'r', encoding=b'utf-8') as (fd):
            for line in fd:
                python_name, sep, debian_name = line.partition(b'=')
                if sep != b'=':
                    continue
                python_name = python_name.strip()
                if not python_name.startswith(b'#'):
                    package_mapping[python_name] = debian_name.strip()

    required_packages = []
    if args.requirements is None:
        for r in get_installed_distributions():
            assert isinstance(r, Distribution)
            required_packages.append(r.project_name)

    else:
        for r in parse_requirements(args.requirements, session=PipSession()):
            assert isinstance(r, InstallRequirement)
            required_packages.append(r.name)

    builder = EnvironmentBuilder(base_urls, python_version=args.python, package_mapping=package_mapping, required_packages=required_packages)
    builder.print_requirements()
    return