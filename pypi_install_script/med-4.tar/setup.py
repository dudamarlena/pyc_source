#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run campagne with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='med',
    version='4',
    url='https://pikacode.com/bthate/med',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" which way to turn. ",
    license='MIT',
    zip_safe=True,
    install_requires=["medz",],
    scripts=["bin/med", ],
    packages=["med", ],
    long_description = """ 

::

 Ontleden (taalkundig)		Allesomvattend
 Logica				Intuïtief
 Detail georiënteerd		Breed georiënteerd
 Weloverwogen			Gevoelsmatig
 Rationeel			Innerlijk bewustzijn
 Methodisch			Creativiteit
 Geschreven taal		Inzicht
 Numerieke vaardigheden/orde	Ruimtelijk inzicht
 Feiten belangrijk		Beelden belangrijk
 Beredeneert			Verbeelding
 Weet de naam			Weet de functie
 Gericht op realiteit		Gericht op fantasie
 Wetenschappelijk		Muziek, kunst
 Wiskunde en wetenschap		Filosofie & religie
 Woord en taal			Symbolen en beeld
 Herkent			Waardeert
 Proactief			Reactief, passief
 Volgordelijk			Gelijktijdig
 Verbale intelligentie		Praktische intelligentie
 Bedenkt strategieën		Bedenkt mogelijkheden
 Veilig/safe			Neemt risico’s
 Heden en verleden		Heden en toekomst
 Weet				Gelooft
 Intellectueel			Zintuiglijk
 Analytisch			Geheel overziend
 

""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
