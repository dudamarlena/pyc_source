# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christian/Dropbox/workspace/masai/doc/sphinxext/fortran_autodoc.py
# Compiled at: 2012-11-24 14:59:46
"""Sphinx extension for autodocumenting fortran codes.

"""
from sphinx.directives import Directive
from docutils.parsers.rst.directives import unchanged
from docutils import nodes
from docutils.statemachine import string2lines
from glob import glob
from numpy.f2py.crackfortran import crackfortran, fortrantypes
import re, os, sys
from fortran_domain import FortranDomain

class F90toRstException(Exception):
    pass


class F90toRst(object):
    """Fortran 90 parser and restructeredtext formatter
    
    :Parameters:
    
         - **ffiles**: Fortran files (glob expression allowed) or dir (or list of)
         
    :Options:
    
        - **ic**: Indentation char.
        - **ulc**: Underline char for titles.
        - **sst**: Subsection type.
        - **vl**: Verbose level (0=quiet).
    """
    _re_unended_match = re.compile('(.*)&\\s*', re.I).match
    _re_unstarted_match = re.compile('\\s*&(.*)', re.I).match
    _re_comment_match = re.compile('\\s*!(.*)', re.I).match
    _re_space_prefix_match = re.compile('^(\\s*).*$', re.I).match
    _fmt_vardesc = ':%(role)s %(vtype)s %(vname)s%(vdim)s%(vattr)s: %(vdesc)s'
    _fmt_vattr = ' [%(vattr)s]'
    _fmt_fvardesc = '%(vtype)s%(vdim)s %(vattr)s%(vdesc)s'

    def __init__(self, ffiles, ic='\t', ulc='-', vl=0, encoding='utf8', sst='rubric'):
        global quiet
        global verbose
        if not isinstance(ffiles, list):
            ffiles = [
             ffiles]
        self.src = {}
        self.ffiles = ffiles
        for ff in ffiles:
            f = open(ff)
            self.src[ff] = []
            for l in f.readlines():
                try:
                    self.src[ff].append(l[:-1].decode(encoding))
                except:
                    raise F90toRstException('Encoding error\n  file = %s\n  line = %s' % (ff, l))

            f.close()

        import numpy.f2py.crackfortran
        self._verbose = numpy.f2py.crackfortran.verbose = verbose = vl
        numpy.f2py.crackfortran.quiet = quiet = 1 - verbose
        self.crack = crackfortran(ffiles)
        self.build_index()
        self.scan()
        self.build_callfrom_index()
        self.rst = {}
        self._ic = ic
        self._ulc = ulc
        self._sst = sst

    def build_index(self):
        """Register modules, functions, types and module variables for quick access
        
        Index constituents are:
        
            .. attribute:: modules
            
                Dictionary where each key is a module name, and each value is the cracked block.
                
            .. attribute:: routines
                   
                Module specific functions and subroutines
                
            .. attribute:: types
            
                Module specific types
            
            .. attribute:: variables
        
                Module specific variables
        """
        self.modules = {}
        self.types = {}
        self.routines = self.functions = self.subroutines = {}
        self.variables = {}
        self.programs = {}
        for block in self.crack:
            if block['block'] == 'module':
                module = block['name']
                self.modules[module] = block
                for subblock in block['body']:
                    if subblock['block'] in ('function', 'type', 'subroutine'):
                        container = getattr(self, subblock['block'] + 's')
                        container[subblock['name']] = subblock
                        subblock['module'] = module
                        for varname, bvar in subblock['vars'].items():
                            bvar['name'] = varname

                for bfunc in self.routines.values():
                    bfunc['aliases'] = []

                for subblock in block['body']:
                    if not subblock['block'] == 'use':
                        continue
                    for monly in block['use'].values():
                        if not monly:
                            continue
                        for fname, falias in monly['map'].items():
                            self.routines[falias] = self.routines[fname]
                            if falias not in self.routines[fname]['aliases']:
                                self.routines[fname]['aliases'].append(falias)

                for varname, bvar in block['vars'].items():
                    self.variables[varname] = bvar
                    bvar['name'] = varname
                    bvar['module'] = module

            elif block['block'] in ('function', 'subroutine', 'program'):
                container = getattr(self, block['block'] + 's')
                container[block['name']] = block
                for varname, bvar in block['vars'].items():
                    bvar['name'] = varname

        subs = [ block['name'].lower() for block in self.routines.values() if block['block'] == 'subroutine' ]
        self._re_callsub_findall = subs and re.compile('call\\s+(%s)\\b' % ('|').join(subs), re.I).findall or (lambda line: [])
        funcs = [ block['name'].lower() for block in self.routines.values() if block['block'] == 'function' ]
        self._re_callfunc_findall = funcs and re.compile('\\b(%s)\\s*\\(' % ('|').join(funcs), re.I).findall or (lambda line: [])
        for block in self.routines.values():
            vars = ('|\\b').join(block['sortvars']) + '|\\$(?P<varnum>\\d+)'
            sreg = '[\\s\\*\\-:]*(?:@param\\s*)?(?P<varname>\\b%s\\b)\\W+(?P<vardesc>.*)' % vars
            block['vardescmatch'] = re.compile(sreg).match

        for block in self.types.values() + self.modules.values() + self.routines.values():
            sreg = '\\b(?P<varname>%s)\\b[\\W\\d]*!\\s*(?P<vardesc>.*)' % ('|').join(block['sortvars'])
            if block['sortvars']:
                block['vardescsearch'] = re.compile(sreg).search
            else:
                block['vardescsearch'] = lambda x: None

    def build_callfrom_index(self):
        """For each function, index which function call it"""
        for bfunc in self.routines.values():
            bfunc['callfrom'] = []
            for bfuncall in self.routines.values() + self.programs.values():
                if bfunc['name'] in bfuncall['callto']:
                    bfunc['callfrom'].append(bfuncall['name'])

    def filter_by_srcfile(self, sfile, mode='basename', objtype=None):
        """Search for subblocks according to origin file
        
        :Params:
            - **sfile**: Source file name.
            - **mode**, optional: Mode for searching for sfile.
              If ``"strict"``, exact match is needed, else only basename.
            - **objtype**, optional: Restrict search to one or a list of object types
              (i.e. ``"function"``, ``"program"``, etc).
        """
        if blocktype and not isinstance(blocktype, list):
            blocktype = [
             blocktype]
        bb = []
        if mode != 'strict':
            sfile = os.path.basename(sfile)
        for b in self.crack:
            if objtype and objtype != 'all' and block['block'] not in objtype:
                continue
            bfile = b['from'].split(':')[0]
            if mode == 'strict':
                bfile = os.path.basename(bfile)
            if sfile == bfile:
                bb.append(b)

        return bb

    def scan(self):
        """Scan """
        for block in self.crack:
            if block['block'] == 'module':
                modsrc = self.get_blocksrc(block)
                block['desc'] = self.get_comment(modsrc, aslist=True)
                for subblock in block['body']:
                    self.scan_container(subblock, insrc=modsrc)

                self.strip_blocksrc(block, ['type', 'function', 'subroutine'], src=modsrc)
                for line in modsrc:
                    if line.strip().startswith('!'):
                        continue
                    m = block['vardescsearch'](line)
                    if m:
                        block['vars'][m.group('varname')]['desc'] = m.group('vardesc')

                for bvar in block['vars'].values():
                    bvar.setdefault('desc', '')

            elif block['block'] in ('function', 'subroutine', 'program'):
                self.scan_container(block)

    def scan_container(self, block, insrc=None):
        """Scan a block of program, routines or type"""
        if block['block'] not in ('type', 'function', 'subroutine', 'program'):
            return
        else:
            subsrc = self.get_blocksrc(block, insrc)
            block['desc'] = self.get_comment(subsrc, aslist=True)
            if block['block'] in ('function', 'subroutine', 'program'):
                if block['block'] in ('function', 'subroutine'):
                    varname = None
                    for iline, line in enumerate(block['desc']):
                        m = block['vardescmatch'](line)
                        if m:
                            varname = m.group('varname')
                            if m.group('varnum'):
                                ivar = int(m.group('varnum'))
                                ivar = ivar - 1
                                if ivar < 0 or ivar >= len(block['args']):
                                    continue
                                block['desc'][iline] = line.replace(varname, block['args'][ivar])
                                varname = block['args'][ivar]
                            ifirst = len(line) - len(line.strip())
                            block['vars'][varname]['desc'] = m.group('vardesc')
                        elif line.strip() and varname is not None and len(line) - len(line.strip()) > ifirst:
                            block['vars'][varname]['desc'].append(' ' + line.strip())
                        else:
                            varname = None

                block['callto'] = []
                if subsrc is not None:
                    self.join_src(subsrc)
                    for line in subsrc[1:-1]:
                        if line.strip().startswith('!'):
                            continue
                        line = line.lower()
                        for fn in self._re_callsub_findall(line) + self._re_callfunc_findall(line):
                            if fn not in block['callto']:
                                block['callto'].append(fn)
                                continue

            if block['block'] in ('function', 'subroutine') and subsrc is not None:
                for line in subsrc:
                    if line.strip().startswith('!'):
                        continue
                    m = block['vardescsearch'](line)
                    if m:
                        block['vars'][m.group('varname')]['desc'] = m.group('vardesc')

            for bvar in block['vars'].values():
                bvar.setdefault('desc', '')

            del subsrc
            return

    def get_module(self, block):
        """Get the name of the current module"""
        while block['block'] != 'module':
            if block['parentblock'] == 'unknown':
                break
            block = block['parentblock']

        return block['name']

    def get_src(self, block):
        """Get the source lines of the file including this block"""
        srcfile = block['from'].split(':')[0]
        return self.src[srcfile]

    def join_src(self, src):
        """Join unended lines that does not finish with a comment"""
        for iline, line in enumerate(src):
            m = self._re_unended_match(line)
            if m:
                thisline = m.group(1)
                m = self._re_unstarted_match(src[(iline + 1)])
                nextline = m.group(1) if m else src[(iline + 1)]
                src[iline] = thisline + nextline
                del src[iline + 1]

        return src

    def get_blocksrc(self, block, src=None, istart=0, getidx=False, stopmatch=None, exclude=None):
        """Extract an identified block of source code
        
        :Parameters:
        
            - *block*: Cracked block
            
        :Options:
        
            - *src*: List of source line including the block
            - *istart*: Start searching from this line number
            
        :Return:
        
            ``None`` or a list of lines            
        """
        if src is None:
            src = self.get_src(block)
        blocktype = block['block'].lower()
        blockname = block['name'].lower()
        ftypes = '(?:(?:%s).*\\s+)?' % fortrantypes if blocktype == 'function' else ''
        rstart = re.compile('^\\s*%s%s\\s+%s\\b.*$' % (ftypes, blocktype, blockname), re.I).match
        rend = re.compile('^\\s*end\\s+%s\\b.*$' % blocktype, re.I).match
        if isinstance(stopmatch, str):
            stopmatch = re.compile(stopmatch).match
        for ifirst in xrange(istart, len(src)):
            if stopmatch and stopmatch(src[ifirst]):
                return
            if rstart(src[ifirst]):
                break
        else:
            return

        for ilast in xrange(ifirst, len(src)):
            if stopmatch and stopmatch(src[ilast]):
                break
            if rend(src[ilast].lower()):
                break

        mysrc = list(src[ifirst:ilast + 1])
        self.strip_blocksrc(block, exclude, src=mysrc)
        if getidx:
            return (mysrc, (ifirst, ilast))
        else:
            return mysrc

    def strip_blocksrc(self, block, exc, src=None):
        """Strip blocks from source lines
        
        :Parameters:
        
            - *block*: 
            - *exc* list of block type to remove
        
        :Options:
        
            - *src*: list of source lines        
        
        :Example:
        
        >>> obj.strip_blocksrc(lines, 'type')
        >>> obj.strip_blocksrc(lines, ['function', 'type']
        """
        if src is None:
            self.get_blocksrc(block)
        if exc is None:
            return
        else:
            if not isinstance(exc, list):
                exc = [exc]
            for subblock in block['body']:
                if subblock['block'] in exc:
                    subsrc = self.get_blocksrc(subblock, src=src, getidx=True)
                    if subsrc is None:
                        continue
                    del src[subsrc[1][0]:subsrc[1][1]]
                    del subsrc

            return

    def get_comment(self, src, iline=1, aslist=False, stripped=False, getilast=False, rightafter=True):
        """Search for and return the comment starting after ``iline`` in ``src``
        
        :Params:
        
            - **src**: A list of lines.
            - **iline**, optional: Index of first line to read.
            - **aslist**, optional: Return the comment as a list.
            - **stripped**, optional: Strip each line of comment.
            - **getilast**, optional: Get also index of last line of comment.
            - **rightafter**, optional: Suppose the comment right after 
              the signature line. If True, it prevents from reading a comment
              that is not a description of the routine.
        
        :Return:
       
            - ``scomment``: string or list
            - OR ``scomment,ilast``: if ``getilast is True``
        """
        scomment = []
        in_a_breaked_line = False
        if src is not None:
            for iline in xrange(iline, len(src)):
                line = src[iline].strip()
                if line.startswith('&'):
                    continue
                m = self._re_comment_match(line)
                if m is None:
                    if not scomment:
                        if line.endswith('&'):
                            in_a_breaked_line = True
                            continue
                        if in_a_breaked_line:
                            in_a_breaked_line = False
                            continue
                        if not rightafter and not line:
                            continue
                    break
                comment = m.group(1)
                if stripped:
                    comment = comment.strip()
                if not scomment:
                    prefix = self._re_space_prefix_match(comment).group(1)
                if comment.startswith(prefix):
                    comment = comment[len(prefix):]
                scomment.append(comment)

        if not aslist:
            scomment = self.format_lines(scomment, nlc=' ')
        if getilast:
            return (scomment, iline)
        else:
            return scomment

    def get_synopsis(self, block, nmax=2):
        """Get the first ``nmax`` non empty lines of the function, type or module comment as 1 line.
        
        If the header has more than ``nmax`` lines, the first one is taken and appended of '...'.
        If description if empty, it returns an empty string.
        """
        sd = []
        for line in block['desc']:
            line = line.strip()
            if not line:
                if not sd:
                    continue
                break
            sd.append(line)
            if len(sd) > nmax:
                if sd[(-1)].endswith('.'):
                    sd[(-1)] += '...'
                break

        if not sd:
            return ''
        sd = (' ').join(sd)
        return sd

    def get_blocklist(self, choice, module):
        """Get the list of types, variables or function of a module"""
        choice = choice.lower()
        if not choice.endswith('s'):
            choice += 's'
        assert choice in ('types', 'variables', 'functions', 'subroutines'), 'Wrong type of declaration'
        module = module.lower()
        assert module in self.modules.keys(), 'Wrong module name'
        baselist = getattr(self, choice).values()
        return [ v for v in baselist if v.has_key('module') and v['module'] == module.lower() ]

    def set_ulc(self, ulc):
        """Set the underline character for title inside module description"""
        self._ulc = ulc

    def get_ulc(self):
        """Get the underline character for title inside module description"""
        return self._ulc

    ulc = property(get_ulc, set_ulc, doc='Underline character for title inside module description')

    def set_ic(self, ic):
        """Set the indentation character"""
        self._ic = ic

    def get_ic(self):
        """Get the indentation character"""
        return self._ic

    ic = property(get_ic, set_ic, doc='Indentation character')

    def set_sst(self, sst):
        """Set the subsection type"""
        self._sst = sst

    def get_sst(self):
        """Get the subsection type"""
        return self._sst

    sst = property(get_sst, set_sst, doc='Subsection type ("title" or "rubric")')

    def indent(self, n):
        """Get a proper indentation"""
        return n * self.ic

    def format_lines(self, lines, indent=0, bullet=None, nlc='\n', strip=False):
        """Convert a list of lines to text"""
        if not lines:
            return ''
        if bullet is True:
            bullet = '-'
        bullet = str(bullet) + ' ' if bullet else ''
        if isinstance(lines, basestring):
            lines = [lines]
        tmp = []
        for line in lines:
            if not line:
                tmp.append(line)
            else:
                tmp.extend(line.splitlines())

        lines = tmp
        del tmp
        lines = [ line.expandtabs(4) for line in lines ]
        if strip:
            tmp = []
            for line in lines:
                if not tmp and not line:
                    continue
                tmp.append(line)

            lines = tmp
            del tmp
        if not lines:
            return ''
        goodlines = [ len(line) - len(line.lstrip()) for line in lines if line.expandtabs().strip() ]
        firstchar = goodlines and min(goodlines) or 0
        del goodlines
        mylines = [ self.indent(indent) + bullet + line[firstchar:] for line in lines ]
        text = nlc.join(mylines) + nlc
        del mylines
        return text

    def format_title(self, text, ulc=None, indent=0):
        """Create a simple rst titlec with indentation
        
        :Parameters:
        
            - *text*: text of the title
        
        :Options:
        
            - *ulc*: underline character (default to attribute :attr:`ucl`)
        
        :Example:
        
            >>> print o.format_title('My title', '-')
            My title
            --------
        """
        if ulc is None:
            ulc = self.ulc
        return self.format_lines([text, ulc * len(text)], indent=indent) + '\n'

    def format_rubric(self, text, indent=0):
        """Create a simple rst rubric with indentation
        
        :Parameters:
        
            - *text*: text of the rubric
        
        :Example:
        
            >>> print o.format_rubric('My title', '-')
            .. rubric:: My rubric
        """
        return self.format_lines('.. rubric:: ' + text, indent=indent) + '\n'

    def format_subsection(self, text, indent=indent, **kwargs):
        """Format a subsection for describing list of subroutines, types, etc"""
        if self.sst == 'title':
            return self.format_title(text, indent=indent, **kwargs)
        return self.format_rubric(text, indent=indent, **kwargs)

    def format_declaration(self, dectype, name, description=None, indent=0, bullet=None, options=None):
        """Create an simple rst declaration
        
        :Example:
        
        >>> print format_declaration('var', 'myvar', 'my description', indent=1, bullet='-')
            - .. f:var:: myvar
            
                my description
        """
        declaration = self.format_lines('.. f:%(dectype)s:: %(name)s' % locals(), bullet=bullet, indent=indent)
        if options:
            declaration += self.format_options(options, indent=indent + 1)
        declaration += '\n'
        if description:
            declaration += self.format_lines(description, indent=indent + 1)
        return declaration + '\n'

    def format_options(self, options, indent=0):
        """Format directive options"""
        options = [ ':%s: %s' % option for option in options.items() if option[1] is not None ]
        return self.format_lines(options, indent=indent)

    def format_funcref(self, fname, current_module=None, aliasof=None, module=None):
        """Format the reference link to a module function
        
        Formatting may vary depending on if function is local
        and is an alias.
        
        :Example:
        
        >>> print obj.format_type('myfunc')
        :f:func:`~mymodule.myfunc`
        """
        fname = fname.lower()
        if aliasof is not None:
            falias = fname
            fname = aliasof
        if fname in self.routines.keys() and fname in self.routines[fname]['aliases']:
            falias = fname
            fname = self.routines[fname]['name']
        else:
            falias = None
        if module is None and self.routines.has_key(fname):
            module = self.routines[fname].get('module')
        if module is None or current_module is not None and module == current_module:
            if falias:
                return ':f:func:`%(falias)s<%(fname)s>`' % locals()
            return ':f:func:`%(fname)s`' % locals()
        else:
            from fortran_domain import f_sep
            if falias:
                ':f:func:`%(falias)s<~%(module)s%(f_sep)s%(fname)s>`' % locals()
            return ':f:func:`~%(module)s%(f_sep)s%(fname)s`' % locals()

    def format_use(self, block, indent=0, short=False):
        """Format use statement
        
        :Parameters:
        
            - *block*: a module block
        """
        use = ''
        if block.has_key('use'):
            if short:
                use = ':use: '
            else:
                use = self.format_subsection('Needed modules', indent=indent)
            lines = []
            for mname, monly in block['use'].items():
                line = ((short or self.indent)(indent) if 1 else '') + ':f:mod:`%s`' % mname
                if monly:
                    funcs = []
                    for fname, falias in monly['map'].items():
                        func = self.format_funcref(fname, module=mname)
                        if fname != falias:
                            falias = self.format_funcref(falias, module=mname, aliasof=fname)
                            func = '%s => %s' % (falias, func)
                        funcs.append(func)

                    line += ' (%s)' % (', ').join(funcs)
                if self.modules.has_key(mname) and not short:
                    sdesc = self.get_synopsis(self.modules[mname])
                    if sdesc:
                        line += ': ' + sdesc
                lines.append(line)

            if short:
                use += (', ').join(lines)
                use = self.format_lines(use, indent)
            else:
                use += self.format_lines(lines, indent, bullet='-') + '\n'
            del lines
        return use

    def format_argdim(self, block):
        """Format the dimension of a variable
        
         :Parameters:
        
            - *block*: a variable block
        """
        if block.has_key('dimension'):
            return '(%s)' % (',').join([ s.strip('()') for s in block['dimension'] ])
        return ''

    def format_argattr(self, block):
        """Filter and format the attributes (optional, in/out/inout, etc) of a variable
        
         :Parameters:
        
            - *block*: a variable block
        """
        vattr = []
        if block.has_key('intent') and block['intent']:
            vattr.append(('/').join(block['intent']))
        if block.has_key('attrspec') and block['attrspec']:
            newattrs = []
            for attr in block['attrspec']:
                if '=' in block:
                    if attr == 'optional':
                        continue
                    elif attr == 'parameter':
                        attr += '=' + block['=']
                if attr in ():
                    attr = attr.upper()
                newattrs.append(attr)

            block['attrspec'] = newattrs
            vattr.append(('/').join(block['attrspec']))
        if not vattr:
            return ''
        vattr = (',').join(vattr)
        if vattr:
            return self._fmt_vattr % locals()
        return ''

    def format_argtype(self, block):
        vtype = block['typespec']
        if vtype == 'type':
            vtype = block['typename']
        return vtype

    def format_argfield(self, blockvar, role=None, block=None):
        """Format the description of a variable
        
         :Parameters:
        
            - *block*: a variable block
        """
        vname = blockvar['name']
        vtype = self.format_argtype(blockvar)
        vdim = self.format_argdim(blockvar)
        vattr = self.format_argattr(blockvar)
        vdesc = blockvar['desc'] if blockvar.has_key('desc') else ''
        optional = blockvar.has_key('attrspec') and 'optional' in blockvar['attrspec']
        if not role:
            if block and vname in [block['name'], block.get('result')]:
                role = 'r'
            else:
                role = 'o' if optional else 'p'
        return self._fmt_vardesc % locals()

    def format_type(self, block, indent=0, bullet=True):
        """Format the description of a module type
        
         :Parameters:
        
            - *block*: block of the type
        """
        declaration = self.format_declaration('type', block['name'], block['desc'], indent=indent, bullet=bullet) + '\n'
        vlines = []
        for bvar in block['vars'].values():
            vlines.append(self.format_argfield(bvar, role='f'))

        variables = self.format_lines(vlines, indent=indent + 1) + '\n'
        del vlines
        return declaration + variables

    def get_varopts(self, block):
        """Get options for variable declaration as a dict"""
        options = {}
        vdim = self.format_argdim(block)
        if vdim:
            options['shape'] = vdim
        options['type'] = self.format_argtype(block)
        vattr = self.format_argattr(block).strip(' []')
        if vattr:
            options['attrs'] = vattr
        return options

    def format_var(self, block, indent=0, bullet=True):
        """Format the description of a module type
        
         :Parameters:
        
            - *block*: block of the variable
        """
        options = self.get_varopts(block)
        description = block.get('desc', None)
        declaration = self.format_declaration('variable', block['name'], description=description, options=options, indent=indent, bullet=bullet)
        return declaration

    def format_signature(self, block):
        signature = ''
        nopt = 0
        for i, var in enumerate(block['args']):
            optional = 'optional' in block['vars'][var]['attrspec'] and '=' not in block['vars'][var] if block['vars'][var].has_key('attrspec') else False
            signature += '[' if optional else ''
            signature += ', ' if i else ''
            if optional:
                nopt += 1
            signature += var

        signature += nopt * ']'
        return signature

    def format_routine(self, block, indent=0):
        """Format the description of a function, a subroutine or a program"""
        if isinstance(block, basestring):
            if block not in self.programs.keys() + self.routines.keys():
                raise F90toRstException('Unknown function, subroutine or program: %s' % block)
            if block in self.programs:
                block = self.programs[block]
            else:
                block = self.routines[block]
        elif block['name'] not in self.modules.keys() + self.routines.keys():
            raise F90toRstException('Unknown %s: %s' % (block['type'], block['name']))
        name = block['name']
        blocktype = block['block']
        signature = '(%s)' % self.format_signature(block) if blocktype != 'program' else ''
        declaration = self.format_declaration(blocktype, '%(name)s%(signature)s' % locals(), indent=indent)
        comments = list(block['desc']) + ['']
        if blocktype != 'program':
            found = []
            for iline in xrange(len(comments)):
                m = block['vardescmatch'](comments[iline])
                if m:
                    varname = m.group('varname')
                    found.append(varname)
                    comments[iline] = self.format_argfield(block['vars'][varname], block=block)

            for varname in block['args'] + block['sortvars']:
                if varname not in found:
                    comments.append(self.format_argfield(block['vars'][varname], block=block))
                    found.append(varname)

        description = self.format_lines(comments, indent + 1)
        use = self.format_use(block, indent=indent + 1, short=True)
        calls = []
        module = block.get('module')
        if blocktype in ('function', 'subroutine'):
            if block['callfrom']:
                callfrom = []
                for fromname in block['callfrom']:
                    if fromname in self.routines:
                        cf = self.format_funcref(fromname, module)
                    else:
                        cf = ':f:prog:`%s`' % fromname
                    callfrom.append(cf)

                callfrom = ':from: ' + (', ').join(callfrom)
                calls.append(callfrom)
        if block['callto']:
            callto = (', ').join([ self.format_funcref(fn, module) for fn in block['callto'] ])
            if callto == '':
                callto = 'None'
            callto = ':to: ' + callto
            calls.append(callto)
        calls = '\n' + self.format_lines(calls, indent=indent + 1)
        return declaration + description + use + calls + '\n\n'

    format_function = format_routine
    format_subroutine = format_routine

    def format_quickaccess(self, module, indent=indent):
        """Format an abstract of all types, variables and routines of a module"""
        if not isinstance(module, basestring):
            module = module['name']
        title = self.format_subsection('Quick access', indent=indent) + '\n'
        decs = []
        tlist = self.get_blocklist('types', module)
        tlist.sort()
        if tlist:
            decs.append(':Types: ' + (', ').join([ ':f:type:`%s`' % tt['name'] for tt in tlist ]))
        vlist = self.get_blocklist('variables', module)
        vlist.sort()
        if vlist:
            decs.append(':Variables: ' + (', ').join([ ':f:var:`%s`' % vv['name'] for vv in vlist ]))
        flist = self.get_blocklist('functions', module)
        flist.sort()
        if flist:
            decs.append(':Routines: ' + (', ').join([ ':f:func:`~%s/%s`' % (module, ff['name']) for ff in flist ]))
        if decs:
            return self.format_lines(title + ('\n').join(decs)) + '\n\n'
        return ''

    def format_types(self, block, indent=0):
        """Format the description of all fortran types"""
        types = []
        for subblock in block['body']:
            if subblock['block'] == 'type':
                types.append(self.format_type(subblock, indent=indent))

        if types:
            types = self.format_subsection('Types', indent=indent) + ('\n').join(types)
        else:
            types = ''
        return types

    def format_variables(self, block, indent=0):
        """Format the description of all variables (global or module)"""
        variables = ''
        if block['vars']:
            for bvar in block['vars'].values():
                variables += self.format_var(bvar, indent=indent)

            variables = self.format_subsection('Variables', indent=indent) + variables + '\n\n'
        return variables

    def format_description(self, block, indent=0):
        """Format the description of an object"""
        description = ''
        if block['desc']:
            description = self.format_subsection('Description', indent=indent)
            description += self.format_lines(block['desc'], indent=indent, strip=True) + '\n'
        return description

    def format_routines(self, block, indent=0):
        """Format the list of all subroutines and functions"""
        routines = ''
        if block['body']:
            fdecs = []
            for subblock in block['body']:
                if subblock['block'] in ('function', 'subroutine'):
                    fdecs.append(self.format_routine(subblock, indent))

            if fdecs:
                fdecs = ('\n').join(fdecs)
                routines = self.format_subsection('Subroutines and functions', indent=indent) + fdecs
        return routines

    def format_module(self, block, indent=0):
        """Recursively format a module and its declarations"""
        if isinstance(block, basestring):
            if block not in self.modules:
                raise F90toRstException('Unknown module: %s' % block)
            block = self.modules[block]
        elif block['name'] not in self.modules:
            raise F90toRstException('Unknown module: %' % block['name'])
        modname = block['name']
        declaration = self.format_declaration('module', modname, indent=indent, options=dict(synopsis=self.get_synopsis(block).strip() or None))
        description = self.format_description(block, indent=indent)
        quickaccess = self.format_quickaccess(modname, indent=indent)
        use = self.format_use(block, indent=indent)
        types = self.format_types(block, indent=indent)
        variables = self.format_variables(block, indent=indent)
        routines = self.format_routines(block, indent=indent)
        return declaration + description + quickaccess + use + types + variables + routines

    def format_srcfile(self, srcfile, indent=0, **kwargs):
        """Format all declaration of a file, except modules"""
        rst = ''
        bprog = self.filter_by_srcfile(srcfile, objtype='program', **kwargs)
        if bprog:
            programs = self.format_subsection('Program', indent=indent) + '\n'
            rst += self.format_program(bprog[0], indent=indent) + '\n'
        brouts = self.filter_by_srcfile(srcfile, objtype=['function', 'subroutine'], **kwargs)
        if brouts:
            self.format_subsection('Functions et subroutines', indent=indent) + '\n'
            for block in brouts:
                rst += self.format_routines(block, indent=indent) + '\n'

        return rst

    def __getitem__(self, module):
        return self.format_module(self.modules[module])


def setup(app):
    app.add_description_unit('ftype', 'ftype', indextemplate='pair: %s; Fortran type')
    app.add_description_unit('fvar', 'fvar', indextemplate='pair: %s; Fortran variable')
    app.add_config_value('fortran_title_underline', '-', False)
    app.add_config_value('fortran_indent', 4, False)
    app.add_config_value('fortran_subsection_type', 'rubric', False)
    app.add_config_value('fortran_src', '.', False)
    app.add_config_value('fortran_ext', ['f90', 'f95'], False)
    app.add_config_value('fortran_encoding', 'utf8', False)
    FortranDomain.directives.update(automodule=FortranAutoModuleDirective, autoroutine=FortranAutoObjectDirective, autofunction=FortranAutoFunctionDirective, autosubroutine=FortranAutoSubroutineDirective, autoprogram=FortranAutoProgramDirective, autosrcfile=FortranAutoSrcfileDirective)
    app.connect('builder-inited', fortran_parse)


def list_files(fortran_src, exts=[
 'f', 'f90', 'f95'], absolute=True):
    """Get the list of fortran files"""
    if not isinstance(exts, list):
        exts = list(exts)
    for e in exts:
        if e.lower() not in exts:
            exts.append(e.lower())
        if e.upper() not in exts:
            exts.append(e.upper())

    ffiles = []
    for fg in fortran_src:
        if not isinstance(fg, basestring):
            continue
        if os.path.isdir(fg):
            for ext in exts:
                ffiles.extend(glob(os.path.join(fg, '*.' + ext)))

        else:
            ffiles.extend(glob(fg))

    if absolute:
        ffiles = [ os.path.abspath(ffile) for ffile in ffiles ]
    return ffiles


def fortran_parse(app):
    env = app.builder.env
    if isinstance(app.config.fortran_src, (str, list)):
        app.info('Parsing fortran sources...', nonl=True)
        if not isinstance(app.config.fortran_src, list):
            app.config.fortran_src = [
             app.config.fortran_src]
        ffiles = list_files(app.config.fortran_src, app.config.fortran_ext)
        if not ffiles:
            app.warn('No fortran files found')
            app.config._f90torst = None
            app._status.write('\n')
        else:
            app.config.fortran_indent = fmt_indent(app.config.fortran_indent)
            app.config._f90torst = F90toRst(ffiles, ic=app.config.fortran_indent, ulc=app.config.fortran_title_underline, encoding=app.config.fortran_encoding)
            app._status.write('done\n')
        app._status.flush()
    else:
        app.warn('Wrong list of fortran 90 source specifications: ' + str(app.config.fortran_src))
        app.config._f90torst = None
    return


def fmt_indent(string):
    if string is None:
        return
    else:
        if isinstance(string, int):
            string = ' ' * string
        if string == 'tab':
            string = '\t'
        elif string == 'space':
            string = ' '
        return string


class FortranAutoModuleDirective(Directive):
    has_content = True
    option_spec = dict(title_underline=unchanged, indent=fmt_indent, subsection_type=unchanged)
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        f90torst = self.state.document.settings.env.config._f90torst
        if f90torst is None:
            return []
        else:
            module = self.arguments[0]
            if not f90torst.modules.has_key(module):
                self.warn('Wrong fortran module name: ' + module)
            ic = f90torst.ic
            ulc = f90torst.ulc
            if self.options.get('indent'):
                f90torst.ic = self.options['indent']
            if self.options.get('title_underline'):
                f90torst.ulc = self.options['title_underline']
            if self.options.get('subsection_type'):
                f90torst.ulc = self.options['subsection_type']
            raw_text = f90torst.format_module(module)
            source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
            include_lines = string2lines(raw_text, convert_whitespace=1)
            self.state_machine.insert_input(include_lines, source)
            if self.options.has_key('indent'):
                f90torst.ic = ic
            if self.options.has_key('title_underline'):
                f90torst.ulc = ulc
            if self.options.has_key('subsection_type'):
                f90torst.sst = sst
            return []


class FortranAutoObjectDirective(Directive):
    """Generic directive for fortran object auto-documentation
    
    Redefine :attr:`_warning` and :attr:`_objtype` attribute when subcassling.
    
    .. attribute:: _warning
    
        Warning message when object is not found, like:
        
        >>> _warning = 'Wrong function or subroutine name: %s'
        
    .. attribute:: _objtype
    
        Type of fortran object.
        If "toto" is set as object type, then :class:`F90toRst` must have 
        attribute :attr:`totos` containg index of all related fortran objects,
        and method :meth:`format_totos` for formatting the object.
            
    """
    has_content = False
    option_spec = {}
    required_arguments = 1
    optional_arguments = 0
    _warning = 'Wrong routine name: %s'
    _objtype = 'routine'

    def run(self):
        f90torst = self.state.document.settings.env.config._f90torst
        if f90torst is None:
            return []
        else:
            objname = self.arguments[0].lower()
            from fortran_domain import f_sep
            if f_sep in objname:
                objname = objname.split(f_sep)[(-1)]
            objects = getattr(f90torst, self._objtype + 's')
            if not objects.has_key(objname):
                self.warn(self._warning % objname)
            raw_text = getattr(f90torst, 'format_' + self._objtype)(objname)
            b = objects[objname]
            if b.has_key('parent_block'):
                curmod_text = '.. f:currentmodule:: %s\n\n' % b['parent_block']['name']
                raw_text = curmod_text + raw_text
            source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
            include_lines = string2lines(raw_text, convert_whitespace=1)
            self.state_machine.insert_input(include_lines, source)
            return []


class FortranAutoFunctionDirective(FortranAutoObjectDirective):
    _warning = 'Wrong function name: %s'
    _objtype = 'function'


class FortranAutoSubroutineDirective(FortranAutoObjectDirective):
    _warning = 'Wrong subroutine name: %s'
    _objtype = 'subroutine'


class FortranAutoTypeDirective(FortranAutoObjectDirective):
    _warning = 'Wrong type name: %s'
    _objtype = 'type'


class FortranAutoVariableDirective(FortranAutoObjectDirective):
    _warning = 'Wrong variable name: %s'
    _objtype = 'variable'


class FortranAutoProgramDirective(Directive):
    has_content = False
    option_spec = {}
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        f90torst = self.state.document.settings.env.config._f90torst
        if f90torst is None:
            return []
        else:
            program = self.arguments[0].lower()
            if not f90torst.programs.has_key(program):
                self.warning('Wrong program name: ' + program)
            raw_text = f90torst.format_routine(program)
            source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
            include_lines = string2lines(raw_text, convert_whitespace=1)
            self.state_machine.insert_input(include_lines, source)
            return []


class FortranAutoSrcfileDirective(Directive):
    has_content = False
    option_spec = dict(search_mode=unchanged, objtype=unchanged)
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        f90torst = self.state.document.settings.env.config._f90torst
        if f90torst is None:
            return []
        else:
            srcfile = self.arguments[0].lower()
            if not f90torst.programs.has_key(program):
                self.warning('Wrong program name: ' + program)
            search_mode = self.options.get('search_mode')
            objtype = self.options.get('objtype')
            if objtype:
                objtype = objtype.split(' ,')
            raw_text = f90torst.format_srcfile(srcfile, search_mode=search_mode, objtype=objtype)
            if not raw_text:
                self.warning('No valid content found for file: ' + srcfile)
            source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
            include_lines = string2lines(raw_text, convert_whitespace=1)
            self.state_machine.insert_input(include_lines, source)
            return []