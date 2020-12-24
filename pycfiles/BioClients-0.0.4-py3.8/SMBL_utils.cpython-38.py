# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/reactome/SMBL_utils.py
# Compiled at: 2020-03-11 09:26:37
# Size of source mod 2**32: 1108 bytes
"""
BRN = Biochemical Network Analysis (pybrn)
"""
import sys, os, re, logging, numpy
from .. import reactome
try:
    import brn
except Exception as e:
    try:
        logging.error('pybrn not installed.')
        sys.exit()
    finally:
        e = None
        del e

else:
    API_HOST = 'reactomews.oicr.on.ca:8080'
    BASE_PATH = '/ReactomeRESTfulAPI/RESTfulWS'
    API_BASE_URL = 'http://' + API_HOST + BASE_PATH
    net = brn.fromSBML('data/reactome_reactions_homo_sapiens.2.sbml')
    logging.info('reactions: %d' % len(net.reactions))
    logging.info('species: %d' % len(net.species))
    logging.info('values: %d' % len(net.values))
    n_reac = 0
for r in net.reactions:
    n_reac += 1
    logging.info('%3d. %s' % (n_reac, net.showreact(r, printstr=False)))
else:
    logging.info('n_reac: %d' % n_reac)
    n_spec = 0
    for s in net.species:
        n_spec += 1
        id_spec = re.sub('[^\\d]', '', s)
        spec = reactome.Utils.GetId(API_BASE_URL, id_spec, 'PhysicalEntity')
        displayName = spec['displayName'] if 'displayName' in spec else ''
        schemaClass = spec['schemaClass'] if 'schemaClass' in spec else ''
        logging.info('%3d. %s: (%s) %s' % (n_spec, id_spec, schemaClass, displayName))
    else:
        logging.info('n_spec: %d' % n_spec)