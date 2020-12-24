# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/slice.py
# Compiled at: 2020-05-03 14:22:42
# Size of source mod 2**32: 10800 bytes
__doc__ = "\nDataFrame namespace additions\n\ndf can usually be Dataset or Results\ncolumn is short or long name like l, lemma, lemmata\n\ndf.find.column.name: very simple search, same as 'just'\ndf.find.column(regex): search column by regex\ndf.see.column(): value_counts for this column\ndf.see.column.by.column: make table\ndf.just.column.name: filter a df to just matching\ndf.just.column(regex): same as above but allow regex, kwargs\ndf.skip.column.name: remove matching rows\ndf.skip.column(regex); same as above but allow regex\n\nYou can string these together however you like:\n\ncorpus.just.speaker.MOOKIE.skip.xpos.PUNCT.see.lemma.by.wordclass\n\n"
from abc import ABC, abstractmethod
import pandas as pd
from .exceptions import DataTypeError
from .search import Searcher
from .utils import _ensure_list_of_short_names, _get_short_name_from_long_name, _order_df_columns

class Filter(object):
    """Filter"""

    def __init__(self, corpus, column, inverse=False, distance=None):
        """
        Unlike other slices, we can't have multiple columns here
        """
        if isinstance(column, (list, set)):
            problem = 'Can only past str/length 1 iterable here: {}'.format(column)
            assert len(column) == 1, problem
            column = list(column)[0]
        self.column = _get_short_name_from_long_name(column)
        self.inverse = inverse
        self.distance = distance
        self._corpus = corpus

    def _make_column_to_match_against(self, case, entry):
        """
        Get a stringified column from the dataset
        """
        if isinstance(entry, (list, set, tuple)):
            entry = list(entry)[0]
        typ = type(entry)
        try:
            if self.column in self._corpus.columns:
                strung = self._corpus[self.column].astype(typ)
            else:
                index_data = self._corpus.index.get_level_values(self.column)
                index_data = index_data.astype(typ)
                strung = pd.Series(index_data, index=(self._corpus.index))
            if not case:
                if typ == str:
                    strung = strung.str.lower()
            return strung
        except KeyError:
            blank = '' if typ == str else -1
            blank = [blank] * len(self._corpus)
            return pd.Series(blank, index=(self._corpus.index))
        except ValueError as err:
            try:
                prob = 'Mismatch between query and column types: ' + str(err)
                raise DataTypeError(prob) from err
            finally:
                err = None
                del err

    @staticmethod
    def _normalise_entry(entry, case):
        """
        Casefold the search text and normalise to set if need be
        """
        if case:
            return entry
        if isinstance(entry, (set, list)):
            return {i.casefold() for i in entry}
        return entry.casefold()

    def _make_bool_index(self, entry, strung, exact_match, **kwargs):
        """
        Get a boolean index of matches for this entry over strung
        """
        if isinstance(entry, (int, float)):
            return strung == entry
        else:
            if isinstance(entry, (set, list)):
                if exact_match:
                    return strung.isin(entry)
                return strung.apply(lambda x: any((i in x for i in entry)))
            if not kwargs.get('regex'):
                if exact_match:
                    return strung == entry
        search_method = strung.str.match if exact_match else strung.str.contains
        return search_method(entry, **kwargs)

    def _normalise(self, entry, case=True, exact_match=False, **kwargs):
        if not isinstance(self._corpus, pd.DataFrame):
            if self._corpus.files:
                results = []
                for file in self._corpus.files:
                    self._corpus = file.load()
                    res = (self.__call__)(entry, case=case, exact_match=exact_match, **kwargs)
                    results.append(res)

                df = pd.concat(results, sort=True)
                return _order_df_columns(df)
        if not isinstance(self._corpus, pd.DataFrame):
            self._corpus = self._corpus.load()

    def __call__(self, entry, case=True, exact_match=False, **kwargs):
        """
        Accepts pd.series.str.contains kwargs: case, regex, etc.

        exact_match: match whole word, or just part of it
        """
        done = (self._normalise)(entry, case=case, exact_match=exact_match, **kwargs)
        if done is not None:
            return done
        else:
            result = None
            if self.column in ('dependencies', 'depgrep', 'deps', 'd'):
                result = self._corpus.depgrep(entry)
            elif self.column in ('tgrep', 'trees', 't', 'tree'):
                result = self._corpus.tgrep(entry)
        if result is not None:
            if not self.inverse:
                return result
            return self._corpus[(~self._corpus['_n'].isin(result['_n']))]
        strung = self._make_column_to_match_against(case, entry)
        entry = self._normalise_entry(entry, case)
        bool_ix = (self._make_bool_index)(entry, strung, exact_match, **kwargs)
        if self.inverse:
            bool_ix = ~bool_ix
        return self._corpus[bool_ix]

    def __getattr__(self, entry):
        """
        data.just/skip.column.<entry>
        """
        return self.__call__(entry, regex=False, exact_match=True)


class Interim(Filter):
    """Interim"""

    @property
    def by(self):
        """
        df.see.x.by.y
        """
        return Interim(self._corpus, self.column)

    def __call__(self, entry=None, *args, **kwargs):
        if not entry:
            try:
                return self._corpus[self.column].value_counts()
            except Exception:
                raise NotImplementedError('Not done yet.')

        else:
            entry = _ensure_list_of_short_names(entry)
        if not isinstance(self._corpus, pd.DataFrame):
            if isinstance(self.column, str):
                self.column = [
                 self.column]
            self.column = self.column if isinstance(self.column, list) else [self.column]
            usecols = entry + self.column
            self._corpus = self._corpus.load(usecols=usecols)
        return (self._corpus.table)(args, subcorpora=self.column, show=entry, **kwargs)


class Proto(Filter):
    """Proto"""

    @property
    def by(self):
        """
        df.see.x.by.y
        """
        return Proto(self._corpus, self.column)

    @property
    def showing(self):
        """
        Exactly the same as 'by', just different name
        """
        return Proto(self._corpus, self.column)

    def __call__(self, show=[
 'w'], top=10, n_top_members=-1, only_correct=True):
        show = _ensure_list_of_short_names(show)
        return self._corpus.prototypical((self.column),
          show=show,
          top=top,
          n_top_members=n_top_members,
          only_correct=only_correct)


class Finder(Filter):
    """Finder"""

    def __call__(self, *args, **kwargs):
        return (Searcher(self._corpus).run)(self.column, *args, **kwargs)


class Slice(ABC):

    def __init__(self, corpus):
        self._corpus = corpus
        self._valid = list(self._corpus.columns) + list(self._corpus.index.names)
        self._valid += ['depgrep', 'tgrep', 'tree', 'trees', 'deps', 't', 'd']
        self._validate()

    def __getattr__(self, col):
        """
        <operation:> just, skip, see...
        gets ATTRIB in df.<operation>.ATTRIB
        """
        col = _ensure_list_of_short_names(col)
        for i in col:
            if i not in self._valid:
                raise ValueError(f"Invalid name(s): {col}")

        return self._grab(col)

    @abstractmethod
    def _grab(self, *args, **kwargs):
        raise NotImplementedError()

    def _validate(self):
        pass


@pd.api.extensions.register_dataframe_accessor('just')
class Just(Slice):
    """Just"""

    def _grab(self, colname, *args):
        return Filter(self._corpus, colname)


@pd.api.extensions.register_dataframe_accessor('proto')
class Prototypical(Slice):
    """Prototypical"""

    def _grab(self, colname, *args):
        return Proto(self._corpus, colname)


@pd.api.extensions.register_dataframe_accessor('skip')
class Skip(Slice):
    """Skip"""

    def _grab(self, colname, *args):
        return Filter((self._corpus), colname, inverse=True)


@pd.api.extensions.register_dataframe_accessor('see')
class See(Slice):
    """See"""

    def _grab(self, colname):
        return Interim(self._corpus, colname)


class Nearby(Filter):

    def __call__(self, entry, case=True, exact_match=False, **kwargs):
        """
        Accepts pd.series.str.contains kwargs: case, regex, etc.

        exact_match: match whole word, or just part of it
        """
        distance = self.distance or 
        from_reference = kwargs.pop('from_reference', False)
        store_n = self._corpus['_n']
        if not from_reference:
            self._corpus['_n'] = range(len(self._corpus))
        matches = (super().__call__)(entry, case=case, exact_match=exact_match, **kwargs)
        nears = dict()
        for n in matches['_n']:
            start = max([0, n - distance])
            end = min([n + distance + 1, len(self._corpus.reference)])
            for i in range(start, end):
                if i != n:
                    nears[i] = i - n

        ref = self._corpus.reference if from_reference else self._corpus
        out = ref.iloc[sorted(list(nears))]
        out['_position'] = [v for k, v in sorted(nears.items())]
        self._corpus['_n'] = store_n
        return out


@pd.api.extensions.register_dataframe_accessor('near')
class Near(Slice):
    """Near"""

    def _grab(self, colname, *args):
        return Nearby(self._corpus, colname)


@pd.api.extensions.register_dataframe_accessor('bigrams')
class Bigrams(Slice):
    """Bigrams"""

    def _grab(self, colname, *args):
        return Nearby((self._corpus), colname, distance=1)