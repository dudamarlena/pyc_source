#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run burgemeester with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='burgemeester',
    version='1',
    url='https://pikacode.com/bart/burgemeester',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" BURGEMEESTER - mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen """,
    license='MIT',
    zip_safe=False,
    install_requires=["meds"],
    packages=['burgemeester',
             ],
    long_description = """ 

RONDJE STRAFRECHTER

1) gemeente dwingt de politie tot aangifte van mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen
2) gemeente dwingt openbaar ministerie tot vervolging
3) gemeente pleit mishandeling bij de rechter
4) mishandeling bewezen
5) schuld bewezen
6) verdachte beroept zich op Artikel 42
7) verdachte geeft toe dat hij, beroepende op Artikel 42, langdurig en op grote schaal heeft mishandelt

STRAFBAARHEID

1) Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.
2) Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

RECHTVAARDIGHEIDSGRONDEN

1) Artikel 42 Niet strafbaar is hij die een feit begaat ter uitvoering van een wettelijk voorschrift.
2) Vrijwillig ingestemde behandeling
3) Wilsonbekwaam

SCHADE

1) Antipsychotica blokkeren de receptoren, waarna de hersencellen niet meerfunctioneren en dus afsterven.
2) Afsterven van hersencellen veroorzaakt krimp van het brein.
3) Afsterven van hersencellen zorgt voor een dusdanig disfunctioneren van het geestesvermogen dat men uit psychische nood de dood verkiest.

TEKENEN VAN SCHADE

De gevolgen van het behandelen van antipsychotica zijn de negatieve symptomen van schizofrenie:

1) weinig emotie
2) minder sociale contacten
3) gebrek aan initief
4) gebrek aan aandacht en concentratie
5) weinig gemotiveerd
6) weinig energie
7) depressieve symptomen (angst)
8) manische symptomen (druk, vol energie, weinig slaap nodig)

GEEN VERPLEGING

De gevolgen van behandeling zonder de noodzakelijke verpleging zijn symptomen van vergiftiging:

1) Verwardheid.
2) Delirium.
3) Duizeligheid.
4) Dubbelzien.
5) Gedesorienteerd in plaats, tijd en persoon.
6) Hallucinaties, vooral auditieve.
7) Oorsuizen.
8) Tijdelijke gehoorverlies.
9) Sufheid.
10) Coma.

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
