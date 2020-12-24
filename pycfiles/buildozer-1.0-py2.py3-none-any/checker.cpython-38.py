# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/checker.py
# Compiled at: 2020-03-06 05:58:11
# Size of source mod 2**32: 8759 bytes
__doc__ = '\nVersion checker for Buildout Versions Checker\n'
import json, os, socket
from collections import OrderedDict
from concurrent import futures
from configparser import NoSectionError
from urllib.error import URLError
from urllib.request import urlopen
from bvc.configparser import VersionsConfigParser
import bvc.logger as logger
from packaging.specifiers import SpecifierSet
import packaging.version as parse_version

class VersionsChecker(object):
    """VersionsChecker"""
    default_version = '0.0.0'

    def __init__(self, source, specifiers={}, allow_pre_releases=False, includes=[], excludes=[], service_url='https://pypi.python.org/pypi', timeout=10, threads=10):
        """
        Parses a config file containing pinned versions
        of eggs and check available updates.
        """
        self.source = source
        self.includes = includes
        self.excludes = excludes
        self.specifiers = specifiers
        self.allow_pre_releases = allow_pre_releases
        self.timeout = timeout
        self.threads = threads
        self.service_url = service_url
        self.source_versions = OrderedDict(self.parse_versions(self.source))
        self.versions = self.include_exclude_versions(self.source_versions, self.includes, self.excludes)
        self.package_specifiers = self.build_specifiers(self.versions.keys(), self.specifiers)
        self.last_versions = OrderedDict(self.fetch_last_versions(self.package_specifiers, self.allow_pre_releases, self.service_url, self.timeout, self.threads))
        self.updates = OrderedDict(self.find_updates(self.versions, self.last_versions))

    def parse_versions--- This code section failed: ---

 L.  73         0  LOAD_GLOBAL              VersionsConfigParser
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config'

 L.  74         6  LOAD_FAST                'config'
                8  LOAD_METHOD              read
               10  LOAD_FAST                'source'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'has_read'

 L.  76        16  LOAD_FAST                'has_read'
               18  POP_JUMP_IF_TRUE     36  'to 36'

 L.  77        20  LOAD_GLOBAL              logger
               22  LOAD_METHOD              warning
               24  LOAD_STR                 "'%s' cannot be read."
               26  LOAD_FAST                'source'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L.  78        32  BUILD_LIST_0          0 
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'

 L.  80        36  SETUP_FINALLY        52  'to 52'

 L.  81        38  LOAD_FAST                'config'
               40  LOAD_METHOD              items
               42  LOAD_STR                 'versions'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'versions'
               48  POP_BLOCK        
               50  JUMP_FORWARD         88  'to 88'
             52_0  COME_FROM_FINALLY    36  '36'

 L.  82        52  DUP_TOP          
               54  LOAD_GLOBAL              NoSectionError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  83        66  LOAD_GLOBAL              logger
               68  LOAD_METHOD              debug

 L.  84        70  LOAD_STR                 "'versions' section not found in %s."

 L.  85        72  LOAD_FAST                'source'

 L.  83        74  CALL_METHOD_2         2  ''
               76  POP_TOP          

 L.  87        78  BUILD_LIST_0          0 
               80  ROT_FOUR         
               82  POP_EXCEPT       
               84  RETURN_VALUE     
             86_0  COME_FROM            58  '58'
               86  END_FINALLY      
             88_0  COME_FROM            50  '50'

 L.  89        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              info

 L.  90        92  LOAD_STR                 '- %d versions found in %s.'

 L.  91        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'versions'
               98  CALL_FUNCTION_1       1  ''

 L.  91       100  LOAD_FAST                'source'

 L.  89       102  CALL_METHOD_3         3  ''
              104  POP_TOP          

 L.  94       106  LOAD_FAST                'versions'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 80

    def include_exclude_versions(self, source_versions, includes=[], excludes=[]):
        """
        Includes and excludes packages to be checked in
        the default dict of packages with versions.
        """
        versions = source_versions.copy()
        packages_lower = [x.lower() for x in versions.keys()]
        excludes_lower = [x.lower() for x in excludes]
        for include in includes:
            if include.lower() not in packages_lower:
                versions[include] = self.default_version

        for package in list(versions.keys()):
            if package.lower() in excludes_lower:
                del versions[package]
            logger.info('- %d packages need to be checked for updates.', len(versions))
            return versions

    def build_specifiers(self, packages, source_specifiers):
        """
        Builds a list of tuple (package, version specifier)
        """
        specifiers = []
        source_specifiers = dict(((
         k.lower(), v) for k, v in source_specifiers.items()))
        for package in packages:
            specifier = source_specifiers.get(package.lower(), '')
            specifiers.append((package, specifier))

        return specifiers

    def fetch_last_versions--- This code section failed: ---

 L. 145         0  BUILD_LIST_0          0 
                2  STORE_FAST               'versions'

 L. 147         4  LOAD_FAST                'threads'
                6  LOAD_CONST               1
                8  COMPARE_OP               >
               10  POP_JUMP_IF_FALSE    94  'to 94'

 L. 148        12  LOAD_GLOBAL              futures
               14  LOAD_ATTR                ThreadPoolExecutor

 L. 149        16  LOAD_FAST                'threads'

 L. 148        18  LOAD_CONST               ('max_workers',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  SETUP_WITH           86  'to 86'

 L. 150        24  STORE_DEREF              'executor'

 L. 151        26  LOAD_CLOSURE             'allow_pre_releases'
               28  LOAD_CLOSURE             'executor'
               30  LOAD_CLOSURE             'self'
               32  LOAD_CLOSURE             'service_url'
               34  LOAD_CLOSURE             'timeout'
               36  BUILD_TUPLE_5         5 
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'VersionsChecker.fetch_last_versions.<locals>.<listcomp>'
               42  MAKE_FUNCTION_8          'closure'

 L. 159        44  LOAD_FAST                'packages'

 L. 151        46  GET_ITER         
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'tasks'

 L. 161        52  LOAD_GLOBAL              futures
               54  LOAD_METHOD              as_completed
               56  LOAD_FAST                'tasks'
               58  CALL_METHOD_1         1  ''
               60  GET_ITER         
               62  FOR_ITER             82  'to 82'
               64  STORE_FAST               'task'

 L. 162        66  LOAD_FAST                'versions'
               68  LOAD_METHOD              append
               70  LOAD_FAST                'task'
               72  LOAD_METHOD              result
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            62  'to 62'
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM_WITH       22  '22'
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  END_FINALLY      
               92  JUMP_FORWARD        126  'to 126'
             94_0  COME_FROM            10  '10'

 L. 164        94  LOAD_FAST                'packages'
               96  GET_ITER         
               98  FOR_ITER            126  'to 126'
              100  STORE_FAST               'package'

 L. 165       102  LOAD_FAST                'versions'
              104  LOAD_METHOD              append

 L. 166       106  LOAD_DEREF               'self'
              108  LOAD_METHOD              fetch_last_version

 L. 167       110  LOAD_FAST                'package'

 L. 168       112  LOAD_DEREF               'allow_pre_releases'

 L. 169       114  LOAD_DEREF               'service_url'

 L. 170       116  LOAD_DEREF               'timeout'

 L. 166       118  CALL_METHOD_4         4  ''

 L. 165       120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            98  'to 98'
            126_0  COME_FROM            92  '92'

 L. 174       126  LOAD_FAST                'versions'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 84

    def fetch_last_version(self, package, allow_pre_releases, service_url, timeout):
        """
        Fetch the last version of a package on Pypi.
        """
        package, specifier = package
        specifier = SpecifierSet(specifier, allow_pre_releases)
        max_version = parse_version(self.default_version)
        package_json_url = '%s/%s/json' % (service_url, package)
        logger.info('> Fetching latest datas for %s...', package)
        socket.setdefaulttimeout(timeout)
        try:
            content = urlopen(package_json_url).read().decode('utf-8')
        except URLError as error:
            try:
                content = '{"releases": []}'
                logger.debug('!> %s %s', package_json_url, error.reason)
            finally:
                error = None
                del error

        else:
            results = json.loads(content)
            socket.setdefaulttimeout(None)
        for version in specifier.filter(results['releases']):
            version = parse_version(version)
            if version > max_version:
                max_version = version
            logger.debug'-> Last version of %s%s is %s.'packagespecifiermax_version
            return (
             package, str(max_version))

    def find_updates(self, versions, last_versions):
        """
        Compare the current versions of the packages
        with the last versions to find updates.
        """
        updates = []
        for package, current_version in versions.items():
            last_version = last_versions[package]
            if last_version != current_version:
                logger.debug'=> %s current version (%s) and last version (%s) are different.'packagecurrent_versionlast_version
                updates.append((
                 package, last_version))
            logger.info('- %d package updates found.', len(updates))
            return updates


class UnusedVersionsChecker(VersionsChecker):
    """UnusedVersionsChecker"""

    def __init__(self, source, egg_directory, excludes=[]):
        """
        Parses a config file containing pinned versions
        of eggs and check their installation in the egg_directory.
        """
        self.source = source
        self.excludes = excludes
        self.egg_directory = egg_directory
        self.source_versions = OrderedDict(self.parse_versions(self.source))
        self.versions = self.include_exclude_versions((self.source_versions),
          excludes=(self.excludes))
        self.used_versions = self.get_used_versions(self.egg_directory)
        self.unused = self.find_unused_versions(self.versions.keys(), self.used_versions)

    def get_used_versions(self, egg_directory):
        """
        Walk into the egg_directory to know the packages installed.
        """
        return [egg.split('-')[0] for egg in os.listdir(egg_directory) if egg.endswith('.egg')]

    def find_unused_versions(self, versions, used_versions):
        """
        Make the difference between the listed versions and
        the used versions.
        """
        unused = list(versions)
        used_version_lower = [x.lower() for x in used_versions]
        for version in versions:
            if version.lower().replace('-', '_') in used_version_lower:
                unused.remove(version)
            return unused