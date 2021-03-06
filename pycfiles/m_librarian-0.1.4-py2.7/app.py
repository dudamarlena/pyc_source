# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/web/app.py
# Compiled at: 2018-06-11 09:54:59
import os
from sqlobject.sqlbuilder import CONCAT
from bottle import cheetah_view, redirect, request, route, static_file
from m_librarian.config import get_config
from m_librarian.db import Author, Book
from m_librarian.download import download
from m_librarian.search import search_authors, search_books

@route('/')
@cheetah_view('index.tmpl')
def index():
    return {'get_config': get_config}


@route('/search_authors', method='GET')
def _search_authors():
    return redirect('/search_authors/')


@route('/search_authors/', method='GET')
@cheetah_view('search_authors.tmpl')
def search_authors_get():
    return {}


def decode(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def _guess_case_sensitivity(value):
    return not value.islower()


@route('/search_authors/', method='POST')
@cheetah_view('list_authors.tmpl')
def search_authors_post():
    value = request.forms.get('search_authors')
    if not value:
        return redirect('/search_authors/')
    else:
        value = decode(value)
        search_type = request.forms.get('search_type')
        if not search_type:
            search_type = 'start'
        case_sensitive = request.forms.get('case_sensitive')
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(value)
        expressions = [
         (CONCAT(Author.q.surname, ' ', Author.q.name, ' ', Author.q.misc_name),
          decode(value))]
        authors = search_authors(search_type, case_sensitive, {}, expressions, orderBy=('surname',
                                                                                        'name',
                                                                                        'misc_name'))
        columns = get_config().getlist('columns', 'author', ['fullname'])
        return {'authors': list(authors), 
           'search_authors': value, 
           'search_type': search_type, 
           'case_sensitive': case_sensitive, 
           'columns': columns}


@route('/books-by-author/<id:int>/', method='GET')
@cheetah_view('books_by_author.tmpl')
def books_by_author(id):
    use_filters = get_config().getint('filters', 'use_in_books_list', 1)
    columns = get_config().getlist('columns', 'book', ['title'])
    if use_filters:
        join_expressions = []
        join_expressions.append(Book.j.authors)
        join_expressions.append(Author.q.id == id)
        books = search_books('full', None, {}, join_expressions, orderBy=('series',
                                                                          'ser_no',
                                                                          'title'), use_filters=use_filters)
        return {'author': Author.get(id), 
           'books': books, 
           'columns': columns}
    else:
        return {'author': Author.get(id), 'books': Book.select(Book.j.authors & (Author.q.id == id), orderBy=[
                   'series', 'ser_no', 'title']), 
           'columns': columns}
        return


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), 'static'))


@route('/download/', method='POST')
@cheetah_view('download.tmpl')
def download_books():
    books_ids = request.forms.getall('books')
    download_path = get_config().getpath('download', 'path')
    if books_ids:
        for id in books_ids:
            book = Book.get(int(id))
            download(book, download_path)

        return {'message': 'Книги сохранены.'}
    else:
        return {'message': 'Не выбрано книг для сохранения.'}


@route('/search_books', method='GET')
def _search_books():
    return redirect('/search_books/')


@route('/search_books/', method='GET')
@cheetah_view('search_books.tmpl')
def search_books_get():
    return {'get_config': get_config}


@route('/search_books/', method='POST')
@cheetah_view('list_books.tmpl')
def search_books_post():
    value = request.forms.get('search_books')
    if not value:
        return redirect('/search_books/')
    else:
        value = decode(value)
        search_type = request.forms.get('search_type')
        if not search_type:
            search_type = 'start'
        case_sensitive = request.forms.get('case_sensitive')
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(value)
        use_filters = request.forms.get('use_filters')
        books = search_books(search_type, case_sensitive, {'title': value}, None, orderBy=('title', ), use_filters=use_filters)
        books_by_authors = {}
        for book in books:
            author = book.author1
            if author in books_by_authors:
                books_by_author = books_by_authors[author]
            else:
                books_by_author = books_by_authors[author] = []
            books_by_author.append(book)

        columns = get_config().getlist('columns', 'book', ['title'])
        return {'books_by_author': books_by_authors, 
           'search_books': value, 
           'search_type': search_type, 
           'case_sensitive': case_sensitive, 
           'columns': columns}