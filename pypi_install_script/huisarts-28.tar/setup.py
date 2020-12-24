#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run huisarts with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='huisarts',
    version='28',
    url='https://pikacode.com/bthate/huisarts',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" HUISARTS - Behandeling met medicijnen die de hersenen vergiftigen is langdurige opzettelijke benadeling van de gezondheid tot de dood erop volgt. """,
    license='MIT',
    zip_safe=False,
    install_requires=["rechter"],
    scripts=["bin/huisarts"],
    packages=['huisarts',
             ],
    long_description = """ 

PRAKTIJK

1) patient meld bijwerkingen die duiden op vergiftiging (flauwvallen, slecht zien)
2) patient word doorverwezen voor klacht
3) arts meet niet de medicijnspiegel
4) patient is vergiftigt en/of zit zonder medicijnen
5) patient pleegt suicide


MILDE SYMPTOMEN VAN VERGIFTIGING

1) gedragsveranderingen (bijv., rusteloosheid, crankiness)
2) diarree
3) duizeligheid
4) slaperigheid
5) vermoeidheid
6) hoofdpijn
7) verlies van eetlust
8) kleine huid- of oogirritaties
9) misselijkheid of maagklachten
10) passen hoest (hoest die komt en gaat)
11) pijn of stijfheid in de gewrichten
12) dorst

MATIGE SYMPTOMEN

1) wazig zicht
2) Verwarring en desoriëntatie
3) ademhalingsproblemen
4) kwijlen
5) overmatig tranen
6) koorts
7) lage bloeddruk (hypotensie)
8) verlies van spiercontrole en spiertrekkingen
9) bleekheid (bleekheid) of gespoeld of gelige huid
10) aanhoudende hoest
11) snelle hartslag
12) toevallen
13) ernstige diarree
14) ernstige misselijkheid
15) maagkrampen
16) zweten
17) dorst
18) bevend
19) zwakte

BELANGERIJKSTE SYMPTOMEN

1) hartstilstand
2) krampen
3) diffuse intravasale stolling (mits ongecontroleerde bloeden of bloedstolling veroorzaakt)
4) oesofageale vernauwing (vernauwing van het orgaan dat voedsel uit de mond draagt naar de maag)
5) koorts (vaak hoog)
6) onvermogen om te ademen
7) versnelde ademhaling (snelle ademhaling)
8) verlies van bewustzijn
9) spiertrekkingen (ongecontroleerd en ernstige)
10) snelle hartslag met een lage bloeddruk
11) ademnood dat intubatie vereist (betreft het passeren van een buis naar beneden de luchtpijp [luchtpijp] om de longen te ademen bijstand te verlenen; mechanische beademing [dwz een ventilator] kan nodig zijn)
12) epileptische aanvallen die niet reageren op de behandeling (de zogenaamde status epilepticus)
13) dorst (vaak extreme)

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
