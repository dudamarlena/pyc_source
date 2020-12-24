# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/papydvd/utils.py
# Compiled at: 2011-02-13 13:02:58
import csv, transaction
from papydvd.models import DBSession
from papydvd.models import Movie

def importMovies(path):
    """Import movies from CSV"""
    reader = csv.reader(open(path, 'r'), delimiter='\t', quotechar='"')
    session = DBSession()
    for row in reader:
        (movie_id, title, genre_id, primary_number, secondary_number, director_id, year, add_date) = row
        movie = Movie(title=title, primary_number=primary_number, secondary_number=secondary_number or 0, genre_id=genre_id or None, director_id=director_id or None, year=year or None)
        session.add(movie)

    session.flush()
    transaction.commit()
    return