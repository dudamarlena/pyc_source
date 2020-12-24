# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/block/function.py
# Compiled at: 2019-03-06 14:20:36
# Size of source mod 2**32: 4031 bytes
import re
from ..util import py, pypy, ensure_buffer
from inline.flush import flush_template

class Function(object):
    __doc__ = 'Proces function declarations within templates.\n\t\n\tSyntax:\n\t\n\t\t: def <name> <arguments>\n\t\t: end\n\t\n\t'
    priority = -50
    STARARGS = re.compile('(^|,\\s*)\\*([^*\\s,]+|\\s*,|$)')
    STARSTARARGS = re.compile('(^|,\\s*)\\*\\*\\S+')
    OPTIMIZE = [
     '_escape', '_bless', '_args']

    def match(self, context, line):
        """Match code lines using the "def" keyword."""
        return line.kind == 'code' and line.partitioned[0] == 'def'

    def _optimize(self, context, argspec):
        """Inject speedup shortcut bindings into the argument specification for a function.
                
                This assigns these labels to the local scope, avoiding a cascade through to globals(), saving time.
                
                This also has some unfortunate side-effects for using these sentinels in argument default values!
                """
        argspec = argspec.strip()
        optimization = ', '.join((i + '=' + i for i in self.OPTIMIZE))
        split = None
        prefix = ''
        suffix = ''
        if argspec:
            matches = list(self.STARARGS.finditer(argspec))
            if matches:
                split = matches[(-1)].span()[1]
                if split != len(argspec):
                    prefix = ', ' if argspec[split] == ',' else ''
                    suffix = '' if argspec[split] == ',' else ', '
                else:
                    matches = list(self.STARSTARARGS.finditer(argspec))
                    prefix = ', *, '
                    suffix = ', '
                    if matches:
                        split = matches[(-1)].span()[0]
                        if split == 0:
                            prefix = '*, '
                        else:
                            suffix = ''
            else:
                split = len(argspec)
                suffix = ''
        else:
            prefix = '*, '
        if split is None:
            return prefix + optimization + suffix
        return argspec[:split] + prefix + optimization + suffix + argspec[split:]

    def __call__(self, context):
        input = context.input
        try:
            declaration = input.next()
        except StopIteration:
            return
        else:
            line = declaration.partitioned[1]
            line, _, annotation = line.rpartition('->')
            if annotation:
                if not line:
                    line = annotation
                    annotation = ''
            name, _, line = line.partition(' ')
            argspec = line.rstrip()
            name = name.strip()
            annotation = annotation.lstrip()
            added_flags = []
            removed_flags = []
            if annotation:
                for flag in (i.lower().strip() for i in annotation.split()):
                    if not flag.strip('!'):
                        continue
                    if flag[0] == '!':
                        flag = flag[1:]
                        if flag in context.flag:
                            context.flag.remove(flag)
                            removed_flags.append(flag)
                            continue
                        if flag not in context.flag:
                            context.flag.add(flag)
                            added_flags.append(flag)

            if py == 3:
                if not pypy:
                    argspec = self._optimize(context, argspec)
            line = 'def ' + name + '(' + argspec + '):'
            yield declaration.clone(line=line)
            context.scope += 1
            for i in ensure_buffer(context, False):
                yield i

            for i in context.stream:
                yield i

            if 'using' in context.flag:
                context.flag.remove('using')
            if 'text' in context.flag:
                context.templates.append(name)
            for i in flush_template(context, reconstruct=False):
                yield i

            if 'text' in context.flag:
                context.flag.remove('text')
            for flag in added_flags:
                if flag in context.flag:
                    context.flag.remove(flag)

            for flag in removed_flags:
                if flag not in context.flag:
                    context.flag.add(flag)

            context.scope -= 1