#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run oolib with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='oolib',
    version='12',
    url='https://pikacode.com/milla/oolib',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='oolib - not a object-oriented library.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["beautifulsoup4"],
    scripts=["bin/bot", "bin/bli", "bin/bgrep"],
    packages=['oolib', 
              'oolib.plugs',
              'oolib.drivers',
             ],
    long_description = """ Not A Object-Oriented Library. """,
    data_files=[('doc', ["LICENSE", ]),],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
