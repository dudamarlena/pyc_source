#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run core with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='cored',
    version='45',
    url='https://pikacode.com/bthate/core',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="CORE - CLI, XMPP, IRC, UDP, RSS, REST, SPIDER",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/core", "bin/core-local", "bin/core-sed", "bin/core-udp", "bin/core-do", "bin/core-docs"],
    packages=['core',
              'core.bots',
              'core.plugs',
              'core.extra',
              'core.service',
              'core.utils',
             ],
    long_description=""" CORE - Common Object Request Engine """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
