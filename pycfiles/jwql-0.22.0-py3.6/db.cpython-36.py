# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/apps/jwql/db.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 4400 bytes
"""Connects to the ``jwql`` database.

This module is the primary interface between the ``jwql`` webapp and
the ``jwql`` database. It uses ``SQLAlchemy`` to start a session with
the database, and provides class methods that perform useful queries on
that database (for example, getting the names of all the files
associated with a certain instrument).

Authors
-------

    - Lauren Chambers

Use
---
    This module can be used as such:

    ::
        from db import DatabaseConnection
        db_connect = DatabaseConnection()
        data = db_connect.get_filenames_for_instrument('NIRCam')

Dependencies
------------
    The user must have a configuration file named ``config.json``
    placed in ``jwql/utils/`` directory.
"""
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from astroquery.mast import Mast
from jwql.utils.utils import get_config

class DatabaseConnection:
    __doc__ = 'Facilitates connection with the ``jwql`` database.\n\n    Attributes\n    ----------\n    ObservationWebtest : obj\n        Class instance in an "automap" schema corresponding to the\n        ``observationwebtest`` database table\n    session : obj\n        Session with the database that enables querying\n    '

    def __init__(self, db_type, instrument=None):
        """Determine what kind of database is being queried, and
        call appropriate initialization method
        """
        self.db_type = db_type
        assert self.db_type in ('MAST', 'SQL'), 'Unrecognized database type: {}. Must be SQL or MAST.'.format(db_type)
        if self.db_type == 'MAST':
            self.init_MAST(instrument)
        elif self.db_type == 'SQL':
            self.init_SQL()

    def init_SQL(self):
        """Start SQLAlchemy session with the ``jwql`` database"""
        connection_string = get_config()['database']['connection_string']
        engine = create_engine(connection_string)
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        self.ObservationWebtest = Base.classes.observations_webtest
        self.session = Session(engine)

    def init_MAST(self, instrument=None):
        """Determine the necessary service string to query the MAST
        database.
        """
        if instrument:
            instrument = instrument[0].upper() + instrument[1:].lower()
        else:
            raise TypeError('Must provide instrument to initialize MAST database.')
        self.service = 'Mast.Jwst.Filtered.' + instrument
        print(self.service)

    def get_files_for_instrument(self, instrument):
        """Given an instrument, query the database for all filenames
        and paths associated with said instrument

        Parameters
        ----------
        instrument : str
            Name of JWST instrument

        Returns
        -------
        filepaths: list
            List of all filepaths in database for the provided
            instrument
        filenames: list
            List of all filenames in database for the provided
            instrument
        """
        instrument = instrument.upper()
        if self.db_type == 'SQL':
            results = self.session.query(self.ObservationWebtest).filter(self.ObservationWebtest.instrument == instrument)
        else:
            if self.db_type == 'MAST':
                params = {'columns':'*', 
                 'filters':[]}
                response = Mast.service_request_async(self.service, params)
                results = response[0].json()['data']
        filepaths = []
        filenames = []
        for i in results:
            if self.db_type == 'SQL':
                filename = i.filename
            else:
                if self.db_type == 'MAST':
                    filename = i['filename']
            prog_id = filename[2:7]
            file_path = os.path.join('jw' + prog_id, filename)
            filepaths.append(file_path)
            filenames.append(filename)

        return (filepaths, filenames)