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

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='apoclaim',
    version='3',
    url='https://pikacode.com/bthate/apoclaim',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="""  Een nano bloedmeter is wat we nodig hebben, een bloedglucose meter meet nu in de milli. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["cored", ],
    scripts=["bin/apo", "bin/apo-local", ],
    packages=['apo',
              'apo.plugs',
             ],
    long_description = """ 

POGING nummer 202358 http://pypi.python.org/pypi/apoclaim  (820 days) #vvd #apotheker #meds
SUICIDE nummer 4047 http://pypi.python.org/pypi/apoclaim (820 days) #pvda #apotheker #meds

Hedendaagse medicijnen vereisen dat men bijhoud hoe de medicijnen op je
inwerken.  De arts zal je niet waarschuwen voor de bijwerkingen waar je op
moet letten, zodat je niet weet of symptomen het resultaat zijn van je ziekte of
van je medicijnen. Nu is het zo dat men aan je gedragingen afleest wat je ziekte is
en aan de hand daarvan de diagnose stelt, waarna men de juiste medicijnen probeert
voor te schrijven. Vaak een kwestie van trial en error, waarbij men nog maar moet
kijken hoe de medicijnen op de persoon inwerken.

Het is de bedoeling om later een bloedmeter te koppelen aan dit programma
zodat men een overdosis of een tekort aan bepaalde stoffen in je bloed kan
waarnemen VOORDAT ze een probleem worden. Een bloedmeter kan dan ook inzicht
geven in welke lichaamseigen stoffen een invloed hebben op gedrag.

Een nano bloedmeter is wat we nodig hebben, een bloedglucose meter meet nu
in de milli.

De apotheker is verantwoordelijk voor eventuele medicijnbewaking van de
patient en zal dus ook VOORDAT er bijwerkingen onstaan al het bloed moeten
meten.

http://pypi.python.org/pypi/apoclaim

""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
