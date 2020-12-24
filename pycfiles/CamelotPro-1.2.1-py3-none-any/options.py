# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/orm/options.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nThis module provides support for defining several options on your\nentities.  \n\n`using_options`\n---------------\nThe \'using_options\' DSL statement allows you to set up some additional\nbehaviors on your model objects, including table names, ordering, and\nmore.  To specify an option, simply supply the option as a keyword\nargument onto the statement, as follows:\n\n.. sourcecode:: python\n\n    class Person(Entity):\n        using_options(tablename=\'person\', order_by=\'name\')\n        name = Field(Unicode(64))\n\n        \n\nThe list of supported arguments are as follows:\n\n+---------------------+-------------------------------------------------------+\n| Option Name         | Description                                           |\n+=====================+=======================================================+\n| ``metadata``        | Specify a custom MetaData for this entity.            |\n|                     | By default, entities uses the global                  |\n|                     | ``camelot.core.orm.metadata``.                        |\n|                     | This option can also be set for all entities of a     |\n|                     | module by setting the ``__metadata__`` attribute of   |\n|                     | that module.                                          |\n+---------------------+-------------------------------------------------------+\n| ``tablename``       | Specify a custom tablename. You can either provide a  |\n|                     | plain string or a callable. The callable will be      |\n|                     | given the entity (ie class) as argument and must      |\n|                     | return a string representing the name of the table    |\n|                     | for that entity. By default, the tablename is         |\n|                     | automatically generated: it is a concatenation of the |\n|                     | full module-path to the entity and the entity (class) |\n|                     | name itself. The result is lower-cased and separated  |\n|                     | by underscores ("_"), eg.: for an entity named        |\n|                     | "MyEntity" in the module "project1.model", the        |\n|                     | generated table name will be                          |\n|                     | "project1_model_myentity".                            |\n+---------------------+-------------------------------------------------------+\n| ``order_by``        | How to order select results. Either a string or a     |\n|                     | list of strings, composed of the field name,          |\n|                     | optionally lead by a minus (for descending order).    |\n+---------------------+-------------------------------------------------------+\n| ``session``         | Specify a custom contextual session for this entity.  |\n|                     | By default, entities uses the global                  |\n|                     | ``camelot.core.orm.Session``.                         |\n|                     | This option takes a ``ScopedSession`` object or       |\n|                     | ``None``. In the later case your entity will be       |\n|                     | mapped using a non-contextual mapper which requires   |\n|                     | manual session management, as seen in pure SQLAlchemy.|\n+---------------------+-------------------------------------------------------+\n\nFor examples, please refer to the examples and unit tests.\n\n'
from sqlalchemy import types
from .statements import ClassMutator
DEFAULT_AUTO_PRIMARYKEY_NAME = 'id'
DEFAULT_AUTO_PRIMARYKEY_TYPE = types.Integer
OLD_M2MCOL_NAMEFORMAT = lambda data: '%(tablename)s_%(key)s%(numifself)s' % data
ALTERNATE_M2MCOL_NAMEFORMAT = lambda data: '%(inversename)s_%(key)s' % data

def default_m2m_column_formatter(data):
    if data['selfref']:
        return ALTERNATE_M2MCOL_NAMEFORMAT(data)
    else:
        return OLD_M2MCOL_NAMEFORMAT(data)


NEW_M2MCOL_NAMEFORMAT = default_m2m_column_formatter
FKCOL_NAMEFORMAT = '%(relname)s_%(key)s'
M2MCOL_NAMEFORMAT = NEW_M2MCOL_NAMEFORMAT
CONSTRAINT_NAMEFORMAT = '%(tablename)s_%(colnames)s_fk'
MULTIINHERITANCECOL_NAMEFORMAT = '%(entity)s_%(key)s'
options_defaults = dict(identity=None, tablename=None, shortnames=False, auto_primarykey=True, order_by=None, table_options={})
valid_options = options_defaults.keys() + [
 'metadata',
 'session']

class using_options(ClassMutator):
    """This statement its sole reason of existence is to keep existing Elixir
    model definitions working.  Do not use it when writing new code, instead
    use Declarative directly."""

    def process(self, entity_dict, tablename=None, **kwargs):
        if tablename:
            entity_dict.setdefault('__tablename__', tablename)
        for kwarg in kwargs:
            if kwarg in valid_options:
                setattr(entity_dict['_descriptor'], kwarg, kwargs[kwarg])
            else:
                raise Exception("'%s' is not a valid option for entities." % kwarg)