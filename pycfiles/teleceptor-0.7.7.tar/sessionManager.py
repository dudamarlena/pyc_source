# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esalazar/git/teleceptor/teleceptor/sessionManager.py
# Compiled at: 2014-09-03 00:02:17
"""
    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import teleceptor
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = 'sqlite:///' + teleceptor.DBFILE

@contextmanager
def sessionScope():
    """Provide a transactional scope around a series of operations."""
    db = create_engine(engine)
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise

    finally:
        session.close()