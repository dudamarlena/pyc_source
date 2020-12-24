# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/cache.py
# Compiled at: 2012-03-18 03:50:21
import contextlib, datetime, logging, os, sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    engine = Column(String, primary_key=True)
    tag = Column(String, primary_key=True)
    filename = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, engine, tag, filename, timestamp=None):
        self.engine = engine
        self.tag = tag
        self.filename = filename
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return ('<Entry(engine="{}", tag="{}", filename="{}", timestamp={})>').format(self.engine, self.tag, self.filename, self.timestamp)


log = logging.getLogger(__name__)

class Cache:

    def __init__(self, filename):
        self.engine = sqlalchemy.create_engine(('sqlite:///{}').format(filename))
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _get_entry(self, engine, tag):
        return self.session.query(Entry).filter_by(tag=tag, engine=engine).first()

    def get(self, engine, tag):
        log.info(('retrieving from cache: {} {}').format(engine, tag))
        entry = self._get_entry(engine, tag)
        if not entry:
            log.info(('cache miss: {} {}').format(engine, tag))
            return None
        else:
            log.info(('cache hit: {} {}').format(engine, tag))
            if not os.path.exists(entry.filename):
                log.info(('cache file missing: {} {}').format(engine, tag))
                self.session.delete(entry)
                return None
            return entry.filename

    def set(self, engine, tag, filename):
        log.info(('Cache set: {} {} -> {}').format(engine, tag, filename))
        e = self._get_entry(engine, tag)
        if e:
            e.filename = filename
        else:
            e = Entry(engine=engine, tag=tag, filename=filename)
            self.session.add(e)

    def trim(self, size):
        log.info(('Cache trim: {}').format(size))
        curr_size = self.size()
        if curr_size <= size:
            return
        query = self.session.query(Entry).order_by(Entry.timestamp).limit(curr_size - size)
        for entry in query:
            self.session.delete(entry)

    def size(self):
        return self.session.query(Entry).count()

    def close(self, commit=True):
        log.info('Closing cache')
        if commit:
            self.session.commit()


@contextlib.contextmanager
def open_cache(filename, size):
    cache = Cache(filename)
    try:
        yield cache
        cache.trim(size)
        cache.close()
    except Exception:
        cache.close(commit=False)
        raise