#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run ggz with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='ggz',
    version='8',
    url='https://pikacode.com/bthate/ggz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" Behandeling met antispychotica is langdurige opzettelijke benadeling van de gezondheid met de dood ten gevolge. ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["meds"],
    scripts=["bin/ggz"],
    packages=['ggz'],
    long_description="""

(F)ACT bied niet de noodzakelijke verpleging die behandeling met antipsychotica verantwoord maken:

 1) verpleging naar gelang de situatie - meer zorg naarmate de situatie erger is, is niet preventief.
 2) niet 7 x 24 uurs verpleging - in het weekend en avonduren niet aanwezig.
 3) psychiater is niet op de hoogte van de situatie van.
 4) behandelovereenkomsten zijn niet volledig.
 5) geen snelle terugbrenging naar ziekenhuis mogelijk.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
