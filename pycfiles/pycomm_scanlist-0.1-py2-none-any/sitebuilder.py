# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/sitebuilder.py
# Compiled at: 2007-02-12 09:02:44
__doc__ = ' builds the website\n'
from configuration import Configuration
from generator import run
import tasks

def buildSite(conf='pycommunity.conf'):
    """generates the website"""
    configuration = Configuration(conf)
    sequence = ('index', 'glossary', 'recipe', 'tutorial', 'package')
    run(sequence, configuration)