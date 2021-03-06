# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/qparser/default.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = "\nThis module contains the default search query parser.\n\nThis uses the excellent Pyparsing module \n(http://pyparsing.sourceforge.net/) to parse search query strings\ninto nodes from the query module.\n\nThis parser handles:\n\n* 'AND', 'OR', 'NOT'\n* grouping with parentheses\n* quoted phrase searching\n* wildcards, e.g. help*\n* ranges, e.g. [a TO b]\n* fields, e.g. title:whoosh\n\nThis parser was originally based on the searchparser example code available at:\n\nhttp://pyparsing.wikispaces.com/space/showimage/searchparser.py\n"
from pyparsing import printables, alphanums, OneOrMore, Group, Combine, Suppress, Optional, FollowedBy, Literal, CharsNotIn, Word, Keyword, Empty, White, Forward, QuotedString, StringEnd
from alfanous.Support.whoosh.query import *

def _make_default_parser():
    escapechar = '\\'
    wordtext = CharsNotIn('\\*?^():"{}[] ')
    escape = Suppress(escapechar) + (Word(printables, exact=1) | White(exact=1))
    wordtoken = Combine(OneOrMore(wordtext | escape))
    plainWord = Group(wordtoken).setResultsName('Word')
    wildchars = Word('?*')
    wildmixed = wordtoken + OneOrMore(wildchars + Optional(wordtoken))
    wildstart = wildchars + (OneOrMore(wordtoken + Optional(wildchars)) | FollowedBy(White() | StringEnd()))
    wildcard = Group(Combine(wildmixed | wildstart)).setResultsName('Wildcard')
    startfence = Literal('[') | Literal('{')
    endfence = Literal(']') | Literal('}')
    rangeitem = QuotedString('"') | wordtoken
    openstartrange = Group(Empty()) + Suppress(Keyword('TO') + White()) + Group(rangeitem)
    openendrange = Group(rangeitem) + Suppress(White() + Keyword('TO')) + Group(Empty())
    normalrange = Group(rangeitem) + Suppress(White() + Keyword('TO') + White()) + Group(rangeitem)
    range = Group(startfence + (normalrange | openstartrange | openendrange) + endfence).setResultsName('Range')
    generalWord = range | wildcard | plainWord
    quotedPhrase = Group(QuotedString('"')).setResultsName('Quotes')
    expression = Forward()
    parenthetical = Group(Suppress('(') + expression + Suppress(')')).setResultsName('Group')
    boostableUnit = generalWord | quotedPhrase
    boostedUnit = Group(boostableUnit + Suppress('^') + Word('0123456789', '.0123456789')).setResultsName('Boost')
    fieldableUnit = parenthetical | boostedUnit | boostableUnit
    fieldedUnit = Group(Word(alphanums + '_') + Suppress(':') + fieldableUnit).setResultsName('Field')
    unit = fieldedUnit | fieldableUnit
    operatorNot = Group(Suppress(Keyword('not', caseless=True)) + Suppress(White()) + unit).setResultsName('Not')
    generalUnit = operatorNot | unit
    andToken = Keyword('AND', caseless=False)
    orToken = Keyword('OR', caseless=False)
    andNotToken = Keyword('ANDNOT', caseless=False)
    operatorAnd = Group(generalUnit + Suppress(White()) + Suppress(andToken) + Suppress(White()) + expression).setResultsName('And')
    operatorOr = Group(generalUnit + Suppress(White()) + Suppress(orToken) + Suppress(White()) + expression).setResultsName('Or')
    operatorAndNot = Group(unit + Suppress(White()) + Suppress(andNotToken) + Suppress(White()) + unit).setResultsName('AndNot')
    expression << (OneOrMore(operatorAnd | operatorOr | operatorAndNot | generalUnit | Suppress(White())) | Empty())
    toplevel = Group(expression).setResultsName('Toplevel') + StringEnd()
    return toplevel.parseString


DEFAULT_PARSER = _make_default_parser()

class PyparsingBasedParser(object):

    def _field(self, fieldname):
        if self.schema:
            return self.schema[fieldname]

    def parse(self, input, normalize=True):
        """Parses the input string and returns a Query object/tree.
        
        This method may return None if the input string does not result in any
        valid queries. It may also raise a variety of exceptions if the input
        string is malformed.
        
        :param input: the unicode string to parse.
        :param normalize: whether to call normalize() on the query object/tree
            before returning it. This should be left on unless you're trying to
            debug the parser output.
        :rtype: :class:`whoosh.query.Query`
        """
        ast = self.parser(input)[0]
        q = self._eval(ast, self.default_field)
        if q and normalize:
            q = q.normalize()
        return q

    def _eval(self, node, fieldname):
        name = node.getName()
        return getattr(self, '_' + name)(node, fieldname)

    def get_term_text(self, field, text, **kwargs):
        for t in field.process_text(text, mode='query', **kwargs):
            return t

    def make_term(self, fieldname, text):
        field = self._field(fieldname)
        if field:
            if field.parse_query:
                return field.parse_query(fieldname, text)
            text = self.get_term_text(field, text)
        if text is None:
            return NullQuery
        else:
            return self.termclass(fieldname, text)

    def make_phrase(self, fieldname, text):
        field = self._field(fieldname)
        if field:
            if field.parse_query:
                return field.parse_query(fieldname, text)
            else:
                texts = list(field.process_text(text, mode='query'))
                if not texts:
                    return self.termclass(fieldname, '')
                if len(texts) == 1:
                    return self.termclass(fieldname, texts[0])
                return Phrase(fieldname, texts)

        else:
            return Phrase(fieldname, text.split(' '))

    def make_wildcard(self, fieldname, text):
        field = self._field(fieldname)
        if field:
            text = self.get_term_text(field, text, tokenize=False, removestops=False)
        return Wildcard(fieldname, text)

    def make_range(self, fieldname, start, end, startexcl, endexcl):
        field = self._field(fieldname)
        if field:
            if start:
                start = self.get_term_text(field, start, tokenize=False, removestops=False)
            if end:
                end = self.get_term_text(field, end, tokenize=False, removestops=False)
        if not start and not end:
            raise QueryError('TermRange must have start and/or end')
        if not start:
            start = ''
        if not end:
            end = '\uffff'
        return TermRange(fieldname, start, end, startexcl, endexcl)

    def make_and(self, qs):
        return And(qs)

    def make_or(self, qs):
        return Or(qs)

    def make_andnot(self, positive, negative):
        return AndNot(positive, negative)

    def make_not(self, q):
        return Not(q)


class QueryParser(PyparsingBasedParser):
    """The default parser for Whoosh, implementing a powerful fielded query
    language similar to Lucene's.
    """
    __inittypes__ = dict(default_field=str, schema='whoosh.fields.Schema', conjunction='whoosh.query.Query', termclass='whoosh.query.Query')

    def __init__(self, default_field, schema=None, conjunction=And, termclass=Term):
        """
        :param default_field: Use this as the field for any terms without
            an explicit field. For example, if the query string is
            "hello f1:there" and the default field is "f2", the parsed
            query will be as if the user had entered "f2:hello f1:there".
            This argument is required.
        :param conjuction: Use this query.Query class to join together clauses
            where the user has not explictly specified a join. For example, if
            this is query.And, the query string "a b c" will be parsed as
            "a AND b AND c". If this is query.Or, the string will be parsed as
            "a OR b OR c".
        :param termclass: Use this query.Query class for bare terms. For
            example, query.Term or query.Variations.
        :param schema: An optional fields.Schema object. If this argument is
            present, the appropriate field will be used to tokenize
            terms/phrases before they are turned into query objects.
        """
        self.default_field = default_field
        self.conjunction = conjunction
        self.termclass = termclass
        self.schema = schema
        self.parser = DEFAULT_PARSER

    def _Toplevel(self, node, fieldname):
        return self.conjunction([ self._eval(s, fieldname) for s in node ])

    def _Word(self, node, fieldname):
        return self.make_term(fieldname, node[0])

    def _Quotes(self, node, fieldname):
        return self.make_phrase(fieldname, node[0])

    def _Range(self, node, fieldname):
        startchar, start, end, endchar = node
        startexcl = startchar == '{'
        endexcl = endchar == '}'
        starttext = endtext = None
        if start:
            starttext = start[0]
        if end:
            endtext = end[0]
        return self.make_range(fieldname, starttext, endtext, startexcl, endexcl)

    def _Wildcard(self, node, fieldname):
        return self.make_wildcard(fieldname, node[0])

    def _And(self, node, fieldname):
        return self.make_and([ self._eval(s, fieldname) for s in node ])

    def _Or(self, node, fieldname):
        return self.make_or([ self._eval(s, fieldname) for s in node ])

    def _AndNot(self, node, fieldname):
        return self.make_andnot(self._eval(node[0], fieldname), self._eval(node[1], fieldname))

    def _Not(self, node, fieldname):
        return self.make_not(self._eval(node[0], fieldname))

    def _Group(self, node, fieldname):
        return self.conjunction([ self._eval(s, fieldname) for s in node ])

    def _Field(self, node, fieldname):
        return self._eval(node[1], node[0])

    def _Boost(self, node, fieldname):
        obj = self._eval(node[0], fieldname)
        obj.boost = float(node[1])
        return obj


class MultifieldParser(QueryParser):
    """A subclass of QueryParser. Instead of assigning unfielded clauses to a
    default field, this class transforms them into an OR clause that searches a
    list of fields. For example, if the list of multi-fields is "f1", "f2" and
    the query string is "hello there", the class will parse "(f1:hello OR
    f2:hello) (f1:there OR f2:there)". This is very useful when you have two
    textual fields (e.g. "title" and "content") you want to search by default.
    """
    __inittypes__ = dict(fieldnames=list, schema='whoosh.fields.Schema', conjunction='whoosh.query.Query', termclass='whoosh.query.Query')

    def __init__(self, fieldnames, schema=None, conjunction=And, termclass=Term):
        super(MultifieldParser, self).__init__(None, schema=schema, conjunction=conjunction, termclass=termclass)
        self.fieldnames = fieldnames
        return

    def _make(self, methodname, fieldname, *args):
        method = getattr(super(MultifieldParser, self), methodname)
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