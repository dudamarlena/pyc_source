# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/examples/db/storm_examples.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 2181 bytes
"""examples for using Storm fixtures."""
try:
    import storm
except ImportError:
    storm = None

Category, Product, Offer = (None, None, None)
if storm:
    from storm.locals import *

    class Category(Storm):
        __storm_table__ = 'fixture_storm_category'
        id = Int(primary=True)
        name = RawStr()


    class Product(Storm):
        __storm_table__ = 'fixture_storm_product'
        id = Int(primary=True)
        name = RawStr()
        category_id = Int()
        category = Reference(category_id, Category.id)


    class Offer(Storm):
        __storm_table__ = 'fixture_storm_offer'
        id = Int(primary=True)
        name = RawStr()
        category_id = Int()
        category = Reference(category_id, Category.id)
        product_id = Int()
        product = Reference(product_id, Product.id)


def setup_db(conn):
    if not conn is not None:
        raise AssertionError
    else:
        conn.rollback()
        backend = conn._connection.__class__.__name__
        tmpl = {'pk':{'PostgresConnection': 'serial primary key'}.get(backend, 'integer primary key'), 
         'str_type':{'PostgresConnection': 'bytea'}.get(backend, 'text collate binary')}
        conn.execute(SQL('DROP TABLE IF EXISTS fixture_storm_category'))
        conn.execute(SQL('CREATE TABLE fixture_storm_category (\n      id %(pk)s,\n      name %(str_type)s\n      )' % tmpl))
        assert conn.find(Category).count() == 0
        conn.execute(SQL('CREATE TABLE fixture_storm_product (\n       id %(pk)s,\n       name %(str_type)s,\n       category_id integer\n      )' % tmpl))
        assert conn.find(Product).count() == 0
        conn.execute(SQL('DROP TABLE IF EXISTS fixture_storm_offer'))
        conn.execute(SQL('CREATE TABLE fixture_storm_offer (\n       id %(pk)s,\n       name %(str_type)s,\n       category_id integer,\n       product_id integer\n      )' % tmpl))
        assert conn.find(Offer).count() == 0
    conn.commit()


def teardown_db(conn):
    assert conn is not None
    conn.rollback()
    for tb in (Offer, Product, Category):
        conn.execute(SQL('drop table ' + tb.__storm_table__))

    conn.commit()