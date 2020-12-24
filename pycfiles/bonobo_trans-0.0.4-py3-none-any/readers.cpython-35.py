# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/readers.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 3713 bytes
from bonobo.config import Option, use_context
from bonobo.config.configurables import Configurable
from bonobo.config.services import Service

@use_context
class Select(Configurable):
    """Select"""
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