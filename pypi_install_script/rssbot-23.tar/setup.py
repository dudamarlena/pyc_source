#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RSSBOT - bot you can use to display RSS feeds.

""" setup.py """

from setuptools import setup

setup(
    name='rssbot',
    version='23',
    url='https://github.com/bthate/rssbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="IRC bot you can use to display RSS feeds.",
    long_description="""RSSBOT is a IRC bot you can use to display RSS feeds.
RSSBOT is in the Public Domain and contains no copyright or LICENSE.

1) pip3 install rssbot
2) rssbot <server> <channel> <nick> 
3) !rss <url>
4) !fetch

    """,
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib", "feedparser"],
    scripts=["bin/rssbot", "bin/rssctl"],
    packages=["rssbot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
