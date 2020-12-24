# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/readers.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 3713 bytes
from bonobo.config import Option, use_context
from bonobo.config.configurables import Configurable
from bonobo.config.services import Service

@use_context
class Select(Configurable):
    __doc__ = '\n    Reads data from a database using a SQL query and a limit-offset based pagination.\n\n    Example:\n\n    .. code-block:: python\n\n        Select(\'SELECT * from foo;\')\n\n    Caveats:\n\n    We\'re using "limit-offset" pagination, but limit-offset pagination can be inconsistent.\n\n    Suppose a user moves from page n to n+1 while simultaneously a new element is inserted into page n. This will cause\n    both a duplication (the previously-final element of page n is pushed into page n+1) and an omission (the new\n    element). Alternatively consider an element removed from page n just as the user moves to page n+1. The previously\n    initial element of page n+1 will be shifted to page n and be omitted.\n\n    A better implementation could be to use database-side cursors, to have the external system mark the last row\n    extracted and "stabilize" pagination. Here is an example of how this can be done (although it\'s not implemented in\n    bonobo-sqlalchemy, for now).\n\n    .. code-block:: sql\n\n        -- We must be in a transaction\n        BEGIN;\n        -- Open a cursor for a query\n        DECLARE select_cursor CURSOR FOR SELECT * FROM foo;\n        -- Retrieve ten rows\n        FETCH 10 FROM select_cursor;\n        -- ...\n        -- Retrieve ten more from where we left off\n        FETCH 10 FROM select_cursor;\n        -- All done\n        COMMIT;\n\n    '
    query = Option(str, positional=True, default='SELECT 1', __doc__='The actual SQL query to run.')
    pack_size = Option(int, required=False, default=1000, __doc__='How many rows to retrieve at once.')
    limit = Option(int, required=False, __doc__='Maximum rows to retrieve, in total.')
    engine = Service('sqlalchemy.engine', __doc__='Database connection (an sqlalchemy.engine).')

    def formatter(self, context, index, row):
        """
        Formats a result row into whataver you need to send on this transformations' output stream.

        :param context:
        :param index:
        :param row:

        :return: mixed

        """
        if not index:
            context.set_output_fields(row.keys())
        return tuple(row)

    @property
    def parameters(self):
        """
        Provide parameters for input query.

        See https://www.python.org/dev/peps/pep-0249/#paramstyle

        :return: dict

        """
        return {}

    def __call__(self, context, *, engine):
        query = self.query.strip(' \n;')
        assert self.pack_size > 0, 'Pack size must be > 0 for now.'
        offset = 0
        parameters = self.parameters
        while not self.limit or offset * self.pack_size < self.limit:
            real_offset = offset * self.pack_size
            if self.limit:
                _limit = max(min(self.pack_size, self.limit - real_offset), 0)
            else:
                _limit = self.pack_size
            if not _limit:
                break
            _offset = real_offset and ' OFFSET {}'.format(real_offset) or ''
            _query = '{query} LIMIT {limit}{offset}'.format(query=query, limit=_limit, offset=_offset)
            results = engine.execute(_query, parameters, use_labels=True).fetchall()
            if not len(results):
                break
            for i, row in enumerate(results):
                formatted_row = self.formatter(context, real_offset + i, row)
                if formatted_row:
                    yield formatted_row

            offset += 1