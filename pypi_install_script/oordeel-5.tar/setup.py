#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run OORDEEL with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='oordeel',
    version='5',
    url='https://pikacode.com/bthate/oordeel',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='XMPP, IRC, CLI, UDP, HTTP, UDP, RSS, EMAIL',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["meds", ],
    scripts=["bin/oordeel", ],
    packages=['oor',
              'oor.plugs',
             ],
    long_description = """  

* Een wet die een maatschappij maakt waarbij je zonder schuld niet kan leven.
* Een gevangeniswezen die je ziekt maakt met 4 muren.
* Een arts die je daarna met medicijnen voor de samenleving geneest.

1) geen wet die schuld maakt.
2) geen gevang wat ziek maakt.
3) geen medicijn dat dood maakt.


""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
