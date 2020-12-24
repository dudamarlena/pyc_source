# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/twine/twine/package.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 7609 bytes
from __future__ import absolute_import, unicode_literals, print_function
import collections, hashlib, io, os, subprocess, pkginfo, pkg_resources
try:
    from hashlib import blake2b
except ImportError:
    try:
        from pyblake2 import blake2b
    except ImportError:
        blake2b = None

from twine.wheel import Wheel
from twine.wininst import WinInst
from twine import exceptions
DIST_TYPES = {'bdist_wheel':Wheel, 
 'bdist_wininst':WinInst, 
 'bdist_egg':pkginfo.BDist, 
 'sdist':pkginfo.SDist}
DIST_EXTENSIONS = {'.whl':'bdist_wheel', 
 '.exe':'bdist_wininst', 
 '.egg':'bdist_egg', 
 '.tar.bz2':'sdist', 
 '.tar.gz':'sdist', 
 '.zip':'sdist'}

class PackageFile(object):

    def __init__(self, filename, comment, metadata, python_version, filetype):
        self.filename = filename
        self.basefilename = os.path.basename(filename)
        self.comment = comment
        self.metadata = metadata
        self.python_version = python_version
        self.filetype = filetype
        self.safe_name = pkg_resources.safe_name(metadata.name)
        self.signed_filename = self.filename + '.asc'
        self.signed_basefilename = self.basefilename + '.asc'
        self.gpg_signature = None
        hasher = HashManager(filename)
        hasher.hash()
        hexdigest = hasher.hexdigest()
        self.md5_digest = hexdigest.md5
        self.sha2_digest = hexdigest.sha2
        self.blake2_256_digest = hexdigest.blake2

    @classmethod
    def from_filename(cls, filename, comment):
        for ext, dtype in DIST_EXTENSIONS.items():
            if filename.endswith(ext):
                meta = DIST_TYPES[dtype](filename)
                break
        else:
            raise exceptions.InvalidDistribution("Unknown distribution format: '%s'" % os.path.basename(filename))

        if dtype == 'bdist_egg':
            pkgd = pkg_resources.Distribution.from_filename(filename)
            py_version = pkgd.py_version
        else:
            if dtype == 'bdist_wheel':
                py_version = meta.py_version
            else:
                if dtype == 'bdist_wininst':
                    py_version = meta.py_version
                else:
                    py_version = None
        return cls(filename, comment, meta, py_version, dtype)

    def metadata_dictionary(self):
        meta = self.metadata
        data = {'name':self.safe_name, 
         'version':meta.version, 
         'filetype':self.filetype, 
         'pyversion':self.python_version, 
         'metadata_version':meta.metadata_version, 
         'summary':meta.summary, 
         'home_page':meta.home_page, 
         'author':meta.author, 
         'author_email':meta.author_email, 
         'maintainer':meta.maintainer, 
         'maintainer_email':meta.maintainer_email, 
         'license':meta.license, 
         'description':meta.description, 
         'keywords':meta.keywords, 
         'platform':meta.platforms, 
         'classifiers':meta.classifiers, 
         'download_url':meta.download_url, 
         'supported_platform':meta.supported_platforms, 
         'comment':self.comment, 
         'md5_digest':self.md5_digest, 
         'sha256_digest':self.sha2_digest, 
         'blake2_256_digest':self.blake2_256_digest, 
         'provides':meta.provides, 
         'requires':meta.requires, 
         'obsoletes':meta.obsoletes, 
         'project_urls':meta.project_urls, 
         'provides_dist':meta.provides_dist, 
         'obsoletes_dist':meta.obsoletes_dist, 
         'requires_dist':meta.requires_dist, 
         'requires_external':meta.requires_external, 
         'requires_python':meta.requires_python, 
         'provides_extras':meta.provides_extras, 
         'description_content_type':meta.description_content_type}
        if self.gpg_signature is not None:
            data['gpg_signature'] = self.gpg_signature
        return data

    def add_gpg_signature(self, signature_filepath, signature_filename):
        if self.gpg_signature is not None:
            raise exceptions.InvalidDistribution('GPG Signature can only be added once')
        with open(signature_filepath, 'rb') as (gpg):
            self.gpg_signature = (
             signature_filename, gpg.read())

    def sign(self, sign_with, identity):
        print('Signing {}'.format(self.basefilename))
        gpg_args = (sign_with, '--detach-sign')
        if identity:
            gpg_args += ('--local-user', identity)
        gpg_args += ('-a', self.filename)
        subprocess.check_call(gpg_args)
        self.add_gpg_signature(self.signed_filename, self.signed_basefilename)


Hexdigest = collections.namedtuple('Hexdigest', ['md5', 'sha2', 'blake2'])

class HashManager(object):
    __doc__ = 'Manage our hashing objects for simplicity.\n\n    This will also allow us to better test this logic.\n    '

    def __init__(self, filename):
        """Initialize our manager and hasher objects."""
        self.filename = filename
        try:
            self._md5_hasher = hashlib.md5()
        except ValueError:
            self._md5_hasher = None

        self._sha2_hasher = hashlib.sha256()
        self._blake_hasher = None
        if blake2b is not None:
            self._blake_hasher = blake2b(digest_size=32)

    def _md5_update(self, content):
        if self._md5_hasher is not None:
            self._md5_hasher.update(content)

    def _md5_hexdigest(self):
        if self._md5_hasher is not None:
            return self._md5_hasher.hexdigest()

    def _sha2_update(self, content):
        if self._sha2_hasher is not None:
            self._sha2_hasher.update(content)

    def _sha2_hexdigest(self):
        if self._sha2_hasher is not None:
            return self._sha2_hasher.hexdigest()

    def _blake_update(self, content):
        if self._blake_hasher is not None:
            self._blake_hasher.update(content)

    def _blake_hexdigest(self):
        if self._blake_hasher is not None:
            return self._blake_hasher.hexdigest()

    def hash(self):
        """Hash the file contents."""
        with open(self.filename, 'rb') as (fp):
            for content in iter(lambda : fp.read(io.DEFAULT_BUFFER_SIZE), b''):
                self._md5_update(content)
                self._sha2_update(content)
                self._blake_update(content)

    def hexdigest(self):
        """Return the hexdigest for the file."""
        return Hexdigest(self._md5_hexdigest(), self._sha2_hexdigest(), self._blake_hexdigest())