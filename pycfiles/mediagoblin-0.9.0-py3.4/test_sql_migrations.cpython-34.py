# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_sql_migrations.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 32611 bytes
import six, pytest
pytestmark = pytest.mark.skipif(six.PY3, reason='needs sqlalchemy.migrate')
import copy
from sqlalchemy import Table, Column, MetaData, Index, Integer, Float, Unicode, UnicodeText, DateTime, Boolean, ForeignKey, UniqueConstraint, PickleType, VARCHAR
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, insert
if six.PY2:
    from migrate import changeset
from mediagoblin.db.base import GMGTableBase
from mediagoblin.db.migration_tools import MigrationManager, RegisterMigration
from mediagoblin.tools.common import CollectingPrinter
FULL_MIGRATIONS = {}
Base1 = declarative_base(cls=GMGTableBase)

class Creature1(Base1):
    __tablename__ = 'creature'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False, index=True)
    num_legs = Column(Integer, nullable=False)
    is_demon = Column(Boolean)


class Level1(Base1):
    __tablename__ = 'level'
    id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    exits = Column(PickleType)


SET1_MODELS = [
 Creature1, Level1]
FOUNDATIONS = {Creature1: [{'name': 'goblin',  'num_legs': 2,  'is_demon': False}, {'name': 'cerberus',  'num_legs': 4,  'is_demon': True}]}
SET1_MIGRATIONS = {}
Base2 = declarative_base(cls=GMGTableBase)

class Creature2(Base2):
    __tablename__ = 'creature'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False, index=True)
    num_legs = Column(Integer, nullable=False)
    magical_powers = relationship('CreaturePower2')


class CreaturePower2(Base2):
    __tablename__ = 'creature_power'
    id = Column(Integer, primary_key=True)
    creature = Column(Integer, ForeignKey('creature.id'), nullable=False)
    name = Column(Unicode)
    description = Column(Unicode)
    hitpower = Column(Integer, nullable=False)


class Level2(Base2):
    __tablename__ = 'level'
    id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)


class LevelExit2(Base2):
    __tablename__ = 'level_exit'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    from_level = Column(Unicode, ForeignKey('level.id'), nullable=False)
    to_level = Column(Unicode, ForeignKey('level.id'), nullable=False)


SET2_MODELS = [
 Creature2, CreaturePower2, Level2, LevelExit2]

@RegisterMigration(1, FULL_MIGRATIONS)
def creature_remove_is_demon(db_conn):
    """
    Remove the is_demon field from the creature model.  We don't need
    it!
    """
    pass


@RegisterMigration(2, FULL_MIGRATIONS)
def creature_powers_new_table(db_conn):
    """
    Add a new table for creature powers.  Nothing needs to go in it
    yet though as there wasn't anything that previously held this
    information
    """
    metadata = MetaData(bind=db_conn.bind)
    creature_table = Table('creature', metadata, autoload=True, autoload_with=db_conn.bind)
    creature_powers = Table('creature_power', metadata, Column('id', Integer, primary_key=True), Column('creature', Integer, ForeignKey('creature.id'), nullable=False), Column('name', Unicode), Column('description', Unicode), Column('hitpower', Integer, nullable=False))
    metadata.create_all(db_conn.bind)


@RegisterMigration(3, FULL_MIGRATIONS)
def level_exits_new_table(db_conn):
    """
    Make a new table for level exits and move the previously pickled
    stuff over to here (then drop the old unneeded table)
    """
    metadata = MetaData(bind=db_conn.bind)
    levels = Table('level', metadata, Column('id', Unicode, primary_key=True), Column('name', Unicode), Column('description', Unicode), Column('exits', PickleType))
    level_exits = Table('level_exit', metadata, Column('id', Integer, primary_key=True), Column('name', Unicode), Column('from_level', Unicode, ForeignKey('level.id'), nullable=False), Column('to_level', Unicode, ForeignKey('level.id'), nullable=False))
    metadata.create_all(db_conn.bind)
    result = db_conn.execute(select([levels], levels.c.exits != None))
    for level in result:
        for exit_name, to_level in six.iteritems(level['exits']):
            db_conn.execute(level_exits.insert().values(name=exit_name, from_level=level.id, to_level=to_level))

    levels.drop_column('exits')


SET2_MIGRATIONS = copy.copy(FULL_MIGRATIONS)
Base3 = declarative_base(cls=GMGTableBase)

class Creature3(Base3):
    __tablename__ = 'creature'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False, index=True)
    num_limbs = Column(Integer, nullable=False)
    magical_powers = relationship('CreaturePower3')


class CreaturePower3(Base3):
    __tablename__ = 'creature_power'
    id = Column(Integer, primary_key=True)
    creature = Column(Integer, ForeignKey('creature.id'), nullable=False, index=True)
    name = Column(Unicode)
    description = Column(Unicode)
    hitpower = Column(Float, nullable=False)


class Level3(Base3):
    __tablename__ = 'level'
    id = Column(Unicode, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)


class LevelExit3(Base3):
    __tablename__ = 'level_exit'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    from_level = Column(Unicode, ForeignKey('level.id'), nullable=False, index=True)
    to_level = Column(Unicode, ForeignKey('level.id'), nullable=False, index=True)


SET3_MODELS = [
 Creature3, CreaturePower3, Level3, LevelExit3]
SET3_MIGRATIONS = FULL_MIGRATIONS

@RegisterMigration(4, FULL_MIGRATIONS)
def creature_num_legs_to_num_limbs(db_conn):
    """
    Turns out we're tracking all sorts of limbs, not "legs"
    specifically.  Humans would be 4 here, for instance.  So we
    renamed the column.
    """
    metadata = MetaData(bind=db_conn.bind)
    creature_table = Table('creature', metadata, autoload=True, autoload_with=db_conn.bind)
    creature_table.c.num_legs.alter(name='num_limbs')


@RegisterMigration(5, FULL_MIGRATIONS)
def level_exit_index_from_and_to_level(db_conn):
    """
    Index the from and to levels of the level exit table.
    """
    metadata = MetaData(bind=db_conn.bind)
    level_exit = Table('level_exit', metadata, autoload=True, autoload_with=db_conn.bind)
    Index('ix_level_exit_from_level', level_exit.c.from_level).create(db_conn.bind)
    Index('ix_level_exit_to_level', level_exit.c.to_level).create(db_conn.bind)


@RegisterMigration(6, FULL_MIGRATIONS)
def creature_power_index_creature(db_conn):
    """
    Index our foreign key relationship to the creatures
    """
    metadata = MetaData(bind=db_conn.bind)
    creature_power = Table('creature_power', metadata, autoload=True, autoload_with=db_conn.bind)
    Index('ix_creature_power_creature', creature_power.c.creature).create(db_conn.bind)


@RegisterMigration(7, FULL_MIGRATIONS)
def creature_power_hitpower_to_float(db_conn):
    """
    Convert hitpower column on creature power table from integer to
    float.

    Turns out we want super precise values of how much hitpower there
    really is.
    """
    metadata = MetaData(bind=db_conn.bind)
    creature_table = Table('creature', metadata, autoload=True, autoload_with=db_conn.bind)
    creature_power = Table('creature_power', metadata, Column('id', Integer, primary_key=True), Column('creature', Integer, ForeignKey('creature.id'), nullable=False, index=True), Column('name', Unicode), Column('description', Unicode), Column('hitpower', Integer, nullable=False))
    creature_power.c.hitpower.alter(type=Float)


@RegisterMigration(8, FULL_MIGRATIONS)
def creature_power_name_creature_unique(db_conn):
    """
    Add a unique constraint to name and creature on creature_power.

    We don't want multiple creature powers with the same name per creature!
    """
    metadata = MetaData(bind=db_conn.bind)
    creature_power = Table('creature_power', metadata, autoload=True, autoload_with=db_conn.bind)
    cons = changeset.constraint.UniqueConstraint('name', 'creature', table=creature_power)
    cons.create()


def _insert_migration1_objects(session):
    """
    Test objects to insert for the first set of things
    """
    session.add_all([
     Creature1(name='centipede', num_legs=100, is_demon=False),
     Creature1(name='wolf', num_legs=4, is_demon=False),
     Creature1(name='wizardsnake', num_legs=0, is_demon=True)])
    session.add_all([
     Level1(id='necroplex', name='The Necroplex', description='A complex full of pure deathzone.', exits={'deathwell': 'evilstorm', 
      'portal': 'central_park'}),
     Level1(id='evilstorm', name='Evil Storm', description='A storm full of pure evil.', exits={}),
     Level1(id='central_park', name='Central Park, NY, NY', description="New York's friendly Central Park.", exits={'portal': 'necroplex'})])
    session.commit()


def _insert_migration2_objects(session):
    """
    Test objects to insert for the second set of things
    """
    session.add_all([
     Creature2(name='centipede', num_legs=100),
     Creature2(name='wolf', num_legs=4, magical_powers=[
      CreaturePower2(name='ice breath', description='A blast of icy breath!', hitpower=20),
      CreaturePower2(name='death stare', description='A frightening stare, for sure!', hitpower=45)]),
     Creature2(name='wizardsnake', num_legs=0, magical_powers=[
      CreaturePower2(name='death_rattle', description='A rattle... of DEATH!', hitpower=1000),
      CreaturePower2(name='sneaky_stare', description="The sneakiest stare you've ever seen!", hitpower=300),
      CreaturePower2(name='slithery_smoke', description='A blast of slithery, slithery smoke.', hitpower=10),
      CreaturePower2(name='treacherous_tremors', description='The ground shakes beneath footed animals!', hitpower=0)])])
    session.add_all([
     Level2(id='necroplex', name='The Necroplex', description='A complex full of pure deathzone.'),
     Level2(id='evilstorm', name='Evil Storm', description='A storm full of pure evil.', exits=[]),
     Level2(id='central_park', name='Central Park, NY, NY', description="New York's friendly Central Park.")])
    session.add_all([
     LevelExit2(name='deathwell', from_level='necroplex', to_level='evilstorm'),
     LevelExit2(name='portal', from_level='necroplex', to_level='central_park')])
    session.add_all([
     LevelExit2(name='portal', from_level='central_park', to_level='necroplex')])
    session.commit()


def _insert_migration3_objects(session):
    """
    Test objects to insert for the third set of things
    """
    session.add_all([
     Creature3(name='centipede', num_limbs=100),
     Creature3(name='wolf', num_limbs=4, magical_powers=[
      CreaturePower3(name='ice breath', description='A blast of icy breath!', hitpower=20.0),
      CreaturePower3(name='death stare', description='A frightening stare, for sure!', hitpower=45.0)]),
     Creature3(name='wizardsnake', num_limbs=0, magical_powers=[
      CreaturePower3(name='death_rattle', description='A rattle... of DEATH!', hitpower=1000.0),
      CreaturePower3(name='sneaky_stare', description="The sneakiest stare you've ever seen!", hitpower=300.0),
      CreaturePower3(name='slithery_smoke', description='A blast of slithery, slithery smoke.', hitpower=10.0),
      CreaturePower3(name='treacherous_tremors', description='The ground shakes beneath footed animals!', hitpower=0.0)])], Creature3(name='deity', numb_limbs=30, magical_powers=[
     CreaturePower3(name='smite', description='Smitten by holy wrath!', hitpower=9999.9)]))
    session.add_all([
     Level3(id='necroplex', name='The Necroplex', description='A complex full of pure deathzone.'),
     Level3(id='evilstorm', name='Evil Storm', description='A storm full of pure evil.', exits=[]),
     Level3(id='central_park', name='Central Park, NY, NY', description="New York's friendly Central Park.")])
    session.add_all([
     LevelExit3(name='deathwell', from_level='necroplex', to_level='evilstorm'),
     LevelExit3(name='portal', from_level='necroplex', to_level='central_park')])
    session.add_all([
     LevelExit3(name='portal', from_level='central_park', to_level='necroplex')])
    session.commit()


def create_test_engine():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///:memory:', echo=False)
    Session = sessionmaker(bind=engine)
    return (engine, Session)


def assert_col_type(column, this_class):
    assert isinstance(column.type, this_class)


def _get_level3_exits(session, level):
    return dict([(level_exit.name, level_exit.to_level) for level_exit in session.query(LevelExit3).filter_by(from_level=level.id)])


def test_set1_to_set3():
    engine, Session = create_test_engine()
    printer = CollectingPrinter()
    migration_manager = MigrationManager('__main__', SET1_MODELS, FOUNDATIONS, SET1_MIGRATIONS, Session(), printer)
    assert migration_manager.latest_migration == 0
    assert migration_manager.database_current_migration == None
    result = migration_manager.init_or_migrate()
    assert result == 'inited'
    assert printer.combined_string == '-> Initializing main mediagoblin tables... done.\n' + '   + Laying foundations for Creature1 table\n'
    assert migration_manager.latest_migration == 0
    assert migration_manager.database_current_migration == 0
    _insert_migration1_objects(Session())
    migration_manager = MigrationManager('__main__', SET1_MODELS, FOUNDATIONS, SET1_MIGRATIONS, Session(), printer)
    assert migration_manager.init_or_migrate() == None
    assert migration_manager.latest_migration == 0
    assert migration_manager.database_current_migration == 0
    metadata = MetaData(bind=engine)
    creature_table = Table('creature', metadata, autoload=True, autoload_with=engine)
    assert set(creature_table.c.keys()) == set([
     'id', 'name', 'num_legs', 'is_demon'])
    assert_col_type(creature_table.c.id, Integer)
    assert_col_type(creature_table.c.name, VARCHAR)
    assert creature_table.c.name.nullable is False
    assert_col_type(creature_table.c.num_legs, Integer)
    assert creature_table.c.num_legs.nullable is False
    assert_col_type(creature_table.c.is_demon, Boolean)
    level_table = Table('level', metadata, autoload=True, autoload_with=engine)
    assert set(level_table.c.keys()) == set([
     'id', 'name', 'description', 'exits'])
    assert_col_type(level_table.c.id, VARCHAR)
    assert level_table.c.id.primary_key is True
    assert_col_type(level_table.c.name, VARCHAR)
    assert_col_type(level_table.c.description, VARCHAR)
    session = Session()
    creature = session.query(Creature1).filter_by(name='goblin').one()
    assert creature.num_legs == 2
    assert creature.is_demon == False
    creature = session.query(Creature1).filter_by(name='cerberus').one()
    assert creature.num_legs == 4
    assert creature.is_demon == True
    creature = session.query(Creature1).filter_by(name='centipede').one()
    assert creature.num_legs == 100
    assert creature.is_demon == False
    creature = session.query(Creature1).filter_by(name='wolf').one()
    assert creature.num_legs == 4
    assert creature.is_demon == False
    creature = session.query(Creature1).filter_by(name='wizardsnake').one()
    assert creature.num_legs == 0
    assert creature.is_demon == True
    level = session.query(Level1).filter_by(id='necroplex').one()
    assert level.name == 'The Necroplex'
    assert level.description == 'A complex full of pure deathzone.'
    assert level.exits == {'deathwell': 'evilstorm', 
     'portal': 'central_park'}
    level = session.query(Level1).filter_by(id='evilstorm').one()
    assert level.name == 'Evil Storm'
    assert level.description == 'A storm full of pure evil.'
    assert level.exits == {}
    level = session.query(Level1).filter_by(id='central_park').one()
    assert level.name == 'Central Park, NY, NY'
    assert level.description == "New York's friendly Central Park."
    assert level.exits == {'portal': 'necroplex'}
    printer = CollectingPrinter()
    migration_manager = MigrationManager('__main__', SET3_MODELS, FOUNDATIONS, SET3_MIGRATIONS, Session(), printer)
    assert migration_manager.latest_migration == 8
    assert migration_manager.database_current_migration == 0
    result = migration_manager.init_or_migrate()
    assert result == 'migrated'
    assert printer.combined_string == '-> Updating main mediagoblin tables:\n   + Running migration 1, "creature_remove_is_demon"... done.\n   + Running migration 2, "creature_powers_new_table"... done.\n   + Running migration 3, "level_exits_new_table"... done.\n   + Running migration 4, "creature_num_legs_to_num_limbs"... done.\n   + Running migration 5, "level_exit_index_from_and_to_level"... done.\n   + Running migration 6, "creature_power_index_creature"... done.\n   + Running migration 7, "creature_power_hitpower_to_float"... done.\n   + Running migration 8, "creature_power_name_creature_unique"... done.\n'
    migration_manager = MigrationManager('__main__', SET3_MODELS, FOUNDATIONS, SET3_MIGRATIONS, Session(), printer)
    assert migration_manager.latest_migration == 8
    assert migration_manager.database_current_migration == 8
    metadata = MetaData(bind=engine)
    creature_table = Table('creature', metadata, autoload=True, autoload_with=engine)
    assert set(creature_table.c.keys()) == set([
     'id', 'name', 'num_limbs', 'is_demon'])
    assert_col_type(creature_table.c.id, Integer)
    assert_col_type(creature_table.c.name, VARCHAR)
    assert creature_table.c.name.nullable is False
    assert_col_type(creature_table.c.num_limbs, Integer)
    assert creature_table.c.num_limbs.nullable is False
    creature_power_table = Table('creature_power', metadata, autoload=True, autoload_with=engine)
    assert set(creature_power_table.c.keys()) == set([
     'id', 'creature', 'name', 'description', 'hitpower'])
    assert_col_type(creature_power_table.c.id, Integer)
    assert_col_type(creature_power_table.c.creature, Integer)
    assert creature_power_table.c.creature.nullable is False
    assert_col_type(creature_power_table.c.name, VARCHAR)
    assert_col_type(creature_power_table.c.description, VARCHAR)
    assert_col_type(creature_power_table.c.hitpower, Float)
    assert creature_power_table.c.hitpower.nullable is False
    level_table = Table('level', metadata, autoload=True, autoload_with=engine)
    assert set(level_table.c.keys()) == set([
     'id', 'name', 'description'])
    assert_col_type(level_table.c.id, VARCHAR)
    assert level_table.c.id.primary_key is True
    assert_col_type(level_table.c.name, VARCHAR)
    assert_col_type(level_table.c.description, VARCHAR)
    level_exit_table = Table('level_exit', metadata, autoload=True, autoload_with=engine)
    assert set(level_exit_table.c.keys()) == set([
     'id', 'name', 'from_level', 'to_level'])
    assert_col_type(level_exit_table.c.id, Integer)
    assert_col_type(level_exit_table.c.name, VARCHAR)
    assert_col_type(level_exit_table.c.from_level, VARCHAR)
    assert level_exit_table.c.from_level.nullable is False
    assert_col_type(level_exit_table.c.to_level, VARCHAR)
    assert level_exit_table.c.to_level.nullable is False
    session = Session()
    assert session.query(Creature3).filter_by(name='goblin').count() == 1
    assert session.query(Creature3).filter_by(name='cerberus').count() == 1
    creature = session.query(Creature3).filter_by(name='centipede').one()
    assert creature.num_limbs == 100.0
    assert creature.magical_powers == []
    creature = session.query(Creature3).filter_by(name='wolf').one()
    assert creature.num_limbs == 4.0
    assert creature.magical_powers == []
    creature = session.query(Creature3).filter_by(name='wizardsnake').one()
    assert creature.num_limbs == 0.0
    assert creature.magical_powers == []
    level = session.query(Level3).filter_by(id='necroplex').one()
    assert level.name == 'The Necroplex'
    assert level.description == 'A complex full of pure deathzone.'
    level_exits = _get_level3_exits(session, level)
    assert level_exits == {'deathwell': 'evilstorm', 
     'portal': 'central_park'}
    level = session.query(Level3).filter_by(id='evilstorm').one()
    assert level.name == 'Evil Storm'
    assert level.description == 'A storm full of pure evil.'
    level_exits = _get_level3_exits(session, level)
    assert level_exits == {}
    level = session.query(Level3).filter_by(id='central_park').one()
    assert level.name == 'Central Park, NY, NY'
    assert level.description == "New York's friendly Central Park."
    level_exits = _get_level3_exits(session, level)
    assert level_exits == {'portal': 'necroplex'}