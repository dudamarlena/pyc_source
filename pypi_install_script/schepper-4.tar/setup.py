#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run SCHEPPER with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='schepper',
    version='4',
    url='https://pikacode.com/bthate/schepper',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='SCHEPPER - niet de verboden maar de geboden vrucht ...',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=['schepper', 
             ],
    long_description = """

De hedendaagse vrucht van de boom van de kennis over goed en kwaad zijn de medicijnen die men de mens geeft. 
Denk men nu nog in termen van verboden vruchtgebruik als de oorzaak der problemen, het zijn de medicijnen die 
eerst aandacht vereisen om problemen op te kunnen lossen.

Door te wijzen naar drugsgebruik als de oorzaak van het probleem en niet de medicijnen gaat men de negatieve gevolgen 
van de medicijnen voorbij.

Het is beter om eerst bloed te meten en te kijken of de medicijnen geen probleem vormen.

 """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
