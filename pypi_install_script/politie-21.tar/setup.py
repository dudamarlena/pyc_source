#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run politie with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='politie',
    version='21',
    url='https://pikacode.com/bthate/politie',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" POLITIE - met mishandeling word gelijkgesteld opzettelijke benadeling van gezondheid. """,
    license='MIT',
    zip_safe=False,
    scripts=["bin/politie"],
    install_requires=["meds"],
    packages=['politie'],
    long_description = """ 

EVRM


Artikel 3 - Verbod van foltering

Niemand mag worden onderworpen aan folteringen of aan onmenselijke of vernederende behandelingen of bestraffingen. 


OORDEEL


Behandeling met antipsychotica is langdurige opzettelijke benadeling van de gezondheid met de dood ten gevolge.


STRAFRECHT


Artikel 300.4 - Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.


LANGDURIGE


Zolang een arts de bloedspiegel van een medicijn niet meet, word de toestand van vergiftiging niet opgeheven.


OPZETTELIJKE


Opzet als bedoeling is de vorm van opzet die veel te maken heeft met boos opzet. De verdachte heeft een bepaald doel voor ogen en daarom pleegt hij een strafbaar feit. De verdachte weet en wil dat een bepaald gevolg intreedt. Het is bij opzet als bedoeling niet vereist dat het beoogde gevolg ook daadwerkelijk optreedt. Als er wordt gesproken over opzet als bedoeling, dan komt dit, naast het bestanddeel opzet, in een delictsomschrijving vaak tot uiting door het bestanddeel oogmerk. Het gaat dan om het doel dat de verdachte heeft. Om dit doel te bereiken pleegt de verdachte willens en wetens een strafbaar feit.

“Men dient de antipsychotica toe voor het blokkeren van de receptoren, opzettelijke benadeling van de gezondheid.”

“De staat pleegt opzettelijke benadeling van de gezondheid met als oogmerk het verminderen van gevaar voor de samenleving of de persoon zelf.”

“De arts pleegt opzettelijke benadeling van de gezondheid met als oogmerk het verminderen van de symptomen van schizofrenie.”


Om te kunnen spreken van opzet als zekerheidsbewustzijn moet het gaan om een gevolg waar de wil van de dader niet op is gericht. Met een bepaalde handeling heeft de dader een bepaald doel willen bereiken, maar als rechtstreeks gevolg van deze handeling is het ongewilde gevolg ingetreden. Wanneer de dader wist dat dit gevolg in zou treden, dan is er sprake van opzet als zekerheidsbewustzijn, simpeler gezegd: het is niet het hoofddoel van de verdachte, maar de verdachte weet wel zeker dat dit ongewenste gevolg in zal treden.

“Bijwerkingen als ongewenst gevolg waar men van op de hoogte is.”

“Ontbrekende verpleging met gevolgen waar men van op de hoogte is.”


BENADELING VAN DE GEZONDHEID


Antipsychotica blokkeren de receptoren, waarna de hersencellen niet meer functioneren en dus afsterven. Afsterven van hersencellen veroorzaakt krimp van het brein.

After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume.

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/


MET DE DOOD TEN GEVOLGE


Langdurige opzettelijke banadeling van de gezondheid resulteert in dood door suicide.


""", 

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
