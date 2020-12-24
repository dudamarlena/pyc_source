# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/nlp/norm.py
# Compiled at: 2020-04-17 19:37:40
# Size of source mod 2**32: 8707 bytes
"""Normalize text and map Spacy documents.

"""
__author__ = 'Paul Landes'
import logging, re, itertools as it
from abc import abstractmethod
from spacy.tokens.token import Token
from zensols.actioncli import ConfigFactory
logger = logging.getLogger(__name__)

class TokenNormalizer(object):
    __doc__ = 'Base token extractor returns tuples of tokens and their normalized version.\n\n    '

    def __init__(self, normalize=True, embed_entities=True, remove_first_stop=False, limit=None):
        """Initialize the normalizer.

        :param normalize: whether or not to normalize the text (useful since
                          this class has other functionality.
        :param embed_entities: whether or not to replace tokens with their
                          respective named entity version
        :param remove_first_stop: whether to remove the first top word in named
                                  entities when ``embed_entities`` is ``True``

        """
        logger.debug(f"init embedding entities: {embed_entities}")
        self._normalize = normalize
        self.embed_entities = embed_entities
        self.remove_first_stop = remove_first_stop
        self.limit = limit

    def __embed_entities(self, doc):
        """For each token, return the named entity form if it exists.

        :param doc: the spacy document to iterate over

        """
        tlen = len(doc)
        ents = {}
        for ent in doc.ents:
            logger.debug(f"adding entity start: {ent.start} -> {ent}")
            ents[ent.start] = ent

        logger.debug(f"entities: {ents}")
        i = 0
        while i < tlen:
            if i in ents:
                ent = ents[i]
                logger.debug(f"adding entity: {ent}")
                yield ent
                i = ent.end
            else:
                tok = doc[i]
                logger.debug(f"adding token: {tok}")
                yield tok
                i += 1

    def __norm_to_tok_tups(self, doc):
        """Normalize the document in to (token, normal text) tuples."""

        def norm(tok_or_ent):
            if isinstance(tok_or_ent, Token):
                stok = tok_or_ent.lemma_
            else:
                if self.remove_first_stop:
                    if tok_or_ent[0].is_stop:
                        tok_or_ent = tok_or_ent[1:]
                stok = tok_or_ent.text.lower()
            return (
             tok_or_ent, stok)

        logger.debug(f"embedding entities: {self.embed_entities}")
        if self.embed_entities:
            toks = self._TokenNormalizer__embed_entities(doc)
        else:
            toks = doc
        if self._normalize:
            toks = map(norm, toks)
        else:
            toks = map(lambda t: (t, t.orth_), toks)
        return toks

    def _map_tokens(self, token_tups):
        """Map token tuples in sub classes.

        :param token_tups: tuples generated from ``__norm_to_tok_tups``
        """
        pass

    def normalize(self, doc):
        """Normalize Spacey document ``doc`` in to (token, normal text) tuples.
        """
        tlist = self._TokenNormalizer__norm_to_tok_tups(doc)
        maps = self._map_tokens(tlist)
        if maps is not None:
            tlist = tuple(maps)
        return iter(tlist)

    def __str__(self):
        if hasattr(self, 'name'):
            name = self.name
        else:
            name = type(self).__name__
        return f"{name}: embed={self.embed_entities}, " + f"normalize: {self._normalize} " + f"remove first stop: {self.remove_first_stop}"

    def __repr__(self):
        return self.__str__()


class TokenNormalizerFactory(ConfigFactory):
    INSTANCE_CLASSES = {}

    def __init__(self, config):
        super(TokenNormalizerFactory, self).__init__(config, '{name}_token_normalizer')


TokenNormalizerFactory.register(TokenNormalizer)

class TokenMapper(object):
    __doc__ = 'Abstract class used to transform token tuples generated from\n    ``TokenNormalizer.normalize``.\n\n    '

    @abstractmethod
    def map_tokens(self, token_tups):
        """Transform token tuples.

        """
        pass


class TokenMapperFactory(ConfigFactory):
    INSTANCE_CLASSES = {}

    def __init__(self, config):
        super(TokenMapperFactory, self).__init__(config, '{name}_token_mapper')


class SplitTokenMapper(TokenMapper):
    __doc__ = 'Splits the normalized text on a per token basis with a regular expression.\n\n    '

    def __init__(self, regex, *args, **kwargs):
        (super(SplitTokenMapper, self).__init__)(*args, **kwargs)
        self.regex = re.compile(eval(regex))

    def map_tokens(self, token_tups):
        rg = self.regex
        return map(lambda t: map(lambda s: (t[0], s), re.split(rg, t[1])), token_tups)


TokenMapperFactory.register(SplitTokenMapper)

class FilterTokenMapper(TokenMapper):
    __doc__ = 'Filter tokens based on token (Spacy) attributes.\n\n    '

    def __init__(self, *args, remove_stop=False, remove_space=False, remove_pronouns=False, remove_punctuation=False, remove_determiners=False, **kwargs):
        (super(FilterTokenMapper, self).__init__)(*args, **kwargs)
        self.remove_stop = remove_stop
        self.remove_space = remove_space
        self.remove_pronouns = remove_pronouns
        self.remove_punctuation = remove_punctuation
        self.remove_determiners = remove_determiners
        logger.debug(f"created {self.__class__}: " + f"remove_stop: {remove_stop}, " + f"remove_space: {remove_space}, " + f"remove_pronouns: {remove_pronouns}, " + f"remove_punctuation: {remove_punctuation}, " + f"remove_determiners: {remove_determiners}")

    def _filter(self, tok_or_ent_tup):
        tok_or_ent = tok_or_ent_tup[0]
        logger.debug(f"filter: {tok_or_ent} ({type(tok_or_ent)})")
        keep = False
        if isinstance(tok_or_ent, Token):
            t = tok_or_ent
            logger.debug(f"token {t}: l={len(t)}, s={t.is_stop}, p={t.is_punct}")
            if self.remove_stop:
                if t.is_stop or self.remove_space:
                    if t.is_space or self.remove_pronouns:
                        if t.lemma_ == '-PRON-' or self.remove_punctuation:
                            if t.is_punct or self.remove_determiners:
                                if t.tag_ == 'DT' or len(t) > 0:
                                    keep = True
        else:
            keep = True
        logger.debug(f"filter: keeping={keep}")
        return keep

    def map_tokens(self, token_tups):
        return (
         filter(self._filter, token_tups),)


TokenMapperFactory.register(FilterTokenMapper)

class SubstituteTokenMapper(TokenMapper):
    __doc__ = 'Replace a string in normalized token text.\n\n    '

    def __init__(self, regex, replace_char, *args, **kwargs):
        (super(SubstituteTokenMapper, self).__init__)(*args, **kwargs)
        self.regex = re.compile(eval(regex))
        self.replace_char = replace_char

    def map_tokens(self, token_tups):
        return (
         map(lambda x: (x[0], re.sub(self.regex, self.replace_char, x[1])), token_tups),)


TokenMapperFactory.register(SubstituteTokenMapper)

class LambdaTokenMapper(TokenMapper):
    __doc__ = 'Use a lambda expression to map a token tuple.\n\n    This is handy for specialized behavior that can be added directly to a\n    configuration file.\n\n    '

    def __init__(self, add_lambda=None, map_lambda=None, *args, **kwargs):
        (super(LambdaTokenMapper, self).__init__)(*args, **kwargs)
        if add_lambda is None:
            self.add_lambda = lambda x: ()
        else:
            self.add_lambda = eval(add_lambda)
        if map_lambda is None:
            self.map_lambda = lambda x: x
        else:
            self.map_lambda = eval(map_lambda)

    def map_tokens(self, terms):
        return (map(self.map_lambda, terms),)


TokenMapperFactory.register(LambdaTokenMapper)

class MapTokenNormalizer(TokenNormalizer):
    __doc__ = 'A normalizer that applies a sequence of ``TokenMappers`` to transform\n    the normalized token text.\n\n    '

    def __init__(self, config, mapper_class_list, *args, **kwargs):
        (super(MapTokenNormalizer, self).__init__)(*args, **kwargs)
        ta = TokenMapperFactory(config)
        self.mappers = tuple(map(ta.instance, mapper_class_list))

    def _map_tokens(self, token_tups):
        for mapper in self.mappers:
            logger.debug(f"mapping token_tups with {mapper}")
            token_tups = (it.chain)(*mapper.map_tokens(token_tups))

        return token_tups


TokenNormalizerFactory.register(MapTokenNormalizer)