#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run medz with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='medz',
    version='24',
    url='https://pikacode.com/bthate/medz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="medicine effect registration program",
    license='MIT',
    zip_safe=True,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/medz", ],
    packages=['medz',
              'medz.bots',
              'medz.plugs',
              'medz.extra',
              'medz.service',
              'medz.utils',
             ],
     long_description = """ 

####################################
MEDICINE EFFECT REGISTRATION PROGRAM
####################################

Positive symptoms:

 1) delusions
 2) hallucinations
 3) confused thinking
 4) excitement

To fight these symptoms medicine are given that block the receptors in the
brain, making them non-functional. Non-functional brains give these
negative symptoms:

 1) lack of emotions
 2) less social contact
 3) no initiative
 4) no concentration
 5) no motivation
 6) no energy

Problem with negative symptoms are that the patient gets the blame of them.

Affective symptoms:

 1) Depression
 2) Manical

Makes social paranoid. Always negative interpreting.

""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
