# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/parse.py
# Compiled at: 2019-08-17 10:38:25
# Size of source mod 2**32: 13475 bytes
import argparse, os, shutil, nltk
from nltk.parse import BllipParser
from .html import MetadataStripper
from .constants import SPACY_LANGUAGES
from .utils import _get_nlp, _get_tqdm, _make_meta_dict_from_sent, _tqdm_close, _tqdm_update
tqdm = _get_tqdm()
BLLIP = None

def _parse_cmd_line():
    parser = argparse.ArgumentParser(description='Parse a corpus.')
    parser.add_argument('-l',
      '--language',
      nargs='?',
      default='english',
      type=str,
      required=False,
      help='Language of the corpus')
    parser.add_argument('-p',
      '--cons-parser',
      nargs='?',
      default='benepar',
      type=str,
      required=False,
      choices=[
     'bllip', 'benepar', 'none'],
      help='Constituency parser to use (bllip/benepar)')
    parser.add_argument('path', help='Directory containing files to parse')
    return vars(parser.parse_args())


class Phony(object):
    __doc__ = '\n    shitty object that overrides the str.decode method in bllip, currently broken\n    '

    def __init__(self, word):
        self.word = Parser._normalise_word(word)

    def decode(self, *args, **kwargs):
        return self.word

    def __str__(self):
        return str(self.word)

    def __repr__(self):
        return str(self.word)


class Parser:
    __doc__ = '\n    Create an object that can parse a Corpus.\n    '

    def __init__(self, cons_parser='bllip', language='english'):
        self.cons_parser = cons_parser if cons_parser != 'none' else None
        self.language = language
        self.nlp = _get_nlp(language=language)
        if self.cons_parser == 'bllip':
            self._prepare_bllip()
        else:
            if self.cons_parser == 'benepar':
                self._prepare_benepar()

    def _prepare_bllip(self):
        global BLLIP
        print('Loading BLLIP...')
        try:
            model_dir = nltk.data.find('models/bllip_wsj_no_aux').path
        except LookupError:
            print('Downloading constituency data...')
            nltk.download('bllip_wsj_no_aux')
            model_dir = nltk.data.find('models/bllip_wsj_no_aux').path

        try:
            BLLIP = BllipParser.from_unified_model_dir(model_dir)
        except RuntimeError:
            pass

    def _prepare_benepar(self):
        from benepar.spacy_plugin import BeneparComponent
        lang = SPACY_LANGUAGES.get(self.language.capitalize())
        ben_file = f"benepar_{lang}"
        try:
            nltk.data.find(ben_file).path
        except LookupError:
            import benepar
            benepar.download(ben_file)

        self.nlp.add_pipe(BeneparComponent(ben_file))

    @staticmethod
    def _normalise_word(word, wrap=False):
        norm = str(word).strip().replace('\t', '').replace('\n', '')
        if wrap:
            return Phony(norm)
        return norm

    @staticmethod
    def _strip_punct(span):
        """
        Fallback only --- last ditch effort to match token in span
        """
        return ''.join((i for i in span if i.isalnum() or i in {'-'}))

    def _get_token_index_in_span(self, span, word):
        """
        Inherently imperfect: from span given by html parser, find spacy token

        We should avoid tokenising where possible, because it is imperfect.

        Edge cases are when the span is 'word.'. This is two tokens
        """
        if span.strip().isalnum() or len(span.strip()) == 1:
            return 0
        if span.strip().startswith(word.text):
            return 0
        tokens = self.nlp(span, disable=['parser', 'ner'])
        gen = (i for i, t in enumerate(tokens) if t.text == word.text)
        try:
            return next(gen)
        except StopIteration:
            split = enumerate(span.split())
            fallback = (i for i, t in split if self._strip_punct(t) == word.text)
            return next(fallback, 0)

        return 0

    def _is_correct_span(self, word, span, nth, features):
        """
        Is this spacy token inside an html span? (for token metadata)
        nth is the number of times this exact span appears to the left in sent.
        So we need to check that not only is word in the span, but that the ix
        of the span is correct
        """
        if word.text not in span or len(span) < len(word.text):
            return False
        nth_in_span = self._get_token_index_in_span(span, word)
        ix_in_sent = next((i for i, t in enumerate(word.sent) if t == word))
        toks_after = word.sent[ix_in_sent - nth_in_span:]
        after = str(toks_after)[:len(span)]
        if span != after:
            return False
        count_before_here = str(word.sent[:ix_in_sent]).count(after)
        return count_before_here == nth

    def _make_misc_field(self, word, token_meta):
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
            if not self._is_correct_span(word, span, nth, features):
                continue
            for key, val in features.items():
                misc += '|{}={}'.format(key, val)

        return misc

    @staticmethod
    def _get_governor_id(word):
        if word.i == word.head.i:
            return '0'
        return str(word.head.i - word.sent[0].i + 1)

    @staticmethod
    def _strip_metadata(plain):
        out = []
        for line in plain.splitlines():
            parser = MetadataStripper()
            parser.feed(line)
            out.append(parser.text)

        return '\n'.join(out)

    @staticmethod
    def _get_line_with_meta(start, plain, stripped):
        all_before = stripped[:start]
        line_index = all_before.count('\n')
        plain = plain.splitlines()
        return plain[line_index]

    def _process_sent(self, sent_index, sent, file_meta, plain, stripped_data):
        word_index = 1
        sent_parts = list()
        text = sent.text.strip(' ').replace('\n', ' ')
        toks = [i for i in sent if not i.is_space]
        self.ntokens += len(toks)
        sent_meta = dict(sent_id=(str(sent_index)), text=(text.strip()), sent_len=(len(toks)))
        if self.trees:
            if self.language.lower().startswith('en'):
                parse = [self._normalise_word((str(i)), wrap=True) for i in toks]
                if self.cons_parser == 'bllip':
                    parse = BLLIP.parse_one(parse)
                    if parse:
                        parse = parse[0]._pformat_flat('', ('(', ')'), '')
                    else:
                        parse = '(. .)'
                else:
                    parse = sent._.parse_string
                sent_meta['parse'] = parse.replace('\n', ' ').strip()
        metaline = self._get_line_with_meta(sent.start_char, plain, stripped_data)
        inner_sent_meta, token_meta = _make_meta_dict_from_sent(metaline)
        all_meta = {**file_meta, **sent_meta, **inner_sent_meta}
        for field, value in sorted(all_meta.items()):
            sent_parts.append('# {} = {}'.format(field, value))

        for word in sent:
            if word.is_space:
                continue
            governor = self._get_governor_id(word)
            word_text = self._normalise_word(str(word))
            named_ent = self._make_misc_field(word, token_meta)
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

    def _process_string(self, plain, path=None):
        """
        spacy: process a string of text
        """
        plain = [i.strip(' ') for i in plain.splitlines() if i.strip(' ')]
        file_meta, _ = _make_meta_dict_from_sent((plain[0]), first=True)
        if file_meta:
            plain = plain[1:]
        plain = '\n'.join(plain)
        stripped_data = self._strip_metadata(plain)
        doc = self.nlp(stripped_data)
        output = list()
        self.nsents += len(list(doc.sents))
        for sent_index, sent in enumerate((doc.sents), start=1):
            sstr = self._process_sent(sent_index, sent, file_meta, plain, stripped_data)
            output.append(sstr)

        output = '\n\n'.join(output).strip() + '\n'
        if not self.save_as:
            if isinstance(self.plain_corpus, str):
                return output
        outpath = path.replace(self.corpus_name, self.corpus_name + '-parsed')
        outpath = outpath.rstrip('.') + '.conllu'
        os.makedirs((os.path.split(outpath)[0]), exist_ok=True)
        self.made_new_dir = True
        with open(outpath, 'w') as (fo):
            fo.write(output)

    def _spacy_parse(self):
        if self.from_str:
            return self._process_string(self.plain_corpus)
        abspath = os.path.abspath(os.getcwd())
        fs = [os.path.join(abspath, f.path) for f in self.plain_corpus.files]
        kwa = dict(ncols=120, unit='file', desc='Parsing', total=(len(fs)))
        t = None
        t = tqdm(**kwa) if len(fs) > 1 else None
        for path in sorted(fs):
            with open(path, 'r') as (fo):
                plain = fo.read().strip()
            self._process_string(plain, path=path)
            _tqdm_update(t)

        _tqdm_close(t)
        print('Done!')

    def _make_metadata(self, description):
        return dict(language=(self.language),
          parser='spacy',
          cons_parser=(self.cons_parser),
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

        Return:
            Corpus: parsed corpus
        """
        from .corpus import Corpus
        self.plain_corpus = corpus
        self.save_as = save_as
        self.trees = bool(self.cons_parser)
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