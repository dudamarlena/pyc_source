# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/mongo.py
# Compiled at: 2014-12-16 17:37:19
import pymongo
from seqtools import simplifySeqRecord, complicateSeqRecord
from vdj import ImmuneChain

def encode_chain(chain):
    document = simplifySeqRecord(chain)
    if hasattr(chain, 'v'):
        document['v'] = chain.v
    if hasattr(chain, 'd'):
        document['d'] = chain.d
    if hasattr(chain, 'j'):
        document['j'] = chain.j
    if hasattr(chain, 'junction_nt'):
        document['junction_nt'] = chain.junction_nt
    if hasattr(chain, 'junction_aa'):
        document['junction_aa'] = chain.junction_aa
    if hasattr(chain, 'num_mutations'):
        document['num_mutations'] = chain.num_mutations
    return document


def decode_document(document):
    assert document['__SeqRecord__']
    return ImmuneChain(complicateSeqRecord(document))


def connect_to_spleen(connect_to='vaccination'):
    connection = pymongo.Connection('spleen.res.med.harvard.edu', 27017)
    db = connection[connect_to]
    db.authenticate('mongodbuser', 'asdffdsa')
    return db


def connect_to_lymph(connect_to='vaccination'):
    connection = pymongo.Connection('hero1614.rc.fas.harvard.edu', 27017)
    db = connection[connect_to]
    return db


def connect_to_localhost(connect_to='vaccination'):
    connection = pymongo.Connection('localhost', 27017)
    db = connection[connect_to]
    return db


from pymongo.son_manipulator import SONManipulator
from Bio.SeqRecord import SeqRecord

class ImmuneChainTransform(SONManipulator):

    def transform_incoming(self, son, collection):
        for key, value in son.items():
            if isinstance(value, SeqRecord):
                son[key] = simplifySeqRecord(value)
            elif isinstance(value, dict):
                son[key] = self.transform_incoming(value, collection)

        return son

    def transform_outgoing(self, son, collection):
        for key, value in son.items():
            if isinstance(value, dict):
                if '__SeqRecord__' in value and value['__SeqRecord__']:
                    son[key] = ImmuneChain(complicateSeqRecord(value))
                else:
                    son[key] = self.transform_outgoing(value, collection)

        return son