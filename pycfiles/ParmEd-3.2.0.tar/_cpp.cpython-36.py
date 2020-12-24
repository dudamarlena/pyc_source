# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/gromacs/_cpp.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 14020 bytes
"""
A little utiltity for performing C-like preprocessing using standard CPP
directives like #if, #ifdef, and #define.

Written by Jason Swails
"""
from parmed.exceptions import PreProcessorError, PreProcessorWarning
from parmed.utils.io import genopen
from parmed.utils.six import string_types, iteritems, wraps
from collections import OrderedDict
from os import path
import re, warnings
ppre = re.compile('#\\s*(ifdef|ifndef|if|else|elif|endif|define|undef|include)\\s*(.+)?')
ppcomments = re.compile('(?://.+|/\\*(?:.*)\\*/)')
includere = re.compile('[<"](.+)[>"]')
novarcharre = re.compile('\\W')

def _strip_pp_comments(func):
    """
    Decorator to apply to functions that will strip out C-style comments before
    calling the preprocessor function on the resulting arguments to the
    preprocessor directive
    """

    @wraps(func)
    def wrapper(self, args):
        args = ppcomments.sub('', args)
        return func(self, args)

    return wrapper


def _find_all_instances_in_string(string, substr):
    """ Find indices of all instances of substr in string """
    indices = []
    idx = string.find(substr, 0)
    while idx > -1:
        indices.append(idx)
        idx = string.find(substr, idx + 1)

    return indices


def _replace_defines(line, defines):
    """ Replaces defined tokens in a given line """
    if not defines:
        return line
    else:
        for define in reversed(defines):
            value = defines[define]
            indices = _find_all_instances_in_string(line, define)
            if not indices:
                pass
            else:
                inside = ''
                idx = 0
                n_to_skip = 0
                new_line = []
                for i, char in enumerate(line):
                    if n_to_skip:
                        n_to_skip -= 1
                    else:
                        if char in '\'"':
                            if not inside:
                                inside = char
                            elif inside == char:
                                inside = ''
                        if idx < len(indices) and i == indices[idx]:
                            if inside:
                                new_line.append(char)
                                idx += 1
                                continue
                            if i == 0 or novarcharre.match(line[(i - 1)]):
                                endidx = indices[idx] + len(define)
                                if endidx >= len(line) or novarcharre.match(line[endidx]):
                                    new_line.extend(list(value))
                                    n_to_skip = len(define) - 1
                                    idx += 1
                                    continue
                            idx += 1
                        new_line.append(char)

            line = ''.join(new_line)

        return line


_IN_IF = 'in if'
_IN_ELIF = 'in elif'
_IN_ELSE = 'in else'

class CPreProcessor(object):
    __doc__ = '\n    Steps through a file line-by-line, yielding only the preprocessed contents\n\n    Parameters\n    ----------\n    fname : str or file-like\n        The file name of the file to open or the open file object\n    defines : dict{str : value}, optional\n        The dict of defines to apply to this preprocessed file if any;\n        equivalent to the list of -DXYZ=ABC in the standard preprocessor\n    includes : list of str, optional\n        List of directory names to search for included files, if any\n    notfound_fatal : bool, optional\n        If True, include files not found are fatal. If False, they will simply\n        be skipped (with a warning emitted). Default True\n\n    Notes\n    -----\n    If ``fname`` is a file name, the directory containing that file name is the\n    first directory searched for include files. If ``fname`` is a file-like\n    object, then the current directory is the first searched.\n    '

    def __init__(self, fname, defines=None, includes=None, notfound_fatal=True):
        if isinstance(fname, string_types):
            self._fileobj = genopen(fname, 'r')
            self._ownhandle = True
            curpath = path.abspath(path.split(fname)[0])
            self.filename = fname
        else:
            self._fileobj = fname
            self._ownhandle = False
            curpath = path.abspath(path.curdir)
            self.filename = None
        if includes is None:
            self._includes = [
             curpath]
        else:
            self._includes = [
             curpath] + list(includes)
        if defines is None:
            self.defines = OrderedDict()
        else:
            self.defines = OrderedDict()
            for define, value in iteritems(defines):
                self.defines[define] = str(value)

        self._notfound_fatal = notfound_fatal
        self.included_files = []
        self._ifstack = []
        self._elsestack = []
        self._satisfiedstack = []
        self._num_ignoring_if = 0
        self._includefile = None

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, '_ownhandle'):
            if self._ownhandle:
                self._fileobj.close()

    def readline(self):
        try:
            return next(iter(self))
        except StopIteration:
            return ''

    def readlines(self):
        return [line for line in self]

    def read(self):
        return ''.join(self.readlines())

    def tell(self):
        return self._fileobj.tell()

    def seek(self, value):
        raise NotImplementedError('Cannot seek through a preprocessed file')

    def __iter__(self):
        """ Step through the preprocessed file line-by-line """
        for line in self._fileobj:
            rematch = ppre.match(line)
            if rematch:
                cmd, args = rematch.groups()
                args = args or ''
                self._ppcmdmap[cmd](self, args)
                if self._includefile is not None:
                    for line in self._includefile:
                        yield line

                    self._includefile.close()
                    self.defines = self._includefile.defines
                    self._includefile = None
                    continue
                    if self._satisfiedstack:
                        if not self._satisfiedstack[(-1)]:
                            continue
                    yield _replace_defines(line, self.defines)

        if self._ifstack:
            raise PreProcessorError('EOF: Unterminated #if(def)')

    @_strip_pp_comments
    def _pp_if(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                self._num_ignoring_if += 1
                return
        args = args.strip()
        if args.strip() in ('0', '1'):
            satisfied = bool(int(args))
            self._ifstack.append(str(bool(satisfied)))
            self._satisfiedstack.append(bool(satisfied))
            self._elsestack.append(_IN_IF)
            return
        raise NotImplementedError('Only "#if 0|1" is currently supported')

    @_strip_pp_comments
    def _pp_ifdef(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                self._num_ignoring_if += 1
                return
        words = args.split()
        if len(words) == 0:
            raise PreProcessorError('Bad #ifdef syntax: "#ifdef %s"' % args)
        else:
            if len(words) > 1:
                warnings.warn('Ignored tokens in #ifdef: %s' % ', '.join(words[1:]), PreProcessorWarning)
        self._ifstack.append('%s in self.defines' % words[0])
        self._elsestack.append(_IN_IF)
        self._satisfiedstack.append(words[0] in self.defines)

    @_strip_pp_comments
    def _pp_ifndef(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                self._num_ignoring_if += 1
                return
        words = args.split()
        if len(words) == 0:
            raise PreProcessorError('Bad #ifndef syntax: "#ifndef %s"' % args)
        else:
            if len(words) > 1:
                warnings.warn('Ignored tokens in #ifndef: %s' % ', '.join(words[1:]), PreProcessorWarning)
        self._ifstack.append('%s not in self.defines' % words[0])
        self._elsestack.append(_IN_IF)
        self._satisfiedstack.append(words[0] not in self.defines)

    @_strip_pp_comments
    def _pp_elif(self, args):
        raise NotImplementedError('#elif conditionals are not yet implemented.')

    @_strip_pp_comments
    def _pp_else(self, args):
        if self._num_ignoring_if > 0:
            return
        else:
            if not self._ifstack:
                raise PreProcessorError('#else missing #if(def)')
            words = args.split()
            if len(words) > 0:
                warnings.warn('Ignored tokens in #else: %s' % ', '.join(words[1:]), PreProcessorWarning)
            if self._elsestack[(-1)] == _IN_ELSE:
                raise PreProcessorError('#else following #else')
        self._elsestack[-1] = _IN_ELSE
        self._satisfiedstack[-1] = not self._satisfiedstack[(-1)]

    @_strip_pp_comments
    def _pp_endif(self, args):
        if self._num_ignoring_if > 0:
            self._num_ignoring_if -= 1
            return
        else:
            if args.strip():
                warnings.warn('Ignored tokens in #endif: %s' % args.strip(), PreProcessorWarning)
            raise self._ifstack or PreProcessorError('#endif missing #if(def)')
        self._ifstack.pop()
        self._satisfiedstack.pop()
        self._elsestack.pop()

    @_strip_pp_comments
    def _pp_include(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                return
        rematch = includere.match(args)
        if not rematch:
            raise PreProcessorError('Bad #include syntax')
        includefile = rematch.groups()[0]
        self.included_files.append(includefile)
        for folder in self._includes:
            testfile = path.join(folder, includefile)
            if path.isfile(testfile):
                break
        else:
            if self._notfound_fatal:
                raise PreProcessorError('Could not find %s' % includefile)
            warnings.warn('Could not find %s; skipping' % includefile, PreProcessorWarning)

        self._includefile = CPreProcessor(testfile, defines=(self.defines),
          includes=(self._includes),
          notfound_fatal=(self._notfound_fatal))

    @_strip_pp_comments
    def _pp_define(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                return
            words = args.split()
            if len(words) == 0:
                raise PreProcessorError('Nothing defined in #define')
            if words[0] in self.defines:
                warnings.warn('%s already defined; overwriting' % words[0], PreProcessorWarning)
        else:
            if len(words) == 1:
                self.defines[words[0]] = '1'
            elif len(words) >= 2:
                self.defines[words[0]] = args[len(words[0]):].strip()

    @_strip_pp_comments
    def _pp_undef(self, args):
        if self._satisfiedstack:
            if not self._satisfiedstack[(-1)]:
                return
        words = args.split()
        if len(words) == 1:
            try:
                del self.defines[words[0]]
            except KeyError:
                pass

        else:
            if len(words) > 1:
                warnings.warn('Ignored tokens in #undef: %s' % ', '.join(words[1:]), PreProcessorWarning)
            elif len(words) == 0:
                raise PreProcessorError('Nothing defined in #undef')

    def __exit__(self, type, value, traceback):
        self.close()

    def __enter__(self):
        return self

    _ppcmdmap = {'if':_pp_if, 
     'elif':_pp_elif,  'ifdef':_pp_ifdef,  'else':_pp_else, 
     'define':_pp_define,  'undef':_pp_undef,  'include':_pp_include, 
     'endif':_pp_endif,  'ifndef':_pp_ifndef}


if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input', metavar='FILE', required=True,
      help="Input file to pre-process. Either a file\n                name or, if '-' is given, from standard input.")
    parser.add_argument('-o', '--output-file', dest='output', metavar='FILE', default=None,
      help='Output file with preprocessed results.\n                Default is standard output')
    parser.add_argument('-D', dest='defines', metavar='VAR[=VAL]', action='append',
      help='List of predefined variables to pass to\n                the preprocessor. Default VAL is 1 when missing.',
      default=[])
    parser.add_argument('-I', dest='includes', metavar='DIRECTORY', action='append',
      help='List of include directories to search\n                for included files',
      default=[])
    opt = parser.parse_args()
    defines = OrderedDict()
    for define in opt.defines:
        if '=' in define:
            define, val = define.split('=')
        else:
            val = '1'
        defines[define] = val

    if opt.input == '-':
        f = sys.stdin
    else:
        f = opt.input
    pp = CPreProcessor(f, defines=defines, includes=(opt.includes))
    if opt.output is None:
        output = sys.stdout
        own_handle = False
    else:
        output = genopen(opt.output, 'w')
        own_handle = True
    for line in pp:
        output.write(line)

    if own_handle:
        output.close()