#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run aangifte with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='aangifte',
    version='3',
    url='https://pikacode.com/bthate/aangifte',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=' AANGIFTE - Men dient de antipsychotica ook toe voor het blokkeren van de receptoren, opzettelijke benadeling van de gezondheid.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["kern"],
    packages=["aangifte"],
    scripts=["bin/aangifte", ],
    long_description="""

op datum ... doet bij de politie te ... aangifte:

 Naam                        : 

 Voornamen                   : 

 Geboortedatum               : 

 Adres                       : 

 Woonplaats                  : 

 Postcode                    : 

 Telefoon                    : 


tegen de verdachte:


 Naam                        : 

 Voornaam/initialen en titel : 

 Geboortedatum               : 

 Adres                       : 

 Woonplaats                  : 

 Postcode                    : 

 Functie                     : 

 Werkgever                   : 



 Datum/tijdstip plegen feit: van ... tot ...

 Plaats van het feit : 

 Omschrijving incident feit:  

  1) Antipsychotica blokkeren de receptoren en benadelen daarmee de gezondheid.
  2) Men dient de antipsychotica ook toe voor het blokkeren van de receptoren, opzettelijke benadeling van de gezondheid.
  3) Behandeling met antipsychotica is langdurige opzettelijke benadeling van de gezondheid.

 Aankruisen welk artikel en wet van toepassing is.

  [x] Mishandeling  - Wetboek van Strafrecht 300 lid 4 

 Ik verzoek om een bewijs van aangifte.

 Naam aangever:  ...


 Handtekening: 

    ...

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
