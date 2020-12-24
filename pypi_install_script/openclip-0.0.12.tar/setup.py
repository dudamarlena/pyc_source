# -*- coding: utf-8 -*-
"""
    openclip/setup.py
    =======================================

    provides openclip installation routines via setuptools
"""
import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('.'))
from openclip import __version__

ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR != '': os.chdir(ROOT_DIR)
VERSION = __version__
MODULE_DIR = 'openclip'
README=os.path.join(ROOT_DIR,'README.md')
DESCRIPTION = "OpenClip XML Media Management Python Module {version}".format(version=VERSION)
LONG_DESCRIPTION = """\
OpenClip XML Media Management Python Module {version}
============================================================

*(c) 2016 Robert Moggach & python-openclip contributors*

Licensed under the MIT license: `http://www.opensource.org/licenses/mit-license.php<http://www.opensource.org/licenses/mit-license.php>`_

Openclip is a python abstraction of the openclip XML media classification format.
It provides ORM-style access to "dotclip" data (file or generated) to make
the life of a python developer much easier.  This module is not meant to
be a complete solution but rather a stable and standardized component of
various other scripts, tools, guis, and software integrations.
""".format(version=VERSION)

try:
    from pypandoc import convert
    read_markdown = lambda f: convert(f, 'rst', 'md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_markdown = lambda f: eval('LONG_DESCRIPTION')

setup(
    name = "openclip",
    # setup_requires = [
    #     'sphinxcontrib.napoleon',
    # ],
    version = VERSION,
    description = DESCRIPTION,
    long_description = read_markdown(README),
    scripts = [ 'scripts/oc_mkclip' ],
    packages = find_packages(),
    install_requires = [
        'lxml',
        'colorlog',
        'munch',
        'parse',
        'pyseq',
        'timecode'
    ],
    package_data = {
        'openclip': ['data/openclip.*','test.clip'],
        'tests': ['*.clip']
    },
    include_package_data = True,
    # metadata for upload to PyPI
    classifiers = [
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    keywords = 'filesystem media utilities vfx',
    url = 'http://github.com/robmoggach/python-openclip', # 'http://robmoggach.github.io/python-openclip/',
    download_url = 'https://github.com/robmoggach/python-openclip/tarball/v{version}'.format(version=VERSION),
    author = 'Robert Moggach',
    author_email = 'rob@moggach.com',
    maintainer = 'Robert Moggach',
    maintainer_email = 'rob@moggach.com',
    license = 'MIT License'
)
