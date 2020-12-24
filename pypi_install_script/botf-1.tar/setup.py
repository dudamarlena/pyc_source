#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run botf with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='botf',
    version='1',
    url='https://pikacode.com/bthate/botf',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTF - CLI, XMPP, IRC, UDP, RSS, REST, SPIDER",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/botf", "bin/botf-local", "bin/botf-sed", "bin/botf-udp", "bin/botf-do"],
    packages=['botf',
              'botf.plugs',
              'botf.extra',
              'botf.service',
              'botf.utils',
             ],
    long_description=""" BOTF - botf framework """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
