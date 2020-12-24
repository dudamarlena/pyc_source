# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/db.py
# Compiled at: 2016-10-03 09:39:22
import logging
logger = logging.getLogger(__name__)
from sqlalchemy.orm import class_mapper
import datetime, os, re, bauble.error as error
from bauble.i18n import _
try:
    import sqlalchemy as sa
    parts = tuple(int(i) for i in sa.__version__.split('.')[:2])
    if parts < (0, 6):
        msg = _('This version of Ghini requires SQLAlchemy 0.6 or greater. You are using version %s. Please download and install a newer version of SQLAlchemy from http://www.sqlalchemy.org or contact your system administrator.') % ('.').join(parts)
        raise error.SQLAlchemyVersionError(msg)
except ImportError:
    msg = _('SQLAlchemy not installed. Please install SQLAlchemy from http://www.sqlalchemy.org')
    raise

import gtk, sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import bauble.btypes as types, bauble.utils as utils

def sqlalchemy_debug(verbose):
    if verbose:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
    else:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
        logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.WARN)


SQLALCHEMY_DEBUG = False
sqlalchemy_debug(SQLALCHEMY_DEBUG)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance


def natsort(attr, obj):
    """return the naturally sorted list of the object attribute

    meant to be curried.  the main role of this function is to invert
    the order in which the function getattr receives its arguments.

    attr is in the form <attribute> but can also specify a path from the
    object to the attribute, like <a1>.<a2>.<a3>, in which case each
    step should return a single database object until the last step
    where the result should be a list of objects.

    e.g.:
    from functools import partial
    partial(natsort, 'accessions')(species)
    partial(natsort, 'species.accessions')(vern_name)
    """
    from bauble import utils
    jumps = attr.split('.')
    for attr in jumps:
        obj = getattr(obj, attr)

    return sorted(obj, key=utils.natsort_key)


class HistoryExtension(orm.MapperExtension):
    """
    HistoryExtension is a
    :class:`~sqlalchemy.orm.interfaces.MapperExtension` that is added
    to all clases that inherit from bauble.db.Base so that all
    inserts, updates, and deletes made to the mapped objects are
    recorded in the `history` table.
    """

    def _add(self, operation, mapper, instance):
        """
        Add a new entry to the history table.
        """
        global engine
        user = None
        try:
            if engine.name.startswith('sqlite'):
                raise TypeError('this engine know nothing of users')
            import bauble.plugins.users as users
            user = users.current_user()
        except:
            if 'USER' in os.environ and os.environ['USER']:
                user = os.environ['USER']
            elif 'USERNAME' in os.environ and os.environ['USERNAME']:
                user = os.environ['USERNAME']

        row = {}
        for c in mapper.local_table.c:
            row[c.name] = utils.utf8(getattr(instance, c.name))

        table = History.__table__
        table.insert(dict(table_name=mapper.local_table.name, table_id=instance.id, values=str(row), operation=operation, user=user, timestamp=datetime.datetime.today())).execute()
        return

    def after_update(self, mapper, connection, instance):
        self._add('update', mapper, instance)

    def after_insert(self, mapper, connection, instance):
        self._add('insert', mapper, instance)

    def after_delete(self, mapper, connection, instance):
        self._add('delete', mapper, instance)


class MapperBase(DeclarativeMeta):
    """
    MapperBase adds the id, _created and _last_updated columns to all
    tables.

    In general there is no reason to use this class directly other
    than to extend it to add more default columns to all the bauble
    tables.
    """

    def __init__(cls, classname, bases, dict_):
        if '__tablename__' in dict_:
            cls.id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
            cls._created = sa.Column('_created', types.DateTime(True), default=sa.func.now())
            cls._last_updated = sa.Column('_last_updated', types.DateTime(True), default=sa.func.now(), onupdate=sa.func.now())
            cls.__mapper_args__ = {'extension': HistoryExtension()}
        if 'top_level_count' not in dict_:
            cls.top_level_count = lambda x: {classname: 1}
        if 'search_view_markup_pair' not in dict_:
            cls.search_view_markup_pair = lambda x: (utils.xml_safe(str(x)),
             '(%s)' % type(x).__name__)
        super(MapperBase, cls).__init__(classname, bases, dict_)


engine = None
Session = None
Base = declarative_base(metaclass=MapperBase)
metadata = Base.metadata
history_base = declarative_base(metadata=metadata)

class History(history_base):
    """
    The history table records ever changed made to every table that
    inherits from :ref:`Base`

    :Table name: history

    :Columns:
      id: :class:`sqlalchemy.types.Integer`
        A unique identifier.
      table_name: :class:`sqlalchemy.types.String`
        The name of the table the change was made on.
      table_id: :class:`sqlalchemy.types.Integer`
        The id in the table of the row that was changed.
      values: :class:`sqlalchemy.types.String`
        The changed values.
      operation: :class:`sqlalchemy.types.String`
        The type of change.  This is usually one of insert, update or delete.
      user: :class:`sqlalchemy.types.String`
        The name of the user who made the change.
      timestamp: :class:`sqlalchemy.types.DateTime`
        When the change was made.
    """
    __tablename__ = 'history'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    table_name = sa.Column(sa.Text, nullable=False)
    table_id = sa.Column(sa.Integer, nullable=False, autoincrement=False)
    values = sa.Column(sa.Text, nullable=False)
    operation = sa.Column(sa.Text, nullable=False)
    user = sa.Column(sa.Text)
    timestamp = sa.Column(types.DateTime, nullable=False)


def open(uri, verify=True, show_error_dialogs=False):
    """
    Open a database connection.  This function sets bauble.db.engine to
    the opened engined.

    Return bauble.db.engine if successful else returns None and
    bauble.db.engine remains unchanged.

    :param uri: The URI of the database to open.
    :type uri: str

    :param verify: Where the database we connect to should be verified
        as one created by Ghini.  This flag is used mostly for
        testing.
    :type verify: bool

    :param show_error_dialogs: A flag to indicate whether the error
        dialogs should be displayed.  This is used mostly for testing.
    :type show_error_dialogs: bool
    """
    logger.debug('db.open(%s)' % uri)
    from sqlalchemy.orm import sessionmaker
    new_engine = None
    from sqlalchemy.pool import NullPool, SingletonThreadPool
    from bauble.prefs import testing
    poolclass = testing and SingletonThreadPool or NullPool
    poolclass = SingletonThreadPool
    new_engine = sa.create_engine(uri, echo=SQLALCHEMY_DEBUG, implicit_returning=False, poolclass=poolclass, pool_size=20)
    try:
        new_engine.connect().close()
    except Exception:
        logger.info('about to forget about encoding of exception text.')
        raise

    def _bind():
        """bind metadata to engine and create sessionmaker """
        global Session
        global engine
        engine = new_engine
        metadata.bind = engine

        def temp():
            import inspect
            logger.debug('creating session %s' % str(inspect.stack()[1]))
            return sessionmaker(bind=engine, autoflush=False)()

        Session = sessionmaker(bind=engine, autoflush=False)
        Session = temp

    if new_engine is not None and not verify:
        _bind()
        return engine
    else:
        if new_engine is None:
            return
        verify_connection(new_engine, show_error_dialogs)
        _bind()
        return engine


def create(import_defaults=True):
    """
    Create new Ghini database at the current connection

    :param import_defaults: A flag that is passed to each plugins
        install() method to indicate where it should import its
        default data.  This is mainly used for testing.  The default
        value is True
    :type import_defaults: bool

    """
    logger.debug('entered db.create()')
    if not engine:
        raise ValueError('engine is None, not connected to a database')
    import bauble, bauble.meta as meta, bauble.pluginmgr as pluginmgr, datetime
    connection = engine.connect()
    transaction = connection.begin()
    try:
        try:
            metadata.drop_all(bind=connection, checkfirst=True)
            metadata.create_all(bind=connection)
            meta_table = meta.BaubleMeta.__table__
            meta_table.insert(bind=connection).execute(name=meta.VERSION_KEY, value=unicode(bauble.version)).close()
            meta_table.insert(bind=connection).execute(name=meta.CREATED_KEY, value=unicode(datetime.datetime.now())).close()
        except GeneratorExit as e:
            logger.warning('bauble.db.create(): %s' % utils.utf8(e))
            transaction.rollback()
            raise
        except Exception as e:
            logger.warning('bauble.db.create(): %s' % utils.utf8(e))
            transaction.rollback()
            raise
        else:
            transaction.commit()

    finally:
        connection.close()

    connection = engine.connect()
    transaction = connection.begin()
    try:
        try:
            pluginmgr.install('all', import_defaults, force=True)
        except GeneratorExit as e:
            logger.warning('bauble.db.create(): %s' % utils.utf8(e))
            transaction.rollback()
            raise
        except Exception as e:
            logger.warning('bauble.db.create(): %s' % utils.utf8(e))
            transaction.rollback()
            raise
        else:
            transaction.commit()

    finally:
        connection.close()


def verify_connection(engine, show_error_dialogs=False):
    """
    Test whether a connection to an engine is a valid Ghini database. This
    method will raise an error for the first problem it finds with the
    database.

    :param engine: the engine to test
    :type engine: :class:`sqlalchemy.engine.Engine`
    :param show_error_dialogs: flag for whether or not to show message
        dialogs detailing the error, default=False
    :type show_error_dialogs: bool
    """
    import bauble
    if show_error_dialogs:
        try:
            return verify_connection(engine, False)
        except error.EmptyDatabaseError:
            msg = _('The database you have connected to is empty.')
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            raise
        except error.MetaTableError:
            msg = _('The database you have connected to does not have the bauble meta table.  This usually means that the database is either corrupt or it was created with an old version of Ghini')
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            raise
        except error.TimestampError:
            msg = _("The database you have connected to does not have a timestamp for when it was created. This usually means that there was a problem when you created the database or the database you connected to wasn't created with Ghini.")
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            raise
        except error.VersionError as e:
            msg = _('You are using Ghini version %(version)s while the database you have connected to was created with version %(db_version)s\n\nSome things might not work as or some of your data may become unexpectedly corrupted.') % {'version': bauble.version, 'db_version': '%s' % e.version}
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            raise

    if len(engine.table_names()) == 0:
        raise error.EmptyDatabaseError()
    import bauble.meta as meta
    if not engine.has_table(meta.BaubleMeta.__tablename__):
        raise error.MetaTableError()
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine)()
    query = session.query
    result = query(meta.BaubleMeta).filter_by(name=meta.CREATED_KEY).first()
    if not result:
        session.close()
        raise error.TimestampError()
    result = query(meta.BaubleMeta).filter_by(name=meta.VERSION_KEY).first()
    if not result:
        session.close()
        raise error.VersionError(None)
    try:
        major, minor, revision = result.value.split('.')
    except Exception:
        session.close()
        raise error.VersionError(result.value)

    if major != bauble.version_tuple[0] or minor != bauble.version_tuple[1]:
        session.close()
        raise error.VersionError(result.value)
    session.close()
    return True


class WithNotes:
    key_pattern = re.compile('{[^:]+:(.*)}')

    def __getattr__(self, name):
        """retrieve value from corresponding note(s)

        the result can be an atomic value, a list, or a dictionary.
        """
        result = []
        is_dict = False
        for n in self.notes:
            if n.category == '[%s]' % name:
                result.append(n.note)
            elif n.category.startswith('{%s' % name):
                is_dict = True
                match = self.key_pattern.match(n.category)
                key = match.group(1)
                result.append((key, n.note))
            elif n.category == '<%s>' % name:
                try:
                    return eval(n.note)
                except:
                    return n.note

        if result == []:
            raise AttributeError(name)
        if is_dict:
            return dict(result)
        return result


class DefiningPictures:

    @property
    def pictures(self):
        """a list of gtk.Image objects
        """
        result = []
        for n in self.notes:
            if n.category != '<picture>':
                continue
            box = gtk.VBox()
            utils.ImageLoader(box, n.note).start()
            result.append(box)

        return result


class Serializable:
    import re
    single_cap_re = re.compile('([A-Z])')
    link_keys = []

    def as_dict(self):
        result = dict((col, getattr(self, col)) for col in self.__table__.columns.keys() if col not in ('id', ) and col[0] != '_' and getattr(self, col) is not None and not col.endswith('_id'))
        result['object'] = self.single_cap_re.sub('_\\1', self.__class__.__name__).lower()[1:]
        return result

    @classmethod
    def correct_field_names(cls, keys):
        """correct keys dictionary according to class attributes

        exchange format may use different keys than class attributes
        """
        pass

    @classmethod
    def compute_serializable_fields(cls, session, keys):
        """create objects corresponding to keys (class dependent)
        """
        return {}

    @classmethod
    def retrieve_or_create(cls, session, keys, create=True, update=True):
        """return database object corresponding to keys
        """
        logger.debug('initial value of keys: %s' % keys)
        is_in_session = cls.retrieve(session, keys)
        logger.debug('2 value of keys: %s' % keys)
        if not create and not is_in_session:
            logger.debug('returning None (1)')
            return
        else:
            if is_in_session and not update:
                logger.debug('returning not updated existing %s' % is_in_session)
                return is_in_session
            try:
                extradict = cls.compute_serializable_fields(session, keys)
                cls.correct_field_names(keys)
            except error.NoResultException:
                if not is_in_session:
                    logger.debug('returning None (2)')
                    return
                extradict = {}

            logger.debug('3 value of keys: %s' % keys)
            link_values = {}
            for k in cls.link_keys:
                if keys.get(k):
                    link_values[k] = keys[k]

            logger.debug('link_values : %s' % str(link_values))
            for k in keys.keys():
                if k not in class_mapper(cls).mapped_table.c:
                    del keys[k]

            if 'id' in keys:
                del keys['id']
            logger.debug('4 value of keys: %s' % keys)
            keys.update(extradict)
            logger.debug('5 value of keys: %s' % keys)
            if not is_in_session and create:
                logger.debug('links? %s, %s' % (cls.link_keys, keys.keys()))
                for key in cls.link_keys:
                    d = link_values.get(key)
                    if d is None:
                        continue
                    logger.debug('recursive call to construct_from_dict %s' % d)
                    obj = construct_from_dict(session, d)
                    keys[key] = obj

                logger.debug('going to create new %s with %s' % (cls, keys))
                result = cls(**keys)
                session.add(result)
            if is_in_session and update:
                result = is_in_session
                logger.debug('links? %s, %s' % (cls.link_keys, keys.keys()))
                for key in cls.link_keys:
                    d = link_values.get(key)
                    if d is None:
                        continue
                    logger.debug('recursive call to construct_from_dict %s' % d)
                    obj = construct_from_dict(session, d)
                    keys[key] = obj

            logger.debug('going to update %s with %s' % (result, keys))
            if 'id' in keys:
                del keys['id']
            for k, v in keys.items():
                if v is not None:
                    setattr(result, k, v)

            logger.debug('returning updated existing %s' % result)
            session.flush()
            logger.debug('returning new %s' % result)
            return result


def construct_from_dict(session, obj, create=True, update=True):
    logger.debug('construct_from_dict %s' % obj)
    klass = None
    if 'object' in obj:
        klass = class_of_object(obj['object'])
    if klass is None and 'rank' in obj:
        klass = globals().get(obj['rank'].capitalize())
        del obj['rank']
    return klass.retrieve_or_create(session, obj, create=create, update=update)


def class_of_object(o):
    """what class implements object o
    """
    name = ('').join(p.capitalize() for p in o.split('_'))
    return globals().get(name)