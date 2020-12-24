#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run PROJECT with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='project',
    version='20',
    url='https://pikacode.com/bthate/project',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='2012-2014 69389/12',
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    install_requires=["meds", ],
    scripts=["bin/project", ],
    packages=['project',
              'project.plugs',
             ],
    long_description = """De geestelijke gezondheid moet zijn plaats hebben in het leven, gelijk het lichaam. """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
