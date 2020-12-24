#!/usr/bin/env python
#
#

__copyright__ = 'this file is in the public domain'
__revision__ = '$Id: setup.py 71 2005-11-10 13:37:50Z bart $'

from setuptools import setup

import os

upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir): print "%s does not exist" % dir ; os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc"):
                continue
            upl.append(d)

    return upl

setup(
    name='gozerbot',
    version='1.0.3',
    url='http://pikacode.com/bthate/gozerbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description='irc bot and xmpp bot in one',
    license='BSD',
    zip_safe=False,
    scripts = ['bin/gozerbot', 'bin/gozerbot-init', 'bin/gozerbot-start', 'bin/gozerbot-stop', 'bin/gozerbot-udp'],
    include_package_data=True,
    package_data={'': ['*.tar',]},
    packages=['gozerbot', 
              'gozerbot.contrib',
              'gozerbot.rest',
              'gozerbot.persist',
              'gozerbot.utils',
              'gozerbot.irc', 
              'gozerbot.plugs',
              'gozerbot.threads',
              'gozerbot.database',
              'gozerbot.xmpp',
              'gplugs',
              'gplugs.olddb',
              'gplugs.alchemy'],
    install_requires = ['simplejson >= 1.0',
                        'feedparser >= 1.0'],
    long_description = """

GOZERBOT is a channel bot supporting conversations in irc channels
and jabber conference rooms. It is mainly used to send notifications (RSS,
nagios, etc.) and making custom commands available for the channel. More then 
just a channel bot GOZERBOT aims to provide a platform for the user to 
program his own bot and make it into something thats usefull. This is done 
with a plugin structure that makes it easy to program your own plugins. 

GOZERBOT comes with some batteries included.

""",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    data_files=[('files', uploadfiles('files')),
                ('gozernest', uploadfiles('gozernest'))],
)
