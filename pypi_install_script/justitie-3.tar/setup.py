#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run KONING with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='justitie',
    version='3',
    url='https://pikacode.com/bthate/justitie',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" JUSTITIE - Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid """,
    license='MIT',
    script_dir=["bin/justitie"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["kern"],
    packages=['justitie'],
    long_description=""" 

WETBOEK VAN STRAFRECHT

Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.  

Artikel 300.5 Met behandeling word gelijkgesteld langdurige mishandeling.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
