import sys
import os
from setuptools import setup, find_packages
from ConfigParser import SafeConfigParser

from distutils.util import convert_path
from fnmatch import fnmatchcase

config_file = 'setup.cfg'

cfg = SafeConfigParser()
if not os.path.exists(config_file):
    raise IOError('File not found : %s' % config_file)

cfg.read(config_file)

NAME = cfg.get('metadata', 'name')
PRETTYNAME = cfg.get('metadata', 'prettyname')
VERSION = cfg.get('metadata', 'version')
DESCRIPTION = cfg.get('metadata', 'description')
AUTHOR = cfg.get('metadata', 'author')
AUTHOR_EMAIL = cfg.get('metadata', 'author_email')
URL = cfg.get('metadata', 'url')
DOWNLOAD_URL = cfg.get('metadata', 'download_url')
LICENSE = cfg.get('metadata', 'license')

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "Genshi >= 0.5.1",
        "pyf.componentized>=2.0",
        "pyjon.reports>=0.6"
        ],
    namespace_packages=['pyf', 'pyf.components', 'pyf.components.consumers'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points="""
        [pyf.components.consumers]
        rmlpdfwriter = pyf.components.consumers.rmlpdfwriter:RMLPDFWriter
        multirmlpdfwriter = pyf.components.consumers.rmlpdfwriter:MultiRMLPDFWriter
    """,
    keywords = [],
    test_suite = 'nose.collector',
    )
