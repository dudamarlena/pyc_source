# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/model/dbSession.py
# Compiled at: 2009-10-06 09:02:53
import sqlalchemy as sa
from sqlalchemy import orm
import datetime, cPickle, traceback
from ProDaMa.Dataset import Dataset
from ProDaMa.Chain import Chain
from ProDaMa.Protein import Protein
from ProDaMa.model.CATHProteinData import CATHProteinData
from ProDaMa.model.SCOPProteinData import SCOPProteinData
from ProDaMa.services.config import *
engine = sa.create_engine('%s://%s:%s@%s:%s/%s' % (DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))
metadata = sa.MetaData(engine)
protein_table = sa.Table('Protein', metadata, autoload=True, autoload_with=engine)
chain_table = sa.Table('chain', metadata, autoload=True, autoload_with=engine)
membership_table = sa.Table('membership', metadata, autoload=True, autoload_with=engine)
dataset_table = sa.Table('dataset', metadata, autoload=True, autoload_with=engine)
CATH_table = sa.Table('CATHProteinData', metadata, autoload=True, autoload_with=engine)
SCOP_table = sa.Table('SCOPProteinData', metadata, autoload=True, autoload_with=engine)
membraneprotein_table = sa.Table('MembraneProteinData', metadata, autoload=True, autoload_with=engine)
aadata_table = sa.Table('aadata', metadata, autoload=True, autoload_with=engine)

class Membership(object):
    pass


class MPData(object):
    pass


class AAData(object):
    pass


orm.mapper(AAData, aadata_table)
orm.mapper(Dataset, dataset_table)
orm.mapper(Protein, protein_table, properties={'chains': orm.relation(Chain, primaryjoin=protein_table.c.str_id == chain_table.c.str_id, backref='protein')})
orm.mapper(Chain, chain_table, properties={'datasets': orm.relation(Dataset, secondary=membership_table, primaryjoin=sa.and_(chain_table.c.str_id == membership_table.c.str_id, chain_table.c.chain_id == membership_table.c.chain_id), secondaryjoin=dataset_table.c.name == membership_table.c.dataset_name, backref='chains')})
orm.mapper(CATHProteinData, CATH_table, properties={'protein': orm.relation(Protein, backref='cathClassification')})
orm.mapper(SCOPProteinData, SCOP_table, properties={'protein': orm.relation(Protein, backref='scopClassification')})
orm.mapper(MPData, membraneprotein_table, properties={'mp_chain': orm.relation(Chain, primaryjoin=sa.and_(chain_table.c.str_id == membraneprotein_table.c.str_id, chain_table.c.chain_id == membraneprotein_table.c.chain_id), backref='mpData')})
sm = orm.sessionmaker(bind=engine)
Session = orm.scoped_session(sm)