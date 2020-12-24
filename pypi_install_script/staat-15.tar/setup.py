#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run staat with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='staat',
    version='15',
    url='https://pikacode.com/mila/staat',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" Behandeling met antispychotica is langdurige opzettelijke benadeling van de gezondheid met de dood ten gevolge. """,
    license='MIT',
    zip_safe=False,
    install_requires=["rechter"],
    scripts=["bin/staat",],
    packages=['staat'],
    include_package_data=True,
    long_description = """ 

Tweede Kamer der Staten-Generaal
Postbus 20018
2500 EA Den Haag



Geachte Tweede Kamerleden,

uitvoering van wettelijk voorschrift waarbij de rechter niet vervolgt en mishandeling mogelijk maakt, is daarmee WEL aan het mishandelen
en dient voor de strafrechter te verschijnen. Het niet vervolgen van het mishandelen van mensen met antipsychotica maakt dat er geen einde is aan 
de mishandeling behalve door suicide.

Wat op basis van artikel 42 mishandelt dient voor de strafrechter te komen voor mishandeling.
Wat op basis van vrijwilligheid mishandelt ook.

Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

Er zijn in Nederland 150 duizend mensen die elke dag mishandelt word en die hebben recht om hun mishandeling voor de rechter
gemotiveerd te zien. Om de mishandeling gestopt te zien. Een wet die nog meer mensen mishandelt is niet denkbaar, niet straffen 
van wat mishandelt ook niet.

Ik verwacht dat u de Wet verplichte GGZ niet aanneemt omdat het mishandeling onder de wet is.
Ik verwacht ook dat wat nu mishandelt een rechtsgang langs de rechter maakt.

""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)

