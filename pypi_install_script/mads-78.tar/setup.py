#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3:
    print("you need to run mads with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='mads',
    version='78',
    url='https://bitbucket.org/bthate/mads3',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots. JSON backend. MIT license",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["feedparser==5.2.1", "sleekxmpp", "beautifulsoup4", "pyasn1-modules"],
    scripts=["bin/mads", "bin/mads-ps", "bin/mads-sed", "bin/mads-do", "bin/mads-docs", "bin/mads-local"],
    packages=['mads', 'mods', "mids"],
    long_description='''MADS is a python3 framework to use if you want to program IRC or XMPP bots.

PROVIDES

| CLI, IRC and XMPP bots.
| REST server to serve objects of a bot.
| RSS fetcher are provided as well.
| custom written eventhandler.
| launch threads.
| sync objects to disk and back.

CONTACT

| Bartholomeus Henricus Julius Thate (bart)
| botfather on #dunkbots irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com


| MADS is code released onder een MIT compatible license.
| MADS is een event logger.


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
