#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run OMNL with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='omnl',
    version='4',
    url='https://pikacode.com/bthate/omnl',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["meds"],
    packages=['omnl'],
    scripts=["bin/omnl",],
    long_description=""" 

Artikel 302:

1) Hij die aan een ander opzettelijk zwaar lichamelijk letsel toebrengt, wordt, als schuldig aan zware mishandeling, gestraft met gevangenisstraf van ten hoogste acht jaren of geldboete van de vijfde categorie.
2) Indien het feit de dood ten gevolge heeft, wordt de schuldige gestraft met gevangenisstraf van ten hoogste tien jaren of geldboete van de vijfde categorie.

		""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
