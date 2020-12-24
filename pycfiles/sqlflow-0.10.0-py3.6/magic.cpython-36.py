# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlflow/magic.py
# Compiled at: 2020-04-10 03:26:06
# Size of source mod 2**32: 1563 bytes
import sys, logging
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from sqlflow.client import Client, _LOGGER
from IPython.display import display_javascript

@magics_class
class SqlFlowMagic(Magics):
    __doc__ = '\n    Provides the `%%sqlflow` magic\n    '

    def __init__(self, shell):
        super(SqlFlowMagic, self).__init__(shell)
        self.client = Client()

    @cell_magic('sqlflow')
    def execute(self, line, cell):
        """Runs SQL statement

        :param line: The line magic
        :type line: str.
        :param cell: The cell magic
        :type cell: str.

        Example:

        >>> %%sqlflow SELECT *
        ... FROM mytable

        >>> %%sqlflow SELECT *
        ... FROM iris.iris limit 1
        ... TRAIN DNNClassifier
        ... WITH
        ...   n_classes = 3,
        ...   hidden_units = [10, 10]
        ... COLUMN sepal_length, sepal_width, petal_length, petal_width
        ... LABEL class
        ... INTO my_dnn_model;

        """
        return self.client.execute('\n'.join([line, cell]))


def load_ipython_extension(ipython):
    js = "IPython.CodeCell.options_default.highlight_modes['magic_sql'] = {'reg':[/^%%sqlflow/]};"
    display_javascript(js, raw=True)
    magics = SqlFlowMagic(ipython)
    ipython.register_magics(magics)