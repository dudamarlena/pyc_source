# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/autocomp/pycomp.py
# Compiled at: 2012-03-17 12:57:51
"""
Provides completion and calltip support for python documents. To provide the
completion lists and calltips a mix of parsing and introspection is used to
deduct the requested information.

@summary: Python autocompletion support

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__cvsid__ = '$Id: pycomp.py 70229 2012-01-01 01:27:10Z CJP $'
__revision__ = '$Revision: 70229 $'
import os, sys, time, tokenize, types
from token import NAME, DEDENT, STRING
import wx
from wx.py import introspect
from StringIO import StringIO
import completer

class Completer(completer.BaseCompleter):
    """Python Code completion provider"""

    def __init__(self, stc_buffer):
        """Initializes the completer
        @param stc_buffer: buffer that contains code

        """
        super(Completer, self).__init__(stc_buffer)
        self.SetAutoCompKeys([ord('.')])
        self.SetAutoCompStops(' \'"\\`):')
        self.SetAutoCompFillups('.,;([]}<>%^&+-=*/|')
        self.SetCallTipKeys([ord('(')])
        self.SetCallTipCancel([ord(')'), wx.WXK_RETURN])
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '>>>'

        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = '...'

    def _GetCompletionInfo(self, command, calltip=False):
        """Get Completion list or Calltip
        @return: list or string

        """
        if command is None or len(command) and command[0].isdigit():
            if calltip:
                return ''
            return list()
        else:
            try:
                cmpl = PyCompleter()
                fname = self._buffer.GetFileName()
                if fname:
                    fpath = os.path.dirname(fname)
                    sys.path.insert(0, fpath)
                snapshot = list(sys.modules.keys())
                t1 = time.time()
                cmpl.evalsource(self._buffer.GetText(), self._buffer.GetCurrentLine())
                dbg('[pycomp][info] Completion eval time: %f' % (time.time() - t1))
                if fname:
                    sys.path.pop(0)
                nsnapshot = sys.modules.keys()
                nimport = list(set(nsnapshot).difference(set(snapshot)))
                for k in nimport:
                    del sys.modules[k]

                if calltip:
                    return cmpl.get_completions(command + '(', '', calltip)
                complst = cmpl.get_completions(command)
                sigs = list()
                tmap = {'function': completer.TYPE_FUNCTION, 'method': completer.TYPE_METHOD, 
                   'class': completer.TYPE_CLASS, 
                   'attribute': completer.TYPE_ATTRIBUTE, 
                   'property': completer.TYPE_PROPERTY}
                for sig in complst:
                    word = sig['word'].rstrip('(.')
                    tval = tmap.get(sig['type'], completer.TYPE_UNKNOWN)
                    sigs.append(completer.Symbol(word, tval))

                sigs.sort(key=lambda x: x.Name.upper())
                return sigs
            except BaseException, msg:
                self._log('[pycomp][err] _GetCompletionInfo: %s, %s' % (
                 sys.exc_info()[0], sys.exc_info()[1]))
                if calltip:
                    return ''
                return list()

            return

    def GetAutoCompList(self, command):
        """Returns the list of possible completions for a command string.
        @param command: command lookup is done on

        """
        return self._GetCompletionInfo(command)

    def GetCallTip(self, command):
        """Returns the formatted calltip string for the command.
        @param command: command to get calltip for

        """
        alltext = self._GetCompletionInfo(command, calltip=True)
        paratext = alltext.split('\n\n')
        textlimit = 800
        if len(paratext[0]) < textlimit:
            numpara = len(paratext)
            calltiptext = paratext[0]
            ii = 1
            while ii < numpara and len(calltiptext) + len(paratext[ii]) < textlimit:
                calltiptext = calltiptext + '\n\n' + paratext[ii]
                ii = ii + 1

            if ii < numpara:
                calltiptext = calltiptext + '\n[...]'
        else:
            calltiptext = alltext.split('\n')[0]
        if type(calltiptext) != types.UnicodeType:
            try:
                stcbuff = self.GetBuffer()
                encoding = stcbuff.GetEncoding()
                calltiptext = calltiptext.decode(encoding)
            except Exception, msg:
                dbg('%s' % msg)

        return calltiptext


def dbg(msg):
    wx.GetApp().GetLog()(msg)


class PyCompleter(object):
    """Python code completion provider"""

    def __init__(self):
        self.compldict = {}
        self.parser = PyParser()

    def evalsource(self, text, line=0):
        """Evaluate source for introspection
        @param text: Text to evaluate
        @keyword line: current line of cursor

        """
        scope = self.parser.parse(text.replace('\r\n', '\n'), line)
        src = scope.get_code()
        try:
            exec src in self.compldict
        except Exception, msg:
            dbg('[pycomp][err] src exec: %s' % msg)
        else:
            dbg('[pycomp][info] Successfully executed source code')

        for loc in [ l[1] for l in scope.locals ]:
            try:
                exec loc in self.compldict
            except Exception, msg:
                dbg('[pycomp][err] local exec %s [%s]' % (msg, loc))
            else:
                dbg('[pycomp][info] Successfully executed: %s' % loc)

    def get_arguments(self, func_obj):
        """Get the arguments of a given function obj
        @param func_obj: function object to get parameters for

        """

        def _ctor(obj):
            """Get the constructor for an object"""
            try:
                return obj.__init__.im_func
            except AttributeError:
                for base in obj.__bases__:
                    constructor = getattr(base, '__init__', None)
                    if constructor is not None:
                        return constructor

            return

        arg_offset = 1
        if type(func_obj) == types.ClassType:
            func_obj = _ctor(func_obj)
        elif type(func_obj) == types.MethodType:
            func_obj = func_obj.im_func
        else:
            arg_offset = 0
        arg_text = ''
        if type(func_obj) in [types.FunctionType, types.LambdaType]:
            try:
                fcode = func_obj.func_code
                real_args = fcode.co_varnames[arg_offset:fcode.co_argcount]
                defaults = func_obj.func_defaults or ''
                defaults = [ '=%s' % name for name in defaults ]
                defaults = [''] * (len(real_args) - len(defaults)) + defaults
                items = [ arg + default for (arg, default) in zip(real_args, defaults)
                        ]
                if fcode.co_flags & 4:
                    items.append('...')
                if fcode.co_flags & 8:
                    items.append('***')
                arg_text = (',').join(items) + ')'
            except Exception, msg:
                dbg('[pycomp][err] get_arguments: %s' % msg)

        if len(arg_text) == 0:
            doc = getattr(func_obj, '__doc__', False)
            if doc:
                doc = str(doc)
                doc = doc.lstrip()
                pos = doc.find('\n')
                if pos > 0:
                    sigline = doc[:pos]
                    lidx = sigline.find('(')
                    ridx = sigline.find(')')
                    if lidx > 0 and ridx > 0:
                        arg_text = sigline[lidx + 1:ridx] + ')'
        if len(arg_text) == 0:
            arg_text = ')'
        return arg_text

    def get_completions(self, context, match='', ctip=False):
        """Get the completions for the given context
        @param context: command string to get completions for
        @keyword match: for matching an incomplete command string
        @keyword ctip: Get a calltip for the context instead of completion list
        @return: list of dictionaries

        """
        dbg("[pycomp] get_completions('%s','%s')" % (context, match))
        stmt = context + match
        try:
            result = None
            compdict = {}
            ridx = stmt.rfind('.')
            if len(stmt) > 0 and stmt[(-1)] == '(':
                if ctip:
                    tip = introspect.getCallTip(_sanitize(stmt), self.compldict)[2]
                    if not isinstance(tip, basestring):
                        tip = ''
                    if not tip:
                        result = eval(_sanitize(stmt.rstrip('(')), self.compldict)
                        doc = max(getattr(result, '__doc__', ''), ' ')
                        argval = context + _cleanstr(self.get_arguments(result))
                        tip = ('\n').join([argval, _cleanstr(doc)])
                        dbg('[pycomp][info] Used internal calltips')
                    return tip
            elif ridx == -1:
                match = stmt
                compdict = self.compldict
            else:
                match = stmt[ridx + 1:]
                stmt = _sanitize(stmt[:ridx])
                result = eval(stmt, self.compldict)
                compdict = dir(result)
            dbg('[pycomp] completing: stmt:%s' % stmt)
            completions = []
            isdict = isinstance(compdict, dict)
            for meth in compdict:
                if meth == '_PyCmplNoType':
                    continue
                try:
                    if meth.find(match) == 0:
                        if result is None:
                            inst = meth
                        else:
                            inst = getattr(result, meth, None)
                        if len(dir(inst)):
                            doc = getattr(inst, '__doc__', None)
                            if doc is None:
                                doc = max(getattr(result, '__doc__', ' '), ' ')
                        else:
                            doc = ' '
                        if isdict:
                            typestr = str(compdict[inst])
                        else:
                            typestr = str(inst)
                        comp = {'word': meth, 'abbr': meth, 
                           'info': _cleanstr(str(doc)), 
                           'type': typestr}
                        if 'function' in typestr:
                            comp['word'] += '('
                            comp['abbr'] += '(' + _cleanstr(self.get_arguments(inst))
                            comp['type'] = 'function'
                        elif 'method' in typestr or 'slot wrapper' in typestr:
                            comp['word'] += '('
                            comp['abbr'] += '(' + _cleanstr(self.get_arguments(inst))
                            comp['type'] = 'method'
                        elif 'module' in typestr:
                            comp['word'] += '.'
                            comp['type'] = 'module'
                        elif 'class' in typestr:
                            comp['word'] += '('
                            comp['abbr'] += '('
                            comp['type'] = 'class'
                        elif 'attribute' in typestr or not typestr.startswith('__') and not typestr.startswith('<'):
                            comp['type'] = 'attribute'
                        elif 'property' in typestr:
                            comp['type'] = 'property'
                        completions.append(comp)
                except Exception, msg:
                    dbg("[pycomp][err] inner completion: %s [stmt='%s']:" % (msg, stmt))

            return completions
        except Exception, msg:
            dbg("[pycomp][err] get_completions: %s [stmt='%s']" % (msg, stmt))
            if ctip:
                return ''
            return list()

        return


class Scope(object):
    """Base class for representing code objects"""

    def __init__(self, name, indent):
        """Initialize the scope
        @param name: name of this object
        @param indent: the indentation/level of this scope

        """
        super(Scope, self).__init__()
        self.subscopes = list()
        self.docstr = ''
        self.locals = list()
        self.parent = None
        self.name = name
        self.indent = indent
        self.objid = -1
        return

    DocStr = property(lambda self: self.docstr, lambda self, dstr: setattr(self, 'docstr', dstr))
    Locals = property(lambda self: self.locals, lambda self, loc: setattr(self, 'locals', loc))
    Parent = property(lambda self: self.parent, lambda self, parent: setattr(self, 'parent', parent))

    def Clone(self, indent=0):
        """Clone this scope object"""
        obj = Scope(self.name, indent)
        obj.DocStr = self.DocStr
        obj.Locals = list(self.Locals)
        obj.Parent = self.Parent
        for scope in self.subscopes:
            obj.subscopes.append((scope[0], scope[1].Clone(indent + 1)))

        obj.objid = self.objid
        return obj

    def NextObjId(self):
        self.objid += 1
        return self.objid

    def add(self, sub):
        """Push a subscope into this scope
        @param sub: sub scope to push

        """
        sub.parent = self
        self.subscopes.append((self.NextObjId(), sub))
        return sub

    def doc(self, docstr):
        """Format and set the doc string for this scope
        @param docstr: Docstring to format and set

        """
        dstr = docstr
        if len(dstr):
            while len(dstr) and dstr[0] in '"\' ':
                dstr = dstr[1:]

            while len(dstr) and dstr[(-1)] in '"\' ':
                dstr = dstr[:-1]

        dstr = ('\n').join([ d.lstrip() for d in dstr.split('\n') ])
        self.docstr = dstr.rstrip()

    def local(self, loc):
        """Add an object to the scopes locals
        @param loc: local object to add to locals

        """
        self._checkexisting(loc)
        self.locals.append((self.NextObjId(), loc))

    def _checkexisting(self, test):
        """Convenience function... keep out duplicates
        @param test: assignment statement to check for existence of
                     variable in the scopes locals

        """
        if '=' in test:
            var = test.split('=')[0].strip()
            for loc in self.locals:
                if '=' in loc[1] and var == loc[1].split('=')[0].strip():
                    self.locals.remove(loc)

    def get_code(self):
        """Get a string of code that represents this scope
        @return: string

        """
        cstr = '"""' + self.docstr + '"""\n'
        nonimport = list()
        for loc in self.locals:
            if loc[1].startswith('import') or loc[1].startswith('from'):
                cstr += 'try:\n    %s\nexcept ImportError:\n    pass\n' % loc[1]
            else:
                nonimport.append(loc)

        cstr += 'class _PyCmplNoType:\n    def __getattr__(self,name):\n        return None\n'
        decls = self.subscopes + nonimport
        decls.sort(key=lambda x: x[0])
        for decl in [ d[1] for d in decls ]:
            if isinstance(decl, Scope):
                cstr += decl.get_code()
            else:
                cstr += decl + '\n'

        return cstr

    def pop(self, indent):
        """Pop the scope until it is at the level of the given
        indent.
        @param indent: indent level to pop scope to
        @return: scope of given indent level

        """
        outer = self
        while outer.parent != None and outer.indent >= indent:
            outer = outer.parent

        return outer

    def currentindent(self):
        """Return string of current scopes indent level
        @return: string of spaces

        """
        return '    ' * self.indent

    def childindent(self):
        """Return string the next scopes indentation level
        @return: string of spaces

        """
        return '    ' * (self.indent + 1)


class Class(Scope):
    """Class for representing a python class object for the parser"""

    def __init__(self, name, supers, indent):
        """initialize the class object
        @param name: name of class
        @param supers: classes super classes
        @param indent: scope of indentation

        """
        super(Class, self).__init__(name, indent)
        self.supers = supers

    def Clone(self, indent=0):
        """Create a clone of this object"""
        obj = Class(self.name, self.supers, indent)
        obj.DocStr = self.DocStr
        obj.Locals = list(self.Locals)
        obj.Parent = self.Parent
        obj.objid = self.objid
        for scope in self.subscopes:
            obj.subscopes.append((scope[0], scope[1].Clone(indent + 1)))

        return obj

    def get_code(self):
        """Get the code string representation of the Class object
        @return: string

        """
        cstr = '%sclass %s' % (self.currentindent(), self.name)
        if len(self.supers) > 0:
            cstr += '(%s)' % (',').join(self.supers)
        cstr += ':\n'
        if len(self.docstr) > 0:
            cstr += self.childindent() + '"""' + self.docstr + '"""\n'
        need_pass = True
        decls = self.locals + self.subscopes
        decls.sort(key=lambda x: x[0])
        for decl in [ d[1] for d in decls ]:
            need_pass = False
            if isinstance(decl, Scope):
                cstr += decl.get_code()
            else:
                cstr += '%s%s\n' % (self.childindent(), decl)

        if need_pass:
            cstr += '%spass\n' % self.childindent()
        return cstr

    def local(self, loc):
        """Add an object to the scopes locals
        @param loc: local object to add to locals

        """
        if loc and '.' not in loc:
            super(Class, self).local(loc)


class Function(Scope):
    """Create a function object for representing a python function
    definition in the parser.

    """

    def __init__(self, name, params, indent):
        """Create the function object
        @param name: name of function
        @param params: the functions parameters
        @param indent: indentation level of functions declaration (scope)

        """
        super(Function, self).__init__(name, indent)
        self.params = params

    def Clone(self, indent=0):
        """Create a copy of the functions declaration at the given
        scope of indentation.
        @keyword indent: indentation level of the declaration

        """
        obj = Function(self.name, self.params, indent)
        obj.DocStr = self.DocStr
        obj.Locals = list(self.Locals)
        obj.Parent = self.Parent
        for scope in self.subscopes:
            obj.subscopes.append((scope[0], scope[1].Clone(indent + 1)))

        obj.objid = self.objid
        return obj

    def get_code(self):
        """Get code string representation of the function object
        @return: string

        """
        cstr = '%sdef %s(%s):\n' % (
         self.currentindent(), self.name, (',').join(self.params))
        if len(self.docstr) > 0:
            cstr += self.childindent() + '"""' + self.docstr + '"""\n'
        cstr += '%spass\n' % self.childindent()
        return cstr


class PyParser(object):
    """Python parsing class"""

    def __init__(self):
        """Initialize and create the PyParser"""
        super(PyParser, self).__init__()
        self.top = Scope('global', 0)
        self.scope = self.top
        self.gen = None
        self.curline = 0
        self.currentscope = None
        return

    def _parsedotname(self, pre=None):
        """Parse a dotted name string
        @return: tuple of (dottedname, nexttoken)

        """
        name = list()
        if pre is None:
            (tokentype, token) = self.next()[:2]
            if token == '(':
                self._parenparse()
            if tokentype != NAME and token != '*':
                return ('', token)
        else:
            token = pre
        name.append(token)
        while True:
            (tokentype, token) = self.next()[:2]
            if token == '(':
                self._parenparse()
                break
            if token != '.':
                break
            (tokentype, token) = self.next()[:2]
            if tokentype != NAME:
                break
            name.append(token)

        return (
         ('.').join(name), token)

    def _parseimportlist(self):
        """Parse and collect import statements
        @return: list of imports

        """
        imports = []
        while True:
            (name, token) = self._parsedotname()
            if not name:
                break
            name2 = ''
            if token == 'as':
                (name2, token) = self._parsedotname()
            imports.append((name, name2))
            while token != ',' and '\n' not in token:
                token = self.next()[1]

            if token != ',':
                break

        return imports

    def _parenparse(self):
        """Parse paren enclosed statement
        @return: list of named items enclosed in the parens

        """
        name = ''
        names = []
        level = 1
        while True:
            token = self.next()[1]
            if token in (')', ',') and level == 1:
                if '=' in name:
                    name = name.split('=')[0].strip()
                names.append(name)
                name = ''
            if token == '(':
                level += 1
            elif token == ')':
                level -= 1
                if level == 0:
                    break
            elif token == ',' and level == 1:
                pass
            else:
                name += str(token)

        return names

    def _parsefunction(self, indent):
        """Parse a function definition at the given scope of
        indentation and create a class token object from the
        results.
        @param indent: scope of functions declaration

        """
        self.scope = self.scope.pop(indent)
        (tokentype, fname, findent) = self.next()
        if tokentype != NAME:
            return None
        else:
            (tokentype, open_paren, tindent) = self.next()
            if open_paren != '(':
                return None
            params = self._parenparse()
            (tokentype, colon, tindent) = self.next()
            if colon != ':':
                return None
            return Function(fname, params, indent)

    def _parseclass(self, indent):
        """Parse a class definition at the given scope of
        indentation and create a class token object from the
        results.
        @param indent: scope of classes declaration

        """
        self.scope = self.scope.pop(indent)
        (tokentype, cname) = self.next()[:-1]
        if tokentype != NAME:
            return None
        else:
            super_cls = []
            (tokentype, next) = self.next()[:-1]
            if next == '(':
                super_cls = self._parenparse()
            elif next != ':':
                return None
            return Class(cname, super_cls, indent)

    def _parseassignment(self):
        """Parse a variable assignment to resolve the variables type
        for introspection.
        @return: string of objects type

        """
        assign = ''
        (tokentype, token) = self.next()[:-1]
        tokens = {'{': '{}', 
           'dict': '{}', 'locals': '{}', 
           'globals': '{}', 'open': 'file', 
           'file': 'file', '[': '[]', 
           'list': '[]', 'dir': '["",""]', 
           'zip': '[]', 'map': '[]', 'sorted': '[]', 
           'range': '[]', 'None': '_PyCmplNoType()', 
           tokenize.NUMBER: '0', 
           'ord': '0', 'id': '0', 'abs': '0', 
           'sum': '0', 'pow': '0', 'len': '0', 'hash': '0', 
           'property': 'property()', 
           tokenize.STRING: '""', 
           'str': '""', 'repr': '""', 
           'chr': '""', 'unichr': '""', 'hex': '""', 
           'oct': '""', "'": '""', '"': '""', 'type': 'type(_PyCmplNoType)', 
           '(': '()', 
           'tuple': '()', 'coerce': '()'}
        if tokentype == tokenize.NUMBER or tokentype == tokenize.STRING:
            return token
        else:
            if token in tokens:
                return tokens[token]
            assign += token
            level = 0
            while True:
                (tokentype, token) = self.next()[:-1]
                if token in ('(', '{', '['):
                    level = level + 1
                elif token in (']', '}', ')'):
                    level = level - 1
                    if level == 0 or level == -1:
                        break
                elif level == 0:
                    if token in (';', '\n', '='):
                        break
                    elif token in ('+', '*'):
                        if assign.endswith('"') or assign.endswith("'"):
                            assign = '""'
                        else:
                            assign = '0'
                        break
                    elif token in ('/', '-'):
                        assign = '0'
                        break
                    elif token in ('and', 'or', 'in', '==', '<', '>', '!=', 'not',
                                   '>=', '<='):
                        assign = 'bool'
                        break
                    elif token == '.' or assign.endswith('.'):
                        assign += token
                    else:
                        assign += ' %s' % token

            try:
                compile(assign, '_pycomp', 'eval')
            except:
                dbg('[pycomp][err] parseassignment bad token: %s' % assign)
                return '_PyCmplNoType()'

            return assign

    def next(self):
        """Get tokens of next line in parse
        @return: tuple of (type, token, indent)

        """
        (ttype, token, (lineno, indent)) = self.gen.next()[:3]
        if lineno == self.curline:
            self.currentscope = self.scope
        return (
         ttype, token, indent)

    def _adjustvisibility(self):
        """Adjust the visibility of the current contexts scope
        @return: current scope

        """
        newscope = Scope('result', 0)
        scopes = list()
        tscp = self.currentscope.parent
        while tscp != None:
            scopes.append(tscp)
            tscp = tscp.parent

        scopes.append(self.currentscope)
        for scp in scopes:
            if type(scp) == Function:
                cut = 0
                if scp.parent != None and type(scp.parent) == Class:
                    cut = 1
                    params = scp.params[0]
                    ind = params.find('=')
                    if ind != -1:
                        params = params[:ind]
                    newscope.local('%s = %s' % (_sanitizeParam(scp.params[0]), scp.parent.name))
                for param in scp.params[cut:]:
                    ind = param.find('=')
                    if len(param) == 0:
                        continue
                    if ind == -1:
                        newscope.local('%s = _PyCmplNoType()' % _sanitizeParam(param))
                    else:
                        newscope.local('%s = %s' % (_sanitizeParam(param[:ind]),
                         _sanitize(param[ind + 1:])))

            decls = scp.subscopes + scp.locals
            decls.sort(key=lambda x: x[0])
            for decl in [ d[1] for d in decls ]:
                if isinstance(decl, Scope):
                    newscope.add(decl.Clone(0))
                else:
                    newscope.local(decl)

        self.currentscope = newscope
        return self.currentscope

    def parse(self, text, curline=0):
        """Parse the given text
        @param text: python code text to parse
        @keyword curline: current line of cursor for context

        """
        self.curline = curline
        buf = StringIO(text)
        self.gen = tokenize.generate_tokens(buf.readline)
        self.currentscope = self.scope
        try:
            freshscope = True
            while True:
                (tokentype, token, indent) = self.next()
                if tokentype == DEDENT or token == 'pass':
                    self.scope = self.scope.pop(indent)
                elif token == 'def':
                    func = self._parsefunction(indent)
                    if func == None:
                        continue
                    freshscope = True
                    self.scope = self.scope.add(func)
                elif token == 'class':
                    cls = self._parseclass(indent)
                    if cls == None:
                        continue
                    freshscope = True
                    self.scope = self.scope.add(cls)
                elif token == 'import':
                    imports = self._parseimportlist()
                    for (mod, alias) in imports:
                        loc = 'import %s' % mod
                        if len(alias) > 0:
                            loc += ' as %s' % alias
                        self.scope.local(loc)

                    freshscope = False
                elif token == 'from':
                    (mod, token) = self._parsedotname()
                    if not mod or token != 'import':
                        continue
                    names = self._parseimportlist()
                    for (name, alias) in names:
                        loc = 'from %s import %s' % (mod, name)
                        if len(alias) > 0:
                            loc += ' as %s' % alias
                        self.scope.local(loc)

                    freshscope = False
                elif tokentype == STRING:
                    if freshscope:
                        self.scope.doc(token)
                elif tokentype == NAME:
                    (name, token) = self._parsedotname(token)
                    if token == '=':
                        stmt = self._parseassignment()
                        dbg('[pycomp] parseassignment: %s = %s' % (name, stmt))
                        if stmt != None:
                            if '.' not in name or name.startswith('self.'):
                                self.scope.local('%s = %s' % (name, stmt))
                    freshscope = False

        except StopIteration:
            pass
        except:
            dbg('[pycomp][err] Pyparser.parse: %s, %s' % (
             sys.exc_info()[0], sys.exc_info()[1]))

        return self._adjustvisibility()


def _cleanstr(doc):
    """Clean up a docstring by removing quotes
    @param doc: docstring to clean up

    """
    return doc.replace('"', ' ').replace("'", ' ')


def _sanitize(cstr):
    """Sanitize a command string for namespace lookup
    @param cstr: command string to cleanup

    """
    val = ''
    level = 0
    for char in cstr:
        if char in ('(', '{', '['):
            level += 1
        elif char in (']', '}', ')'):
            level -= 1
        elif level == 0:
            val += char

    return val


def _sanitizeParam(param):
    """Cleanup a value string
    value = foo
    to ensure that 'value' is syntactically correct.

    """
    for (i, c) in enumerate(param):
        if c.isalpha() or c == '_':
            return param[i:]
    else:
        return param