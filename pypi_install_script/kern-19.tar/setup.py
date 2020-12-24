#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run kern with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='kern',
    version='19',
    url='https://pikacode.com/bthate/kern',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="KERN - Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid. ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/kern", "bin/kern-local", "bin/kern-sed", "bin/kern-udp", "bin/kern-do", "bin/kern-docs"],
    packages=['kern',
              'kern.bots',
              'kern.plugs',
              'kern.extra',
              'kern.services',
              'kern.utils',
             ],
    long_description="""

1. Medicijnen die de receptoren blokkeren
2. Doseringen die zo hoog zijn dat ze giftig worden.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
