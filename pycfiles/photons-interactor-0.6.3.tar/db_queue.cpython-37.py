# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stephenmoore/Projects/utility/photons-interactor/photons_interactor/database/db_queue.py
# Compiled at: 2020-02-25 22:11:59
# Size of source mod 2**32: 3110 bytes
"""
A connector between a bunch of database connections in threads
and the asyncio event loop.

Usage is as follows:

    def some_action(db):
        # db is an instance of photons_interactor.database.connection.DatabaseConnection
        entry = db.create_entry(...)
        db.add(entry)
    await db_queue.request(some_action)

By requesting the function you are putting it onto a queue that will be
picked up by another thread. That thread will then create a database session
that is passed into the function.

The `request` function returns a future that is eventually fulfilled by that
worker and that's how we get the result from the different thread back into the
event loop.
"""
from photons_interactor.database.connection import DatabaseConnection
from photons_app.errors import PhotonsAppError
from photons_app import helpers as hp
from sqlalchemy.pool import StaticPool
import sqlalchemy, logging, sys
log = logging.getLogger('photosn_interactor.database.db_queue')

class DBQueue(hp.ThreadToAsyncQueue):
    __doc__ = 'Connect asyncio to threaded database connections'
    _merged_options_formattable = True

    def setup(self, database):
        self.database = database

    def create_args(self, thread_number, existing):
        """This is run when the queue starts and before every request"""
        if existing:
            return existing
        return (DatabaseConnection((self.database), poolclass=StaticPool),)

    def wrap_request(self, proc, args):
        """We create a new session for every database request"""

        def ret():
            tries = 0
            while True:
                db, = args
                database = db.new_session()
                try:
                    try:
                        res = proc(database)
                        database.commit()
                        return res
                    except sqlalchemy.exc.OperationalError as error:
                        try:
                            database.rollback()
                            log.error(hp.lc('Failed to use database, will rollback and maybe try again',
                              error=error))
                            tries += 1
                            if tries > 1:
                                raise
                        finally:
                            error = None
                            del error

                    except sqlalchemy.exc.InvalidRequestError as error:
                        try:
                            database.rollback()
                            log.error(hp.lc('Failed to perform database operation', error=error))
                            raise
                        finally:
                            error = None
                            del error

                    except PhotonsAppError as error:
                        try:
                            database.rollback()
                            log.error(hp.lc('Failed to use database', error=error))
                            raise
                        finally:
                            error = None
                            del error

                    except:
                        database.rollback()
                        exc_info = sys.exc_info()
                        log.exception(hp.lc('Unexpected failure when using database', error=(exc_info[1])))
                        raise

                finally:
                    database.close()

        return ret