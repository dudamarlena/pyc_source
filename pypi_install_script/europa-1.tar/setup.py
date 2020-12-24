#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run europa with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='europa',
    version='1',
    url='https://pikacode.com/bart/europa',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" EUROPA - dreiging met de dood is foltering """,
    license='MIT',
    zip_safe=False,
    scripts=["bin/europa",],
    install_requires=["meds"],
    packages=['europa',
             ],
    long_description = """ 

Artikel 3. Verbod van foltering

Artikel 2. Recht op leven

Artikel 5. Recht op vrijheid en veilighed

Artikel 13. Recht op een daadwerkelijk rechtsmiddel

Artikel 17. Verbod van misbruik van recht

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
