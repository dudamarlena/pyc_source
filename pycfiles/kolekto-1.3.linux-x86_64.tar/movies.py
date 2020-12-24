# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/profiles/movies.py
# Compiled at: 2014-06-16 16:12:17
import unicodedata, re
from . import Profile

class Movie(dict):
    """ Represent a movie in a dict.
    """

    @property
    def slug(self):
        """ Get a slug from the movie title.
        """
        slug = unicodedata.normalize('NFKD', self['title']).encode('ascii', 'ignore')
        slug = slug.lower().replace(' ', '_')
        slug = re.sub('[^a-z0-9_]', '', slug)
        return slug

    def __unicode__(self):
        if self.get('directors'):
            directors = ' by '
            if len(self['directors']) > 1:
                directors += '%s and %s' % ((', ').join(self['directors'][0:-1]),
                 self['directors'][(-1)])
            else:
                directors += self['directors'][0]
        else:
            directors = ''
        fmt = '<b>{title}</b> ({year}){directors}'
        return fmt.format(title=self.get('title', 'No title'), year=self.get('year', 'Unknown'), directors=directors)


class Movies(Profile):
    """ A profile for movies.
    """
    object_class = Movie