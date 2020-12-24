#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run Meek with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

import meek

setup(
    name='Meek',
    version='%s' % meek.__version__,
    url='https://pikacode.com/milla/Meek',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='Meek - no help ;[',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    requires=['distribute', 'sleekxmpp'],
    scripts=['bin/Meek',
            ],
    packages=['meek',
              'meek.drivers',
              'meek.plugs',
             ],
    long_description = """ Help ! Kenmerk 69389/12. """,
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
