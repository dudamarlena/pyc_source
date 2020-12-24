#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run campagne with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='igz',
    version='8',
    url='https://pikacode.com/bthate/igz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" IGZ - niet de verboden maar de geboden vrucht. medicijnen eerst. ",
    license='MIT',
    zip_safe=False,
    install_requires=["kern",],
    packages=["igz", ],
    long_description = """ 

U schrijft onder andere: "de Inspectie heeft onder de BOPZ allerlei taken om
toe te zien op verantwoorde zorg voor de patient. Het zelfde zou moeten
gelden voor ambulant behandelde patienten...".

"Daar heeft u absoluut gelijk in, en dat is ook het geval: de Inspectie ziet
toe op alle zorg en behandeling die verleend wordt, binnen de GGZ maar ook
in andere vormen van gezondheidszorg; aan patienten die zijn opgenomen maar
ook aan patienten die in ambulante behandeling zijn; ongeacht of iemand
vrijwillig of krachtens de wet BOPZ wordt behandeld."

Hoe is de IGZ van plan om onder de WvGGZ de kwaliteit van de behandeling te
controleren nu de multidisciplinaire commissie uit de wet geschrapt is ?

""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
