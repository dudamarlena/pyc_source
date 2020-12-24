#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run gemeente with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='gemeente',
    version='30',
    url='https://pikacode.com/bart/gemeente',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="""Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.""",
    license='MIT',
    zip_safe=False,
    install_requires=["obj"],
    scripts=["bin/gemeente",],
    packages=['gemeente'],
    long_description = """ 

AANTAL OPNAMES

:: 

 TABEL 1	 Bopz-aanvragen in Nederland 2003-2013 (bron cijfers Raad voor de Rechtspraak)

 Type Bopz-aanvraag 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 verhouding 2013 vs. 2003

 IBS                6923   7402  7700  8002  8031  6610  7340  7422  7458  7377  7964 115%
 RM                 7371   8010  8600  8931  9381  9703 11558 12500 13235 13979 14902 202%

 Type RM

 - VM               3979   3916  4064  4163  4395  4712  5495  5690  5837  5937  6163 155%
 - MVV              3249   3133  3212  2678  2796  2712  3195  3455  3620  3705  3966 122%
 - VW               57      860  1256  1960  2081  2187  2755  3272  3689  4244  4699 -
 - Eigen Verzoek    86      101    68    78    72    63   112    77    86    92    65 76%
 - Observatie       0         0     0    52    37    29     1     1     0     0     0 -
 - Zelfbinding      0         0     0     0     0     0     0     5     3     1     9 -

 opnames            14294 15412 16300 16933 17412 16313 18898 19922 20693 21356 22866

 t.o.v. 2003        100   108   114   118   122   114   132   139   145   149   160

SOORTEN 

1) IBS: inbewaringstelling;
2) RM:  rechterlijke machtiging
3) VM:  voorlopige machtiging;
4) MVV: machtiging voortgezet verblijf;
5) VM:  voorwaardelijke machtiging

URL

 bron: http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf

BEDREIGEND

::

 Te laat komen - 10% , 1 maand 
 Te weinig solliciteren - 10% , 1 maand 
 Huiswerk niet af - 20% , 1 maand 
 Ongewenst gedrag vertoont - 20% , 1 maand 
 Weigering van algemeen geaccepteerde arbeid - 100% , 2 maanden 
 In het geheel niet meewerken - 100% , 2 maanden 
 Verbaal geweld - 50% , 1 maand 
 Bedreiging - 25% , 1 maand



""", 
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
