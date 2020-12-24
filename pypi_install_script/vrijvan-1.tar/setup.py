#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run vrijvan with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='vrijvan',
    version='1',
    url='https://pikacode.com/bthate/vrijvan',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=' VRIJVAN - vrij van gemaakt zijn voordat men is ',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["kern"],
    packages=["vrijvan"],
    scripts=["bin/vrijvan", ],
    long_description=""" vrij (bn):los, onafhankelijk, onbegrensd, onbelemmerd, onbeperkt, onbezet, onbezwaard, onconventioneel, ongebonden, ongedwongen, vrijmoedig """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
