#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run KONING with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='minister',
    version='38',
    url='https://pikacode.com/bart/minister',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Behandeling met medicijnen die de hersenen vergiftigen is langdurige opzettelijke benadeling van de gezondheid tot de dood erop volgt. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=["minister",],
    scripts=["bin/minister"],
    install_requires=["meds", "advocaat", "minister"],
    long_description=""" 

In Nederland draagt men zorg voor de meest kwetsbaren in Nederland door ze de volgende zorg te leveren, deze zorg mag niet geleverd worden want het zijn strafbare feiten die men pleegt:

 1) een interventie, bestaande uit een vorm van verzorging, bejegening, behandeling, begeleiding of bescherming;
 2) toediening van medicatie, vocht en voeding, regelmatige medische controle of andere medische handelingen;
 3) pedagogische of therapeutische maatregelen;
 4) opname in een accommodatie;
 5) beperking van de bewegingsvrijheid;
 6) afzondering of separatie in een daartoe geschikte verblijfsruimte;
 7) beperking van het recht op het ontvangen van bezoek of het gebruik van communicatiemiddelen;
 8) toezicht op betrokkene;
 9) onderzoek aan kleding of lichaam;
 10) controle op de aanwezigheid van gedrag beïnvloedende middelen;
 11) beperkingen in de vrijheid het eigen leven in te richten, die tot gevolg hebben dat betrokkene iets moet doen of nalaten.

 """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
