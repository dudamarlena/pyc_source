# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/firmware_package.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: firmware_package.py'
import os, tarfile, ConfigParser, pkg_resources, cxmanage_api
from cxmanage_api import temp_dir
from cxmanage_api.image import Image

class FirmwarePackage(object):
    """A firmware update package contains multiple images & version information.

    .. note::
        * Valid firmware packages are in tar.gz format.

    >>> from cxmanage_api.firmware_package import FirmwarePackage
    >>> fwpkg = FirmwarePackage('/path/to/ECX-1000_update-v1.7.1-dirty.tar.gz')

    :param filename: The file to extract and read.
    :type filename: string

    :raises ValueError: If cxmanage version is too old.

    """

    def __init__(self, filename=None):
        """Default constructor for the FirmwarePackage class."""
        self.images = []
        self.version = None
        self.config = None
        self.required_socman_version = None
        self.work_dir = temp_dir()
        if filename:
            try:
                tarfile.open(filename, 'r').extractall(self.work_dir)
            except (IOError, tarfile.ReadError):
                raise ValueError('%s is not a valid tar.gz file' % os.path.basename(filename))

            config = ConfigParser.SafeConfigParser()
            if len(config.read(self.work_dir + '/MANIFEST')) == 0:
                raise ValueError('%s is not a valid firmware package' % os.path.basename(filename))
            if 'package' in config.sections():
                required_cxmanage_version = config.get('package', 'required_cxmanage_version')
                if pkg_resources.parse_version(cxmanage_api.__version__) < pkg_resources.parse_version(required_cxmanage_version):
                    raise ValueError('%s requires cxmanage version %s or later.' % (
                     filename, required_cxmanage_version))
                if config.has_option('package', 'required_socman_version'):
                    self.required_socman_version = config.get('package', 'required_socman_version')
                if config.has_option('package', 'firmware_version'):
                    self.version = config.get('package', 'firmware_version')
                if config.has_option('package', 'firmware_config'):
                    self.config = config.get('package', 'firmware_config')
            image_sections = [ x for x in config.sections() if x != 'package' ]
            for section in image_sections:
                filename = '%s/%s' % (self.work_dir, section)
                image_type = config.get(section, 'type').upper()
                simg = None
                daddr = None
                skip_crc32 = False
                version = None
                if config.has_option(section, 'simg'):
                    simg = config.getboolean(section, 'simg')
                if config.has_option(section, 'daddr'):
                    daddr = int(config.get(section, 'daddr'), 16)
                if config.has_option(section, 'skip_crc32'):
                    skip_crc32 = config.getboolean(section, 'skip_crc32')
                if config.has_option(section, 'versionstr'):
                    version = config.get(section, 'versionstr')
                self.images.append(Image(filename, image_type, simg, daddr, skip_crc32, version))

        return

    def __str__(self):
        return self.version

    def save_package(self, filename):
        """Save all images as a firmware package.

        .. note::
            * Supports tar .gz and .bz2 file extensions.

        >>> from cxmanage_api.firmware_package import FirmwarePackage
        >>> fwpkg = FirmwarePackage()
        >>> fwpkg.save_package(filename='my_fw_update_pkg.tar.gz')

        :param filename: Name (or path) of of the file you wish to save.
        :type filename: string

        """
        config = ConfigParser.SafeConfigParser()
        for image in self.images:
            section = os.path.basename(image.filename)
            config.add_section(section)
            config.set(section, 'type', image.type)
            config.set(section, 'simg', str(image.simg))
            if image.priority != None:
                config.set(section, 'priority', str(image.priority))
            if image.daddr != None:
                config.set(section, 'daddr', '%x' % image.daddr)
            if image.skip_crc32:
                config.set(section, 'skip_crc32', str(image.skip_crc32))
            if image.version != None:
                config.set(section, 'versionstr', image.version)

        manifest = open('%s/MANIFEST' % self.work_dir, 'w')
        config.write(manifest)
        manifest.close()
        if filename.endswith('gz'):
            tar = tarfile.open(filename, 'w:gz')
        else:
            if filename.endswith('bz2'):
                tar = tarfile.open(filename, 'w:bz2')
            else:
                tar = tarfile.open(filename, 'w')
            tar.add('%s/MANIFEST' % self.work_dir, 'MANIFEST')
            for image in self.images:
                tar.add(image.filename, os.path.basename(image.filename))

        tar.close()
        return