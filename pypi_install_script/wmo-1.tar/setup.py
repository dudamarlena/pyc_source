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
    name='wmo',
    version='1',
    url='https://pikacode.com/bart/wmo',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" WMO - recht op casemanagement, recht op bewindvoering, behandeling met medicijnen strafbaar. ",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["meds"],
    scripts=["bin/wmo"],
    packages=['wmo',
             ],
    long_description="""

    1) Verplicht casemanagement voor zij die niet voor hun belangen op kunnen komen
    2) Verplicht bewindvoering voor zij die niet in staat zijn hun financien te beheren
    3) Behandeling met medicijnen strafbaar

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
