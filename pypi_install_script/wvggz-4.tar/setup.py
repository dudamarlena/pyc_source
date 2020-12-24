#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3:
    print("you need to run madbot with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='wvggz',
    version='4',
    url='https://bitbucket.org/bthate/wvggz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Met de WvGGZ pleegt men strafbare feiten.",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=['obot'],
    scripts=["bin/wvggz"],
    packages=[],
    long_description='''
WvGGZ
#####

Geachte <naam advocaat>,

ik ben Bart Thate, een 50 jaar oude schizofreen.

Ik schrijf u om naar uw mening te vragen omtrend de gedwongen behandeling die men met de Wet verplichte GGZ onder wettelijk voorschrift gaat leveren.
Zou het voor u mogelijk zijn om een inschatting te maken welke strafbare feiten men daar pleeft als deze zorg niet voor het wettelijk voorschrift tot niet-strafbaar worden verklaart ?

Argument is dat een GGZ patient kan vrezen dat men in de verplichte zorg zoals omschreven in de WvGGZ strafbare feiten gaat plegen.
Argument is dat een voorstel tot deze zorg bedreiging met zware mishandeling is, zoniet bedreiging met enig misdrijf op het leven gericht.
Argument is dat het niet medicijnen maar gif betreft en gif toedienen een misdrijf tegen het leven gericht is.
Argument is dat men een wettelijk voorschrift tot het toedienen van medicijnen niet kan gebruiken voor het toedienen van gif

Omdat de koning al geinformeerd is dat het hier niet medicijnen betreft maar gif, is er aangifte gedaan tegen de koning voor het laten plegen van genocide misdrijven (impotent maken, folteren, doden).
Dit programma is voor het voor de rechter halen van mensen die onder BOPZ met gif hebben behandeld of zich vrijwillig hebben laten behandelen onde BOPZ dreiging.

Dat antipsychotica gif zijn is te vinden op de website van het Europeese Chemicals Agency:

zie https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831 (clozapine)

Ik denk zelf aan de volgende misdrijven:

gijzeling
=========

* GGZ patienten zonder schuldig bevinding opsluiten is gijzeling.

282a.1 Hij die opzettelijk iemand wederrechtelijk van de vrijheid berooft of beroofd houdt met het oogmerk een ander te dwingen iets te doen of niet te doen wordt als schuldig aan gijzeling gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

282a.2 Indien het feit de dood ten gevolge heeft wordt hij gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

mishandeling
============

300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

* De medicijnen blijken gif te zijn

verzwijging
===========

174.1 Hij die waren verkoopt, te koop aanbiedt, aflevert of uitdeelt, wetende dat zij voor het leven of de gezondheid schadelijk zijn, en dat schadelijk karakter verzwijgende, wordt gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

174.2 Indien het feit iemands dood ten gevolge heeft, wordt de schuldige gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

* De arts informeert de patient niet dat het een gif betreft.
* De arts verzwijgt het schadelijk karakter van zijn medicijnen.

moord
=====

285.1 Bedreiging met enig misdrijf tegen het leven gericht wordt gestraft met gevangenisstraf van ten hoogste twee jaren of geldboete van de vierde categorie.

287 Hij die opzettelijk een ander van het leven berooft, wordt, als schuldig aan doodslag, gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

289 Hij die opzettelijk en met voorbedachten rade een ander van het leven berooft, wordt, als schuldig aan moord, gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

294.1 Hij die opzettelijk een ander tot zelfdoding aanzet, wordt, indien de zelfdoding volgt, gestraft met een gevangenisstraf van ten hoogste drie jaren of geldboete van de vierde categorie.

* Dodelijke stof toedienen met het leveren van onverantwoorde zorg erbij is moord.

Zou u in staat zijn om te bepalen welke misdrijven in de geleverde zorg plaats kunnen vinden, en de dreiging daarmee, voor een rechter aannemelijk maken ?
Dat een potentiele patient werkelijk kan vrezen dat er misdrijven in de geleverde zorg gaan plaats vinden ?


bij voorbaat dank voor uw reactie,


Bart Thate

bthate@dds.nl, thatebart@gmail.com 


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
