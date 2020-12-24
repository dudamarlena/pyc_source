#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run GGZ Claim with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='ggzclaim',
    version='39',
    url='https://pikacode.com/bthate/ggzclaim',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" "Van alle personen die zich suïcideren is ongeveer 40% op moment van suïcide in behandeling in de ggz." - Rijksinstituut voor Volksgezondheid en Milieu. """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["cored", ],
    scripts=["bin/ggz", ],
    packages=['ggz',
              'ggz.plugs',
             ],
    long_description = """

Kunt u maatregelen nemen om ervoor te zorgen dat psychiatrische patiënten met hoge psychische nood
ook in het weekend voldoende hulp krijgen?

Antwoord op vraag 4.

Personen die in acute psychische nood verkeren kunnen 24 uur per dag en zeven dagen in de week terecht bij
de crisisdienst van een psychiatrische instelling. Voor personen die kampen met acute suïcidale problemen
bieden de Stichting Ex6 en de Stichting 113online via de telefoon en via internet anoniem crisiscounseling
eveneens met een 24 uur bereikbaarheid. Er wordt dus in voldoende mate voorzien in hulpverlening aan mensen met
acute psychische problemen die in het weekend opspelen.

"Op grond van al deze argumenten en bevindingen is besloten dat FACT teams
geen eigen 24-uurs bereikbaarheid hebben." - J.R. van Veldhuizen, voorzitter Stichting CCAF

De patient moet zelf in het weekend via 112 de crisis dienst van de GGZ zien te bereiken. Voor een patient met 
een Ernstige Psychiatrische Aandoening kompleet onmogelijk om te doen. In acute psychische nood kan men NIET terecht 
bij een crisisdienst.

POGING nummer 30399 http://pypi.python.org/pypi/ggzclaim (792 days)

                       """, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
