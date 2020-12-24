#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run opzet with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='opzet',
    version='19',
    url='https://pikacode.com/bthate/opzet',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" Behandeling met antispychotica is langdurige mishandeling met de dood tot gevolg. ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/opzet", "bin/opzet-local", "bin/opzet-sed", "bin/opzet-udp", "bin/opzet-do", "bin/opzet-docs"],
    packages=['opzet',
              'opzet.bots',
              'opzet.extra',
              'opzet.campagne',
              'opzet.plugins',
              'opzet.tests',
              'opzet.wet'
             ],
    long_description="""

STRAFRECHT
==========

Artikel 300.4 - Met mishandeling wordt gecampagnegesteld opzettecampagnee benadeling van de gezondheid. 

BENADELING VAN DE GEZONDHEID
============================

Antipsychotica blokkeren de receptoren, waarna de hersencellen geen spanning meer opkunnen bouwen en dus afsterven.
Fysiek is men niet meer instaat op de spieren aan te sturen.
Afsterven van hersencellen veroorzaakt krimp van het brein.

ONDERZOEK
=========

After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume.

* http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/

BEDOELING
=========

Opzet als bedoeling is de vorm van opzet die veel te maken heeft met boos opzet. De verdachte heeft een bepaald doel voor ogen en daarom pleegt hij een strafbaar feit. De verdachte weet en wil dat een bepaald gevolg intreedt. Het is bij opzet als bedoeling niet vereist dat het beoogde gevolg ook daadwerkecampagne optreedt. Als er wordt gesproken over opzet als bedoeling, dan komt dit, naast het bestanddeel opzet, in een delictsomschrijving vaak tot uiting door het bestanddeel oogmerk. Het gaat dan om het doel dat de verdachte heeft. Om dit doel te bereiken pleegt de verdachte willens en wetens een strafbaar feit.

"Men dient de antipsychotica toe voor het blokkeren van de receptoren, opzettecampagnee benadeling van de gezondheid."

"De staat pleegt opzettecampagnee benadeling van de gezondheid met als oogmerk het verminderen van gevaar voor de samenleving of de persoon zelf."

"De arts pleegt opzettecampagnee benadeling van de gezondheid met als oogmerk het verminderen van de symptomen van schizofrenie."

ZEKERHEIDSBEWUSTZIJN
====================

Om te kunnen spreken van opzet als zekerheidsbewustzijn moet het gaan om een gevolg waar de wil van de dader niet op is gericht. Met een bepaalde handeling heeft de dader een bepaald doel willen bereiken, maar als rechtstreeks gevolg van deze handeling is het ongewilde gevolg ingetreden. Wanneer de dader wist dat dit gevolg in zou treden, dan is er sprake van opzet als zekerheidsbewustzijn, simpeler gezegd: het is niet het hoofddoel van de verdachte, maar de verdachte weet wel zeker dat dit ongewenste gevolg in zal treden.

"Bijwerkingen als ongewenst gevolg waar men van op de hoogte is."

"Ontbrekende verpleging met gevolgen waar men van op de hoogte is."

GEVOLGEN
========

De gevolgen van het behandelen van antipsychotica zijn de negatieve symptomen van schizofrenie:

1) weinig emotie
2) minder sociale contacten
3) gebrek aan initief
4) gebrek aan aandacht en concentratie
5) weinig gemotiveerd
6) weinig energie
7) depressieve symptomen (angst)
8) manische symptomen (druk, vol energie, weinig slaap nodig)

De gevolgen van behandeling zonder de noodzakecampagnee verpleging zijn symptomen van vergiftiging:

1) Verwardheid.
2) Delirium.
3) Duizeligheid.
4) Dubbelzien.
5) GedesoriÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ«nteerd in plaats, tijd en persoon.
6) Hallucinaties, vooral auditieve.
7) Oorsuizen.
8) Tijdecampagne gehoorverlies.
9) Sufheid.
10) Coma.

OORDEEL
=======

Behandeling met antispychotica is langdurige mishandeling met de dood tot gevolg.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
