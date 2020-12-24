# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/examples/db/sqlobject_examples.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1207 bytes
"""examples for using SQLObject fixtures."""
try:
    import sqlobject
except ImportError:
    sqlobject = None

Category, Product, Offer = (None, None, None)
if sqlobject:
    from sqlobject import *

    class Category(SQLObject):

        class sqlmeta:
            table = 'fixture_sqlobject_category'

        name = StringCol()


    class Product(SQLObject):

        class sqlmeta:
            table = 'fixture_sqlobject_product'

        name = StringCol()
        category = ForeignKey('Category')


    class Offer(SQLObject):

        class sqlmeta:
            table = 'fixture_sqlobject_offer'

        name = StringCol()
        category = ForeignKey('Category')
        product = ForeignKey('Product')


def setup_db(conn):
    assert conn is not None
    Category.createTable(connection=conn)
    Product.createTable(connection=conn)
    Offer.createTable(connection=conn)


def teardown_db(conn):
    assert conn is not None
    for tb in (Offer, Product, Category):
        tb.dropTable(connection=conn)