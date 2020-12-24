#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run meds with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='meds',
    version='1215',
    url='https://pikacode.com/bart/meds',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='Opzettelijke benadeling van de gezondheid',
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["feedparser==5.2.1","beautifulsoup4", "sleekxmpp", "setuptools", "pyasn1", "pyasn1-modules"],
    scripts=["bin/meds", "bin/meds-ps", "bin/meds-sed", "bin/meds-docs", "bin/meds-cleandocs", "bin/meds-do", "bin/meds-local", "bin/meds-test", "bin/meds-doctest"],
    packages=['meds',
              'meds.bots',
              'meds.cbs',
              'meds.plugs',
              'meds.run',
              'meds.utils'
             ],
    long_description="""

LEVENSGEVAAR
############

Antipsychotica zijn antagonisten, medicijnen die receptoren in de hersenen blokkeren. Dit blokkeren is een benadeling van de gezondheid, er treed een
verminderde werking op van de neurotransmitter die geblokkeerd word. Dat de arts deze medicijnen inzet
voor hun schadelijke werking, maakt het toedienen ervan opzettelijke benadeling van de gezondheid. Er is dus geen sprake van behandeling maar van
mishandeling.

Als men naast de mishandeling ook nog eens de noodzakelijke verpleging achterwege laat, dan genereert men levensgevaar voor de
patient:

* als een arts ontkent dat hij aan het mishandelen is (dood door overdosis).
* als een arts de bloedspiegel van een medicijn niet meet (dood door nalatigheid).
* eerst een afspraak maken voordat je een crisis kan melden, zodat ook in acute crisis er geen verpleging is (dood door vergiftiging).

EVRM
####

“After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume when compared with the sham group.”

In 2012 heb ik het Europeese Hof voor de Rechten van de Mens :ref:`aangeschreven <verzoek>` om een klacht 
tegen Nederland in te dienen. De klacht betrof het afwezig
zijn van verpleging in het nieuwe ambulante behandeltijdperk van de GGZ.
:ref:`uitspraak <uitspraak>` was niet-ontvankelijk. Voor verder correspondentie zie :ref:`hier <correspondentie>`.

Het is niet mogelijk voor de koning om :ref:`tussenkomst` te verlenen als het de
amublantisering van de GGZ in Nederland betreft. Ik heb ook een :ref:`brief <minister>` van de minister kunnen 
krijgen na aandringen van de koningin waarin zij ontkent dat de ambulante zorg problematisch is.
De IGZ heeft wel erkent verantwoordelijk te zijn voor ambulante zorg, zowel voor vrijwillig als onder de BOPZ behandelde
patienten, zie :ref:`quote <absoluut>`.

(F)ACT, de methode die gebruikt word voor zorg aan mensen met Ernstige Psychiatrische Stoornissen, bied niet de noodzakelijke verpleging:

* verpleging naar gelang de situatie - meer zorg naarmate de situatie erger is, is niet preventief (stepped care).
* geen 7 x 24 uurs verpleging - in het weekend en avonduren niet aanwezig (meeste suicides in het weekend).
* behandelovereenkomsten zijn niet volledig (verplichtingen niet vastgelegd).
* Een SPV-er 1 keer in de 3 maanden is veels te weinig, de symptomen die men opdoet door de mishandeling worden niet tijdig gezien.

LOGGEN
######

De controle op de geleverde verpleging is zo slecht dat het aan een slachtoffer
is om bij te houden hoe het met toename/afname van symptomen gaat.
Echter Het slachtoffer is helemaal niet in staat om symptomen bij te houden, het is aan de mantelzorger 
om te constateren dat een slachtoffer in een toestand van vergiftiging verkeerd.
Het is, zeker als slachtoffer, zaak om bij te houden hoe het met symptomen
is, vooral over een periode van tijd.
Een patient kan te maken krijgen met positieve en negatieve symptomen, symptomen van vergiftiging, onthoudingsverschijnselen en ernstige
bijwerkingen, zie :ref:`hier <symptomen>`.

Je kan het log command gebruiken om een symptoom of verschijnsel te registreren:

* log <txt>
* log <txt> +5
* log <txt> -2

Het find command om log terug te zoeken:

* find log
* find log=slaap
* find email From=om.nl From Subject Date start=2013-01-01 end=2013-02-01

Om over een periode te kunnen zoeken:

* today log
* week log
* week log=wiet

""",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
