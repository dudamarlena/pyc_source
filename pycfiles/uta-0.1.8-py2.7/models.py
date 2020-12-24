# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/models.py
# Compiled at: 2014-09-02 22:52:35
"""Schema for Universal Transcript Archive
"""
import datetime, hashlib, sqlalchemy as sa, sqlalchemy.orm as sao, sqlalchemy.ext.declarative as saed
schema_version = '1'
use_schema = True
if use_schema:
    schema_name = 'uta' + schema_version
    schema_name_dot = schema_name + '.'
else:
    schema_name = None
    schema_name_dot = ''
Base = saed.declarative_base(metadata=sa.MetaData(schema=schema_name))

class UTABase(object):
    pass


class Meta(Base, UTABase):
    __tablename__ = 'meta'
    key = sa.Column(sa.Text, primary_key=True, nullable=False)
    value = sa.Column(sa.Text, nullable=False)


class Origin(Base, UTABase):
    __tablename__ = 'origin'
    origin_id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    descr = sa.Column(sa.Text)
    updated = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    url = sa.Column(sa.Text, nullable=True)
    url_ac_fmt = sa.Column(sa.Text, nullable=True)

    def tickle_update(self):
        self.updated = datetime.datetime.now()


class Seq(Base, UTABase):
    __tablename__ = 'seq'

    def _seq_hash(context):
        seq = context.current_parameters['seq']
        if seq is None:
            return
        else:
            return hashlib.md5(seq.upper()).hexdigest()

    def _seq_len(context):
        seq = context.current_parameters['seq']
        if seq is None:
            return
        else:
            return len(seq)

    seq_id = sa.Column(sa.Text, primary_key=True, default=_seq_hash)
    len = sa.Column(sa.Integer, default=_seq_len, nullable=False)
    seq = sa.Column(sa.Text, nullable=True)


class SeqAnno(Base, UTABase):
    __tablename__ = 'seq_anno'
    __table_args__ = (
     sa.Index('seq_anno_ac_unique_in_origin', 'origin_id', 'ac', unique=True),)
    seq_anno_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    seq_id = sa.Column(sa.Text, sa.ForeignKey('seq.seq_id'), index=True)
    origin_id = sa.Column(sa.Integer, sa.ForeignKey('origin.origin_id'), nullable=False)
    ac = sa.Column(sa.Text, index=True, nullable=False)
    descr = sa.Column(sa.Text)
    added = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.now())
    origin = sao.relationship('Origin', backref='aliases')
    seq = sao.relationship('Seq', backref='aliases')


class Gene(Base, UTABase):
    __tablename__ = 'gene'
    hgnc = sa.Column(sa.Text, primary_key=True)
    maploc = sa.Column(sa.Text)
    descr = sa.Column(sa.Text)
    summary = sa.Column(sa.Text)
    aliases = sa.Column(sa.Text)
    added = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.now())


class Transcript(Base, UTABase):
    """class representing unique transcripts, as defined by unique <seq_id,cds_se,exons_se_i>
    """
    __tablename__ = 'transcript'
    __table_args__ = (
     sa.CheckConstraint('cds_start_i <= cds_end_i', 'cds_start_i_must_be_le_cds_end_i'),)
    ac = sa.Column(sa.Text, primary_key=True)
    origin_id = sa.Column(sa.Integer, sa.ForeignKey('origin.origin_id'), nullable=False, index=True)
    hgnc = sa.Column(sa.Text)
    cds_start_i = sa.Column(sa.Integer, nullable=False)
    cds_end_i = sa.Column(sa.Integer, nullable=False)
    cds_md5 = sa.Column(sa.Text, nullable=False, index=True)
    added = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)
    origin = sao.relationship('Origin', backref='transcripts')


class ExonSet(Base, UTABase):
    __tablename__ = 'exon_set'
    __table_args__ = (
     sa.UniqueConstraint('tx_ac', 'alt_ac', 'alt_aln_method', name='<transcript,reference,method> must be unique'),)
    exon_set_id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    tx_ac = sa.Column(sa.Text, nullable=False)
    alt_ac = sa.Column(sa.Text, nullable=False)
    alt_strand = sa.Column(sa.SmallInteger, nullable=False)
    alt_aln_method = sa.Column(sa.Text, nullable=False)
    added = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)

    def exons_se_i(self, transcript_order=False):
        """return exon [start_i,end_i) pairs in reference sequence order, or transcript order if requested"""
        rev = transcript_order and self.ref_strand == -1
        return sorted([ (e.start_i, e.end_i) for e in self.exons ], reverse=rev)


class Exon(Base, UTABase):
    __tablename__ = 'exon'
    __table_args__ = (
     sa.CheckConstraint('start_i < end_i', 'exon_start_i_must_be_lt_end_i'),
     sa.UniqueConstraint('exon_set_id', 'start_i', name='start_i_must_be_unique_in_exon_set'),
     sa.UniqueConstraint('exon_set_id', 'end_i', name='end_i_must_be_unique_in_exon_set'))

    def __unicode___(self):
        return ('[{self.start_i},{self.end_i})').format(self=self)

    exon_id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    exon_set_id = sa.Column(sa.Integer, sa.ForeignKey('exon_set.exon_set_id'), nullable=False, index=True)
    start_i = sa.Column(sa.Integer, nullable=False)
    end_i = sa.Column(sa.Integer, nullable=False)
    ord = sa.Column(sa.Integer, nullable=False)
    name = sa.Column(sa.Text)
    exon_set = sao.relationship('ExonSet', backref='exons')


class ExonAln(Base, UTABase):
    __tablename__ = 'exon_aln'
    __table_args__ = ()
    exon_aln_id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    tx_exon_id = sa.Column(sa.Integer, sa.ForeignKey('exon.exon_id'), index=True, nullable=False)
    alt_exon_id = sa.Column(sa.Integer, sa.ForeignKey('exon.exon_id'), index=True, nullable=False)
    cigar = sa.Column(sa.Text, nullable=False)
    added = sa.Column(sa.DateTime, default=datetime.datetime.now(), nullable=False)
    tx_aseq = sa.Column(sa.Text, nullable=False)
    alt_aseq = sa.Column(sa.Text, nullable=False)
    tx_exon = sao.relationship('Exon', backref='tx_aln', foreign_keys=[tx_exon_id])
    alt_exon = sao.relationship('Exon', backref='alt_aln', foreign_keys=[alt_exon_id])