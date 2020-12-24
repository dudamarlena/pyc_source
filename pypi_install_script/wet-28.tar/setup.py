#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run wet with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='wet',
    version='28',
    url='https://pikacode.com/bthate/wet2',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="XMPP - IRC - CLI - RSS - UDP - REST",
    license='MIT',
    include_package_data=False,
    zip_safe=True,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/wet", ],
    packages=['wet',
              'wet.bots',
              'wet.plugs',
              'wet.extra',
              'wet.service',
              'wet.utils',
             ],
    long_description=""" 

WET 1 - Noem jezelf geen God als je geen respect hebt voor de schepping.

WET 2 - Ga vanuit onsterfelijkheid niet de sterfelijke mens duiden op zijn sterfelijkheid.

WET 3 - Laat een ieder zoals hij is, want veranderen brengt meer leed dan goed.

WET 4 - Gebruik leed niet om de mens naar God te leiden.

WET 5 - De mens is bedoelt om op de aarde te leven, voor de aarde. Niet voor de Hemel.

WET 6 - Accepteer geen hemel aarde interactie die een hel tot gevolg heeft.  

WET 7 - Niet dat van een ander.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
