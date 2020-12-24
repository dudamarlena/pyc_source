#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run OOR with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='oor',
    version='3',
    url='https://pikacode.com/bthate/oor',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='XMPP - IRC - CLI - RSS - UDP - API.',
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/oor", "bin/oor-local", "bin/oor-sed", "bin/oor-udp"],
    packages=['oor',
              'oor.service',
              'oor.contrib',
              'oor.plugs',
              'oor.bots',
             ],
    long_description = """ negatief oordeel maakt dat je zelf die fout niet kan maken, fout oordeel brengt dat je schuld maakt. """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
