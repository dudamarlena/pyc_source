# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/setup.py
# Compiled at: 2017-09-08 07:43:40
__author__ = 'Paul Ross'
__date__ = '2012-03-26'
__version__ = '0.9.5'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from distutils.core import setup
setup(name='CPIP', version='0.9.5', description='A C Preprocessor implemented in Python.', author='Paul Ross', author_email='apaulross@gmail.com', url='http://cpip.sourceforge.net/', packages=[
 'core',
 'util',
 'plot',
 'core.test',
 'util.test',
 'plot.test',
 'test'], py_modules=[
 'CPIPMain',
 'CppCondGraphToHtml',
 'IncGraphSVG',
 'IncGraphSVGBase',
 'IncGraphSVGPpi',
 'IncGraphXML',
 'IncList',
 'ItuToHtml',
 'MacroHistoryHtml',
 'TokenCss',
 'Tu2Html',
 'TuIndexer'])