#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3:
    print("you need to run madz with python3")
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
    name='madz',
    version='2',
    url='https://bitbucket.org/bthate/madz',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots. JSON backend. MIT license",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["feedparser==5.2.1", "sleekxmpp", "beautifulsoup4", "pyasn1-modules"],
    scripts=["bin/madz", "bin/madz-ps", "bin/madz-sed", "bin/madz-do", "bin/madz-local"],
    packages=['madz', 'modz', "midz"],
    long_description='''MADZ is a python3 framework to use if you want to program IRC or XMPP bots.

PROVIDES

| CLI, IRC and XMPP bots.
| REST server to serve objects of a bot.
| RSS fetcher are provided as well.
| custom written eventhandler.
| launch threads.
| sync objects to disk and back.

CONTACT

| Bart Thate
| botfather on #dunkbots irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com


| MADZ is code released onder een MIT compatible license.
| MADZ is een event logger.


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
