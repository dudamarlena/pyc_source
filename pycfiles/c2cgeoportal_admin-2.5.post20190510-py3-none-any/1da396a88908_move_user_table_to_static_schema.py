# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/static/versions/1da396a88908_move_user_table_to_static_schema.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Move user table to static schema\n\nRevision ID: 1da396a88908\nRevises: 3f89a7d71a5e\nCreate Date: 2015-02-20 14:09:04.875390\n'
try:
    from hashlib import sha1
    sha1
except ImportError:
    from sha import new as sha1

from alembic import op, context
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Unicode, Boolean
revision = '1da396a88908'
down_revision = '3f89a7d71a5e'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    staticschema = schema + '_static'
    parentschema = context.get_context().config.get_main_option('parentschema')
    engine = op.get_bind().engine
    if type(engine).__name__ != 'MockConnection' and op.get_context().dialect.has_table(engine, 'user', schema=staticschema):
        return
    else:
        op.create_table('user', Column('type', String(10), nullable=False), Column('id', Integer, primary_key=True), Column('username', Unicode, unique=True, nullable=False), Column('password', Unicode, nullable=False), Column('email', Unicode, nullable=False), Column('is_password_changed', Boolean, default=False), Column('role_name', String), schema=staticschema)
        parent_column = ''
        parent_select = ''
        parent_join = ''
        if parentschema is not None and parentschema is not '':
            op.add_column('user', Column('parent_role_name', String), schema=staticschema)
            parent_column = ', parent_role_name'
            parent_select = ', pr.name'
            parent_join = ('LEFT OUTER JOIN {parentschema!s}.role AS pr ON (pr.id = u.parent_role_id)').format(parentschema=parentschema)
        try:
            op.execute('INSERT INTO %(staticschema)s.user (type, username, password, email, is_password_changed, role_name%(parent_column)s) (SELECT u.type, u.username, u.password, u.email, u.is_password_changed, r.name%(parent_select)s FROM %(schema)s.user AS u LEFT OUTER JOIN %(schema)s.role AS r ON (r.id = u.role_id) %(parent_join)s)' % {'staticschema': staticschema, 
               'schema': schema, 
               'parent_select': parent_select, 
               'parent_column': parent_column, 
               'parent_join': parent_join})
            op.drop_table('user', schema=schema)
        except:
            op.execute("INSERT INTO %(staticschema)s.user (type, username, email, password, role) VALUES ( 'user', 'admin', 'info@example.com', '%(pass)s', 'role_admin')" % {'staticschema': staticschema, 
               'pass': sha1('admin').hexdigest()})

        return


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    staticschema = schema + '_static'
    parentschema = context.get_context().config.get_main_option('parentschema')
    op.create_table('user', Column('type', String(10), nullable=False), Column('id', Integer, primary_key=True), Column('username', Unicode, unique=True, nullable=False), Column('password', Unicode, nullable=False), Column('email', Unicode, nullable=False), Column('is_password_changed', Boolean, default=False), Column('role_id', Integer, ForeignKey(schema + '.role.id'), nullable=False), schema=schema)
    parent_column = ''
    parent_select = ''
    parent_join = ''
    if parentschema is not None and parentschema is not '':
        op.add_column('user', Column('parent_role_id', Integer, ForeignKey(parentschema + '.role.id')), schema=schema)
        parent_column = ', parent_role_id'
        parent_select = ', pr.id'
        parent_join = ('LEFT OUTER JOIN {parentschema}.role AS pr ON (pr.name = u.parent_role_name)').format(parentschema=parentschema)
    op.execute('INSERT INTO %(schema)s.user (type, username, password, email, is_password_changed, role_id%(parent_column)s) (SELECT u.type, u.username, u.password, u.email, u.is_password_changed, r.id%(parent_select)s FROM %(staticschema)s.user AS u LEFT OUTER JOIN %(schema)s.role AS r ON (r.name = u.role_name) %(parent_join)s)' % {'staticschema': staticschema, 
       'schema': schema, 
       'parent_select': parent_select, 
       'parent_column': parent_column, 
       'parent_join': parent_join})
    op.drop_table('user', schema=staticschema)
    return