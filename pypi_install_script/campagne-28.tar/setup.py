#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run campagne with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='campagne',
    version='28',
    url='https://pikacode.com/bart/campagne',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='anti suicide campagne',
    license='Public Domain',
    zip_safe=True,
    install_requires=["obot"],
    packages=["campagne"],
    scripts=["bin/campagne", ],
    long_description="""

Artikel 51

1.      Het College schorst een handelsvergunning, wijzigt deze of trekt deze in indien:

        a.      het geneesmiddel schadelijk is,


""",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
