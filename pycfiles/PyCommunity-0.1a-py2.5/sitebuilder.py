# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/sitebuilder.py
# Compiled at: 2007-02-12 09:02:44
""" builds the website
"""
from configuration import Configuration
from generator import run
import tasks

def buildSite(conf='pycommunity.conf'):
    """generates the website"""
    configuration = Configuration(conf)
    sequence = ('index', 'glossary', 'recipe', 'tutorial', 'package')
    run(sequence, configuration)