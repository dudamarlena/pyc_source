# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\tsp.py
# Compiled at: 2018-04-03 04:08:53
# Size of source mod 2**32: 8048 bytes
from strategycontainer.exception import UnsupportedPipelineOutput
from strategycontainer.utils.input_validation import expect_element, expect_types, optional
from .filters import Filter
from .term import AssetExists, ComputableTerm, Term
from .graph import ExecutionPlan, TermGraph
from strategycontainer.utils.asset_finder import AssetFinder

class TSP(object):
    __doc__ = "\n    A Pipeline object represents a collection of named expressions to be\n    compiled and executed by a PipelineEngine.\n\n    A Pipeline has two important attributes: 'columns', a dictionary of named\n    `Term` instances, and 'screen', a Filter representing criteria for\n    including an asset in the results of a Pipeline.\n\n    To compute a pipeline in the context of a TradingAlgorithm, users must call\n    ``attach_pipeline`` in their ``initialize`` function to register that the\n    pipeline should be computed each trading day.  The outputs of a pipeline on\n    a given day can be accessed by calling ``pipeline_output`` in\n    ``handle_data`` or ``before_trading_start``.\n\n    Parameters\n    ----------\n    columns : dict, optional\n        Initial columns.\n    screen : zipline.pipeline.term.Filter, optional\n        Initial screen.\n    "
    __slots__ = ('_columns', '_screen', '_universe', 'var', '__weakref__')

    @expect_types(columns=(optional(dict)),
      screen=(optional(Filter)))
    def __init__(self, universe, columns=None, screen=None, var=None):
        if columns is None:
            columns = {}
        validate_column = self.validate_column
        for column_name, term in columns.items():
            validate_column(column_name, term)
            if not isinstance(term, ComputableTerm):
                raise TypeError("Column {column_name!r} contains an invalid pipeline term ({term}). Did you mean to append '.latest'?".format(column_name=column_name,
                  term=term))

        self._columns = columns
        self._screen = screen
        self._universe = universe
        self.var = var

    @property
    def asset_finder(self):
        return AssetFinder(self._universe, self.var)

    @property
    def columns(self):
        """
        The columns registered with this pipeline.
        """
        return self._columns

    @property
    def screen(self):
        """
        The screen applied to the rows of this pipeline.
        """
        return self._screen

    @expect_types(term=Term, name=str)
    def add(self, term, name, overwrite=False):
        """
        Add a column.

        The results of computing `term` will show up as a column in the
        DataFrame produced by running this pipeline.

        Parameters
        ----------
        column : zipline.pipeline.Term
            A Filter, Factor, or Classifier to add to the pipeline.
        name : str
            Name of the column to add.
        overwrite : bool
            Whether to overwrite the existing entry if we already have a column
            named `name`.
        """
        self.validate_column(name, term)
        columns = self.columns
        if name in columns:
            if overwrite:
                self.remove(name)
            else:
                raise KeyError("Column '{}' already exists.".format(name))
        if not isinstance(term, ComputableTerm):
            raise TypeError("{term} is not a valid pipeline column. Did you mean to append '.latest'?".format(term=term))
        self._columns[name] = term

    @expect_types(name=str)
    def remove(self, name):
        """
        Remove a column.

        Parameters
        ----------
        name : str
            The name of the column to remove.

        Raises
        ------
        KeyError
            If `name` is not in self.columns.

        Returns
        -------
        removed : zipline.pipeline.term.Term
            The removed term.
        """
        return self.columns.pop(name)

    @expect_types(screen=Filter, overwrite=(bool, int))
    def set_screen(self, screen, overwrite=False):
        """
        Set a screen on this Pipeline.

        Parameters
        ----------
        filter : zipline.pipeline.Filter
            The filter to apply as a screen.
        overwrite : bool
            Whether to overwrite any existing screen.  If overwrite is False
            and self.screen is not None, we raise an error.
        """
        if self._screen is not None:
            if not overwrite:
                raise ValueError('set_screen() called with overwrite=False and screen already set.\nIf you want to apply multiple filters as a screen use set_screen(filter1 & filter2 & ...).\nIf you want to replace the previous screen with a new one, use set_screen(new_filter, overwrite=True).')
        self._screen = screen

    def to_execution_plan(self, screen_name, default_screen, all_dates, start_date, end_date):
        """
        Compile into an ExecutionPlan.

        Parameters
        ----------
        screen_name : str
            Name to supply for self.screen.
        default_screen : zipline.pipeline.term.Term
            Term to use as a screen if self.screen is None.
        all_dates : pd.DatetimeIndex
            A calendar of dates to use to calculate starts and ends for each
            term.
        start_date : pd.Timestamp
            The first date of requested output.
        end_date : pd.Timestamp
            The last date of requested output.
        """
        return ExecutionPlan(self._prepare_graph_terms(screen_name, default_screen), all_dates, start_date, end_date)

    def to_simple_graph(self, screen_name, default_screen):
        """
        Compile into a simple TermGraph with no extra row metadata.

        Parameters
        ----------
        screen_name : str
            Name to supply for self.screen.
        default_screen : zipline.pipeline.term.Term
            Term to use as a screen if self.screen is None.
        """
        return TermGraph(self._prepare_graph_terms(screen_name, default_screen))

    def _prepare_graph_terms(self, screen_name, default_screen):
        """Helper for to_graph and to_execution_plan."""
        columns = self.columns.copy()
        screen = self.screen
        if screen is None:
            screen = default_screen
        columns[screen_name] = screen
        return columns

    @expect_element(format=('svg', 'png', 'jpeg'))
    def show_graph(self, format='svg'):
        """
        Render this Pipeline as a DAG.

        Parameters
        ----------
        format : {'svg', 'png', 'jpeg'}
            Image format to render with.  Default is 'svg'.
        """
        g = self.to_simple_graph('', AssetExists())
        if format == 'svg':
            return g.svg
        if format == 'png':
            return g.png
        if format == 'jpeg':
            return g.jpeg
        raise AssertionError('Unknown graph format %r.' % format)

    @staticmethod
    @expect_types(term=Term, column_name=str)
    def validate_column(column_name, term):
        if term.ndim == 1:
            raise UnsupportedPipelineOutput(column_name=column_name, term=term)