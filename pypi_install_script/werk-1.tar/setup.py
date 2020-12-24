#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run kamer with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='werk',
    version='1',
    url='https://pikacode.com/bart/werk',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" WERK - geen daadwerkelijk rechtsmiddel aanwezig """,
    license='MIT',
    zip_safe=False,
    scripts=["bin/werk",],
    install_requires=["meds"],
    packages=['werk',
             ],
    long_description = """ 

Op basis van een wettelijk voorschrift  is deze mishandeling niet strafbaar:

* Artikel 42 Niet strafbaar is hij die een feit begaat ter uitvoering van een wettelijk voorschrift

Een wet die tot behandeling verplicht en op die manier de mishandeling niet strafbaar maakt, maakt niet dat men geen misdrijf pleegt. Er word nog steeds een misdrijf gepleegd, waar men schuldig aan is en wat direct gestopt dient te worden. Het is de plicht van het Openbaar Ministerie om op te treden als er strafbare feiten worden gepleegd, ook als vervolging tot niet strafbaar leid, met als argument dat als het plegen van mishandeling niet gestopt word er geen einde komt aan de mishandeling.

Met het aannemen van de Wet verplichte Geestelijke Gezondheidzorg maakt de Tweede Kamer de behandeling met antipsychotica verplicht en daarmee mishandeling gepleegd door het toedienen van voor het leven en de gezondheid schadelijke stoffen niet strafbaar. De Tweede Kamer maakt zich hiermee schuldig aan het op grote schaal mogelijk maken van mishandeling.

De Wet verplichte GGZ dient u daarom niet aan te nemen en om huidige mishandelingen te stoppen dient u terstond het Openbaar Ministerie ontvankelijk te maken voor elke patient die zijn mishandeling door de strafrechter gestopt wil zien worden.


                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
