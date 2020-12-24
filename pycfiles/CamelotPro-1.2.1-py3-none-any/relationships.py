# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/orm/relationships.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nThis module provides support for defining relationships between your\nentities.  Two syntaxes are supported to do so: the default\n`Attribute-based syntax`_ which supports the following types of relationships:\nManyToOne_, OneToMany_, OneToOne_ and ManyToMany_, as well as a\n`DSL-based syntax`_ which provides the following statements: belongs_to_,\nhas_many_, has_one_ and has_and_belongs_to_many_.\n\n======================\nAttribute-based syntax\n======================\n\nThe first argument to all these "normal" relationship classes is the name of\nthe class (entity) you are relating to.\n\nFollowing that first mandatory argument, any number of additional keyword\narguments can be specified for advanced behavior. See each relationship type\nfor a list of their specific keyword arguments. At this point, we\'ll just note\nthat all the arguments that are not specifically processed, as\nmentioned in the documentation below are passed on to the SQLAlchemy\n``relationship`` function. So, please refer to the `SQLAlchemy relationship function\'s\ndocumentation <http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html\n#building-a-relationship>`_ for further detail about which\nkeyword arguments are supported.\n\nYou should keep in mind that the following\nkeyword arguments are automatically generated and should not be used\nunless you want to override the default value provided : ``uselist``,\n``remote_side``, ``secondary``, ``primaryjoin`` and ``secondaryjoin``.\n\nAdditionally, if you want a bidirectionnal relationship, you should define the\ninverse relationship on the other entity explicitly (as opposed to how\nSQLAlchemy\'s backrefs are defined). In non-ambiguous situations, relationships will\nbe matched together automatically. If there are several relationships\nof the same type between two entities, you have to disambiguate the\nsituation by giving the name of the inverse relationship in the ``inverse``\nkeyword argument.\n\nHere is a detailed explanation of each relation type:\n\n`ManyToOne`\n-----------\n\nDescribes the child\'s side of a parent-child relationship.  For example,\na `Pet` object may belong to its owner, who is a `Person`.  This could be\nexpressed like so:\n\n.. sourcecode:: python\n\n    class Pet(Entity):\n        owner = ManyToOne(\'Person\')\n\nBehind the scene, assuming the primary key of the `Person` entity is\nan integer column named `id`, the ``ManyToOne`` relationship will\nautomatically add an integer column named `owner_id` to the entity, with a\nforeign key referencing the `id` column of the `Person` entity.\n\nIn addition to the keyword arguments inherited from SQLAlchemy\'s relation\nfunction, ``ManyToOne`` relationships accept the following optional arguments\nwhich will be directed to the created column:\n\n+----------------------+------------------------------------------------------+\n| Option Name          | Description                                          |\n+======================+======================================================+\n| ``colname``          | Specify a custom name for the foreign key column(s). |\n|                      | This argument accepts either a single string or a    |\n|                      | list of strings. The number of strings passed must   |\n|                      | match the number of primary key columns of the target|\n|                      | entity. If this argument is not used, the name of the|\n|                      | column(s) is generated with the pattern              |\n|                      | defined in options.FKCOL_NAMEFORMAT, which is, by    |\n|                      | default: "%(relname)s_%(key)s", where relname is the |\n|                      | name of the ManyToOne relationship, and \'key\' is the |\n|                      | name (key) of the primary column in the target       |\n|                      | entity. That\'s with, in the above Pet/owner example, |\n|                      | the name of the column would be: "owner_id".         |\n+----------------------+------------------------------------------------------+\n| ``required``         | Specify whether or not this field can be set to None |\n|                      | (left without a value). Defaults to ``False``,       |\n|                      | unless the field is a primary key.                   |\n+----------------------+------------------------------------------------------+\n| ``primary_key``      | Specify whether or not the column(s) created by this |\n|                      | relationship should act as a primary_key.            |\n|                      | Defaults to ``False``.                               |\n+----------------------+------------------------------------------------------+\n| ``column_kwargs``    | A dictionary holding any other keyword argument you  |\n|                      | might want to pass to the Column.                    |\n+----------------------+------------------------------------------------------+\n| ``target_column``    | Name (or list of names) of the target column(s).     |\n|                      | If this argument is not specified, the target entity |\n|                      | primary key column(s) are used.                      |\n+----------------------+------------------------------------------------------+\n\nThe following optional arguments are also supported to customize the\nForeignKeyConstraint that is created:\n\n+----------------------+------------------------------------------------------+\n| Option Name          | Description                                          |\n+======================+======================================================+\n| ``use_alter``        | If True, SQLAlchemy will add the constraint in a     |\n|                      | second SQL statement (as opposed to within the       |\n|                      | create table statement). This permits to define      |\n|                      | tables with a circular foreign key dependency        |\n|                      | between them.                                        |\n+----------------------+------------------------------------------------------+\n| ``ondelete``         | Value for the foreign key constraint ondelete clause.|\n|                      | May be one of: ``cascade``, ``restrict``,            |\n|                      | ``set null``, or ``set default``.                    |\n+----------------------+------------------------------------------------------+\n| ``onupdate``         | Value for the foreign key constraint onupdate clause.|\n|                      | May be one of: ``cascade``, ``restrict``,            |\n|                      | ``set null``, or ``set default``.                    |\n+----------------------+------------------------------------------------------+\n| ``constraint_kwargs``| A dictionary holding any other keyword argument you  |\n|                      | might want to pass to the Constraint.                |\n+----------------------+------------------------------------------------------+\n\nIn some cases, you may want to declare the foreign key column explicitly,\ninstead of letting it be generated automatically.  There are several reasons to\nthat: it could be because you want to declare it with precise arguments and\nusing column_kwargs makes your code ugly, or because the name of\nyour column conflicts with the property name (in which case an error is\nthrown).  In those cases, you can use the ``field`` argument to specify an\nalready-declared field to be used for the foreign key column.\n\nFor example, for the Pet example above, if you want the database column\n(holding the foreign key) to be called \'owner\', one should use the field\nparameter to specify the field manually.\n\n.. sourcecode:: python\n\n    class Pet(Entity):\n        owner_id = Field(Integer, colname=\'owner\')\n        owner = ManyToOne(\'Person\', field=owner_id)\n\n+----------------------+------------------------------------------------------+\n| Option Name          | Description                                          |\n+======================+======================================================+\n| ``field``            | Specify the previously-declared field to be used for |\n|                      | the foreign key column. Use of this parameter is     |\n|                      | mutually exclusive with the colname and column_kwargs|\n|                      | arguments.                                           |\n+----------------------+------------------------------------------------------+\n\n\nAdditionally, the belongs_to_ statement is supported as an alternative,\nDSL-based, syntax to define ManyToOne_ relationships.\n\n\n`OneToMany`\n-----------\n\nDescribes the parent\'s side of a parent-child relationship when there can be\nseveral children.  For example, a `Person` object has many children, each of\nthem being a `Person`. This could be expressed like so:\n\n.. sourcecode:: python\n\n    class Person(Entity):\n        parent = ManyToOne(\'Person\')\n        children = OneToMany(\'Person\')\n\nNote that a ``OneToMany`` relationship **cannot exist** without a\ncorresponding ``ManyToOne`` relationship in the other way. This is because the\n``OneToMany`` relationship needs the foreign key created by the ``ManyToOne``\nrelationship.\n\nIn addition to keyword arguments inherited from SQLAlchemy, ``OneToMany``\nrelationships accept the following optional (keyword) arguments:\n\n+--------------------+--------------------------------------------------------+\n| Option Name        | Description                                            |\n+====================+========================================================+\n| ``order_by``       | Specify which field(s) should be used to sort the      |\n|                    | results given by accessing the relation field.         |\n|                    | Note that this sort order is only applied when loading |\n|                    | objects from the database. Objects appended to the     |\n|                    | collection afterwards are not re-sorted in-memory on   |\n|                    | the fly.                                               |\n|                    | This argument accepts either a string or a list of     |\n|                    | strings, each corresponding to the name of a field in  |\n|                    | the target entity. These field names can optionally be |\n|                    | prefixed by a minus (for descending order).            |\n+--------------------+--------------------------------------------------------+\n| ``filter``         | Specify a filter criterion (as a clause element) for   |\n|                    | this relationship. This criterion will be ``and_`` ed  |\n|                    | with the normal join criterion (primaryjoin) generated |\n|                    | by Elixir for the relationship. For example:           |\n|                    | boston_addresses =                                     |\n|                    | OneToMany(\'Address\', filter=Address.city == \'Boston\')  |\n+--------------------+--------------------------------------------------------+\n\nAdditionally, an alternate DSL-based is supported, syntax to define\nOneToMany_ relationships, with the has_many_ statement.\n\n\n`OneToOne`\n----------\n\nDescribes the parent\'s side of a parent-child relationship when there is only\none child.  For example, a `Car` object has one gear stick, which is\nrepresented as a `GearStick` object. This could be expressed like so:\n\n.. sourcecode:: python\n\n    class Car(Entity):\n        gear_stick = OneToOne(\'GearStick\', inverse=\'car\')\n\n    class GearStick(Entity):\n        car = ManyToOne(\'Car\')\n\nNote that a ``OneToOne`` relationship **cannot exist** without a corresponding\n``ManyToOne`` relationship in the other way. This is because the ``OneToOne``\nrelationship needs the foreign_key created by the ``ManyToOne`` relationship.\n\nAdditionally, an alternate DSL-based syntax is supported to define\nOneToOne_ relationships, with the has_one_ statement.\n\n\n`ManyToMany`\n------------\n\nDescribes a relationship in which one kind of entity can be related to several\nobjects of the other kind but the objects of that other kind can be related to\nseveral objects of the first kind.  For example, an `Article` can have several\ntags, but the same `Tag` can be used on several articles.\n\n.. sourcecode:: python\n\n    class Article(Entity):\n        tags = ManyToMany(\'Tag\')\n\n    class Tag(Entity):\n        articles = ManyToMany(\'Article\')\n\nBehind the scene, the ``ManyToMany`` relationship will automatically create an\nintermediate table to host its data.\n\nNote that you don\'t necessarily need to define the inverse relationship.  In\nour example, even though we want tags to be usable on several articles, we\nmight not be interested in which articles correspond to a particular tag.  In\nthat case, we could have omitted the `Tag` side of the relationship.\n\nIf your ``ManyToMany`` relationship is self-referencial, the entity\ncontaining it is autoloaded (and you don\'t intend to specify both the\nprimaryjoin and secondaryjoin arguments manually), you must specify at least\none of either the ``remote_colname`` or ``local_colname`` argument.\n\nIn addition to keyword arguments inherited from SQLAlchemy, ``ManyToMany``\nrelationships accept the following optional (keyword) arguments:\n\n+--------------------+--------------------------------------------------------+\n| Option Name        | Description                                            |\n+====================+========================================================+\n| ``tablename``      | Specify a custom name for the intermediary table. This |\n|                    | can be used both when the tables needs to be created   |\n|                    | and when the table is autoloaded/reflected from the    |\n|                    | database. If this argument is not used, a name will be |\n|                    | automatically generated by Elixir depending on the name|\n|                    | of the tables of the two entities of the relationship, |\n|                    | the name of the relationship, and, if present, the name|\n|                    | of its inverse. Even though this argument is optional, |\n|                    | it is wise to use it if you are not sure what are the  |\n|                    | exact consequence of using a generated table name.     |\n+--------------------+--------------------------------------------------------+\n| ``schema``         | Specify a custom schema for the intermediate table.    |\n|                    | This can be used both when the tables needs to         |\n|                    | be created and when the table is autoloaded/reflected  |\n|                    | from the database.                                     |\n+--------------------+--------------------------------------------------------+\n| ``remote_colname`` | A string or list of strings specifying the names of    |\n|                    | the column(s) in the intermediary table which          |\n|                    | reference the "remote"/target entity\'s table.          |\n+--------------------+--------------------------------------------------------+\n| ``local_colname``  | A string or list of strings specifying the names of    |\n|                    | the column(s) in the intermediary table which          |\n|                    | reference the "local"/current entity\'s table.          |\n+--------------------+--------------------------------------------------------+\n| ``table``          | Use a manually created table. If this argument is      |\n|                    | used, Elixir won\'t generate a table for this           |\n|                    | relationship, and use the one given instead.           |\n+--------------------+--------------------------------------------------------+\n| ``order_by``       | Specify which field(s) should be used to sort the      |\n|                    | results given by accessing the relation field.         |\n|                    | Note that this sort order is only applied when loading |\n|                    | objects from the database. Objects appended to the     |\n|                    | collection afterwards are not re-sorted in-memory on   |\n|                    | the fly.                                               |\n|                    | This argument accepts either a string or a list of     |\n|                    | strings, each corresponding to the name of a field in  |\n|                    | the target entity. These field names can optionally be |\n|                    | prefixed by a minus (for descending order).            |\n+--------------------+--------------------------------------------------------+\n| ``ondelete``       | Value for the foreign key constraint ondelete clause.  |\n|                    | May be one of: ``cascade``, ``restrict``,              |\n|                    | ``set null``, or ``set default``.                      |\n+--------------------+--------------------------------------------------------+\n| ``onupdate``       | Value for the foreign key constraint onupdate clause.  |\n|                    | May be one of: ``cascade``, ``restrict``,              |\n|                    | ``set null``, or ``set default``.                      |\n+--------------------+--------------------------------------------------------+\n| ``table_kwargs``   | A dictionary holding any other keyword argument you    |\n|                    | might want to pass to the underlying Table object.     |\n+--------------------+--------------------------------------------------------+\n\n\n================\nDSL-based syntax\n================\n\nThe following DSL statements provide an alternative way to define relationships\nbetween your entities. The first argument to all those statements is the name\nof the relationship, the second is the \'kind\' of object you are relating to\n(it is usually given using the ``of_kind`` keyword).\n\n`belongs_to`\n------------\n\nThe ``belongs_to`` statement is the DSL syntax equivalent to the ManyToOne_\nrelationship. As such, it supports all the same arguments as ManyToOne_\nrelationships.\n\n.. sourcecode:: python\n\n    class Pet(Entity):\n        belongs_to(\'feeder\', of_kind=\'Person\')\n        belongs_to(\'owner\', of_kind=\'Person\', colname="owner_id")\n\n\n`has_many`\n----------\n\nThe ``has_many`` statement is the DSL syntax equivalent to the OneToMany_\nrelationship. As such, it supports all the same arguments as OneToMany_\nrelationships.\n\n.. sourcecode:: python\n\n    class Person(Entity):\n        belongs_to(\'parent\', of_kind=\'Person\')\n        has_many(\'children\', of_kind=\'Person\')\n\nThere is also an alternate form of the ``has_many`` relationship that takes\nonly two keyword arguments: ``through`` and ``via`` in order to encourage a\nricher form of many-to-many relationship that is an alternative to the\n``has_and_belongs_to_many`` statement.  Here is an example:\n\n.. sourcecode:: python\n\n    class Person(Entity):\n        has_field(\'name\', Unicode)\n        has_many(\'assignments\', of_kind=\'Assignment\')\n        has_many(\'projects\', through=\'assignments\', via=\'project\')\n\n    class Assignment(Entity):\n        has_field(\'start_date\', DateTime)\n        belongs_to(\'person\', of_kind=\'Person\')\n        belongs_to(\'project\', of_kind=\'Project\')\n\n    class Project(Entity):\n        has_field(\'title\', Unicode)\n        has_many(\'assignments\', of_kind=\'Assignment\')\n\nIn the above example, a `Person` has many `projects` through the `Assignment`\nrelationship object, via a `project` attribute.\n\n\n`has_one`\n---------\n\nThe ``has_one`` statement is the DSL syntax equivalent to the OneToOne_\nrelationship. As such, it supports all the same arguments as OneToOne_\nrelationships.\n\n.. sourcecode:: python\n\n    class Car(Entity):\n        has_one(\'gear_stick\', of_kind=\'GearStick\', inverse=\'car\')\n\n    class GearStick(Entity):\n        belongs_to(\'car\', of_kind=\'Car\')\n\n\n`has_and_belongs_to_many`\n-------------------------\n\nThe ``has_and_belongs_to_many`` statement is the DSL syntax equivalent to the\nManyToMany_ relationship. As such, it supports all the same arguments as\nManyToMany_ relationships.\n\n.. sourcecode:: python\n\n    class Article(Entity):\n        has_and_belongs_to_many(\'tags\', of_kind=\'Tag\')\n\n    class Tag(Entity):\n        has_and_belongs_to_many(\'articles\', of_kind=\'Article\')\n\n'
import logging
from sqlalchemy import schema, sql
from sqlalchemy.orm import relationship, backref, class_mapper
from .properties import DeferredProperty
from .entity import EntityBase
from .fields import Field
from .statements import ClassMutator
from . import options
LOGGER = logging.getLogger('camelot.core.orm.relationships')

class Relationship(DeferredProperty):
    """Generates a one to many or many to one relationship."""
    process_order = 0

    def __init__(self, of_kind, inverse=None, *args, **kwargs):
        super(Relationship, self).__init__()
        self.of_kind = of_kind
        self.inverse_name = inverse
        self._target = None
        self.property = None
        self.backref = None
        self.args = args
        self.kwargs = kwargs
        return

    @property
    def target(self):
        if not self._target:
            if isinstance(self.of_kind, basestring):
                try:
                    self._target = self.entity._decl_class_registry[self.of_kind.split('.')[(-1)]]
                except KeyError:
                    LOGGER.error('Error setting up %s of %s' % (self.name,
                     self.entity.__name__))
                    raise

            else:
                self._target = self.of_kind
        return self._target

    def attach(self, entity, name):
        super(Relationship, self).attach(entity, name)
        entity._descriptor.relationships.append(self)

    @property
    def inverse(self):
        if hasattr(self, '_inverse') or self.inverse_name:
            desc = self.target._descriptor
            inverse = desc.find_relationship(self.inverse_name)
            if inverse is None:
                raise Exception("Couldn't find a relationship named '%s' in entity '%s' or its parent entities." % (
                 self.inverse_name, self.target.__name__))
            if not self.match_type_of(inverse):
                raise AssertionError("Relationships '%s' in entity '%s' and '%s' in entity '%s' cannot be inverse of each other because their types do not form a valid combination." % (
                 self.name, self.entity.__name__,
                 self.inverse_name, self.target.__name__))
            else:
                check_reverse = not self.kwargs.get('viewonly', False)
                if issubclass(self.target, EntityBase):
                    inverse = self.target._descriptor.get_inverse_relation(self, check_reverse=check_reverse)
                else:
                    inverse = None
            self._inverse = inverse
            if inverse and not self.kwargs.get('viewonly', False):
                inverse._inverse = self
        return self._inverse

    def match_type_of(self, other):
        return False

    def is_inverse(self, other):
        return not other.kwargs.get('viewonly', False) and other is not self and self.match_type_of(other) and self.entity == other.target and other.entity == self.target and (self.inverse_name == other.name or not self.inverse_name) and (other.inverse_name == self.name or not other.inverse_name)

    def create_pk_cols(self):
        self.create_keys(True)

    def create_non_pk_cols(self):
        self.create_keys(False)

    def create_keys(self, pk):
        """
        Subclasses (ie. concrete relationships) may override this method to
        create foreign keys.
        """
        pass

    def create_properties(self):
        if self.property or self.backref:
            return
        kwargs = self.get_prop_kwargs()
        if 'order_by' in kwargs:
            kwargs['order_by'] = self.target._descriptor.translate_order_by(kwargs['order_by'])
        if self.inverse and not kwargs.get('viewonly', False):
            if self.inverse.backref:
                if 'backref' not in kwargs:
                    kwargs['backref'] = self.inverse.backref
            else:
                kwargs.pop('secondary', None)
                self.backref = backref(self.name, **kwargs)
                return
        self.property = relationship(self.target, **kwargs)
        setattr(self.entity, self.name, self.property)
        return


class OneToOne(Relationship):
    uselist = False
    process_order = 2

    def __init__(self, of_kind, filter=None, *args, **kwargs):
        self.filter = filter
        if filter is not None:
            if 'viewonly' not in kwargs:
                kwargs['viewonly'] = True
        super(OneToOne, self).__init__(of_kind, *args, **kwargs)
        return

    def match_type_of(self, other):
        return isinstance(other, ManyToOne)

    def create_keys(self, pk):
        if pk == False and self.inverse is None:
            raise Exception("Couldn't find any relationship in '%s' which match as inverse of the '%s' relationship defined in the '%s' entity. If you are using inheritance you might need to specify inverse relationships manually by using the 'inverse' argument." % (
             self.target, self.name,
             self.entity))
        return

    def get_prop_kwargs(self):
        kwargs = {'uselist': self.uselist}
        if self.entity.table is self.target.table:
            kwargs['remote_side'] = self.inverse.foreign_key
        joinclauses = self.inverse.primaryjoin_clauses
        if self.filter:
            joinclauses = joinclauses[:] + [self.filter(self.target.table.c)]
        if joinclauses:
            kwargs['primaryjoin'] = sql.and_(*joinclauses)
        kwargs.update(self.kwargs)
        return kwargs


class OneToMany(OneToOne):
    """Generates a one to many relationship."""
    uselist = True

    def _get_pk_fk(self, cls, target_cls):
        return (
         cls, target_cls)


class ManyToOne(Relationship):
    """Generates a many to one relationship."""
    process_order = 1

    def __init__(self, of_kind, column_kwargs=None, colname=None, required=None, primary_key=None, field=None, constraint_kwargs=None, use_alter=None, ondelete=None, onupdate=None, target_column=None, *args, **kwargs):
        assert not (isinstance(field, (schema.Column, Field)) and (column_kwargs or colname)), "ManyToOne can accept the 'field' argument or column arguments ('colname' or 'column_kwargs') but not both!"
        if colname and not isinstance(colname, list):
            colname = [
             colname]
        self.colname = colname or []
        column_kwargs = column_kwargs or {}
        if required is not None:
            column_kwargs['nullable'] = not required
        if primary_key is not None:
            column_kwargs['primary_key'] = primary_key
        column_kwargs.setdefault('index', True)
        self.column_kwargs = column_kwargs
        if isinstance(field, (schema.Column, Field)) and not isinstance(field, list):
            self.field = [
             field]
        else:
            self.field = []
        constraint_kwargs = constraint_kwargs or {}
        if use_alter is not None:
            constraint_kwargs['use_alter'] = use_alter
        if ondelete is not None:
            constraint_kwargs['ondelete'] = ondelete
        if onupdate is not None:
            constraint_kwargs['onupdate'] = onupdate
        self.constraint_kwargs = constraint_kwargs
        if target_column and not isinstance(target_column, list):
            target_column = [
             target_column]
        self.target_column = target_column
        self.foreign_key = []
        self.primaryjoin_clauses = []
        super(ManyToOne, self).__init__(of_kind, *args, **kwargs)
        return

    def _get_pk_fk(self, cls, target_cls):
        return (
         target_cls, cls)

    def create_keys(self, pk):
        """
        Find all primary keys on the target and create foreign keys on the
        source accordingly.
        """
        if self.foreign_key:
            return
        else:
            if self.column_kwargs.get('primary_key', False) != pk:
                return
            source_desc = self.entity._descriptor
            target_table = self.target_table
            fk_refcols = []
            fk_colnames = []
            if self.target_column is None:
                target_columns = target_table.primary_key.columns
            else:
                target_columns = [ target_table.columns[col] for col in self.target_column
                                 ]
            if not target_columns:
                raise Exception("No primary key found in target table ('%s') for the '%s' relationship of the '%s' entity." % (
                 target_table.name, self.name,
                 self.entity.__name__))
            if self.colname and len(self.colname) != len(target_columns):
                raise Exception("The number of column names provided in the colname keyword argument of the '%s' relationship of the '%s' entity is not the same as the number of columns of the primary key of '%s'." % (
                 self.name, self.entity.__name__,
                 self.target.__name__))
            for key_num, target_col in enumerate(target_columns):
                if self.field:
                    col = self.field[key_num]
                    if isinstance(col, Field):
                        col.create_col()
                        col = col.column
                else:
                    if self.colname:
                        colname = self.colname[key_num]
                    else:
                        colname = options.FKCOL_NAMEFORMAT % {'relname': self.name, 'key': target_col.key}
                    col = schema.Column(colname, target_col.type, **self.column_kwargs)
                    if col.key == self.name:
                        raise ValueError("ManyToOne named '%s' in '%s' conficts  with the column of the same name. You should probably define the foreign key field manually and use the 'field' argument on the ManyToOne relationship" % (
                         self.name, self.entity.__name__))
                    source_desc.add_column(self.column_kwargs.get('key', colname), col)
                self.foreign_key.append(col)
                fk_colnames.append(col.key)
                fk_refcols.append('%s.%s' % (
                 target_table.fullname, target_col.key))
                self.primaryjoin_clauses.append(col == target_col)
                if 'name' not in self.constraint_kwargs:
                    fk_name = options.CONSTRAINT_NAMEFORMAT % {'tablename': source_desc.tablename, 'colnames': ('_').join(fk_colnames)}
                    self.constraint_kwargs['name'] = fk_name
                constraint = schema.ForeignKeyConstraint(fk_colnames, fk_refcols, **self.constraint_kwargs)
                source_desc.add_constraint(constraint)

            return

    def get_prop_kwargs(self):
        kwargs = {'uselist': False}
        if self.entity.table is self.target_table:
            kwargs['remote_side'] = [ col for col in self.target_table.primary_key.columns ]
        if self.primaryjoin_clauses:
            kwargs['primaryjoin'] = sql.and_(*self.primaryjoin_clauses)
        kwargs.update(self.kwargs)
        return kwargs

    def match_type_of(self, other):
        return isinstance(other, (OneToMany, OneToOne))

    @property
    def target_table(self):
        return class_mapper(self.target).local_table


class ManyToMany(Relationship):
    uselist = True

    def __init__(self, of_kind, tablename=None, local_colname=None, remote_colname=None, ondelete=None, onupdate=None, table=None, schema=None, filter=None, table_kwargs=None, *args, **kwargs):
        self.user_tablename = tablename
        if local_colname and not isinstance(local_colname, list):
            local_colname = [
             local_colname]
        self.local_colname = local_colname or []
        if remote_colname and not isinstance(remote_colname, list):
            remote_colname = [
             remote_colname]
        self.remote_colname = remote_colname or []
        self.ondelete = ondelete
        self.onupdate = onupdate
        self.table = table
        self.schema = schema
        self.filter = filter
        if filter is not None:
            if 'viewonly' not in kwargs:
                kwargs['viewonly'] = True
        self.table_kwargs = table_kwargs or {}
        self.primaryjoin_clauses = []
        self.secondaryjoin_clauses = []
        super(ManyToMany, self).__init__(of_kind, *args, **kwargs)
        return

    def column_format(self, data):
        return options.M2MCOL_NAMEFORMAT(data)

    def match_type_of(self, other):
        return isinstance(other, ManyToMany)

    def create_tables(self):
        if self.table is not None:
            if 'primaryjoin' not in self.kwargs or 'secondaryjoin' not in self.kwargs:
                self._build_join_clauses()
            assert self.inverse is None or self.inverse.table is None or self.inverse.table is self.table
            return
        if self.inverse:
            inverse = self.inverse
            if inverse.table is not None:
                self.table = inverse.table
                self.primaryjoin_clauses = inverse.secondaryjoin_clauses
                self.secondaryjoin_clauses = inverse.primaryjoin_clauses
                return
            assert not inverse.user_tablename or not self.user_tablename or inverse.user_tablename == self.user_tablename
            assert not inverse.remote_colname or not self.local_colname or inverse.remote_colname == self.local_colname
            assert not inverse.local_colname or not self.remote_colname or inverse.local_colname == self.remote_colname
            assert not inverse.schema or not self.schema or inverse.schema == self.schema
            assert not inverse.table_kwargs or not self.table_kwargs or inverse.table_kwargs == self.table_kwargs
            self.user_tablename = inverse.user_tablename or self.user_tablename
            self.local_colname = inverse.remote_colname or self.local_colname
            self.remote_colname = inverse.local_colname or self.remote_colname
            self.schema = inverse.schema or self.schema
            self.local_colname = inverse.remote_colname or self.local_colname
        complete_kwargs = options.options_defaults['table_options'].copy()
        complete_kwargs.update(self.table_kwargs)
        e1_desc = self.entity._descriptor
        e2_desc = self.target._descriptor
        source_part = '%s_%s' % (e1_desc.tablename, self.name)
        if self.inverse:
            target_part = '%s_%s' % (e2_desc.tablename, self.inverse.name)
        else:
            target_part = e2_desc.tablename
        if self.user_tablename:
            tablename = self.user_tablename
        else:
            if self.inverse and source_part < target_part:
                tablename = '%s__%s' % (target_part, source_part)
            else:
                tablename = '%s__%s' % (source_part, target_part)
            source_fk_name = '%s_fk' % source_part
            if self.inverse:
                target_fk_name = '%s_fk' % target_part
            else:
                target_fk_name = '%s_inverse_fk' % source_part
            columns = []
            constraints = []
            for num, desc, fk_name, rel, inverse, colnames, join_clauses in (
             (
              0, e1_desc, source_fk_name, self, self.inverse,
              self.local_colname, self.primaryjoin_clauses),
             (
              1, e2_desc, target_fk_name, self.inverse, self,
              self.remote_colname, self.secondaryjoin_clauses)):
                fk_colnames = []
                fk_refcols = []
                if colnames:
                    assert len(colnames) == len(desc.primary_keys)
                else:
                    data = {'relname': rel and rel.name or 'inverse', 
                       'inversename': inverse and inverse.name or 'inverse', 
                       'selfref': e1_desc is e2_desc, 
                       'num': num, 
                       'numifself': e1_desc is e2_desc and str(num + 1) or '', 
                       'target': desc.entity, 
                       'entity': desc.entity.__name__.lower(), 
                       'tablename': desc.tablename, 
                       'current_table': tablename}
                    colnames = []
                    for pk_col in desc.primary_keys:
                        data.update(key=pk_col.key)
                        colnames.append(self.column_format(data))

                    for pk_col, colname in zip(desc.primary_keys, colnames):
                        col = schema.Column(colname, pk_col.type, primary_key=True)
                        columns.append(col)
                        fk_colnames.append(colname)
                        target_path = '%s.%s' % (desc.table_fullname, pk_col.key)
                        fk_refcols.append(target_path)
                        if self.entity is self.target:
                            join_clauses.append(col == pk_col)

                onupdate = rel and rel.onupdate
                ondelete = rel and rel.ondelete
                constraints.append(schema.ForeignKeyConstraint(fk_colnames, fk_refcols, name=fk_name, onupdate=onupdate, ondelete=ondelete))

        args = columns + constraints
        self.table = schema.Table(tablename, e1_desc.metadata, *args, **complete_kwargs)
        return

    def _build_join_clauses(self):
        if self.entity is self.target:
            if not self.local_colname and not self.remote_colname:
                raise Exception("Self-referential ManyToMany relationships in autoloaded entities need to have at least one of either 'local_colname' or 'remote_colname' argument specified. The '%s' relationship in the '%s' entity doesn't have either." % (
                 self.name, self.entity.__name__))
            self.primaryjoin_clauses, self.secondaryjoin_clauses = _get_join_clauses(self.table, self.local_colname, self.remote_colname, self.entity.table)

    def get_prop_kwargs(self):
        kwargs = {'secondary': self.table, 'uselist': self.uselist}
        if self.filter:
            secondaryjoin_clauses = self.secondaryjoin_clauses[:] + [
             self.filter(self.target.table.c)]
        else:
            secondaryjoin_clauses = self.secondaryjoin_clauses
        if self.target is self.entity or self.filter:
            kwargs['primaryjoin'] = sql.and_(*self.primaryjoin_clauses)
            kwargs['secondaryjoin'] = sql.and_(*secondaryjoin_clauses)
        kwargs.update(self.kwargs)
        return kwargs

    def is_inverse(self, other):
        return super(ManyToMany, self).is_inverse(other) and (self.user_tablename == other.user_tablename or not self.user_tablename and not other.user_tablename)


class belongs_to(ClassMutator):

    def process(self, entity_dict, name, *args, **kwargs):
        entity_dict[name] = ManyToOne(*args, **kwargs)


class has_one(ClassMutator):

    def process(self, entity_dict, name, *args, **kwargs):
        entity_dict[name] = OneToOne(*args, **kwargs)


class has_many(ClassMutator):

    def process(self, entity_dict, name, *args, **kwargs):
        entity_dict[name] = OneToMany(*args, **kwargs)


class has_and_belongs_to_many(ClassMutator):

    def process(self, entity_dict, name, *args, **kwargs):
        entity_dict[name] = ManyToMany(*args, **kwargs)


def _get_join_clauses(local_table, local_cols1, local_cols2, target_table):
    primary_join, secondary_join = [], []
    cols1 = local_cols1[:]
    cols1.sort()
    cols1 = tuple(cols1)
    if local_cols2 is not None:
        cols2 = local_cols2[:]
        cols2.sort()
        cols2 = tuple(cols2)
    else:
        cols2 = None
    constraint_map = {}
    for constraint in local_table.constraints:
        if isinstance(constraint, schema.ForeignKeyConstraint):
            use_constraint = True
            fk_colnames = []
            for fk in constraint.elements:
                if fk.references(target_table):
                    fk_colnames.append(fk.parent.key)
                else:
                    use_constraint = False

            if use_constraint:
                fk_colnames.sort()
                constraint_map[tuple(fk_colnames)] = constraint

    for cols, constraint in constraint_map.iteritems():
        if cols == cols1 or cols != cols2 and not cols1 and (cols2 in constraint_map or cols2 is None):
            join = primary_join
        else:
            if cols == cols2 or cols2 == () and cols1 in constraint_map:
                join = secondary_join
            else:
                continue
            for fk in constraint.elements:
                join.append(fk.parent == fk.column)

    return (
     primary_join, secondary_join)