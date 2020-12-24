#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run elib with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='evidence',
    version=5,
    url='https://pikacode.com/milla/evidence',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='evidence - tool for registering effects of medicine.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=['botz'],
    scripts=['bin/evidence',
            ],
    packages=['evidence',
             ],
    long_description = """ 

This is a medicine effect registration program aimed at giving insight into
the effects of modern medicine on the health of humans. 

Keeping track of side effects indicated by the leaflet will be of the greatest importance in
the proper treatement of illnesses with the medicine used today.

In the meantime we'll be waiting for a blood measurement device that will
allow us to measure the amount of medicine particles in the blood as well as
neurotransmitters, hormones etc.


 """,
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
