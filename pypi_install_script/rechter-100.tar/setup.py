#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run rechter with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='rechter',
    version='100',
    url='https://pikacode.com/rechter/rechter',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" RECHTER - Behandeling met medicijnen die de hersenen vergiftigen is langdurige opzettelijke benadeling van de gezondheid tot de dood erop volgt. ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/rechter", "bin/rechter-local", "bin/rechter-sed", "bin/rechter-udp", "bin/rechter-do", "bin/rechter-docs"],
    packages=['rechter',
              'rechter.bots',
              'rechter.extra',
              'rechter.plugins',
              'rechter.test',
              'rechter.utils',
             ],
    long_description="""

SCHULD

* De arts adviseerd niet over de giftige werking van het medicijn.

* Zolang een arts de bloedspiegel van een medicijn niet meet, word de toestand van vergiftiging niet opgeheven.

* Het oordeel van de arts over het ziektebeeld van de patient houd de werking van de medicijnen buiten beschouwing.

STRAFBAARHEID

* Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

* Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.


UITSLUITING

* Artikel 42 Niet strafbaar is hij die een feit begaat ter uitvoering van een wettelijk voorschrift.

* Vrijwillig ingestemde behandeling

* Wilsonbekwaam

SCHADE

* Antipsychotica blokkeren de receptoren, waarna de hersencellen niet meerfunctioneren en dus afsterven.

* Afsterven van hersencellen veroorzaakt krimp van het brein.

* Afsterven van hersencellen zorgt voor een dusdanig disfunctioneren van het geestesvermogen dat men uit psychische nood de dood verkiest.

PSYCHISCH

* Afstervende hersen geven psychotische verschijnselen

REFERENTIE

"After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated
monkeys had an equivalent and highly significant 8% to 11% decrease in fresh 
brain weight and volume."

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
