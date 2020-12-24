#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run shout with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='shout',
    version='4',
    url='https://pikacode.com/milla/shout',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='shout - when you need to report circumstances that need to be mentioned.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=['distribute', 'sleekxmpp', 'oolib', 'newevidence'],
    scripts=['bin/shout',
            ],
    packages=['shout',
              'shout.plugs',
             ],
    long_description = """ When your circumstances are made in negative way and those responsible for those situations need to be hold accountable for it, this tool will allow you to keep a log of the making of those cirumstances. """,
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
