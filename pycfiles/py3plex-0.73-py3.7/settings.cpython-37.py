# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/settings.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1328 bytes
"""
Global settings file.

@author: anze.vavpetic@ijs.si
"""
import os, logging
from rdflib import Namespace
VERSION = '0.3.1'
DESCRIPTION = 'Hedwig semantic pattern mining (blaz.skrlj@ijs.si and anze.vavpetic@ijs.si)'
logger = logging.getLogger('Hedwig')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
PAR_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
ASSETS_DIR = os.path.abspath(os.path.join(PAR_DIR, 'assets'))
EXAMPLE_SCHEMA = os.path.join(ASSETS_DIR, 'builtin.n3')
W3C = Namespace('http://www.w3.org/')
HEDWIG = Namespace('http://kt.ijs.si/hedwig#')
DEFAULT_ANNOTATION_NAME = 'annotated_with'
GENERIC_NAMESPACE = Namespace('http://kt.ijs.si/ontology/generic#')
INPUT_FORMATS = [
 'n3', 'xml', 'ntriples', 'trix', 'csv']

class Defaults:
    FORMAT = INPUT_FORMATS[0]
    OUTPUT = None
    COVERED = None
    MODE = 'subgroups'
    TARGET = None
    SCORE = 'lift'
    NEGATIONS = False
    ALPHA = 0.05
    ADJUST = 'fwer'
    FDR_Q = 0.05
    LEAVES = False
    LEARNER = 'heuristic'
    OPTIMAL_SUBCLASS = False
    URIS = False
    BEAM_SIZE = 20
    SUPPORT = 0.1
    DEPTH = 5
    NO_CACHE = False
    VERBOSE = False