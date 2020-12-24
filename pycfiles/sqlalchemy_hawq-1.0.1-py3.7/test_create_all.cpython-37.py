# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_create_all.py
# Compiled at: 2019-10-07 13:43:57
# Size of source mod 2**32: 15651 bytes
"""
Tests Hawq compiler output without connecting to live db.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UniqueConstraint, create_engine, Text
from sqlalchemy.testing.suite import fixtures
from sqlalchemy.testing import assert_raises
from collections import OrderedDict
import re
from sqlalchemy_hawq.partition import RangePartition, ListPartition, RangeSubpartition, ListSubpartition
from sqlalchemy_hawq.point import Point

def get_engine_spy():

    class MetadataDumpSpy:

        def __init__(self):
            self.sql = None
            self.engine = None

        def __call__(self, sql, *args, **kwargs):
            self.sql = str(sql.compile(dialect=(self.engine.dialect)))

    spy = MetadataDumpSpy()
    engine = create_engine('hawq://localhost/dummy_user', strategy='mock', executor=spy)
    spy.engine = engine
    return spy


def normalize_whitespace(input_string):
    """
    Strip whitespaces and newline characters from the input string

    Args:
        input_string (str): Given input string

    Returns:
        str: String sans whitespaces and newline characters
    """
    return re.sub('[\\n\\s]+', ' ', input_string, flags=(re.MULTILINE))


class TestCreateAll(fixtures.TestBase):

    def test_multiple(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (
             UniqueConstraint('chrom'),
             {'hawq_distributed_by':'chrom', 
              'hawq_partition_by':ListPartition('chrom', OrderedDict([('chr1', '1'), ('chr2', '2'), ('chr3', '3')])), 
              'hawq_appendonly':True})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (appendonly=True)\nDISTRIBUTED BY (chrom)\nPARTITION BY LIST (chrom)\n(\n    PARTITION chr1 VALUES (\'1\'),\n    PARTITION chr2 VALUES (\'2\'),\n    PARTITION chr3 VALUES (\'3\'),\n    DEFAULT PARTITION other\n)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_distributed_by(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_distributed_by': 'chrom'})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nDISTRIBUTED BY (chrom)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_distributed_with_hash(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (
             UniqueConstraint('chrom'),
             {'hawq_distributed_by':'chrom', 
              'hawq_bucketnum':42})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (bucketnum=42)\nDISTRIBUTED BY (chrom)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_hash_without_distribution(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_bucketnum': 42})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        assert_raises(ValueError, metadata.create_all, engine_spy.engine)

    def test_partition_by_list(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (
             UniqueConstraint('chrom'),
             {'hawq_partition_by': ListPartition('chrom', OrderedDict([('chr1', '1'), ('chr2', '2'), ('chr3', '3')]))})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nPARTITION BY LIST (chrom)\n(\n    PARTITION chr1 VALUES (\'1\'),\n    PARTITION chr2 VALUES (\'2\'),\n    PARTITION chr3 VALUES (\'3\'),\n    DEFAULT PARTITION other\n)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_partition_by_range(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (
             UniqueConstraint('chrom'),
             {'hawq_partition_by': RangePartition('chrom', 0, 10, 2)})
            chrom = Column('chrom', (Integer()), primary_key=True, autoincrement=False)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom INTEGER NOT NULL\n)\nPARTITION BY RANGE (chrom)\n(\n    START (0) END (10) EVERY (2),\n    DEFAULT PARTITION extra\n)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_partition_by_range_subpartition_by_list_and_range(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = {'hawq_partition_by': RangePartition('year', 2002, 2012, 1, [
                                   RangeSubpartition('month', 1, 13, 1),
                                   ListSubpartition('chrom', OrderedDict([('chr1', '1'), ('chr2', '2'), ('chr3', '3')]))])}
            id = Column('id', (Integer()), primary_key=True, autoincrement=False)
            year = Column('year', Integer())
            month = Column('month', Integer())
            chrom = Column('chrom', Text())

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = ' '.join('CREATE TABLE "MockTable" (\n    id INTEGER NOT NULL,\n    year INTEGER,\n    month INTEGER,\n    chrom TEXT\n)\nPARTITION BY RANGE (year)\n    SUBPARTITION BY RANGE (month)\n    SUBPARTITION TEMPLATE\n    (\n        START (1) END (13) EVERY (1),\n        DEFAULT SUBPARTITION extra\n    )\n    SUBPARTITION BY LIST (chrom)\n    SUBPARTITION TEMPLATE\n    (\n        SUBPARTITION chr1 VALUES (\'1\'),\n        SUBPARTITION chr2 VALUES (\'2\'),\n        SUBPARTITION chr3 VALUES (\'3\'),\n        DEFAULT SUBPARTITION other\n    )\n(\n    START (2002) END (2012) EVERY (1),\n    DEFAULT PARTITION extra\n)'.split())
        assert expected == ' '.join(engine_spy.sql.strip().split())

    def test_partition_by_list_subpartition_by_range_and_range(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = {'hawq_partition_by': ListPartition('chrom', OrderedDict([('chr1', '1'), ('chr2', '2'), ('chr3', '3')]), [
                                   RangeSubpartition('year', 2002, 2012, 1),
                                   RangeSubpartition('month', 1, 13, 1)])}
            id = Column('id', (Integer()), primary_key=True, autoincrement=False)
            year = Column('year', Integer())
            month = Column('month', Integer())
            chrom = Column('chrom', Text())

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = ' '.join('CREATE TABLE "MockTable" (\n    id INTEGER NOT NULL,\n    year INTEGER,\n    month INTEGER,\n    chrom TEXT\n)\nPARTITION BY LIST (chrom)\n    SUBPARTITION BY RANGE (year)\n    SUBPARTITION TEMPLATE\n    (\n        START (2002) END (2012) EVERY (1),\n        DEFAULT SUBPARTITION extra\n    )\n\n    SUBPARTITION BY RANGE (month)\n    SUBPARTITION TEMPLATE\n    (\n        START (1) END (13) EVERY (1),\n        DEFAULT SUBPARTITION extra\n    )\n(\n    PARTITION chr1 VALUES (\'1\'),\n    PARTITION chr2 VALUES (\'2\'),\n    PARTITION chr3 VALUES (\'3\'),\n    DEFAULT PARTITION other\n)'.split())
        assert expected == ' '.join(engine_spy.sql.strip().split())

    def test_appendonly(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_appendonly': True})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (appendonly=True)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_appendonly_error(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_appendonly': 'bad value'})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        assert_raises(ValueError, metadata.create_all, engine_spy.engine)

    def test_orientation(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_orientation': 'row'})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (orientation=ROW)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_orientation_error(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_orientation': 'bad value'})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        assert_raises(ValueError, metadata.create_all, engine_spy.engine)

    def test_compresstype(self, engine_spy=get_engine_spy()):
        for compresstype in {'NONE', 'ZLIB', 'GZIP', 'SNAPPY'}:
            Base = declarative_base()

            class MockTable(Base):
                __tablename__ = 'MockTable'
                __table_args__ = (UniqueConstraint('chrom'), {'hawq_compresstype': compresstype})
                chrom = Column('chrom', (Text()), primary_key=True)

            metadata = MockTable.__table__.metadata
            metadata.create_all(engine_spy.engine)
            expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (compresstype={})'.format(compresstype)

        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_compresstype_error(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_compresstype': 'tar'})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        assert_raises(ValueError, metadata.create_all, engine_spy.engine)

    def test_compresslevel(self, engine_spy=get_engine_spy()):
        for compresslevel in range(10):
            Base = declarative_base()

            class MockTable(Base):
                __tablename__ = 'MockTable'
                __table_args__ = (UniqueConstraint('chrom'), {'hawq_compresslevel': compresslevel})
                chrom = Column('chrom', (Text()), primary_key=True)

            metadata = MockTable.__table__.metadata
            metadata.create_all(engine_spy.engine)
            expected = 'CREATE TABLE "MockTable" (\nchrom TEXT NOT NULL\n)\nWITH (compresslevel={})'.format(compresslevel)

        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_compresslevel_error(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            __table_args__ = (UniqueConstraint('chrom'), {'hawq_compresslevel': 10})
            chrom = Column('chrom', (Text()), primary_key=True)

        metadata = MockTable.__table__.metadata
        assert_raises(ValueError, metadata.create_all, engine_spy.engine)

    def test_point_type(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            ptest = Column('ptest', Point, primary_key=True)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        expected = 'CREATE TABLE "MockTable" (\nptest POINT NOT NULL\n)'
        normalize_whitespace(expected) == normalize_whitespace(engine_spy.sql)

    def test_compile_point_type_from_list_input(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            id = Column('id', Integer, primary_key=True)
            ptest = Column('ptest', Point)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        ins = MockTable.__table__.insert().values(id=3, ptest=(3, 4))
        params = ins.compile().params
        expected = {'id':3,  'ptest':(3, 4)}
        assert expected == params

    def test_delete_statement_with_filter_clauses(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            id = Column('id', Integer, primary_key=True)
            ptest = Column('ptest', Point)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        delete_stmt = MockTable.__table__.delete().where(id == 3)
        assert_raises(NotImplementedError, delete_stmt.compile, engine_spy.engine)

    def test_delete_statement_bare(self, base=declarative_base(), engine_spy=get_engine_spy()):

        class MockTable(base):
            __tablename__ = 'MockTable'
            id = Column('id', Integer, primary_key=True)
            ptest = Column('ptest', Point)

        metadata = MockTable.__table__.metadata
        metadata.create_all(engine_spy.engine)
        delete_stmt = MockTable.__table__.delete()
        expected = str(delete_stmt.compile(engine_spy.engine))
        assert expected == 'TRUNCATE TABLE "MockTable"'