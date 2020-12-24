#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3:
    print("you need to run madbot with python3")
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
    name='madbot-extra',
    version='4',
    url='https://bitbucket.org/bthate/madbot-extra',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bot. JSON backend. MIT license",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["madbot"],
    scripts=[],
    packages=['extra'],
    long_description='''MADBOT is a python3 framework to use if you want to program IRC or XMPP bot.

PROVIDES

| CLI, IRC and XMPP bot.
| REST server to serve objects of a bot.
| RSS fetcher are provided as well.
| custom written eventhandler.
| launch threads.
| sync objects to disk and back.

CONTACT

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com


| MADBOT is code released onder een MIT compatible license.
| MADBOT is een event logger.


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
