# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grokimdb/app.py
# Compiled at: 2008-01-27 19:50:14
import imdb, grok
from zope import schema
from zope.interface import Interface, implements

class GrokIMDB(grok.Application, grok.Container):
    __module__ = __name__


class Index(grok.View):
    __module__ = __name__
    grok.context(GrokIMDB)


class IMovie(Interface):
    """Infos about a movie.
    """
    __module__ = __name__
    id = schema.TextLine(title='IMDb ID', required=False)
    title = schema.TextLine(title='Title', required=False)
    year = schema.Int(title='Year', required=False)
    summary = schema.Text(title='Summary', required=False)


class Movie(grok.Model):
    """Infos about a movie.

    We can easily create movies::

    >>> from grokimdb.app import Movie
    >>> movie = Movie()
    >>> movie
    <grokimdb.app.Movie object at 0x...>

    """
    __module__ = __name__
    implements(IMovie)


class AddMovie(grok.AddForm):
    __module__ = __name__
    grok.context(GrokIMDB)
    form_fields = grok.AutoFields(IMovie)

    @grok.action('Add movie')
    def add(self, **data):
        movie = Movie()
        self.applyData(movie, **data)
        self.context[str(data['id'])] = movie
        self.redirect(self.url(movie))

    @grok.action('Lookup IMDb')
    def lookup(self, **data):
        movie = Movie()
        imdb_query = imdb.IMDb(accessSystem='http')
        results = imdb_query.search_movie(data['title'])
        if not results:
            self.redirect(self.url(context) + '/@@addmovie')
            return
        result = results[0]
        imdb_query.update(result)
        data['id'], data['year'], data['title'] = result.getID(), result['year'], result['title']
        data['summary'] = (' ').join(result['plot'])
        self.applyData(movie, **data)
        self.context[str(data['id'])] = movie
        self.redirect(self.url(movie) + '/@@edit')


class DisplayMovie(grok.DisplayForm):
    __module__ = __name__
    grok.context(IMovie)
    grok.name('index')
    form_fields = grok.AutoFields(IMovie)


class EditMovie(grok.EditForm):
    __module__ = __name__
    grok.context(IMovie)
    grok.name('edit')
    form_fields = grok.AutoFields(IMovie)

    @grok.action('Apply changes')
    def applyChanges(self, **data):
        self.applyData(self.context, **data)

    @grok.action('Return to index')
    def returnToIndex(self, **data):
        self.applyData(self.context, **data)
        self.redirect(self.url(self.context.__parent__))


class DeleteMovie(grok.View):
    __module__ = __name__
    grok.context(GrokIMDB)
    grok.name('delete')

    def update(self, id):
        del self.context[id]

    def render(self):
        self.redirect(self.url(self.context))


class GrokIMDB_XMLRPC(grok.XMLRPC):
    __module__ = __name__
    grok.context(GrokIMDB)

    def getMovieIDs(self):
        return list(self.context)

    def getMovie(self, movie_id):
        movie = self.context[movie_id]
        return {'title': movie.title, 'year': movie.year, 'summary': movie.summary}