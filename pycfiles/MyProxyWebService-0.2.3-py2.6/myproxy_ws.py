# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/myproxy/ws/test/myproxy_ws.py
# Compiled at: 2012-08-22 09:00:49
"""Test script to run MyProxy web service interface in the Paster web 
application server.
"""
__author__ = 'P J Kershaw'
__date__ = '03/08/12'
__copyright__ = '(C) 2012 Science and Technology Facilities Council'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: $'
import logging
logging.basicConfig(level=logging.DEBUG)
from os import path
THIS_DIR = path.abspath(path.dirname(__file__))
INI_FILENAME = 'myproxywsgi.ini'
ini_filepath = path.join(THIS_DIR, INI_FILENAME)
from paste.script.serve import ServeCommand
ServeCommand('serve').run([ini_filepath])