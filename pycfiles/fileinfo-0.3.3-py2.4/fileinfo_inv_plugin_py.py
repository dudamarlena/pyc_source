# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_py.py
# Compiled at: 2009-05-07 08:09:29
"""A fileinfo plug-in for Python source files.
"""
import tokenize, cStringIO, keyword, re, operator
from tokenize import NAME, NEWLINE, NL, COMMENT, STRING, OP, INDENT
from fileinfo.compatibility import *
from fileinfo.investigator import BaseInvestigator

def countStaticImportStatements(toks):
    """Count static import statements in sequence of Python tokens."""
    stmts = []
    stmt = []
    currKw = None
    for tokEntry in toks:
        (code, tok, start, end, line) = tokEntry
        if code == NAME and tok in ('from', 'import'):
            if currKw == None:
                stmt = []
            currKw = tok
            stmt.append(tok)
        elif code == NEWLINE and tok == '\n':
            if currKw != None:
                stmts.append(stmt)
                stmt = []
            currKw = None
        elif currKw != None:
            stmt.append(tok)

    if stmt:
        stmts.append(stmt)
    return stmts


def countImportedSources(toks):
    """Count imported symbols from Python tokens."""
    stmts = countStaticImportStatements(toks)
    for s in stmts:
        if s[0] == 'import':
            while True:
                try:
                    pos = s.index('as')
                except ValueError:
                    break

                del s[pos:pos + 2]

    imports = [ s[1:] for s in stmts if s[0] == 'import' ]
    froms = [ s[1:s.index('import')] for s in stmts if s[0] == 'from' ]
    imports = [ ('').join(i) for i in imports ]
    imports = [ i.split(',') for i in imports ]
    imports = reduce(operator.add, imports, [])
    froms = [ ('').join(i) for i in froms ]
    all = imports + froms
    return set(all)


def countDocstrings(toks, verbose=False):
    """Count docstrings in Python code tokens."""
    docstrings = []
    i = 0
    while i < len(toks):
        (code, tok, start, end, line) = toks[i]
        i += 1
        if code in (COMMENT, NL):
            continue
        elif code == STRING:
            docstrings.append(tok)
            while i < len(toks):
                (code, tok, start, end, line) = toks[i]
                i += 1
                if code == STRING:
                    docstrings[(-1)] += tok
                else:
                    break

            break
        else:
            break

    j = i
    for kw in ('class', 'def'):
        i = j
        while i < len(toks):
            (code, tok, start, end, line) = toks[i]
            if code == NAME and tok == kw:
                if verbose:
                    print toks[i]
                column = start[1]
                i += 1
                while i < len(toks):
                    (code, tok, start, end, line) = toks[i]
                    if code == OP and tok == ':':
                        if verbose:
                            print toks[i]
                        i += 1
                        while i < len(toks):
                            (code, tok, start, end, line) = toks[i]
                            i += 1
                            if code in (NEWLINE, INDENT, COMMENT):
                                continue
                            elif code == STRING:
                                if verbose:
                                    print toks[i]
                                docstrings.append(tok)
                                while i < len(toks):
                                    (code, tok, start, end, line) = toks[i]
                                    i += 1
                                    if code == STRING:
                                        docstrings[(-1)] += tok
                                    else:
                                        break

                                break
                            else:
                                break

                        break
                    i += 1

            i += 1

    return docstrings


class PyInvestigator(BaseInvestigator):
    """A class for determining attributes of TrueType files."""
    __module__ = __name__
    attrMap = {'bang': 'getBangLine', 'nclasses': 'getNumClasses', 'ndefs': 'getNumDefs', 'nops': 'getNumOps', 'ndecs': 'getNumDecorators', 'decs': 'getDecorators', 'ncomments': 'getNumComments', 'nstrs': 'getNumStrings', 'ndocstrs': 'getNumDocstrings', 'nkws': 'getNumKeywords', 'ndkws': 'getNumDiffkeywords', 'nimpstmts': 'getNumImportStatements', 'nimpsrcs': 'getNumImportedSources', 'impsrcs': 'getImportedSources', 'ncalls': 'getNumCalls', 'nmtlines': 'getNumEmptyLines', 'mlw': 'getMaxLineWidth', 'mil': 'getMaxIndentLevel', 'enc': 'getEncoding'}
    totals = ('nclasses', 'ndefs', 'nops', 'ncomments', 'nstrs', 'ndocstrs', 'nkws',
              'ndkws', 'nimpstmts', 'nimpsrcs', 'ncalls', 'nmtlines', 'ndecs')

    def activate(self):
        """Try activating self, setting 'active' variable."""
        self.content = open(self.path, 'rU').read()
        self.tokens = []
        gt = tokenize.generate_tokens
        try:
            self.tokens = list(gt(cStringIO.StringIO(self.content).readline))
            self.active = True
        except:
            self.active = False

        return self.active

    def getBangLine(self):
        """Return Boolean if Python file contains a slash bang line."""
        t0 = self.tokens[0]
        if t0[0] == COMMENT and t0[1].startswith('#!'):
            return True
        else:
            return False

    def getNumComments(self):
        """Return number of Python comments."""
        toks = [ t for t in self.tokens if t[0] == COMMENT ]
        return len(toks)

    def getNumClasses(self):
        """Return number of Python classes."""
        toks = [ t for t in self.tokens if t[:2] == (NAME, 'class') ]
        return len(toks)

    def getNumDefs(self):
        """Return number of Python functions or methods."""
        toks = [ t for t in self.tokens if t[:2] == (NAME, 'def') ]
        return len(toks)

    def getNumOps(self):
        """Return number of Python operators."""
        toks = [ t for t in self.tokens if t[0] == OP ]
        return len(toks)

    def getNumDecorators(self):
        """Return number of Python decorators."""
        toks = [ t for t in self.tokens if t[:2] == (OP, '@') ]
        return len(toks)

    def getDecorators(self):
        """Return sorted unique list of all Python decorators."""
        enumDecoToks = [ (i, t) for (i, t) in enumerate(self.tokens) if t[:2] == (OP, '@') ]
        decorators = []
        for (i, t) in enumDecoToks:
            deco = ''
            while True:
                i += 1
                t = self.tokens[i]
                if t[0] == NAME or t[:2] == (OP, '.'):
                    deco += t[1]
                else:
                    break

            decorators.append(deco)

        return sorted(set(decorators))

    def getNumStrings(self):
        """Return number of Python strings."""
        toks = [ t for t in self.tokens if t[0] == STRING ]
        return len(toks)

    def getNumDocstrings(self):
        """Return number of Python docstrings."""
        return len(countDocstrings(self.tokens))

    def getNumKeywords(self):
        """Return number of Python keywords."""
        kwlist = keyword.kwlist
        toks = [ t for t in self.tokens if t[0] == NAME if t[1] in kwlist ]
        return len(toks)

    def getNumDiffkeywords(self):
        """Return number of different Python keywords."""
        kwlist = keyword.kwlist
        kws = [ t[1] for t in self.tokens if t[0] == NAME if t[1] in kwlist ]
        return len(set(kws))

    def getNumImportStatements(self):
        """Return number of static Python import statements."""
        return len(countStaticImportStatements(self.tokens))

    def getNumImportedSources(self):
        """Return number of statically imported Python sources."""
        return len(countImportedSources(self.tokens))

    def getImportedSources(self):
        """Return sorted unique list of statically imported Python sources."""
        res = list(countImportedSources(self.tokens))
        res.sort()
        return res

    def getNumEmptyLines(self):
        """Return number of empty lines in Python code."""
        return len([ tok for tok in self.tokens if tok[0] == NL ])

    def getMaxLineWidth(self):
        """Return max. line width."""
        return max([ len(line) for line in self.content.split('\n') ])

    def getMaxIndentLevel(self):
        """Return max. indent level."""
        indents = [ len(tok[1]) for tok in self.tokens if tok[0] == INDENT ]
        indents = list(set(indents))
        return len(indents)

    def getEncoding(self):
        """Return file encoding."""
        pat = re.compile('# _\\*_ coding: *([\\-\\w]+) *_\\*_\n')
        for tok in self.tokens:
            if tok[0] != COMMENT:
                break
            else:
                m = pat.match(tok[1])
                if m:
                    return m.groups()[0]

        return

    def getNumCalls(self):
        """Return number of static calls."""
        toksf = [ t for (i, t) in enumerate(self.tokens) if t[0] == NAME and self.tokens[(i - 1)][1] not in ('class',
                                                                                                             'def') or t[0] in (OP, NL, NEWLINE) ]
        toksff = []
        tlast = None
        for t in toksf:
            if t[0] == NAME:
                if tlast and tlast[0] == NAME:
                    tlast = t
                    toksff[-1] = t
                else:
                    toksff.append(t)
                    tlast = t
            else:
                toksff.append(t)
                tlast = t

        tokString = ('').join([ t[1] for t in toksff ])
        pat = re.compile('([\\w\\.]+)\\(')
        calls = re.findall(pat, tokString)
        calls = [ c for c in calls if c not in keyword.kwlist ]
        return len(calls)