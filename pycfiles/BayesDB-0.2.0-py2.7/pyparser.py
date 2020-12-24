# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/pyparser.py
# Compiled at: 2015-02-12 15:25:14
from pyparsing import Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional, Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, ZeroOrMore, OneOrMore, restOfLine, Keyword
selectStatement = Forward()
identifier = Word(alphas, alphanums + '_')
selectToken = Keyword('select', caseless=True)
fromToken = Keyword('from', caseless=True)
orderByToken = Keyword('order', caseless=True) + Keyword('by', caseless=True)
limitToken = Keyword('limit', caseless=True)
columnNameList = Group(delimitedList(identifier | '*'))
createBtableStatement = Keyword('create', caseless=True) + Keyword('btable', caseless=True) + identifier.setResultsName('tablename') + fromToken + identifier.setResultsName('filename')
selectStatement << selectToken + columnNameList.setResultsName('columns') + fromToken + identifier.setResultsName('tablename') + Optional(whereClause) + Optional(orderByClause) + Optional(limitClause)
BQLStatement = (selectStatement | createBtableStatement) + Optional(';')
BQL = ZeroOrMore(BQLStatement)
dashComment = '--' + restOfLine
BQL.ignore(dashComment)

def test(str):
    print str, '->'
    try:
        tokens = BQL.parseString(str)
        print 'tokens = ', tokens
        print 'tokens.tablename =', tokens.tablename
        print 'tokens.filename =', tokens.filename
    except ParseException as err:
        print ' ' * err.loc + '^\n' + err.msg
        print err

    print


class PyParser(object):

    def __init__(self):
        pass

    def parse(self, bql_string):
        pass

    def parse_line(self, bql_string):
        pass