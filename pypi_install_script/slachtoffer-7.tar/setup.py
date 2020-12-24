#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run ss with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='slachtoffer',
    version='7',
    url='https://pikacode.com/bthate/slachtoffer',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Status Slachtoffer 69389/12. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["rechter", ],
    scripts=["bin/ss", ],
    packages=['ss',
              'ss.plugs',
             ],
    long_description = """

De patient moet zelf in het weekend via 112 de crisis dienst van de GGZ zien te bereiken. Voor een patient met 
een Ernstige Psychiatrische Aandoening kompleet onmogelijk om te doen. In acute psychische nood kan men NIET terecht 
bij een crisisdienst.

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
