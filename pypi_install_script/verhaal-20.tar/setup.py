#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run GGZ Claim with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='verhaal',
    version='20',
    url='https://pikacode.com/bthate/verhaal',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description= """ De beste manier om de toekomste te maken is haar te voorspellen, letter voor letter. """,
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    install_requires=["meds", ],
    scripts=["bin/verhaal", ],
    packages=['verhaal',
              'verhaal.plugs',
             ],
    long_description = """ Anti maak materie. """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
