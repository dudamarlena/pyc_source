#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run minibot with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='minibot',
    version='2',
    url='https://pikacode.com/milla/minibot',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='mini bot',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["distribute", "beautifulsoup4", "sleekxmpp", "natural", "feedparser", ],
    scripts=["bin/bot", "bin/out", "bin/msed", ],
    packages=['mini', 
              'mini.plugs',
             ],
    long_description = """ xmpp, irc, shell, cli, json - email at milla@dds.nl - documentation is at http://pythonhosted.org/minboti/ """,
    data_files=[('doc', ["LICENSE", ]),],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
