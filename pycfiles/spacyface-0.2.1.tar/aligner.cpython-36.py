# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjamin.hoover@ibm.com/Projects/spacyface-aligner/aligner/aligner.py
# Compiled at: 2020-01-16 10:58:13
# Size of source mod 2**32: 6920 bytes
from typing import List, Iterable, Union
import spacy
from spacy.tokens.token import Token as SpacyToken
from spacy.tokens.doc import Doc as SpacyDoc
import regex as re
from transformers import BertTokenizer, GPT2Tokenizer, RobertaTokenizer, DistilBertTokenizer
from .simple_spacy_token import SimpleSpacyToken
from .utils.f import flatten_, assoc, delegates

def doc_to_fixed_tokens(doc: SpacyDoc) -> List[str]:
    """Fix the tokens in a document to not have exceptions"""
    return [fix_token(t, i) for i, t in enumerate(doc)]


def fix_token(tok: SpacyToken, idx: int=-1) -> str:
    """Determine whether a token should be represented by its text or its norm"""
    out = tok.text if tok.text.lower() == tok.norm_ else tok.norm_
    return out


def MakeAligner(pretrained_tokenizer, spacy_language_model):
    """Create an aligner from the pretrained tokenizers. Some caveats to note:

    Usage:
        BrandNewHuggingfaceAligner = MakeAligner(BrandNewHuggingfaceTokenizer)
    """

    class Aligner(pretrained_tokenizer):

        @delegates(pretrained_tokenizer.__init__)
        def __init__(self, **kwargs):
            (super().__init__)(**kwargs)
            self.nlp = spacy.load(spacy_language_model)
            self.meta_container = SimpleSpacyToken

        def prep_sentence(self, s: str) -> str:
            """Remove contractions and multiple spaces from input sentence"""
            s = re.sub('\\s+', ' ', s)
            out = ' '.join(self._to_normed_spacy(s))
            return out

        @delegates(pretrained_tokenizer.tokenize)
        def tokenize(self, s, **kwargs):
            s = self.prep_sentence(s)
            return (super().tokenize)(s, **kwargs)

        def meta_tokenize(self, s: str) -> List[SimpleSpacyToken]:
            """Tokenize the sentence and return the metadata for it according to Spacy

            Due to implementation differences, does not provide the exact same API as the
            PreTrainedTokenizer's `tokenize` function
            """
            meta_info = self._to_spacy_meta(s)
            return self._tokenize_from_spacy_meta(meta_info)

        def meta_from_tokens(self, sentence: str, tokens: List[str], perform_check=True) -> List[SimpleSpacyToken]:
            """Convert existing tokens into their metadata, ignoring effects of special tokens from the tokenizer

            NOTE that the sentence MUST be the same sentence that produced the tokens, otherwise,
            an unpredictable error may occur. Or worse, it will act like it works when it in fact doesn't.

            Parameters:
                - sentence: Sentence the tokens came from
                - tokens: Tokenized version of the sentence. Can be post encoding or pre-encoding
                    (where special tokens are added)
                - perform_check: If True, check that the tokens come from the sentence. This slows down processing
                    and should be False if speed is more important than accuracy
            """
            orig_meta = self.meta_tokenize(sentence)
            new_meta = []
            j = 0
            if perform_check:
                is_encoded = self.encode(sentence) == self.convert_tokens_to_ids(tokens)
                is_tokenized = self.tokenize(sentence) == tokens
                if not is_encoded:
                    assert is_tokenized, 'Can only take tokens that come from the original sentence!'
            for i, b in enumerate(tokens):
                if b in self.all_special_tokens:
                    new_meta.append(self.meta_container(b))
                else:
                    new_meta.append(orig_meta[j])
                    j += 1

            return new_meta

        def _to_normed_spacy(self, s: str) -> List[str]:
            """Return the normalized tokens (i.e., language exceptions replaced by a lowercased version)"""
            doc = self.nlp(s)
            tokens = self._doc_to_fixed_tokens(doc)
            return tokens

        def _to_spacy_meta(self, s: str) -> List[SimpleSpacyToken]:
            """Convert a string into a list of records containing simplified spacy information"""
            doc = self.nlp(s)
            out = [self.meta_container(t) for t in doc]
            return out

        @delegates(pretrained_tokenizer.tokenize)
        def _raw_tokenize(self, s, **kwargs):
            """This bypasses the custom tokenization for the tokenization of the original model."""
            return (super().tokenize)(s, **kwargs)

        def _to_raw_spacy(self, s: str) -> List[str]:
            """Return the raw spacy tokens of a string"""
            doc = self.nlp(s)
            tokens = [t.text for t in doc]
            return tokens

        def _tokenize_from_spacy_meta(self, spacy_meta: List[SimpleSpacyToken]) -> List[SimpleSpacyToken]:
            """Convert spacy-tokenized SimpleSpacyTokens into the appropriate tokenizer's tokens"""
            out = [self._tokenize_from_meta_single(sm, i) for i, sm in enumerate(spacy_meta)]
            return flatten_(out)

        def _tokenize_from_meta_single(self, meta_token, idx):
            """Split a single spacy token with metadata into tokenizer tokens.

            Because the transformer's tokenizer may split each Spacy-tokenized word into multiple subwords,
            output a list

            For GPT2 tokenization, there is a different behavior for the tokenization of a word if it
            starts the sentence vs if it occurs later in the sentence.
            """
            BUFFER = 'X '

            def choose_norm(t):
                if t['token'].lower() == t['norm']:
                    return t['token']
                else:
                    return t['norm']

            tok = choose_norm(meta_token)
            if idx != 0:
                s = BUFFER + tok
                offset = 1
            else:
                s = tok
                offset = 0
            bpe_tokens = super().tokenize(s)
            return [meta_token.assoc('token', b) for b in bpe_tokens[offset:]]

        def _doc_to_fixed_tokens(self, doc: SpacyDoc) -> List[str]:
            """Extract tokens from a document, accounting for exceptions only if needed"""
            tokens = doc_to_fixed_tokens(doc)
            return tokens

    return Aligner


english = 'en_core_web_sm'
BertAligner = MakeAligner(BertTokenizer, english)
GPT2Aligner = MakeAligner(GPT2Tokenizer, english)
RobertaAligner = MakeAligner(RobertaTokenizer, english)
DistilBertAligner = MakeAligner(DistilBertTokenizer, english)