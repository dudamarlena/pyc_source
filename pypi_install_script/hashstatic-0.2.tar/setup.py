import os
from setuptools import setup, find_packages

__version__ = '0.2'

_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

try:
    _thisdir = os.path.join(os.path.dirname(__file__))
    long_description = open(os.path.join(_thisdir, 'README.md')).read()
except:
    long_description = None

metadata = {
    'name':                   'hashstatic',
    'version':                __version__,
    'packages':               _packages,
    'scripts':                ['scripts/makehash'],
    'include_package_data':   True,
    'author':                 'Carl Crowder',
    'author_email':           'hashstatic@jqx.be',
    'url':                    'https://github.com/carlio/hashstatic',
    'description':            'Simple checker for static content changes',
    'long_description':       long_description,
    'license':                'MIT',
    'keywords':               'static content hash',
}


setup(**metadata)
