# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlpython/completion.py
# Compiled at: 2012-05-26 21:28:24
import pyparsing, re, doctest
sqlStyleComment = pyparsing.Literal('--') + pyparsing.ZeroOrMore(pyparsing.CharsNotIn('\n'))
keywords = {'order by': pyparsing.Keyword('order', caseless=True) + pyparsing.Keyword('by', caseless=True), 
   'select': pyparsing.Keyword('select', caseless=True), 
   'from': pyparsing.Keyword('from', caseless=True), 
   'having': pyparsing.Keyword('having', caseless=True), 
   'update': pyparsing.Keyword('update', caseless=True), 
   'set': pyparsing.Keyword('set', caseless=True), 
   'delete': pyparsing.Keyword('delete', caseless=True), 
   'insert into': pyparsing.Keyword('insert', caseless=True) + pyparsing.Keyword('into', caseless=True), 
   'values': pyparsing.Keyword('values', caseless=True), 
   'group by': pyparsing.Keyword('group', caseless=True) + pyparsing.Keyword('by', caseless=True), 
   'where': pyparsing.Keyword('where', caseless=True)}
for name, parser in keywords.items():
    parser.ignore(pyparsing.sglQuotedString)
    parser.ignore(pyparsing.dblQuotedString)
    parser.ignore(pyparsing.cStyleComment)
    parser.ignore(sqlStyleComment)
    parser.name = name

fromClauseFinder = re.compile('.*(from|update)(.*)(where|set)', re.IGNORECASE | re.DOTALL | re.MULTILINE)
oracleTerms = oracleTerms = re.compile('[A-Z$_#][0-9A-Z_$#]*', re.IGNORECASE)

def tableNamesFromFromClause(statement):
    result = fromClauseFinder.search(statement)
    if not result:
        return []
    result = oracleTerms.findall(result.group(2))
    result = [ r.upper() for r in result if r.upper() not in ('JOIN', 'ON') ]
    return result


def orderedParseResults(parsers, statement):
    results = []
    for parser in parsers:
        results.extend(parser.scanString(statement))

    results.sort(cmp=lambda x, y: cmp(x[1], y[1]))
    return results


at_beginning = re.compile('^\\s*\\S+$')

def whichSegment(statement):
    """
    >>> whichSegment("SELECT col FROM t")
    'from'
    >>> whichSegment("SELECT * FROM t")
    'from'
    >>> whichSegment("DESC ")
    'DESC'
    >>> whichSegment("DES")
    'beginning'
    >>> whichSegment("")
    'beginning'
    >>> whichSegment("select  ")
    'select'
    
    """
    if not statement or at_beginning.search(statement):
        return 'beginning'
    results = orderedParseResults(keywords.values(), statement)
    if results:
        return (' ').join(results[(-1)][0])
    else:
        return statement.split(None, 1)[0]
        return


reserved = ('\n      access\n     add\n     all\n     alter\n     and\n     any\n     as\n     asc\n     audit\n     between\n     by\n     char\n     check\n     cluster\n     column\n     comment\n     compress\n     connect\n     create\n     current\n     date\n     decimal\n     default\n     delete\n     desc\n     distinct\n     drop\n     else\n     exclusive\n     exists\n     file\n     float\n     for\n     from\n     grant\n     group\n     having\n     identified\n     immediate\n     in\n     increment\n     index\n     initial\n     insert\n     integer\n     intersect\n     into\n     is\n     level\n     like\n     lock\n     long\n     maxextents\n     minus\n     mlslabel\n     mode\n     modify\n     noaudit\n     nocompress\n     not\n     nowait\n     null\n     number\n     of\n     offline\n     on\n     online\n     option\n     or\n     order\n     pctfree\n     prior\n     privileges\n     public\n     raw\n     rename\n     resource\n     revoke\n     row\n     rowid\n     rownum\n     rows\n     select\n     session\n     set\n     share\n     size\n     smallint\n     start\n     successful\n     synonym\n     sysdate\n     table\n     then\n     to\n     trigger\n     uid\n     union\n     unique\n     update\n     user\n     validate\n     values\n     varchar\n     varchar2\n     view\n     whenever\n     where\n     with ').split()
if __name__ == '__main__':
    doctest.testmod()