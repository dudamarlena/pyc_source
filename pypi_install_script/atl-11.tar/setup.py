#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run atl with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='atl',
    version='11',
    url='https://pikacode.com/milla/atl',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='atl - wat weet jij van die dag?',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["beautifulsoup4", ],
    scripts=["bin/atl", "bin/abot", "bin/jsb-sed"],
    packages=['atl', 
              'atl.plugs',
              'atl.drivers',
             ],
    long_description = """ALLAH TIJDLIJN (^)#*)/12 (69389/12) !! 

2014-03-13 22:31:32 -=- vrije wil - wil van een ander - wil frictie - wil uitleg - had ik het je niet verteld - kijk dan .. alles ontnomen - had je het maar geweten

verder op https://pikacode.com/milla/botje - easy_install3 -U botje

""",
    data_files=[('doc', ["LICENSE", ]),],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
