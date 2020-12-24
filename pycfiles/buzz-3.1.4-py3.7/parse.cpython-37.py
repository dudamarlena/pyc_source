# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/parse.py
# Compiled at: 2020-05-04 13:36:55
# Size of source mod 2**32: 11325 bytes
import argparse, os, shutil, numpy as np
from joblib import Parallel
from . import multi
from .html import MetadataStripper
from .utils import _get_nlp, _get_tqdm, _make_meta_dict_from_sent
tqdm = _get_tqdm()

def _strip_metadata(plain, speakers):
    out = []
    for line in plain.splitlines():
        parser = MetadataStripper(speakers)
        parser.feed(line)
        out.append(parser.text)

    return '\n'.join(out)


def _normalise_word(word, wrap=False):
    return str(word).strip().replace('\t', '').replace('\n', '')


def _get_line_with_meta(start, plain, stripped):
    all_before = stripped[:start]
    line_index = all_before.count('\n')
    plain = plain.splitlines()
    return plain[line_index]


def _get_governor_id(word):
    if word.i == word.head.i:
        return '0'
    return str(word.head.i - word.sent[0].i + 1)


def _strip_punct(span):
    """
    Fallback only --- last ditch effort to match token in span
    """
    return ''.join((i for i in span if i.isalnum() or i in {'-'}))


def _get_token_index_in_span(span, word, nlp):
    """
    Inherently imperfect: from span given by html parser, find spacy token

    We should avoid tokenising where possible, because it is imperfect.

    Edge cases are when the span is 'word.'. This is two tokens
    """
    if span.strip().isalnum() or len(span.strip()) == 1:
        return 0
    if span.strip().startswith(word.text):
        return 0
    tokens = nlp(span)
    gen = (i for i, t in enumerate(tokens) if t.text == word.text)
    try:
        return next(gen)
    except StopIteration:
        split = enumerate(span.split())
        fallback = (i for i, t in split if _strip_punct(t) == word.text)
        return next(fallback, 0)

    return 0


def _is_correct_span(word, span, nth, features, nlp):
    """
    Is this spacy token inside an html span? (for token metadata)
    nth is the number of times this exact span appears to the left in sent.
    So we need to check that not only is word in the span, but that the ix
    of the span is correct
    """
    if word.text not in span or len(span) < len(word.text):
        return False
    nth_in_span = _get_token_index_in_span(span, word, nlp)
    ix_in_sent = next((i for i, t in enumerate(word.sent) if t == word))
    toks_after = word.sent[ix_in_sent - nth_in_span:]
    after = str(toks_after)[:len(span)]
    if span != after:
        return False
    count_before_here = str(word.sent[:ix_in_sent]).count(after)
    return count_before_here == nth


def _make_misc_field(word, token_meta, nlp, all_meta):
    """
    Build the misc cell for this word. It has NER, sentiment AND user-added
    """
    if not word.ent_iob:
        if not word.sentiment:
            if not token_meta:
                return '_'
    ent = word.ent_type_ or '_'
    formatters = dict(typ=ent, num=(word.ent_iob), iob=(word.ent_iob_))
    misc = ('ent_type={typ}|ent_id={num}|ent_iob={iob}'.format)(**formatters)
    if word.sentiment:
        misc += '|sentiment={}'.format(word.sentiment)
    for (span, nth), features in token_meta.items():
        if not _is_correct_span(word, span, nth, features, nlp):
            continue
        for key, val in features.items():
            if key not in all_meta:
                misc += '|{}={}'.format(key, val)

    return misc


def _process_string(plain, path, save_as, corpus_name, language, constituencies, speakers):
    """
    spacy: process a string of text
    """
    plain = [i.strip(' ') for i in plain.splitlines() if i.strip(' ')]
    file_meta, _ = _make_meta_dict_from_sent((plain[0]), first=True, speakers=speakers)
    if file_meta:
        plain = plain[1:]
    plain = '\n'.join(plain)
    stripped_data = _strip_metadata(plain, speakers)
    nlp = _get_nlp(language=language, constituencies=constituencies)
    doc = nlp(stripped_data)
    output = list()
    for sent_index, sent in enumerate((doc.sents), start=1):
        sstr = _process_sent(sent_index, sent, file_meta, plain, stripped_data, language, nlp, constituencies, speakers)
        output.append(sstr)

    output = '\n\n'.join(output).strip() + '\n'
    outpath = path.replace(corpus_name, corpus_name + '-parsed')
    outpath = outpath.rstrip('.') + '.conllu'
    os.makedirs((os.path.split(outpath)[0]), exist_ok=True)
    with open(outpath, 'w') as (fo):
        fo.write(output)


def _process_sent(sent_index, sent, file_meta, plain, stripped_data, language, nlp, constituencies, speakers):
    word_index = 1
    sent_parts = list()
    text = sent.text.strip(' ').replace('\n', ' ')
    toks = [i for i in sent if not i.is_space]
    sent_meta = dict(sent_id=(str(sent_index)), text=(text.strip()), sent_len=(len(toks)))
    if constituencies:
        sent_meta['parse'] = str(sent._.parse_string).replace('\n', ' ')
    metaline = _get_line_with_meta(sent.start_char, plain, stripped_data)
    inner_sent_meta, token_meta = _make_meta_dict_from_sent(metaline, speakers=speakers)
    all_meta = {**file_meta, **sent_meta, **inner_sent_meta}
    for field, value in sorted(all_meta.items()):
        sent_parts.append('# {} = {}'.format(field, value))

    for word in sent:
        if word.is_space:
            continue
        governor = _get_governor_id(word)
        word_text = _normalise_word(str(word))
        named_ent = _make_misc_field(word, token_meta, nlp, all_meta)
        if '__' in word.tag_ and len(word.tag_) > 2:
            tag, morph = word.tag_.split('__', 1)
        else:
            tag, morph = word.tag_, '_'
        parts = [
         str(word_index),
         word_text,
         word.lemma_,
         word.pos_,
         tag,
         morph,
         governor,
         word.dep_,
         '_',
         named_ent]
        line = '\t'.join(parts)
        sent_parts.append(line)
        word_index += 1

    return '\n'.join(sent_parts)


def _parse_cmd_line():
    parser = argparse.ArgumentParser(description='Parse a corpus.')
    parser.add_argument('-l',
      '--language',
      nargs='?',
      default='en',
      type=str,
      required=False,
      help='Language of the corpus')
    parser.add_argument('-c',
      '--constituencies',
      default=True,
      action='store_true',
      required=False,
      help='Attempt constituency parsing as well as dependency parsing')
    parser.add_argument('path', help='Directory containing files to parse')
    return vars(parser.parse_args())


class Parser:
    __doc__ = '\n    Create an object that can parse a Corpus.\n    '

    def __init__(self, language='en', multiprocess=False, constituencies=False, speakers=True):
        self.multiprocess = multiprocess
        self.language = language
        self.constituencies = constituencies
        self.speakers = speakers

    def _spacy_parse(self):
        if self.from_str:
            args = (
             self.plain_corpus,
             '.',
             self.save_as,
             self.corpus_name,
             self.language,
             self.constituencies,
             self.speakers)
            return (self._process_string)(*args)
        abspath = os.path.abspath(os.getcwd())
        fs = [os.path.join(abspath, f.path) for f in self.plain_corpus.files]
        multiprocess = multi.how_many(self.multiprocess)
        chunks = np.array_split(fs, multiprocess)
        delay = (multi.parse(x, i, self.save_as, self.corpus_name, self.language, self.constituencies, self.speakers) for i, x in enumerate(chunks))
        Parallel(n_jobs=multiprocess)(delay)

    def _make_metadata(self, description):
        return dict(language=(self.language),
          parser='spacy',
          path=(os.path.abspath(self.parsed_path)),
          name=(self.corpus_name),
          parsed=True,
          nsents=(self.nsents),
          ntokens=(self.ntokens),
          nfiles=(len(self.plain_corpus.files)),
          desc=description)

    def run(self, corpus, save_as=None):
        """
        Run the parsing pipeline

        Args:
           corpus (Corpus): plain data to process
           save_as (str): custom save path
           speakers (bool): look for speakers at start of line

        Return:
            Corpus: parsed corpus
        """
        from .corpus import Corpus
        self.plain_corpus = corpus
        self.save_as = save_as
        self.ntokens = 0
        self.nsents = 0
        self.made_new_dir = False
        self.from_str = True
        if isinstance(corpus, Corpus):
            if corpus.is_parsed:
                raise AssertionError('Corpus is already parsed')
            self.corpus_name = corpus.name
            self.parsed_name = corpus.name + '-parsed'
            self.parsed_path = corpus.path + '-parsed'
            self.from_str = False
        else:
            if isinstance(self.save_as, str):
                self.corpus_name = self.save_as
                self.parsed_name = self.corpus_name + '-parsed'
                self.parsed_path = self.parsed_name
            else:
                if self.save_as:
                    msg = 'Please specify a savename with the `save` argument, or do save_as=False'
                    raise ValueError(msg)
                elif self.save_as and os.path.isdir(self.parsed_path):
                    raise OSError(f"Path already exists: {self.parsed_path}")
                try:
                    as_string = self._spacy_parse()
                except Exception:
                    if self.made_new_dir:
                        shutil.rmtree(self.parsed_path)
                    raise

                if as_string is not None:
                    parsed = Corpus.from_string(as_string, save_as=False)
                else:
                    parsed = Corpus(self.parsed_path)
                    metadata = self._make_metadata(None)
                    (parsed.add_metadata)(**metadata)
                return parsed


if __name__ == '__main__':
    from buzz.corpus import Corpus
    kwargs = _parse_cmd_line()
    corpus = Corpus(kwargs.pop('path'))
    (corpus.parse)(**kwargs)