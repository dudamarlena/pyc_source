# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/column_auth.py
# Compiled at: 2015-04-12 12:23:02
# Size of source mod 2**32: 10273 bytes
r"""These objects know how to lookup the allowed columns in the context.

The allowed columns are expressed using the classes provided in the
:mod:`.base_data.allow` module and are stored as an attribute on the current
context.

There are two levels involved in locating the proper attribute for the allowed
columns for any situation:

  #. The action to be taken on that item.  These might be:

     * get (the columns authorized to be seen for a single item, generally a
       more complete list of columns)

     * list (the columns authorized to be seen for each item in a list of items,
       generally more of a summary of all of the available columns)

     * update (the columns authorized to be updated(changed))

     * insert (the columns authorized to be included in an insert(create))

  #. The item that the columns apply to.  When the top-level resource
     contains lists of child items, the columns for the top-level item are
     different than the columns for the child items.  The top-level resource
     may include multiple child lists (generally of different types of items),
     each of which have separate columns.  Also the child lists may themselves
     contain child lists (or grandchildren to the top-level item), which each
     have their own columns.

In order to allow for inheritance of authorized columns between different
actions, each action has a list of attribute names to lookup in the context.
The first one found is the one used.  Generally, actions defer to the columns
used for the get action, which are stored in the `columns` attribute.  Thus
the list of attributes names searched for the update action might be
('update_columns', 'columns').  If `update_columns` isn't in the context, then
the `columns` attribute is used, which is the same attribute used by the get
action.

Each of these lists of attributes names are stored within the context to give
each context full control of this inheritance process.  The defaults are
defined in the :class:`.dry_resource.DRY_Resource` class.  These lists are
stored in attributes called `X_column_suffixes`, where X is the action (get,
list, update or insert).

    >>> from .allow import Allow
    >>> from unittest.mock import Mock
    >>> context = Mock(get_column_suffixes=('columns',),
    ...                list_column_suffixes=('list_columns', 'columns'),
    ...                update_column_suffixes=('update_columns', 'columns'),
    ...                insert_column_suffixes=('insert_columns',
    ...                                        'update_columns', 'columns'),
    ...                columns=Allow('a', 'b', 'c'),
    ...               )
    >>> del context.update_columns  # So Mock won't say it has this.

So the steps to looking up the authorized columns for the update action are as
follows:

    #. Get the list of attribute names from the context by accessing 
       context.update_column_suffixes.  The default value for this is defined
       in the DRY_Resource class as ('update_columns', 'columns').

        >>> context.update_column_suffixes
        ('update_columns', 'columns')

    #. Check for presence of each of these attributes within the context and
       return the first one found.

       #. If the context has an `update_columns` attribute, return
          context.update_columns.

            >>> hasattr(context, 'update_columns')
            False

       #. Otherwise, return context.columns.

            >>> context.columns
            <Allow: ['a', 'b', 'c']>

The different child items are identified by a prefix on the attribute name for
the context.  There is no prefix for the top-level item.  The prefix is formed
by appending '__' to each name in the path to the desired item.  So the prefix
for the items in `top.children.grand_children` is
`children__grand_children__`.  This is prepended to each attribute name
checked in the context.

    >>> context.children__grand_children__columns = Allow('x', 'y', 'z')
    >>> del context.children__grand_children__update_columns

For example, getting the authorized update columns for
the items in top.children.grand_children, are as follows:

    #. Get the list of attribute names from the context by accessing
       context.update_column_suffixes.  (At this point in time, the prefix is
       not added to `update_column_suffixes`).  This results in
       ('update_columns', 'columns'), as before.

        >>> context.update_column_suffixes
        ('update_columns', 'columns')

    #. Check for the presence of each of these attribute names by prepending
       the `children__grand_children__` prefix to each one:

       #. If the context has a `children__grand_children__update_columns`
          attribute, return that.

            >>> hasattr(context, 'children__grand_children__update_columns')
            False

       #. Otherwise, return context.children__grand_children__columns.

            >>> context.children__grand_children__columns
            <Allow: ['x', 'y', 'z']>

The classes in this module help with all of this.

The :class:`.item_column_auth` class handles the authorized columns for an
item.

    >>> item_authorizer = item_column_auth(context)

This can produce action authorizers for different actions.

    >>> update_authorizer = item_authorizer.get_update_column_auth()

Which can then show the allowed and denied columns from any list of column
names.

    >>> sorted(update_authorizer.allowed(('a', 'b', 'w')))
    ['a', 'b']

    >>> sorted(update_authorizer.denied(('a', 'b', 'w')))
    ['w']

    >>> allowed, denied = update_authorizer.allowed_denied(('a', 'b', 'w'))
    >>> sorted(allowed)
    ['a', 'b']
    >>> sorted(denied)
    ['w']

This can also produce item authorizers for children.

    >>> children_authorizer = \
    ...   item_authorizer.get_sublist_column_auth('children')
    >>> grand_children_authorizer = \
    ...   children_authorizer.get_sublist_column_auth('grand_children')

For the update action on grand_children:

    >>> update_authorizer = grand_children_authorizer.get_update_column_auth()
    >>> sorted(update_authorizer.allowed(('x', 'y', 'w')))
    ['x', 'y']
"""
Get_column_suffixes = 'get_column_suffixes'
List_column_suffixes = 'list_column_suffixes'
Update_column_suffixes = 'update_column_suffixes'
Insert_column_suffixes = 'insert_column_suffixes'

class item_column_auth:
    __doc__ = "Manages column authorization for one type of item (record).\n    \n    This is able to produce an item_column_auth for any sublist of these items,\n    as well as an :class:.`action_column_auth` for any action on these items.\n\n    The columns for sublists are stored in the context under a prefix, which\n    is the concatenation of the relationship column names used to navigate\n    from the top-level item to the sublist in question.  Each of these\n    relationship column names has '__' appended to it.  Thus, the column\n    authorizations for top.children.grandchildren would be stored in the top\n    context under a 'children__grandchildren__' prefix.\n    "

    def __init__(self, context, prefix=''):
        self.context = context
        self.prefix = prefix

    def get_sublist_column_auth(self, relationship_column):
        return item_column_auth(self.context, self.prefix + relationship_column + '__')

    def get_action_column_auth(self, suffixes):
        return action_column_auth(self.context, suffixes, self.prefix)

    def get_get_column_auth(self):
        return self.get_action_column_auth(Get_column_suffixes)

    def get_list_column_auth(self):
        return self.get_action_column_auth(List_column_suffixes)

    def get_update_column_auth(self):
        return self.get_action_column_auth(Update_column_suffixes)

    def get_insert_column_auth(self):
        return self.get_action_column_auth(Insert_column_suffixes)


class action_column_auth(item_column_auth):
    __doc__ = "Knows the authorized columns for a given action on one type of item.\n\n    This is an extension of :class:`.item_column_auth`.\n\n    The columns for this action are accessed through a list of suffixes stored\n    in the context under the name passed as `suffixes`.  The default lists of\n    suffixes are defined in the :class:`.dry_resource.DRY_Resource` class.\n    Thus, if the context defines 'update_column_suffixes` as ('update_columns',\n    'columns'), then when 'update_column_suffixes' is used for the action\n    with prefix 'children__grandchildren__', the following names are searched\n    for in the context:\n     \n     * children__grandchild__update_columns\n     * children__grandchild__columns\n\n    The suffixes lists define the order that default column values are searched\n    for if the columns value for this specific action is not specified.\n    "

    def __init__(self, context, suffixes, prefix=''):
        item_column_auth.__init__(self, context, prefix)
        self.suffixes = suffixes
        for suffix in getattr(context, suffixes):
            name = prefix + suffix
            ans = getattr(context, name, None)
            if ans is not None:
                self.columns = ans
                break
        else:
            raise AttributeError('{}.{} does not have columns auth for {}.{}'.format(context.url, context.method, prefix, suffixes))

    def get_sublist_column_auth(self, relationship_column):
        return action_column_auth(self.context, self.suffixes, self.prefix + relationship_column + '__')

    def allowed(self, columns):
        """Returns allowed columns out of `columns`.
        """
        return self.allowed_denied(columns)[0]

    def denied(self, columns):
        """Returns denied columns out of `columns`.
        """
        return self.allowed_denied(columns)[1]

    def allowed_denied(self, columns):
        """Divides `columns` into two sets: those allowed, and those denied.

        Returns allowed_columns, denied_columns.
        """
        return self.columns.allowed_denied(columns)