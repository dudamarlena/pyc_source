# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/QueryProcessing.py
# Compiled at: 2015-06-30 06:52:38
"""
This module contains customized query parsers for Arabic and Quran.

TODO Buckwalter/Other codings Search  {bw!  kutubo }
TODO Upgrading Tuple Search to Embeded Query Search  {1! word="foo"}
TODO Smart-search : take the optimal choice with NLP!
TODO Synonyme-Antonyme Upgrade to related search {syn!  fire }
FIXME multifields
"""
from pyparsing import printables, alphanums
from pyparsing import ZeroOrMore, OneOrMore
from pyparsing import Group, Combine, Suppress, Optional, FollowedBy
from pyparsing import Literal, CharsNotIn, Word, Keyword
from pyparsing import Empty, White, Forward, QuotedString
from pyparsing import StringEnd
from alfanous.Support.whoosh.qparser import QueryParser
from alfanous.Support.whoosh.query import Term, MultiTerm
from alfanous.Support.whoosh.query import Wildcard as whoosh_Wildcard
from alfanous.Support.whoosh.query import Prefix as whoosh_Prefix
from alfanous.Support.whoosh.query import Or, NullQuery, Every, And
try:
    from alfanous.dynamic_resources.synonymes_dyn import syndict
except ImportError:
    syndict = {}

try:
    from alfanous.dynamic_resources.arabicnames_dyn import ara2eng_names
except ImportError:
    ara2eng_names = {}

try:
    from alfanous.dynamic_resources.word_props_dyn import worddict
except ImportError:
    worddict = {}

try:
    from alfanous.dynamic_resources.derivations_dyn import derivedict
except ImportError:
    derivedict = {}

try:
    from alfanous.dynamic_resources.antonymes_dyn import antdict
except ImportError:
    antdict = {}

from alfanous.Indexing import QseDocIndex
from alfanous.Exceptions import FeedBack
from alfanous.TextProcessing import QArabicSymbolsFilter, unicode_
from alfanous.Misc import LOCATE, FIND, FILTER_DOUBLES
FEEDBACK = True

def _make_arabic_parser():
    escapechar = '//'
    alephba = '\n                abcdefghijklmnopqrstuvwxyz_\n                األآإـتنمكطدجحخهعغفقثصضشسيبئءؤرىةوزظذ\n                '
    wordtext = CharsNotIn('//*؟^():"{}[]$><%~#،,\' +-|')
    escape = Suppress(escapechar) + (Word(printables, exact=1) | White(exact=1))
    wordtoken = Combine(OneOrMore(wordtext | escape))
    plainWord = Group(wordtoken).setResultsName('Word')
    wildchars = Word('؟?*')
    wildmixed = wordtoken + OneOrMore(wildchars + Optional(wordtoken))
    wildstart = wildchars + (OneOrMore(wordtoken + Optional(wildchars)) | FollowedBy(White() | StringEnd()))
    wildcard = Group(Combine(wildmixed | wildstart)).setResultsName('Wildcard')
    startfence = Literal('[')
    endfence = Literal(']')
    rangeitem = QuotedString('"') | wordtoken
    to = Keyword('الى') | Keyword('إلى') | Keyword('To') | Keyword('to') | Keyword('TO')
    openstartrange = Group(Empty()) + Suppress(to + White()) + Group(rangeitem)
    openendrange = Group(rangeitem) + Suppress(White() + to) + Group(Empty())
    normalrange = Group(rangeitem) + Suppress(White() + to + White()) + Group(rangeitem)
    range = Group(startfence + (normalrange | openstartrange | openendrange) + endfence).setResultsName('Range')
    syn_symbol = Literal('~')
    synonym = Group(syn_symbol + wordtoken).setResultsName('Synonyms')
    ant_symbol = Literal('#')
    antonym = Group(ant_symbol + wordtoken).setResultsName('Antonyms')
    derive_symbole = Literal('<') | Literal('>')
    derivation = Group(OneOrMore(derive_symbole) + wordtoken).setResultsName('Derivation')
    spellerrors_symbole = Literal('%')
    spellerrors = Group(spellerrors_symbole + wordtoken).setResultsName('SpellErrors')
    tashkil_symbol = Literal("'")
    tashkil = Group(tashkil_symbol + ZeroOrMore(wordtoken | White()) + tashkil_symbol).setResultsName('Tashkil')
    starttuple = Literal('{')
    endtuple = Literal('}')
    bettuple = Literal('،') | Literal(',')
    wordtuple = Group(Optional(wordtoken))
    tuple = Group(starttuple + wordtuple + ZeroOrMore(bettuple + wordtuple) + endtuple).setResultsName('Tuple')
    generalWord = range | wildcard | plainWord | tuple | antonym | synonym | derivation | tashkil | spellerrors
    quotedPhrase = Group(QuotedString('"')).setResultsName('Quotes')
    expression = Forward()
    parenthetical = Group(Suppress('(') + expression + Suppress(')')).setResultsName('Group')
    boostableUnit = generalWord | quotedPhrase
    boostedUnit = Group(boostableUnit + Suppress('^') + Word('0123456789', '.0123456789')).setResultsName('Boost')
    fieldableUnit = parenthetical | boostedUnit | boostableUnit
    fieldedUnit = Group((Word(alephba + '_') | Word(alphanums + '_')) + Suppress(':') + fieldableUnit).setResultsName('Field')
    unit = fieldedUnit | fieldableUnit
    operatorNot = Group(Suppress(Keyword('ليس') | Keyword('NOT')) + Suppress(White()) + unit).setResultsName('Not')
    generalUnit = operatorNot | unit
    andToken = Keyword('و') | Keyword('AND')
    orToken = Keyword('أو') | Keyword('او') | Keyword('OR')
    andNotToken = Keyword('وليس') | Keyword('ANDNOT')
    operatorAnd = Group(generalUnit + Suppress(White()) + Suppress(andToken) + Suppress(White()) + expression | generalUnit + Suppress(Literal('+')) + expression).setResultsName('And')
    operatorOr = Group(generalUnit + Suppress(White()) + Suppress(orToken) + Suppress(White()) + expression | generalUnit + Suppress(Literal('|')) + expression).setResultsName('Or')
    operatorAndNot = Group(unit + Suppress(White()) + Suppress(andNotToken) + Suppress(White()) + expression | unit + Suppress(Literal('-')) + expression).setResultsName('AndNot')
    expression << (OneOrMore(operatorAnd | operatorOr | operatorAndNot | generalUnit | Suppress(White())) | Empty())
    toplevel = Group(expression).setResultsName('Toplevel') + StringEnd()
    return toplevel.parseString


ARABIC_PARSER_FN = _make_arabic_parser()

class StandardParser(QueryParser):

    def __init__(self, schema, mainfield, otherfields, termclass=Term):
        super(StandardParser, self).__init__(mainfield, schema=schema, conjunction=Or, termclass=termclass)


class ArabicParser(StandardParser):
    """a customized parser that respects Arabic properties"""

    def __init__(self, schema, mainfield, otherfields=[], termclass=Term, ara2eng=ara2eng_names):
        super(ArabicParser, self).__init__(schema=schema, mainfield=mainfield, otherfields=otherfields, termclass=termclass)
        self.parser = ARABIC_PARSER_FN
        self.ara2eng = ara2eng

    def _Field(self, node, fieldname):
        if self.ara2eng.has_key(node[0]):
            name = self.ara2eng[node[0]]
        else:
            name = node[0]
        return self._eval(node[1], name)

    def _Synonyms(self, node, fieldname):
        return self.make_synonyms(fieldname, node[1])

    def _Antonyms(self, node, fieldname):
        return self.make_antonyms(fieldname, node[1])

    def _Derivation(self, node, fieldname):
        return self.make_derivation(fieldname, text=node[(-1)], level=len(node) - 1)

    def _SpellErrors(self, node, fieldname):
        return self.make_spellerrors(fieldname, node[1])

    def _Tashkil(self, node, fieldname):
        if len(node) > 2:
            lst = node[1:-1]
        else:
            lst = []
        return self.make_tashkil(fieldname, lst)

    def _Tuple(self, node, fieldname):
        return self.make_tuple(fieldname, [ node[i][0] for i in range(1, len(node), 2) ])

    def _Prefix(self, node, fieldname):
        return self.make_prefix(fieldname, node[1])

    def make_synonyms(self, fieldname, text):
        return self.Synonyms(fieldname, text)

    def make_antonyms(self, fieldname, text):
        return self.Antonyms(fieldname, text)

    def make_derivation(self, fieldname, text, level):
        return self.Derivation(fieldname, text, level)

    def make_spellerrors(self, fieldname, text):
        return self.SpellErrors(fieldname, text)

    def make_tashkil(self, fieldname, words):
        words = [ word for word in words if word[0] not in ' \t\r\n' ]
        if len(words):
            return self.Tashkil(fieldname, words)
        else:
            return NullQuery

    def make_tuple(self, fieldname, items):
        return self.Tuple(fieldname, items)

    def make_wildcard(self, fieldname, text):
        field = self._field(fieldname) if fieldname else None
        if field:
            text = self.get_term_text(field, text, tokenize=False, removestops=False)
        return self.Wildcard(fieldname, text)

    def make_prefix(self, fieldname, text):
        field = self._field(fieldname)
        if field:
            text = self.get_term_text(field, text, tokenize=False, removestops=False)
        return self.Prefix(fieldname, text)

    class QMultiTerm(MultiTerm):
        """ basic class """

        def _words(self, ixreader):
            fieldname = self.fieldname
            return [ word for word in self.words if (
             fieldname, word) in ixreader
                   ]

        def __unicode__(self):
            return '%s:<%s>' % (self.fieldname, self.text)

        def __repr__(self):
            return '%s(%r, %r, boost=%r)' % (self.__class__.__name__,
             self.fieldname,
             self.text,
             self.boost)

        def _all_terms(self, termset, phrases=True):
            for word in self.words:
                termset.add((self.fieldname, word))

        def _existing_terms(self, ixreader, termset, reverse=False, phrases=True):
            fieldname, words = self.fieldname, self.words
            fieldnum = ixreader.fieldname_to_num(fieldname)
            for word in words:
                contains = (
                 fieldnum, word) in ixreader
                if reverse:
                    contains = not contains
                if contains:
                    termset.add((fieldname, word))

    class FuzzyAll(QMultiTerm):
        """  do all possible operations to make a  fuzzy search
                    - Synonyms
                    - root derivation
                    - spell
                    - tashkil
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            self.words = self.pipeline(self.fieldname, self.text)

        def pipeline(self, fieldname, text):
            words = set()
            words |= set(ArabicParser.Synonyms(fieldname, text).words)
            words |= set(ArabicParser.Derivation(fieldname, text).words)
            return list(words)

    class Synonyms(QMultiTerm):
        """
        query that automatically searches for synonyms
        of the given word in the same field.
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            self.words = self.synonyms(self.text)

        @staticmethod
        def synonyms(word):
            """ TODO find an arabic synonyms thesaurus """
            return [
             word]

    class Antonyms(QMultiTerm):
        """
        query that automatically searches for antonyms
        of the given word in the same field.
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            self.words = self.antonyms(self.text)

        @staticmethod
        def antonyms(word):
            """ TODO find an arabic antonyms thesaurus """
            return [
             word]

    class Derivation(QMultiTerm):
        """
        query that automatically searches for derivations
        of the given word in the same field.
        """

        def __init__(self, fieldname, text, level=0, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            self.words = self.derivation(self.text, level)

            @staticmethod
            def derivation(word, leveldist):
                """ 
                TODO find a good specific stemmer for arabic language,
                manipulate at least tow levels of stemming root,lemma 
                """
                return [
                 word]

    class SpellErrors(QMultiTerm):
        """
        query that ignores  the spell errors of arabic letters such as:
            - ta' marbuta and ha'
            - alef maqsura and ya'
            - hamza forms
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            self.words = [text]
            self.ASF = QArabicSymbolsFilter(shaping=True, tashkil=False, spellerrors=True, hamza=True)

        def _words(self, ixreader):
            for field, indexed_text in ixreader.all_terms():
                if field == self.fieldname:
                    if self._compare(self.text, indexed_text):
                        yield indexed_text

        def _compare(self, first, second):
            """ normalize and compare """
            if first[:2] == 'مو':
                print first
            eqiv = self.ASF.normalize_all(first) == self.ASF.normalize_all(second)
            if eqiv:
                self.words.append(second)
            return eqiv

    class Tashkil(QMultiTerm):
        """
        query that automatically searches for different tashkil of words
        of the given word in the same field.
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.fieldname = fieldname
            self.text = text
            self.boost = boost
            ASF = QArabicSymbolsFilter(shaping=False, tashkil=True, spellerrors=False, hamza=False)
            self.words = [ ASF.normalize_all(word) for word in text ]

        def _words(self, ixreader):
            for field, indexed_text in ixreader.all_terms():
                if field == self.fieldname:
                    for word in self.text:
                        if self._compare(word, indexed_text):
                            yield indexed_text

        def _compare(self, first, second):
            """ normalize and compare """
            word1 = unicode_(first)
            word2 = unicode_(second)
            eqiv = word1 == word2
            if eqiv:
                self.words.append(second)
            return eqiv

    class Tuple(QMultiTerm):
        """
        query that automatically searches for different  words that have 
        the same root*pattern*type of the given word in the same field.
        """

        def __init__(self, fieldname, items, boost=1.0):
            self.fieldname = fieldname
            self.props = self._properties(items)
            self.text = '(' + (',').join(items) + ')'
            self.boost = boost
            self.words = self.tuple(self.props)

        def _properties(self, items):
            """ convert list of properties to a dictionary """
            l = len(items)
            if l >= 0:
                D = {}
            if l >= 1:
                D['test'] = items[0]
            if l >= 2:
                pass
            return D

        @staticmethod
        def tuple(props):
            """ search the words that have some specific properties
            TODO find an arabic analyzer that can suggest a word properties
            """
            return []

    class Wildcard(whoosh_Wildcard):
        """customize the wildcards for arabic symbols   """

        def __init__(self, fieldname, text, boost=1.0):
            new_text = text.replace('؟', '?')
            super(ArabicParser.Wildcard, self).__init__(fieldname, new_text, boost)


class QuranicParser(ArabicParser):
    """a customized query parser for Quran"""

    def __init__(self, schema, mainfield='aya', otherfields=[], termclass=Term, ara2eng=ara2eng_names):
        super(QuranicParser, self).__init__(schema=schema, mainfield=mainfield, otherfields=otherfields, termclass=termclass)

    class FuzzyAll(ArabicParser.FuzzyAll):
        """ specific for quran    """

        def pipeline(self, fieldname, text):
            words = set()
            words |= set(QuranicParser.Synonyms(fieldname, text).words)
            words |= set(QuranicParser.Derivation(fieldname, text, level=1).words)
            return list(words)

    class Synonyms(ArabicParser.Synonyms):
        """
        query that automatically searches for synonyms
        of the given word in the same field.specific for qur'an
        """

        @staticmethod
        def synonyms(word):
            if syndict.has_key(word):
                return syndict[word]
            else:
                return [
                 word]

            if FEEDBACK:
                raise FeedBack(table='synonyms', value=word)

    class Antonyms(ArabicParser.Antonyms):
        """
                query that automatically searches for antonyms
                of the given word in the same field.
        """

        @staticmethod
        def antonyms(word):
            if antdict.has_key(word):
                return antdict[word]
            else:
                return [
                 word]

            if FEEDBACK:
                raise FeedBack(table='antonyms', value=word)

    class Derivation(ArabicParser.Derivation):
        """
            specific for quran
        """

        @staticmethod
        def derivation(word, leveldist):
            """ search in defined field """
            if word in derivedict['word_']:
                indexsrc = 'word_'
            elif word in derivedict['lemma']:
                indexsrc = 'lemma'
            elif word in derivedict['root']:
                indexsrc = 'root'
            else:
                indexsrc = None
            if leveldist == 0:
                indexdist = 'word_'
            elif leveldist == 1:
                indexdist = 'lemma'
            elif leveldist == 2:
                indexdist = 'root'
            else:
                indexdist = 'root'
            lst = []
            if indexsrc:
                itm = LOCATE(derivedict[indexsrc], derivedict[indexdist], word)
                if itm:
                    lst = FILTER_DOUBLES(FIND(derivedict[indexdist], derivedict['word_'], itm))
                else:
                    lst = [
                     word]
            return lst

    class Tuple(ArabicParser.Tuple):
        """
        query that automatically searches for different  words that have 
        the same root*pattern*type of the given word in the same field.
                
        """

        def _properties(self, items):
            """ convert list of prop"rties to a dictionary """
            l = len(items)
            if l >= 0:
                D = {}
            if l >= 1:
                D['root'] = items[0]
            if l >= 2:
                D['type'] = items[1]
            if l >= 3:
                D['pattern'] = items[2]
            if l >= 4:
                pass
            return D

        @staticmethod
        def tuple(props):
            """ search the words that have the specific properties """
            wset = set()
            firsttime = True
            for propkey in props.keys():
                if worddict.has_key(propkey):
                    partial_wset = set(FIND(worddict[propkey], worddict['word_'], props[propkey]))
                    if firsttime:
                        wset = partial_wset
                        firsttime = False
                    else:
                        wset &= partial_wset

            return list(wset)

    class Wildcard(ArabicParser.Wildcard, ArabicParser.QMultiTerm):
        """
        customize the wildcards for highlight
        """

        def __init__(self, fieldname, text, boost=1.0):
            self.words = []
            new_text = text.replace('؟', '?')
            super(QuranicParser.Wildcard, self).__init__(fieldname, new_text, boost)

        def _words(self, ixreader):
            if self.prefix:
                candidates = ixreader.expand_prefix(self.fieldname, self.prefix)
            else:
                candidates = ixreader.lexicon(self.fieldname)
            exp = self.expression
            for text in candidates:
                if exp.match(text):
                    self.words.append(text)
                    yield text

        def normalize(self):
            text = self.text
            if text == '*':
                return Every(boost=self.boost)
            else:
                if '*' not in text and '?' not in text:
                    return Term(self.fieldname, self.text, boost=self.boost)
                if '?' not in text and text.endswith('*') and text.find('*') == len(text) - 1 and (len(text) < 2 or text[(-2)] != '\\'):
                    return QuranicParser.Prefix(self.fieldname, self.text[:-1], boost=self.boost)
                return self

    class Prefix(whoosh_Prefix, ArabicParser.QMultiTerm):
        """customize Prefix for  highlight """

        def __init__(self, fieldname, text, boost=1.0):
            self.words = []
            super(QuranicParser.Prefix, self).__init__(fieldname, text, boost)

        def _words(self, ixreader):
            tt = ixreader.termtable
            fieldid = ixreader.schema.to_number(self.fieldname)
            for fn, t in tt.keys_from((fieldid, self.text)):
                if fn != fieldid or not t.startswith(self.text):
                    return
                self.words.append(t)
                yield t


class SuperFuzzyAll(QuranicParser.FuzzyAll):
    """ 
    specific for quran
    search with all possible forms of the  word
    """

    def pipeline(self, fieldname, text):
        words = set()
        words |= set(QuranicParser.Synonyms(fieldname, text).words)
        words |= set(QuranicParser.Derivation(fieldname, text, level=1).words)
        if len(words) == 1:
            wildcarded_text = (' ').join(map(lambda x: '*' + x + '*', text.split(' ')))
            words |= set(QuranicParser.Wildcard(fieldname, wildcarded_text).words)
        return list(words)


class FuzzyQuranicParser(QuranicParser):
    """a customized query parser  that respects Quranic properties"""

    def __init__(self, schema, mainfield='aya', otherfields=[], termclass=SuperFuzzyAll, ara2eng=ara2eng_names):
        super(FuzzyQuranicParser, self).__init__(schema=schema, mainfield=mainfield, otherfields=otherfields, termclass=termclass)
        self.fieldnames = [
         mainfield] + otherfields

    def _make(self, methodname, fieldname, *args):
        method = getattr(super(FuzzyQuranicParser, self), methodname)
        if fieldname is None:
            return Or([ method(fn, *args) for fn in self.fieldnames ])
        return method(fieldname, *args)
        return

    def make_term(self, fieldname, text):
        return self._make('make_term', fieldname, text)

    def make_range(self, fieldname, start, end, startexcl, endexcl):
        return self._make('make_range', fieldname, start, end, startexcl, endexcl)

    def make_wildcard(self, fieldname, text):
        return self._make('make_wildcard', fieldname, text)

    def make_phrase(self, fieldname, text):
        return self._make('make_phrase', fieldname, text)