# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/tables.py
# Compiled at: 2008-07-30 12:52:46
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
import config
engine = sa.create_engine(config.URL)
metadata = sa.MetaData(engine)
Session = scoped_session(sessionmaker(autoflush=True, transactional=True))
expressions = sa.Table('expressions', metadata, sa.Column('expression_id', sa.Integer, sa.Sequence('expression_seq'), primary_key=True), sa.Column('name', sa.String, index=True), sa.Column('symbol', sa.String, index=True), sa.Column('arg_name', sa.String, nullable=True), sa.Column('true', sa.Boolean, default=True), sa.Column('var', sa.Boolean, default=False), sa.Column('depth', sa.Integer, default=0), sa.Column('arity', sa.Integer, default=0), sa.Column('arith', sa.Integer, default=0), sa.Column('parent_id', sa.Integer, sa.ForeignKey('expressions.expression_id'), nullable=True, index=True), sa.Column('rule_id', sa.Integer, sa.ForeignKey('rules.rule_id'), nullable=True, index=True), sa.Column('inrule', sa.Integer, default=0))
sa.Index('covering_expr1_ix', expressions.c.symbol, expressions.c.arity)
sa.Index('covering_expr2_ix', expressions.c.true, expressions.c.depth, expressions.c.arg_name, expressions.c.inrule)
sa.Index('extend_ix', expressions.c.inrule, expressions.c.parent_id, expressions.c.depth, expressions.c.expression_id)
rules = sa.Table('rules', metadata, sa.Column('rule_id', sa.Integer, sa.Sequence('rule_seq'), primary_key=True), sa.Column('name', sa.String, index=True))
proofs = sa.Table('proofs', metadata, sa.Column('step_id', sa.Integer, sa.Sequence('proof_seq'), primary_key=True), sa.Column('parent_expr', sa.Integer, sa.ForeignKey('expressions.expression_id'), index=True), sa.Column('parent_rule', sa.Integer, sa.ForeignKey('rules.rule_id'), index=True), sa.Column('isrule', sa.Boolean, default=False), sa.Column('child_expr', sa.Integer, sa.ForeignKey('expressions.expression_id'), nullable=True, index=True), sa.Column('child_rule', sa.Integer, sa.ForeignKey('rules.rule_id'), nullable=True, index=True))
counters = sa.Table('counters', metadata, sa.Column('counter_id', sa.Integer, sa.Sequence('counter_id_seq'), primary_key=True), sa.Column('name', sa.String, index=True, unique=True), sa.Column('count', sa.Integer))
try:
    metadata.create_all()
except SQLError:
    rules = sa.Table('rules', metadata, autoload=True)
    expressions = sa.Table('expressions', metadata, autoload=True)
    counters = sa.Table('counters', metadata, autoload=True)
    proofs = sa.Table('proofs', metadata, autoload=True)