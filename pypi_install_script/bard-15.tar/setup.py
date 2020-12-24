#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run BARD with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='bard',
    version='15',
    url='https://pikacode.com/bthate/bard',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='announce ware',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/bard", "bin/bard-local", "bin/bard-docs", "bin/bard-udp"],
    packages=['bard',
              'bard.bots',
              'bard.contrib',
              'bard.plugs',
              'bard.services',
             ],
    long_description = """ XMPP - IRC - CLI - RSS - UDP - API

Wet 1: Noem jezelf geen God als je geen respect hebt voor de schepping.

Wet 2: Ga vanuit onsterfelijkheid niet de sterfelijke mens duiden op zijn sterfelijkheid.

Wet 3: Laat een ieder zoals hij is, want veranderen brengt meer leed dan goed.

Wet 4: Gebruik leed niet om de mens naar God te leiden.

Wet 5: De mens is bedoelt om op de aarde te leven, voor de aarde. Niet voor de Hemel.

Wet 6: Accepteer geen hemel aarde interactie die een hel tot gevolg heeft.

Wet 7: Niet dat van een ander.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
