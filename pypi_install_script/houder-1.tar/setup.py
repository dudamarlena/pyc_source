#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run rechter with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='houder',
    version='1',
    url='https://pikacode.com/bart/houder',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" HOUDER - indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["meds"],
    scripts=["bin/houder"],
    packages=['houder',
             ],
    long_description="""

Mishandeling van medicijnen is strafbaar in het Wetboek van Strafrecht:

Artikel 300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

Artikel 304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

Behandeling met antipsychotica is opzettelijke benadeling van de gezondheid gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen om met die benadeling van de gezondheid te proberen de psychotische symptomen te verminderen.

kortom:

Antipsychotica brengen schade toe aan de hersenen in de hoop met toebrenging van die schade de psychotische symptomen te verminderen. De schade die men toebrengt is opzettelijk en daarmee is het mishandeling.

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
