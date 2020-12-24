#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run maak with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='maak',
    version='4',
    url='https://pikacode.com/milla/maak',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='maak - Verhaal der Gemaakten.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=['distribute', 'sleekxmpp', 'oolib', 'newevidence'],
    scripts=['bin/maak',
            ],
    packages=['maak',
              'maak.drivers',
              'maak.plugs',
             ],
    long_description = """ Verhaal der Gemaakten. """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
