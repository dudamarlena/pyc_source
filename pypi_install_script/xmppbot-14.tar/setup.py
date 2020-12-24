#!/usr/bin/env python3

""" setup.py """

from setuptools import setup

setup(
    name='xmppbot',
    version='14',
    url='https://bitbucket.org/bthate/xmppbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="XMPP bot that can relay RSS feeds to jabber rooms and clients.",
    long_description=""" XMPPBOT provides IRC and XMPP bots and is extendible by programming your own commands. 
                         Basic functionality is a RSS feed fetcher you can use to display feeds into your channel. 
                         XMPPBOT has been placed in the Public Domain and contains no copyright or LICENSE.
                     """,   
    license='Public Domain',
    install_requires=["rssbot", "dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6", "sleekxmpp==1.3.1"],
    packages=["xmppbot"],
    scripts=["bin/xmppbot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python'
                ]
)
