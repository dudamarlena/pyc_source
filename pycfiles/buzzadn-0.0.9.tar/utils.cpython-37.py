# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/utils.py
# Compiled at: 2020-05-04 13:38:17
# Size of source mod 2**32: 18505 bytes
import os, re, shutil
from io import StringIO
from typing import List, Optional
import numpy as np, pandas as pd
from joblib import Parallel
from nltk.tree import ParentedTree
from tqdm import tqdm, tqdm_notebook
from .constants import BENEPAR_LANGUAGES, COLUMN_NAMES, CONLL_COLUMNS, DTYPES, LONG_NAMES, MORPH_FIELDS, LANGUAGE_TO_MODEL

def _get_texts(file_data):
    """
    From a CONLL-U string, return a string of just the text metadata
    """
    out = list()
    pre = '# text = '
    for line in file_data.splitlines():
        if line.startswith(pre):
            line = line.replace(pre, '', 1)
            out.append(line.strip())

    return '\n'.join(out)


def _entity_getter(row, reference=None):
    """
    Pandas rowwise apply. Gets fsis
    """
    iob = row['ent_iob']
    file, s, i = row.name
    out = {i}
    if iob in ('_', 'O'):
        return out
    ent_id = row['ent_id']
    sent = reference.loc[(file, s)]
    sent = sent[(sent['ent_id'] == ent_id)]
    sent['_i'] = sent.index
    sent['diff'] = sent['_i'].diff()
    start = i
    end = i
    while True:
        if iob == 'B':
            break
        else:
            start -= 1
            if not start:
                break
            try:
                line = sent.loc[start]
            except Exception:
                break

        if line['diff'] != 1:
            out.add(start)
            break
        iob = line['ent_iob']
        out.add(start)

    while True:
        end += 1
        try:
            line = sent.loc[end]
        except Exception:
            break

        if line['diff'] != 1:
            break
        out.add(end)

    return out


def _join_entities(made, entity_info):
    """
    Once we've formatted needed tokens, for entities, we need to join them
    """
    out = []
    for (f, s, _), set_of_is in entity_info.items():
        sent = made.loc[(f, s)]
        tokens = [v for k, v in sent.items() if k in set_of_is]
        out.append(' '.join(tokens))

    return pd.Series(out, index=(entity_info.index))


def _make_match_col(df, show, preserve_case, show_entities=False, reference=None):
    """
    Make a Series representing the format requested in `show`
    """
    if show_entities:
        ixes = set()
        entity_info = df.apply(_entity_getter, reference=reference, axis=1)
        for (f, s, _), set_of_is in entity_info.items():
            for ix in set_of_is:
                ixes.add((f, s, ix))

        df = reference.loc[list(sorted(ixes))]
    else:
        for s in show:
            if s in df.index.names and s not in df.columns:
                df[s] = df.index.get_level_values(s)

        if len(show) == 1:
            made = df[show[0]].astype(str)
        else:
            cats = [df[i].astype(str) for i in show[1:]]
        made = df[show[0]].str.cat(others=cats, sep='/').str.rstrip('/')
    if not preserve_case:
        made = made.str.lower()
    if show_entities:
        made = _join_entities(made, entity_info)
    return made


def _get_tqdm():
    """
    Get either the IPython or regular version of tqdm
    """
    try:
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            return tqdm_notebook
        return tqdm
    except NameError:
        pass

    return tqdm


def _tree_once(df):
    """
    Get each parse tree once, probably so we can run nltk.ParentedTree on them
    """
    return df['parse'][(df.index.get_level_values('i') == 1)]


def _tqdm_update(tqdm):
    """
    Try to update tqdm, or do nothing
    """
    if tqdm is not None:
        tqdm.update(1)


def _tqdm_close(tqdm):
    """
    Try to close tqdm, or do nothing
    """
    if tqdm is not None:
        tqdm.close()


def _auto_window():
    """
    Get concordance left and right optimal size
    """
    columns = shutil.get_terminal_size().columns
    size = columns / 2 * 0.6
    return [
     int(size), int(size)]


def _make_tree(tree):
    """
    Try to make a tree from this string, or return None
    """
    try:
        return ParentedTree.fromstring(tree)
    except Exception:
        return


def _get_nlp(language='en', constituencies=False):
    """
    Get spaCY/benepar with models by language
    """
    import spacy
    language = language.lower()
    model_name = LANGUAGE_TO_MODEL.get(language, language)
    try:
        nlp = spacy.load(model_name)
    except OSError:
        from spacy.cli import download
        download(model_name)
        nlp = spacy.load(model_name)

    if language in BENEPAR_LANGUAGES:
        if constituencies:
            from benepar.spacy_plugin import BeneparComponent
            try:
                nlp.add_pipe(BeneparComponent(BENEPAR_LANGUAGES[language]))
            except LookupError:
                import benepar
                benepar.download(BENEPAR_LANGUAGES[language])
                nlp.add_pipe(BeneparComponent(BENEPAR_LANGUAGES[language]))

    return nlp


def cast(text):
    """
    Attempt to get object from JSON string, or return the string
    """
    import json
    try:
        return json.loads(text)
    except Exception:
        return text


def _make_csv(raw_lines, fname, usecols, folders):
    """
    Turn raw CONLL-U file data into something pandas' CSV reader can easily and quickly read.

    The main thing to do is to add the [file, sent#, token#] index, and transform the metadata
    stored as comments into additional columns

    folders: a seperate column for subcorpus, or should it
    be in the file level of the multiindex

    Return: str (CSV data) and list of dicts (metadata for each discovered sentence)
    """
    csvdat = list()
    meta_dicts = list()
    fname = fname.rsplit('-parsed/')[(-1)]
    if '.txt' in fname:
        fname = fname.split('.txt', 1)[0]
    if not (folders == 'column' or folders):
        colname, fname = fname.rsplit('/', 1)
    sents = raw_lines.strip().split('\n\n')
    splut = [re.split('\n([0-9])', s, 1) for s in sents]
    regex = '^# (.*?) = (.*?)$'
    try:
        for sent_id, (raw_sent_meta, one, text) in enumerate(splut, start=1):
            text = one + text
            sent_meta = dict()
            if folders == 'column':
                sent_meta['subcorpus'] = colname
            found = re.findall(regex, raw_sent_meta, re.MULTILINE)
            for key, value in found:
                if usecols:
                    if key.strip() not in usecols:
                        continue
                sent_meta[key.strip()] = cast(value.strip())

            lines = text.splitlines()
            text = '\n'.join((f"{fname}\t{sent_id}\t{line}" for line in lines))
            csvdat.append(text)
            meta_dicts.append(sent_meta)

    except ValueError as error:
        try:
            raise
            raise ValueError(f"Problem in file: {fname}") from error
        finally:
            error = None
            del error

    return (
     '\n'.join(csvdat), meta_dicts)


def _order_df_columns(df, metadata=None, morph=None):
    if metadata is None:
        metadata = [i for i in list(df.columns) if i not in COLUMN_NAMES]
    morph = morph or 
    good_names = [i for i in COLUMN_NAMES if i in df.columns]
    with_n = good_names + morph + list(sorted(metadata))
    if '_n' in with_n:
        with_n.remove('_n')
        with_n.append('_n')
    return df[with_n]


def _apply_governor(row, df=None, dummy=None):
    """
    Appliable function to get the governor of a token. Slow.
    """
    try:
        return df.loc[(row.name[0], row.name[1], row['g'])]
    except Exception:
        return dummy


def _add_governor(df):
    """
    Add governor features to dataframe. Slow.
    """
    cols = [
     'w', 'l', 'x', 'p', 'f', 'g']
    dummy = pd.Series(['ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 0])
    govs = df.apply(_apply_governor,
      df=(df[cols]), axis=1, result_type='reduce', dummy=dummy)
    govs['g'] = govs['g'].fillna(0).astype(int)
    govs = govs.fillna('ROOT')
    govs = govs[['w', 'l', 'x', 'p', 'f', 'g']]
    govs.columns = ['g' + i for i in list(govs.columns)]
    return pd.concat([df, govs], axis=1, sort=False)


def _multiples_apply(morph_list, path=None, column=None):
    """
    Function applied to each dataframe row, to extract multi value column data
    """
    out = dict()
    if morph_list == ['_']:
        return out
    for item in morph_list:
        if '=' not in item:
            k, v = 'untitled', item
        else:
            k, v = item.split('=', 1)
        out[k] = v

    return out


def _parse_out_multiples(df, morph=False, path=None):
    """
    Get morphology or metadata stored at token level in m/o columns
    """
    letter = 'm' if morph else 'o'
    col = df[letter].str.split('|')
    multis = col.apply(_multiples_apply, path=path, column=letter)
    multis = pd.DataFrame.from_dict(list(multis)).fillna('_')
    multis.index = df.index
    if morph:
        fix = [MORPH_FIELDS.get(i.lower(), i.lower()) for i in multis.columns]
        multis.columns = fix
    cols = list(multis.columns)
    return (
     multis.join(df, how='inner'), cols)


def _to_df(corpus, subcorpus: Optional[str]=None, folders: Optional[str]='index', usecols: Optional[List[str]]=None, usename: Optional[str]=None, set_data_types: bool=True, add_governor: bool=False, morph: bool=True, misc: bool=True, _complete: bool=True):
    """
    Turn buzz.corpus.Corpus into a Dataset (i.e. pd.DataFrame-like object)
    """
    from .corpus import Corpus
    from .dataset import Dataset
    from .file import File
    if isinstance(corpus, str):
        if os.path.isfile(corpus):
            corpus = File(corpus)
    else:
        if isinstance(corpus, (Corpus, File)):
            with open(corpus.path, 'r') as (fo):
                data = fo.read().strip('\n')
        return data.strip() or None
    if isinstance(corpus, str):
        if not os.path.exists(corpus):
            data = corpus
    data, metadata = _make_csv(data, usename or , usecols, folders)
    csv_usecols = None
    if usecols is not None:
        usecols = usecols + [i for i in ('file', 's', 'i') if i not in usecols]
        csv_usecols = [i for i in usecols if i in ['file', 's'] + CONLL_COLUMNS]
    df = pd.read_csv((StringIO(data)),
      sep='\t',
      header=None,
      names=COLUMN_NAMES,
      quoting=3,
      index_col=[
     'file', 's', 'i'],
      engine='c',
      na_filter=False,
      usecols=csv_usecols)
    morph_cols, misc_cols = list(), list()
    if morph:
        if 'm' in df.columns:
            if (df['m'] != '_').any():
                df, morph_cols = _parse_out_multiples(df, morph=True, path=(corpus.path))
    if misc:
        if 'o' in df.columns:
            if (df['o'] != '_').any():
                df, misc_cols = _parse_out_multiples(df, path=(corpus.path))
    metadata = {i:d for i, d in enumerate(metadata, start=1)}
    metadata = pd.DataFrame(metadata).T
    metadata.index.name = 's'
    df = metadata.join(df, how='inner', lsuffix='_other')
    if subcorpus:
        df['subcorpus'] = subcorpus
    if _complete:
        df = _order_df_columns(df, metadata, morph_cols + misc_cols)
    badcols = [
     'o', 'm']
    df = df.drop(badcols, axis=1, errors='ignore')
    df = df.fillna('_')
    if set_data_types:
        if _complete:
            df = _set_best_data_types(df)
    if 'g' in df.columns:
        if add_governor:
            df = _add_governor(df)
    df = df.replace('_', np.nan)
    if 'w' in df.columns:
        df['w'] = df['w'].replace(np.nan, '_')
    return Dataset(df, name=(usename or ))


def _get_short_name_from_long_name(longname):
    """
    Translate "lemmata" to "l" and so on
    """
    revers = dict()
    for k, vs in LONG_NAMES.items():
        for v in vs:
            revers[v] = k

    return revers.get(longname, longname)


def _make_meta_dict_from_sent(text, first=False, speakers=True):
    """
    Make dict of sentence and token metadata
    """
    from .html import InputParser
    marker = '<meta '
    if first:
        if not text.strip().startswith(marker):
            return (
             dict(), dict())
    parser = InputParser(speakers=speakers)
    parser.feed(text)
    if first:
        return (parser.sent_meta, dict())
    return (parser.sent_meta, parser.result)


def _ensure_list_of_short_names(item):
    """
    Normalise 'word' to ["w"]
    """
    if isinstance(item, str):
        return [_get_short_name_from_long_name(item)]
    fixed = []
    for i in item:
        fixed.append(_get_short_name_from_long_name(i))

    return fixed


def _series_to_wordlist(series, by, top):
    """
    Series is _match, maybe with frequencies

    Return: padded list of words by sort, max top
    """
    lst = None
    if by in {'total', 'infreq'}:
        lst = list(series.value_counts().head(top).index)
    elif by in {'reverse', 'name'}:
        lst = sorted(set(series.values))[:top]
    if by in {'reverse', 'infreq'}:
        lst = [i for i in reversed(lst)]
    if lst is None:
        raise NotImplementedError()
    return lst + [None] * (top - len(lst))


def _load_corpus(self, **kwargs):
    """
    Generic loader for corpus or contents
    """
    from .corpus import Corpus
    from .dataset import Dataset
    from . import multi
    multiprocess = multi.how_many(kwargs.pop('multiprocess', self.is_parsed))
    to_iter = self.files if isinstance(self, Corpus) else self
    if multiprocess and multiprocess > 1:
        chunks = np.array_split(to_iter, multiprocess)
        if self.is_parsed:
            delay = ((multi.load)(x, i, **kwargs) for i, x in enumerate(chunks))
        else:
            delay = (multi.read(x, i) for i, x in enumerate(chunks))
        loaded = Parallel(n_jobs=multiprocess)(delay)
        loaded = [item for sublist in loaded for item in sublist]
    else:
        kwa = dict(ncols=120, unit='file', desc='Loading', total=(len(self)))
        t = tqdm(**kwa) if len(to_iter) > 1 else None
        loaded = list()
        for file in to_iter:
            data = (file.load)(**kwargs) if file.is_parsed else file.read()
            loaded.append(data)
            _tqdm_update(t)

        _tqdm_close(t)
    if not self.is_parsed:
        keys = self.filepaths if self.is_parsed else [i.path for i in self.files]
        return dict(sorted(zip(keys, loaded)))
    df = pd.concat(loaded, sort=False)
    df['_n'] = range(len(df))
    if kwargs.get('set_data_types', True):
        df = _set_best_data_types(df)
    df = _order_df_columns(df)
    print('\n' * multiprocess)
    return Dataset(df, reference=df, name=(self.name))


def _fix_datatypes_on_save(df, to_reduce):
    """
    Before saving as feather/parquet, we need to do stricter handling
    of column dtypes, or else the save operation fails.
    """
    for col in df.columns:
        if col == 'speaker':
            df[col] = df[col].astype(str)
            continue
        if not col not in DTYPES:
            if df[col].dtype.name == 'object':
                if col in to_reduce:
                    continue
            print(f"Stringifying column {col}...")
            df[col] = df[col].astype(str).fillna('_')

    return df


def _set_best_data_types(df):
    """
    Make DF have the best possible column data types

    Used during load from feather, parquet and conll
    """
    for c in list(df.columns):
        if df[c].dtype.name.startswith('date'):
            continue
        try:
            df[c] = df[c].astype(DTYPES.get(c, object))
            try:
                df[c].cat.add_categories('_')
            except AttributeError:
                pass

        except (ValueError, TypeError):
            pass

    return df