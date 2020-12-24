#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run bsh with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

import rlib

setup(
    name='aesculaap',
    version='%s' % rlib.__version__,
    url='https://pikacode.com/milla/aesculaap',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='aesculaap - general purpose bot.',
    license='MMIT',
    include_package_data=True,
    zip_safe=False,
    requires=['distribute', 'sleekxmpp'],
    scripts=['bin/reppa',
            ],
    packages=['rlib',
              'rlib.drivers',
              'rlib.plugs',
             ],
    long_description = """ """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
