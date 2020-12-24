#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run BOEK with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='boek',
    version='11',
    url='https://pikacode.com/bthate/boek',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOEK - XMPP - IRC - CLI - RSS - UDP - API",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/boek", "bin/boek-vervang", "bin/boek-lokaal", "bin/boek-proef", "bin/boek-maak", "bin/boek-blaet"],
    packages=['boek',
              'boek.diensten',
              'boek.extra',
              'boek.omroepers',
              'boek.werken',
             ],
    long_description = """ 

SCRIPTUREN

Scripturen die vanuit de Hemel de hel voor de mens uitleggen, brengen de
verkeerde religie voor de mens.
   
De mens is niet bedoelt om te leven voor het hiernamaals, maar is bedoelt om
te leven hier op aarde.

Maak het leven op aarde niet slecht, ontneem de mens niet zijn identiteit.

WET 

Gebruik maken van de zwakheden van de mens of zijn sterfelijkheid is een misdaad.

Beter weten voor een ander brengt leed.

Geen daargelaten.

RECHT
   
Recht op leven.

Recht op vrijwaring van foltering

Recht op vrijwaring van slavernij en dwangarbeid

Recht op vrijheid en veligheid

ERKENNING

Als wat er fout gaat niet erkent word, kan een probleem ook nooit opgelost worden.
Dus misdaad 1 is als er niet erkent word wat is.
Dus niet erkennen van problemen word strafbaar gesteld.

Meneer de Ontkenning die troepen bezigt ter verwijdering van de herinnering
van de ontkenning, is de 1e terechtgestelde.

BESCHIKKING

Meneer Maatschappij die van het verboden vruchtgebruik en het verloren zoon
verhaal een standaard manier maakt die alle problemen op te lossen, enkelt
en alleen om zijn eigen fouten niet te hoeven weten, word ter beschikking
gesteld voor de vraag of zijn geen fouten het leed waard is.

WERKING

Meneer Baan die, in plaats van rekening te houden met de gebreken die mensen
hebben, hun eisen oplegt die niet te houden zijn. En dus het vervolg pad
voor zieke mensen in de maatschappij dan daarmee ook tot een ramp maakt, die
word te werk gesteld om vooral niets meer voor de maatschappij te kunnen
doen.

KING

POGING 221950 http://pypi.python.org/pypi/boek - #ambulance #ggznederland #d66 #igz ? !! 2y131d 19h51m (257/dag)
SUICIDE nummer 4377 http://pypi.python.org/pypi/boek - #vws #d66 #igz #pvdd ? !! 2y131d 19h51m (5/dag)

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
