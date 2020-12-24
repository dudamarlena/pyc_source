# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/utils.py
# Compiled at: 2019-09-06 05:45:15
# Size of source mod 2**32: 12153 bytes
import multiprocessing, os, re, shutil
from io import StringIO
from typing import List, Optional
import pandas as pd
from nltk.tree import ParentedTree
from tqdm import tqdm, tqdm_notebook
from .constants import COLUMN_NAMES, DTYPES, LONG_NAMES, SPACY_LANGUAGES, MORPH_FIELDS, CONLL_COLUMNS

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


def _make_match_col(df, show, preserve_case):
    """
    Make a Series representing the format requested in `show`
    """
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
    return [int(size), int(size)]


def _set_best_data_types(df):
    """
    Make DF have the best possible column data types
    """
    for c in list(df.columns):
        if df[c].dtype.name.startswith('date'):
            continue
        try:
            df[c] = df[c].astype(DTYPES.get(c, 'category'))
            try:
                df[c].cat.add_categories('_')
            except AttributeError:
                pass

        except (ValueError, TypeError):
            pass

    return df


def _make_tree(tree):
    """
    Try to make a tree from this string, or return None
    """
    try:
        return ParentedTree.fromstring(tree)
    except Exception:
        return


def _get_nlp(language='english'):
    """
    Get spaCY with models by language
    """
    import spacy
    lang = SPACY_LANGUAGES.get(language.capitalize(), language)
    try:
        return spacy.load(lang)
    except OSError:
        from spacy.cli import download
        download(lang)
        return spacy.load(lang)


def cast(text):
    """
    Attempt to get object from JSON string, or return the string
    """
    import json
    try:
        return json.loads(text)
    except Exception:
        return text


def _make_csv(raw_lines, fname, usecols):
    """
    Turn raw CONLL-U file data into something pandas' CSV reader can easily and quickly read.

    The main thing to do is to add the [file, sent#, token#] index, and transform the metadata
    stored as comments into additional columns

    Return: str (CSV data) and list of dicts (metadata for each discovered sentence)
    """
    csvdat = list()
    meta_dicts = list()
    fname = os.path.basename(fname)
    sents = raw_lines.strip().split('\n\n')
    splut = [re.split('\n([0-9])', s, 1) for s in sents]
    regex = '^# (.*?) = (.*?)$'
    try:
        for sent_id, (raw_sent_meta, one, text) in enumerate(splut, start=1):
            text = one + text
            sent_meta = dict()
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
            raise ValueError(f"Problem in file: {fname}") from error
        finally:
            error = None
            del error

    return (
     '\n'.join(csvdat), meta_dicts)


def _order_df_columns(df, metadata=None, morph=None):
    if metadata is None:
        metadata = [i for i in list(df.columns) if i not in COLUMN_NAMES]
    morph = morph or list()
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
    govs = df.apply(_apply_governor, df=(df[cols]), axis=1, reduce=False, dummy=dummy)
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
    return (multis.join(df, how='inner'), cols)


def _get_multiprocess(multiprocess):
    """
    Get number of processes, or False

    Hardest utility ever written.
    """
    if multiprocess is True:
        multiprocess = multiprocessing.cpu_count()
    if type(multiprocess) == int:
        if multiprocess < 2:
            return False
    if multiprocess is False or multiprocess is None:
        return False
    return multiprocess


def _load_multi(paths, position, **kwargs):
    """
    Picklable loader for multiprocessing
    """
    kwa = dict(ncols=120,
      unit='chunk',
      desc='Loading',
      position=position,
      total=(len(paths)))
    t = (_get_tqdm())(**kwa)
    out = []
    for path in paths:
        out.append(_to_df(corpus=path, _complete=False, **kwargs))
        _tqdm_update(t)

    _tqdm_close(t)
    return out


def _to_df(corpus, subcorpus: Optional[str]=None, usecols: Optional[List[str]]=None, usename: Optional[str]=None, set_data_types: bool=True, add_governor: bool=False, morph: bool=True, misc: bool=True, _complete: bool=True):
    """
    Turn buzz.corpus.Corpus into a Dataset (i.e. pd.DataFrame-like object)
    """
    from .corpus import Corpus
    from .dataset import Dataset
    from .file import File
    if isinstance(corpus, str):
        if os.path.isfile(corpus):
            corpus = File(corpus)
    if isinstance(corpus, (Corpus, File)):
        with open(corpus.path, 'r') as (fo):
            data = fo.read().strip('\n')
    else:
        if isinstance(corpus, str):
            if not os.path.exists(corpus):
                data = corpus
            else:
                data, metadata = _make_csv(data, usename or corpus.name, usecols)
                csv_usecols = None
                if usecols is not None:
                    usecols = usecols + [i for i in ('file', 's', 'i') if i not in usecols]
                    csv_usecols = [i for i in usecols if i in ['file', 's'] + CONLL_COLUMNS]
                df = pd.read_csv((StringIO(data)),
                  sep='\t',
                  header=None,
                  names=COLUMN_NAMES,
                  quoting=3,
                  engine='c',
                  na_filter=False,
                  usecols=csv_usecols)
                df = df.set_index(['file', 's', 'i'])
                morph_cols, misc_cols = list(), list()
                if morph:
                    if 'm' in df.columns and (df['m'] != '_').any():
                        df, morph_cols = _parse_out_multiples(df, morph=True, path=(corpus.path))
            if misc:
                if 'o' in df.columns:
                    if (df['o'] != '_').any():
                        df, misc_cols = _parse_out_multiples(df, path=(corpus.path))
            metadata = {i:d for i, d in enumerate(metadata, start=1)}
            metadata = pd.DataFrame(metadata).T
            metadata.index.name = 's'
            df = metadata.join(df, how='inner')
            if subcorpus:
                df['subcorpus'] = subcorpus
            if _complete:
                df = _order_df_columns(df, metadata, morph_cols + misc_cols)
        else:
            badcols = [
             'o', 'm']
            df = df.drop(badcols, axis=1, errors='ignore')
            df = df.fillna('_')
            if set_data_types:
                if _complete:
                    df = _set_best_data_types(df)
            if 'g' in df.columns and add_governor:
                df = _add_governor(df)
        return Dataset(df, name=(usename or corpus.name))


def _get_short_name_from_long_name(longname):
    """
    Translate "lemmata" to "l" and so on
    """
    revers = dict()
    for k, vs in LONG_NAMES.items():
        for v in vs:
            revers[v] = k

    return revers.get(longname, longname)


def _make_meta_dict_from_sent(text, first=False):
    """
    Make dict of sentence and token metadata
    """
    from .html import InputParser
    marker = '<meta '
    if first:
        if not text.strip().startswith(marker):
            return (
             dict(), dict())
    parser = InputParser()
    parser.feed(text)
    if first:
        return (
         parser.sent_meta, dict())
    return (
     parser.sent_meta, parser.result)


def _ensure_list_of_short_names(item):
    """
    Normalise 'word' to ["w"]
    """
    if isinstance(item, str):
        return [
         _get_short_name_from_long_name(item)]
    fixed = []
    for i in item:
        fixed.append(_get_short_name_from_long_name(i))

    return fixed