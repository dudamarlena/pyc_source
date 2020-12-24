# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astropysics/publication.py
# Compiled at: 2013-11-27 17:30:36
"""

============================================================
publication -- tools for preparing astronomy papers in LaTeX 
============================================================

The :mod:`publication` module contains classes and funtions to assist in
preparing papers or other publications with an emphasis on common astronomy
journals. The tools here are for use with `LaTeX
<http://www.latex-project.org/>`_ as the actual authoring tools.

.. todo:: examples

Classes and Inheritance Structure
---------------------------------

.. inheritance-diagram:: astropysics.publication
   :parts: 1

Module API
----------

"""
from __future__ import division, with_statement
import re as _re
try:
    from abc import ABCMeta
    from abc import abstractmethod
    from abc import abstractproperty
    from collections import Sequence, MutableSequence
except ImportError:
    abstractmethod = lambda x: x
    abstractproperty = property
    ABCMeta = type

    class MutableSequence(object):
        __slots__ = ('__weakref__', )


    class Sequence(object):
        __slots__ = ('__weakref__', )


_envre = _re.compile('(\\\\begin{(.*?)}(.*?)\\\\end{\\2})|(\\${1,2}.*?\\${1,2})', _re.DOTALL)
_commandstr = '\\\\(\\w.*?[*]?)((?:(?:(?:{.*?})|(?:\\[.*?\\]))+)|(?=\\W))'
_commandre = _re.compile(_commandstr)
_cmdargsepre = _re.compile('(?:}|])(?=\\s*?(?:$|{|\\[))')
_commentre = _re.compile('(?<!\\\\)%')

class TeXNode(object):
    """
    An element in the TeX parsing tree.  The main shared characteristic is
    that calling the node will return a string with the combined text.
    
    *Subclassing*
    
    Subclasses must implement :meth:`getSelfText` (see docstring for details)
    
    """
    __metaclass__ = ABCMeta
    parent = None
    children = tuple()

    def __init__(self, parent):
        self.parent = parent
        self.children = []

    @abstractmethod
    def getSelfText(self):
        """
        Subclass implementations must return a 2-tuple of strings such that the
        child text goes in between the tuple elements. Alternatively, it can
        return a 3-tuple (before,between,after), and the resulting text will be
        "<beforetext><childtext1><between><childtext2>...<after>". It can also
        be None, in which case just the strings from the children will be
        returned. Otherwise, it can return a string, which will be returned as
        the full text.
        """
        raise NotImplementedError

    def __call__(self):
        """
        Returns the text associated with this node, composed by combining 
        the self text and children text (or just the self text if 
        :meth:`getSelfText` returns a string)
        """
        st = self.getSelfText()
        if st is None:
            return ('').join([ c() for c in self.children ])
        if isinstance(st, basestring):
            return st
        else:
            if len(st) == 2:
                st1, st2 = st
                return st1 + ('').join([ c() for c in self.children ]) + st2
            if len(st) == 3:
                st1, btwn, st2 = st
                return st1 + btwn.join([ c() for c in self.children ]) + st2
            raise TypeError('Self text for node ' + str(self) + ' is invalid length')
            return

    def prune(self, prunechildren=True):
        """
        Removes this node from the tree.
        
        :param prunechildren: 
            If True, all the children of this node will be pruned (recursively).
            This is not strictly necessary, but will speed up garbage collection
            and probably prevent memory leaks. 
        """
        if self.parent is not None:
            self.parent.children.remove(self)
            self.parent = None
        if prunechildren and self.children is not None:
            for c in self.children:
                c.parent = None
                c.prune(True)

            if not self.isLeaf():
                self.children = None
        return

    def visit(self, func):
        """
        Visits all the nodes in the tree (depth-first) and calls the supplied 
        function on those nodes.  
        
        :param func: 
            The function to call on the nodes - should only accept the node as
            an argument.
            
        :returns: 
            A sequence of the return values of the function.  If the `func` 
            returns None, it is not included in the returned list.
        """
        res = func(self)
        retvals = [] if res is None else [res]
        if not self.isLeaf():
            for c in self.children:
                retvals.extend(c.visit(func))

        return retvals

    def isLeaf(self):
        """
        Returns True if this node is a leaf (has no children)
        """
        return self.children is None or len(self.children) == 0

    def isRoot(self):
        """
        Returns True if this node is a root (has no parent)
        """
        return self.parent is None


class TeXFile(TeXNode):
    """
    A TeX Document loaded from a file.
    """
    preamble = None
    document = None

    def __init__(self, fn=None, flatteninputs=False):
        self.parent = None
        self.lastsavefn = None
        self.children = []
        self._flatteninputs = flatteninputs
        if fn is not None:
            with open(fn) as (f):
                s = f.read()
            self._parse(s)
        return

    def _parse(self, f):
        """
        Parse the file - `f` can be a file object or a string w/newlines.
        """
        if hasattr(f, 'read'):
            f = f.read()
        flines = f.split('\n')
        commentcmdname = 'astppubcomment'
        i = 0
        while commentcmdname in f:
            commentcmdname = 'astppubcomment' + str(i)
            i += 1

        comments = []
        for i, l in enumerate(flines):
            commatch = _commentre.search(l)
            if commatch is not None:
                cind = commatch.start()
                flines[i] = '%s\\%s{%i}' % (l[:cind], commentcmdname, len(comments))
                comments.append(l[cind:])

        preamblecontent = []
        content = None
        for l in flines:
            if content is None:
                if '\\begin{document}' in l:
                    content = [
                     l]
                else:
                    preamblecontent.append(l)
            else:
                content.append(l)

        preamblestr = ('\n').join(preamblecontent) + '\n'
        contentstr = ('\n').join(content)
        self.preamble = Preamble(self, preamblestr)
        self.children = text_to_nodes(self, contentstr, self._flatteninputs)
        self.children.insert(0, self.preamble)
        for c in self.children:
            if isinstance(c, Document):
                self.document = c
                break

        _addin_comments(self, comments, commentcmdname)
        return

    def getSelfText(self):
        return

    def save(self, fn):
        """
        Save the content of this object to a new file.
        
        :param str fn: The name of the file to save.
        """
        with open(fn, 'w') as (f):
            f.write(self())
        self.lastsavefn = fn


def _addin_comments(node, commentlist, commentcmdname):
    todel = []
    for i, c in enumerate(node.children):
        if i < 1:
            last2 = last = None
        elif i < 2:
            last = node.children[(i - 1)]
            last2 = None
        else:
            last = node.children[(i - 1)]
            last2 = node.children[(i - 2)]
        if isinstance(last, Comment) and isinstance(c, TeXt) and c.text == '':
            todel.append(i)
        elif isinstance(last2, Comment) and isinstance(last, TeXt) and isinstance(c, Newline):
            todel.append(i)
            last2.children = (Newline(last2),)
        newnode = _addin_comments(c, commentlist, commentcmdname)
        if newnode is not None:
            node.children[i] = newnode

    for i in reversed(todel):
        del node.children[i]

    if isinstance(node, Command):
        if node.name == commentcmdname:
            return Comment(node.parent, commentlist[int(node.reqargs[0])])
    return


class TeXt(TeXNode):
    """
    A node that stores generic text. This is always a leaf.
    """
    text = ''

    def __init__(self, parent, text):
        self.parent = parent
        self.text = text

    def countWords(self, sep=None):
        """
        Returns the number of words in this object.
        
        :param sep: The seperator between words.  If None, use any whitespace.
        
        :returns: The number of words in this :class:`TeXt` object.
        """
        if sep is None:
            return len(self.text.split())
        else:
            return len(self.text.split(sep))
            return

    @property
    def children(self):
        return tuple()

    def getSelfText(self):
        return (
         self.text, '')


class Newline(TeXt):
    """
    A node that stores just a new line. This is always a leaf.
    """
    text = '\n'

    def __init__(self, parent):
        self.parent = parent


class Environment(TeXNode):
    """
    A LaTex environment.  
    
    *Subclassing*
    Subclasses can implement the :meth:`postParse` method - see the method for
    syntax. They should also be registered with the :meth:`registerEnvironment`
    static method to have them be parsed with the default :class:`TeXFile`
    parser. Generally, they should also have a class attribute named `name` that
    gives the name of the environment (this name will be automatically used to
    determine which environments the subclass represents)
    """
    name = ''

    def __init__(self, parent, content, envname=None):
        """
        :param parent: The parent node
        :param content: The string between '\x08egin{...}' and '\\end{...}'
        :param envname: 
            If a string, it will be taken as the environment name. If None, it
            will be taken from the class-level :attr:`name`
        """
        self.parent = parent
        self.children = c = []
        if envname is not None:
            self.name = envname
        elif not hasattr(self, 'name'):
            raise ValueError('Environment must have a name')
        self.children = self.postParse(text_to_nodes(self, content))
        return

    def postParse(self, nodes):
        return nodes

    def getSelfText(self):
        b = '\\begin{' + self.name + '}'
        e = '\\end{' + self.name + '}'
        return (b, e)

    _registry = {}

    @staticmethod
    def registerEnvironment(envclass):
        """
        Registers the provided `envclass` in the environment registry.  Also
        returns the class to allow use as a decorator.
        
        :param envclass: 
            The :class:`Environment` object to be registered.
        
        :except TypeError: 
            If the provided class is not a :class:`Environment` subclass. 
        :except ValueError: 
            If the :attr:`name` attribute of `envclass` matches one already in 
            the registry.
        """
        if not issubclass(envclass, Environment):
            raise TypeError('envclass must be an Environment subclass')
        if isinstance(envclass.name, basestring):
            names = [
             envclass.name]
        else:
            names = envclass.name
        for n in names:
            if n in Environment._registry:
                raise ValueError('Environment name %s already present as class %s' % (n, Environment._registry[n]))
            Environment._registry[n] = envclass

        return envclass

    @staticmethod
    def unregisterEnvironment(envclass):
        """
        Removes the `envclass` :class:`Environment` object from the registered 
        environment list
        
        :param envclass: 
            The :class:`Environment` object to be removed, or its associated
            name.
        """
        if isinstance(envclass, basestring):
            del Environment._registry[envclass]
        else:
            regclass = Environment._registry.pop(envclass.name)
            if regclass is not envclass:
                Environment._registry[envclass.name] = regclass
                raise KeyError("Environment name %s found, but doesn't match class %s" % (envclass.name, envclass))

    @staticmethod
    def getEnvironments():
        """
        Returns a tuple of the registered environments.
        """
        return tuple(Environment._registry.values())


def environment_factory(parent, texstr):
    """
    This function takes a string from a TeX document starting with '\x08egin' and 
    ending in '\\end{...}' and uses it to construct the appropriate Environment
    object.
    """
    enstart = texstr.index('{') + 1
    enend = texstr.index('}')
    envname = texstr[enstart:enend]
    content = texstr[enend + 1:texstr.rindex('\\end')]
    if envname in Environment._registry:
        envcls = Environment._registry[envname]
        return envcls(parent, content, envname)
    else:
        return Environment(parent, content, envname)


@Environment.registerEnvironment
class Document(Environment):
    name = 'document'
    abstract = None
    sections = {}

    def __init__(self, parent, content, envname=None):
        Environment.__init__(self, parent, content, envname)
        self.sections = {}
        for i, c in enumerate(self.children):
            if isinstance(c, Environment) and c.name == 'abstract':
                self.abstract = c
            elif isinstance(c, Command) and (c.name == 'section' or c.name == 'section*'):
                self.sections[c.reqargs[0]] = i


@Environment.registerEnvironment
class Figure(Environment):
    name = ['figure', 'figure*']
    filenames = tuple()

    def __init__(self, parent, content, envname=None):
        Environment.__init__(self, parent, content, envname)
        self._filecmds = filecmds = []
        for c in self.children:
            if isinstance(c, Command):
                if c.name in ('plotone', 'plottwo', 'plotfiddle', 'includegraphics'):
                    filecmds.append(c)

    def _getFilenames(self):
        fns = []
        for c in self._filecmds:
            fns.append(c.reqargs[0])
            if c.name == 'plottwo':
                fns.append(c.reqargs[1])

        return fns

    def _setFilenames(self, val):
        if len(val) != len(self._getFilenames()):
            raise ValueError('filenames input does not match number of pre-existing filenames')
        newfns = list(val)
        i = 0
        for c in self._filecmds:
            for child in c.children:
                if isinstance(child, RequiredArgument):
                    child.text = newfns[i]
                    i += 1

    filenames = property(_getFilenames, _setFilenames, doc=None)


class MathMode(TeXNode):
    """
    A math environment surrounded by $ symbols or $$ (for display mode)
    """
    name = ''
    displaymode = False

    def __init__(self, parent, content):
        """
        :param parent: The parent node
        :param content: 
            The full string (including $) or a tuple(displaymode,content) where
            `displaymode` is a bool and `content` is a string
        """
        if isinstance(content, basestring):
            if content.startswith('$$'):
                displaymode = True
                content = content[2:-2]
            elif content.startswith('$'):
                displaymode = False
                content = content[1:-1]
            else:
                raise ValueError('Tried to make MathMode object with no $')
        else:
            displaymode, content = content
        self.parent = parent
        self.displaymode = displaymode
        self.children = text_to_nodes(self, content)

    def getSelfText(self):
        msymb = '$$' if self.displaymode else '$'
        return (msymb, msymb)


class Command(TeXNode):
    """
    A LaTeX command (anything with leading backslash and possible arguments
    that isn't an environment)
    """

    def __init__(self, parent, content):
        """
        :param parent: The parent node
        :param content:  
            Either a string with the command text, or a (name,args) tuple where
            args is a sequence of strings or a string '{arg1}[oarg1]{arg2}...'
        """
        if isinstance(content, basestring):
            if not content.startswith('\\'):
                raise ValueError("Tried to make a Command that doesn't start with a backslash")
            curlyind = content.find('{')
            squareind = content.find('[')
            if curlyind == -1:
                if squareind == -1:
                    cmdname = content[1:]
                    args = ''
                else:
                    cmdname = content[1:squareind]
                    args = content[squareind:]
            elif squareind == -1:
                cmdname = content[1:curlyind]
                args = content[curlyind:]
            else:
                ind = min(curlyind, squareind)
                cmdname = content[1:ind]
                args = content[ind:]
        elif len(content) == 2:
            cmdname, args = content
        else:
            raise ValueError('Invalid content passed to Command')
        self.parent = parent
        self.name = cmdname
        self.children = argnodes = []
        if args:
            argspl = _cmdargsepre.split(args)
            if argspl[(-1)] != '':
                raise ValueError('invalid argument string in Command:"' + args + '"')
            argspl = argspl[:-1]
            for a in argspl:
                if a[0] == '{':
                    argnodes.append(RequiredArgument(self, a[1:]))
                elif a[0] == '[':
                    argnodes.append(OptionalArgument(self, a[1:]))
                else:
                    raise ValueError('invalid set of arguments ' + args)

    def _getReqargs(self):
        return [ c.text for c in self.children if isinstance(c, RequiredArgument) ]

    def _setReqargs(self, val):
        oldargs = [ c for c in self.children if isinstance(c, RequiredArgument) ]
        if len(oldargs) == len(val):
            for i, a in enumerate(oldargs):
                a.text = val[i]

        else:
            newargs = [ RequiredArgument(self, v) for v in val ]
            for a in oldargs:
                self.children.remove(a)

            self.children.extend(newargs)

    reqargs = property(_getReqargs, _setReqargs, doc='\n        A list of strings with the text of the required arguments (arguments \n        enclosed in curly braces).\n        ')

    def _getOptargs(self):
        return [ c.text for c in self.children if isinstance(c, OptionalArgument) ]

    def _setOptargs(self, val):
        oldargs = [ c for c in self.children if isinstance(c, OptionalArgument) ]
        if len(oldargs) == len(val):
            for i, a in enumerate(oldargs):
                a.text = val[i]

        else:
            newargs = [ OptionalArgument(self, v) for v in val ]
            for a in oldargs:
                self.children.remove(a)

            self.children.extend(newargs)

    optargs = property(_getOptargs, _setOptargs, doc='\n        A list of strings with the text of the optional arguments (arguments \n        enclosed in square brackets)\n        ')

    def getSelfText(self):
        args = [
         '\\', self.name]
        for c in self.children:
            if isinstance(c, RequiredArgument):
                args.append('{' + c.text + '}')
            elif isinstance(c, OptionalArgument):
                args.append('[' + c.text + ']')
            else:
                raise TypeError('Command children should be RequiredArguments or OptionalArguments')

        return ('').join(args)

    def __str__(self):
        return 'Command@%i:%s' % (id(self), self.name)


class TrailingCharCommand(Command):
    r"""
    A special command that allows a single trailing character of any type - 
    used for '\left{' '\right]' and similar.
    """
    children = tuple()

    def __init__(self, parent, content):
        """
        :param parent: The parent node
        :param conent: A (name,char) tuple, or a command string
        """
        if isinstance(content, basestring):
            if not content.startswith('\\'):
                raise ValueError("Tried to make a Command that doesn't start with a backslash")
            name = content[1:-1]
            tchar = content[(-1)]
        else:
            name, tchar = content
        self.parent = parent
        self.name = name
        self.trailingchar = tchar

    def getSelfText(self):
        return '\\' + self.name + self.trailingchar


class RequiredArgument(TeXNode):
    """
    An argument to a macro that is required (i.e. enclosed in curly braces)
    """
    children = tuple()
    text = ''

    def __init__(self, parent, text):
        self.parent = parent
        self.text = text

    def getSelfText(self):
        return self.text


class OptionalArgument(TeXNode):
    """
    An argument to a macro that is required (i.e. enclosed in square brackets)
    """
    children = tuple()

    def __init__(self, parent, text):
        self.parent = parent
        self.text = text

    def getSelfText(self):
        return self.text


class EnclosedDeclaration(TeXNode):
    r"""
    A TeX construct of the form {\name{op}[op] content}. Note that declarations
    terminated by the \end command will not be treated as this kind of object.
    """
    padstr = ''
    cmd = None

    def __init__(self, parent, content):
        """
        :param parent: The parent node
        :param content: 
            A (padstr,commandnode,innercontent) tuple where `padstr` is the
            string before the command, `commandnode` is a :class:`Command`
            object with the command portion of the declaration, and
            `innercontent` is the content after the command either as a string
            or a list of nodes (possibly mixed with strings). Alternatively, it
            can be the full text string including the outermost braces.
        """
        if isinstance(content, basestring):
            if not content.startswith('{\\'):
                raise ValueError("Tried to make enclosed declaration that does't start with {\\")
            if not content.endswith('}'):
                raise ValueError("Tried to make enclosed declaration that does't end with }")
            content = content[1:-1]
            cmdspl = _commandre.search(content)
            if cmdspl is None:
                raise ValueError('Tried to make an enclosed declaration with no enclosed command')
            padstr = content[:cmdspl.start()]
            innercontent = content[cmdspl.end():]
            cmd = Command(self, cmdspl.group(1), '')
        else:
            if len(content) != 3:
                raise ValueError('EnclosedDeclaration content tuple is not length-3')
            padstr, cmd, innercontent = content
            cmd.parent = self
        self.parent = parent
        self.padstr = padstr
        self.cmd = cmd
        if isinstance(innercontent, basestring):
            self.children = text_to_nodes(self, innercontent)
        else:
            self.children = children = []
            for e in innercontent:
                if isinstance(e, basestring):
                    children.extend(text_to_nodes(self, e))
                else:
                    e.parent = self
                    children.append(e)

        return

    def getSelfText(self):
        return (
         '{' + self.padstr + self.cmd(), '}')


class Preamble(TeXNode):
    """
    The preamble of a TeX File (i.e. everything before \x08egin{document} )
    """
    docclass = ''

    def __init__(self, parent, content):
        """
        :param parent: The parent node
        :param string content: The text of the preamble
        """
        self.parent = parent
        self.children = text_to_nodes(self, content)
        self._classcmd = None
        self.packages = []
        for c in self.children:
            if isinstance(c, Command):
                if c.name == 'documentclass':
                    self._classcmd = c
                    self.docclass = c.reqargs[0]
                    self.docclassopts = c.optargs
                if c.name == 'usepackage':
                    self.packages.append(c.reqargs[0])

        return

    def getSelfText(self):
        return

    def _getDocclass(self):
        if self._classcmd is None:
            return
        else:
            return self._classcmd.reqargs[0]
            return

    def _setDocclass(self, val):
        if self._classcmd is not None:
            assert len(self._classcmd.reqargs) == 1, 'documentclass has multiple arguments!'
            self._classcmd.reqargs = [val]
        return

    docclass = property(_getDocclass, _setDocclass, doc='\n    The document class of the tex file as a string.\n    ')

    def _getDocclassopts(self):
        assert len(self._classcmd.optargs) <= 1, 'documentclass has multiple options!'
        if len(self._classcmd.optargs) == 1:
            return self._classcmd.optargs[0]
        return ''

    def _setDocclassopts(self, val):
        if not isinstance(val, basestring):
            val = (',').join(val)
        assert len(self._classcmd.optargs) <= 1, 'documentclass has multiple options!'
        if val.strip() == '':
            self._classcmd.optargs = []
        else:
            self._classcmd.optargs = [
             val]
        for i, c in enumerate(self._classcmd.children):
            if isinstance(c, RequiredArgument):
                reqi = i
                break
        else:
            reqi = None

        if reqi != len(self._classcmd.children) - 1:
            self._classcmd.children.append(self._classcmd.children.pop(reqi))
        return

    docclassopts = property(_getDocclassopts, _setDocclassopts, doc='\n    The document class options for the tex file as a comma-seperated string.\n    ')


class Comment(TeXNode):
    """
    A single-line comment of a TeX File.  Note that unlike most 
    """
    text = ''
    children = tuple()

    def __init__(self, parent, ctext, endswithnewline=False):
        """
        :param parent: The parent node
        :param ctext: The comment text (with or without an initial %)
        """
        if len(ctext) > 0 and ctext[0] == '%':
            ctext = ctext[1:]
        self.parent = parent
        if ctext.endswith('\n'):
            self.text = ctext[:-1]
            self.children = (Newline(),)
        else:
            self.text = ctext

    def getSelfText(self):
        return ('%' + self.text, '')


def text_to_nodes(parent, txt, flatteninputs=False):
    """
    Converts a string into a list of corresponding :class:`TeXNode` objects.
    
    :param parent: The parent node
    :param txt: The text to parse
    :param bool flatteninputs: 
        If True, "include" directives will be replaced by the content if their
        referenced file.
    
    :returns: A list of :class:`TeXNode` objects
    """
    import re
    if flatteninputs:
        inclre = re.compile('\\\\input{(.*?)}')
        txts = inclre.split(txt)
        for i, fn in list(enumerate(txts))[1::2]:
            with open(fn, 'r') as (f):
                txts[i] = f.read()

        txt = ('').join(txts)
    txtnodel = []
    splitenv = _envre.split(txt)
    envstrs = splitenv[1::5]
    for i, txts in enumerate(splitenv[::5]):
        splitedcms = _commandre.split(txts)
        for j in range(0, len(splitedcms) - 1, 3):
            txtnodel.append(splitedcms[j])
            txtnodel.append(Command(parent, (splitedcms[(j + 1)], splitedcms[(j + 2)])))
            txtnodel[(-1)].origtext = splitedcms[(j + 2)]

        if len(splitedcms) > 0:
            txtnodel.append(splitedcms[(-1)])
        if i < len(envstrs):
            if envstrs[i] is not None:
                txtnodel.append(environment_factory(parent, envstrs[i]))
            else:
                txtnodel.append(MathMode(parent, splitenv[(5 * i + 4)]))

    for i in reversed(range(len(txtnodel))):
        if isinstance(txtnodel[i], Command):
            if txtnodel[i].name == 'left' and len(txtnodel[i].children) > 0:
                cmd = txtnodel[i]
                txt = cmd.origtext
                tchar = txt[0]
                tcmd = TrailingCharCommand(parent, (cmd.name, tchar))
                toins = text_to_nodes(parent, txt[1:])
                txtnodel[i] = tcmd
                insi = i + 1
                for j, e in enumerate(toins):
                    txtnodel.insert(i + j + 1, e)

                for c in txtnodel[i].children:
                    print c()

            elif txtnodel[i].name in ('left', 'right') and i < len(txtnodel) - 1 and isinstance(txtnodel[(i + 1)], basestring) and not txtnodel[(i + 1)][0].isspace():
                nm = txtnodel[i].name
                tchar = txtnodel[(i + 1)][0]
                txtnodel[i] = TrailingCharCommand(parent, (nm, tchar))
                newtxt = txtnodel[(i + 1)][1:]
                if newtxt == '':
                    del txtnodel[i + 1]
                else:
                    txtnodel[i + 1] = newtxt

    todel = []
    for i in range(1, len(txtnodel) - 1):
        if isinstance(txtnodel[i], Command) and isinstance(txtnodel[(i - 1)], basestring) and isinstance(txtnodel[(i + 1)], basestring):
            prebracket = txtnodel[(i - 1)].rstrip().endswith('{')
            postwhitespace = len(txtnodel[(i + 1)]) > 0 and txtnodel[(i + 1)][0].isspace()
            if prebracket and postwhitespace:
                cmdnode = txtnodel[i]
                nbraces = 1
                encdeccontent = []
                for j in range(1, len(txtnodel) - i):
                    txtnode = txtnodel[(i + j)]
                    if isinstance(txtnode, basestring):
                        bracescount = txtnode.count('{') - txtnode.count('}')
                        if nbraces + bracescount > 1:
                            encdeccontent.append(txtnode)
                            nbraces += bracescount
                            todel.append(i + j)
                        else:
                            for k, char in enumerate(txtnode):
                                if char == '{':
                                    nbraces += 1
                                elif char == '}':
                                    nbraces -= 1
                                if nbraces == 0:
                                    break

                            if nbraces != 0:
                                _warn('apparent EnclosedDeclaration has unbalanced braces, skipping')
                                encdeccontent = None
                                break
                            encdeccontent.append(txtnode[:k])
                            txtnodel[i + j] = txtnode[k + 1:]
                            break
                    else:
                        encdeccontent.append(txtnode)

                if encdeccontent is not None:
                    braceind = txtnodel[(i - 1)].rfind('{')
                    padstr = txtnodel[(i - 1)][braceind + 1:]
                    txtnodel[i - 1] = txtnodel[(i - 1)][:braceind]
                    txtnodel[i] = EnclosedDeclaration(parent, (padstr, cmdnode, encdeccontent))

    for i in reversed(todel):
        del txtnodel[i]

    for n in txtnodel:
        if hasattr(n, 'origtext'):
            del n.origtext

    nodel = []
    for t in txtnodel:
        if isinstance(t, basestring):
            for txt in t.split('\n'):
                nodel.append(TeXt(parent, txt))
                nodel.append(Newline(parent))

            del nodel[-1]
        elif isinstance(t, TeXNode):
            nodel.append(t)
        else:
            terrstr = 'invalid item %s returned from parsing text to nodes' % t
            raise TypeError(terrstr)

    return nodel


print_warnings = True

def _warn(*args):
    if print_warnings == 'builtin':
        from warnings import warn
        warn(*args)
    elif print_warnings:
        print 'WARNING:', args[0]


_arxiv_abstract_max_lines = 20
_arxiv_abstract_char_per_line = 80

def prep_for_arxiv_pub(texfn, newdir='pubArXiv', overwritedir=False, figexts=('eps', 'pdf'), verbose=True, flatteninputs=True):
    r"""
    Takes a LaTeX file and prepares it for posting to `arXiv
    <http://arxiv.org/>`_.  This includes the following actions:
    
        1. Removes all text after \end{document} from the .tex file
        2. Removes all comments from .tex file.
        3. Checks that the abstract is within the ArXiv line limit and issues a 
           warning if it is not (will require abridging during submission).
        4. Makes the directory for the files.
        5. Copies over all necessary .eps and/or .pdf files.
        6. Copies .bbl (or .bib if no .bbl) file if \bibliography is present.
        7. Creates the modified .tex file.
        8. Creates a .tar.gz file containing the files and places it in the 
           `newdir` directory.
           
    :param str texfn: The filename of the .tex file to be submitted. 
    :param newdir: The directory to save the publication files to.
    :param overwritedir: 
        If True the directory specified by `newdir` will be overwritten if it is
        present. Otherwise, if `newdir` is present, the directory name will be
        ``newdir_#`` where # is the first number (starting from 2) that is not
        already present as a directory.
    :param figexts:
        A sequence of strings with the file name extensions that should be
        copied over for each figure, if present.
    :param verbose: 
        If True, information will be printed when the each action is taken.
        Otherwise, only warnings will be issued when there is a problem.
    :param bool flatteninputs:
        If True, \\input sections will be replaced with their actual content
        in the final output.
    
    :returns: 
        (file,dir) where `file` is the altered :class:`TexFile` object and `dir`
        is the directory used for the publication materials.
    """
    import os, shutil, tarfile
    from contextlib import closing
    if not texfn.endswith('.tex') and os.path.exists(texfn + '.tex'):
        texfn = texfn + '.tex'
    f = TeXFile(texfn, flatteninputs=flatteninputs)
    doc = f.document
    fnodes = f.children
    docind = fnodes.index(doc)
    nnls = [ isinstance(n, Newline) for n in fnodes[docind + 1:] ].count(True)
    del fnodes[docind + 1:]
    fnodes.append(Newline(f))
    if verbose:
        print 'Stripped', nnls, 'Lines after \\end{document}'
    ncomm = len(f.visit(lambda n: n.prune() is None if isinstance(n, Comment) else None))
    if verbose:
        print 'Stripped', ncomm, 'Comments'
    if doc.abstract is not None and _arxiv_abstract_max_lines is not None:
        abstxt = doc.abstract().replace('\\begin{abstract}', '').replace('\\end{abstract}', '').strip()
        lines = []
        line = []
        wcline = -1
        for word in abstxt.split():
            if len(word) + wcline + 1 > _arxiv_abstract_char_per_line:
                lines.append((' ').join(line))
                line = []
                wcline = -1
            line.append(word)
            wcline += len(word) + 1

        if len(lines) > _arxiv_abstract_max_lines:
            _warn('Abstract is %i lines, should be <=%i' % (len(lines), _arxiv_abstract_max_lines))
        elif verbose:
            print 'Abstract within line limit'
    if newdir.endswith(os.sep):
        newdir = newdir[:-1]
    if os.path.exists(newdir):
        if not os.path.isdir(newdir):
            raise IOError(newdir + ' is a file - Aborting!')
        if overwritedir:
            if verbose:
                print 'Removing', newdir
            shutil.rmtree(newdir)
        else:
            idir = 2
            while os.path.exists(newdir + '_' + str(idir)):
                idir += 1

            newdir = newdir + '_' + str(idir)
    os.mkdir(newdir)
    filenames = []
    for figenv in f.visit(lambda n: n if isinstance(n, Figure) else None):
        filenames.extend(figenv.filenames)

    exts = tuple([ e if e.startswith('.') else '.' + e for e in figexts ])
    for fn in filenames:
        copied = False
        for ext in exts:
            fne = fn + ext
            if os.path.exists(fne):
                if verbose:
                    print 'Copying', fne, 'to', newdir + os.sep
                shutil.copy(fne, newdir)
                copied = True

        if not copied:
            _warn('File %s%s does not exist - skipping' % (fn, exts))

    bibs = f.visit(lambda n: n.reqargs[0] if isinstance(n, Command) and n.name == 'bibliography' else None)
    texfn = os.path.join(newdir, os.path.split(texfn)[(-1)])
    if not texfn.endswith('.tex'):
        texfn += '.tex'
    if verbose:
        print 'Saving', texfn
    f.save(texfn)
    bblfn = os.path.split(texfn)[(-1)][:-4] + '.bbl'
    if os.path.exists(bblfn):
        if verbose:
            print '.bbl file found - Copying', bblfn, 'to', newdir + os.sep
        shutil.copy(bblfn, newdir)
    elif len(bibs) > 1:
        _warn('No %s file and multiple \\bibliography entries found, cannot infer bibliography file - skipping bibliography' % bblfn)
    elif len(bibs) == 1:
        bibfn = bibs[0] + '.bib'
        if os.path.exists(bibfn):
            _warn('\\bibliography present, but no %s file found - copying %s instead (not recommended by arXiv)' % (bblfn, bibfn))
            shutil.copy(bibfn, newdir)
        else:
            _warn('\\bibliography present, but no %s nor %s files found - skipping bibliography' % (bblfn, bibfn))
    elif verbose:
        print 'No %s file or \\bibliography entry found - skipping bibliography' % bblfn
    tfn = os.path.join(newdir, newdir + '.tar.gz')
    if verbose:
        print 'writing file', tfn, 'with', newdir, 'contents'
    with closing(tarfile.open(tfn, 'w:gz')) as (tf):
        for fn in os.listdir(newdir):
            tf.add(os.path.join(newdir, fn), fn)

    return (
     f, newdir)


_apj_abstract_max_words = 250

def prep_for_apj_pub(texfn, newdir='pubApJ', overwritedir=False, figexts=('eps', 'pdf'), verbose=True, flatteninputs=True, emulateapj=False):
    r"""
    Takes a LaTeX file and prepares it for submission to `The Astrophysical
    Journal <http://iopscience.iop.org/0004-637X>`_. This involves the following
    actions:
    
        1. Removes all text after \end{document} from the .tex file
        2. Removes all comments from .tex file.
        3. Checks that the abstract is within the ApJ word limit and issues a
           warning if it is not.
        4. Sets the document class to aastex.
        5. Converts deluxetable* environments to deluxetable.
        6. Removes \epsscale{?} from all figures
        7. Makes the directory for the files.
        8. Renames the figures to the 'f1.eps','f2a.eps', etc. convention for
           ApJ, and copies the appropriate files over.
        9. Copies .bib (or .bbl if no .bib) file if \bibliography is present.
        10. Saves the .tex file as "ms.tex"
        11. Creates ms.tar.gz file containing the files and places it in the
            `newdir` directory.
           
    :param str texfn: The filename of the .tex file to be submitted. 
    :param newdir: The directory to save the publication files to.
    :param overwritedir: 
        If True the directory specified by `newdir` will be overwritten if it is
        present. Otherwise, if `newdir` is present, the directory name will be
        ``newdir_#`` where # is the first number (starting from 2) that is not
        already present as a directory.
    :param figexts:
        A sequence of strings with the file name extensions that should be
        copied over for each figure, if present.
    :param verbose: 
        If True, information will be printed when the each action is taken.
        Otherwise, only warnings will be issued when there is a problem.
    :param bool flatteninputs:
        If True, \\input sections will be replaced with their actual content
        in the final output.
    :param bool emulateapj:
        If True, uses the emulateapj style file instead of aastex.
    
    :returns: 
        (file,dir) where `file` is the altered :class:`TexFile` object and `dir`
        is the directory used for the publication materials.
    """
    import os, shutil, tarfile
    from contextlib import closing
    if not texfn.endswith('.tex') and os.path.exists(texfn + '.tex'):
        texfn = texfn + '.tex'
    f = TeXFile(texfn, flatteninputs=flatteninputs)
    doc = f.document
    fnodes = f.children
    docind = fnodes.index(doc)
    nnls = [ isinstance(n, Newline) for n in fnodes[docind + 1:] ].count(True)
    del fnodes[docind + 1:]
    fnodes.append(Newline(f))
    if verbose:
        print 'Stripped', nnls, 'Lines after \\end{document}'
    ncomm = len(f.visit(lambda n: n.prune() is None if isinstance(n, Comment) else None))
    if verbose:
        print 'Stripped', ncomm, 'Comments'
    if doc.abstract is not None and _apj_abstract_max_words is not None:
        wc = 0
        for c in doc.abstract.children:
            if hasattr(c, 'countWords'):
                wc += c.countWords()

        if wc > _apj_abstract_max_words:
            _warn('Abstract is %i words long, should be <=%i' % (wc, _apj_abstract_max_words))
        elif verbose:
            print 'Abstract within word limit'
    if emulateapj:
        f.preamble.docclass = 'emulateapj'
        f.preamble.docclassopts = ''
    else:
        f.preamble.docclass = 'aastex'
        f.preamble.docclassopts = 'manuscript'
    if not emulateapj:
        dts = 0
        dtlochintre = _re.compile('(\\{.*\\})(\\[.*?\\])')
        for dt in f.visit(lambda n: n if isinstance(n, Environment) and n.name == 'deluxetable*' else None):
            dts += 1
            dt.name = 'deluxetable'
            nls = [ i for i, c in enumerate(dt.children) if isinstance(c, Newline) ]
            if len(nls) > 0:
                insi = nls[0] + 1
            else:
                insi = len(nls)
            dt.children.insert(insi, Newline(dt))
            dt.children.insert(insi, Command(dt, ('rotate', [])))
            if hasattr(dt.children[0], 'text'):
                print 'in', dt.children[0].text
                m = dtlochintre.match(dt.children[0].text)
                if m is not None:
                    dt.children[0].text = m.group(1)

        if verbose:
            print 'Replaced deluxetable* with deluxetable', dts, 'times'
    if not emulateapj:
        epssrmcnt = 0
        for figenv in f.visit(lambda n: n if isinstance(n, Figure) else None):
            for c in figenv.children[:]:
                if isinstance(c, Command) and c.name == 'epsscale':
                    c.prune()
                    epssrmcnt += 1

        if verbose:
            print 'Removed epsscale', epssrmcnt, 'times'
    if newdir.endswith(os.sep):
        newdir = newdir[:-1]
    if os.path.exists(newdir):
        if not os.path.isdir(newdir):
            raise IOError(newdir + ' is a file - Aborting!')
        if overwritedir:
            if verbose:
                print 'Removing', newdir
            shutil.rmtree(newdir)
        else:
            idir = 2
            while os.path.exists(newdir + '_' + str(idir)):
                idir += 1

            newdir = newdir + '_' + str(idir)
    os.mkdir(newdir)
    filenamemap = {}
    for i, figenv in enumerate(f.visit(lambda n: n if isinstance(n, Figure) else None)):
        fignumstr = str(i + 1)
        oldfns = figenv.filenames
        if len(oldfns) == 1:
            figenv.filenames = newfns = [
             'f' + fignumstr]
        else:
            figenv.filenames = newfns = [ 'f' + fignumstr + chr(97 + i) for i in range(len(oldfns)) ]
        filenamemap.update(dict(zip(oldfns, newfns)))

    if verbose:
        print 'Figure name to number mapping:'
        maplns = []
        for k, v in filenamemap.iteritems():
            maplns.append(k + ':' + v + ',')

        print ('\n').join(maplns)
    exts = tuple([ e if e.startswith('.') else '.' + e for e in figexts ])
    for oldfn, newfn in filenamemap.iteritems():
        copied = False
        for ext in exts:
            fne = oldfn + ext
            if os.path.exists(fne):
                if verbose:
                    print 'Copying', fne, 'to', os.path.join(newdir, newfn + ext)
                shutil.copy(fne, os.path.join(newdir, newfn + ext))
                copied = True

        if not copied:
            _warn('File %s%s does not exist - skipping' % (oldfn, exts))

    bibs = f.visit(lambda n: n if isinstance(n, Command) and n.name == 'bibliography' else None)
    if len(bibs) > 1:
        _warn('Multiple \\bibliography entries found, cannot infer bibliography file - skipping bibliography')
    elif len(bibs) == 1:
        bibfn, bblfn = bibs[0].reqargs[0] + '.bib', texfn[:-4] + '.bbl'
        newbibfn = os.path.join(newdir, 'ms.bib')
        newbblfn = os.path.join(newdir, 'ms.bbl')
        bblcp = bibcl = False
        if os.path.exists(bibfn):
            if verbose:
                print 'Copying', bibfn, 'to', newbibfn
            shutil.copy(bibfn, newbibfn)
            bibcp = True
        if os.path.exists(bblfn):
            if verbose:
                print 'Copying', bibfn, 'to', newbblfn
            shutil.copy(bblfn, newbblfn)
        if not bibcp and not bblcp:
            _warn('\\bibliography present, but no .bbl or .bib files found - not copying biliography files')
        bibs[0].children[0].text = 'ms'
    elif verbose:
        print 'No \\bibliography entry found - skipping bibliography'
    if verbose:
        print 'Saving', os.path.join(newdir, 'ms.tex')
    f.save(os.path.join(newdir, 'ms.tex'))
    tfn = os.path.join(newdir, 'ms.tar.gz')
    if verbose:
        print 'writing file', tfn, 'with', newdir, 'contents'
    with closing(tarfile.open(tfn, 'w:gz')) as (tf):
        for fn in os.listdir(newdir):
            tf.add(os.path.join(newdir, fn), fn)

    return (
     f, newdir)