# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/examples/db/sqlalchemy_examples.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 2226 bytes
"""Examples for using sqlalchemy fixtures.

See a complete, more accurate example in http://farmdev.com/projects/fixture/docs/

"""
try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

Category, Product, Offer = (None, None, None)
if sqlalchemy:
    from sqlalchemy import *
    from sqlalchemy.orm import *
    metadata = MetaData()
    categories = Table('fixture_sqlalchemy_category', metadata, Column('id', INT, primary_key=True), Column('name', String(100)))

    class Category(object):
        pass


    products = Table('fixture_sqlalchemy_product', metadata, Column('id', INT, primary_key=True), Column('name', String(100)), Column('category_id', INT, ForeignKey('fixture_sqlalchemy_category.id')))

    class Product(object):
        pass


    offers = Table('fixture_sqlalchemy_offer', metadata, Column('id', INT, primary_key=True), Column('name', String(100)), Column('category_id', INT, ForeignKey('fixture_sqlalchemy_category.id')), Column('product_id', INT, ForeignKey('fixture_sqlalchemy_product.id')))

    class Offer(object):
        pass


    authors = Table('authors', metadata, Column('id', Integer, primary_key=True), Column('first_name', String(100)), Column('last_name', String(100)))

    class Author(object):
        pass


    books = Table('books', metadata, Column('id', Integer, primary_key=True), Column('title', String(100)), Column('author_id', Integer, ForeignKey('authors.id')))

    class Book(object):
        pass


def connect(dsn):
    metadata.bind = create_engine(dsn)


def setup_mappers():
    mapper(Category, categories)
    mapper(Product, products, properties={'category': relation(Category)})
    mapper(Offer, offers, properties={'category':relation(Category, backref='products'), 
     'product':relation(Product)})
    mapper(Author, authors)
    mapper(Book, books, properties={'author': relation(Author)})


if __name__ == '__main__':
    import doctest
    doctest.testmod()