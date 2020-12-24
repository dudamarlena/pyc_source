# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/magical/magic.py
# Compiled at: 2016-09-07 10:58:39
# Size of source mod 2**32: 2416 bytes
from IPython import display, get_ipython
from IPython.core import magic_arguments
from typing import Callable
from toolz.curried import partial, pipe, reduce
__all__ = [
 'magical']

@magic_arguments.magic_arguments()
@magic_arguments.argument('name', default='markdown', nargs='?', help='Name of local variable to set to parsed value')
@magic_arguments.argument('-d', '--display', default='Markdown', nargs='?', help='An IPython.display method.')
def _wraps_magic(f, line, cell='', **kwargs):

    def _preprocess_line(line):
        """I don't understand how I would use this yet."""
        return line.strip().split(' ', 1)

    if not cell:
        line, cell = _preprocess_line(line)
    args = magic_arguments.parse_argstring(_wraps_magic, line.strip())
    retval = f(cell)
    if args.name:
        if '.' in args.name or '[' in args.name:
            path = args.name.split('.')
            var = get_ipython().user_ns[path[0]]
            setattr(reduce(lambda x, y: getattr(x, y) if hasattr(x, y) else x[y], path[1:-1], var), path[(-1)], retval)
    else:
        get_ipython().user_ns[args.name] = retval
    if args.display:
        disp = kwargs['display'] if 'display' in kwargs else args.display
        if isinstance(disp, str):
            return display.display(getattr(display, disp)(retval))
        if isinstance(disp, Callable):
            pass
        return disp(retval)


def magical(name, lang=None, **kwargs):
    if lang:
        pipe('require([\n                    "notebook/js/codecell",\n                    "codemirror/mode/{0}/{0}"\n                ],\n                function(cc){{\n                    cc.CodeCell.options_default.highlight_modes.magic_{1} = {{\n                        reg: ["^%%{1}"]\n                    }};\n                }}\n            );\n            '.format(lang, name), display.Javascript, display.display)

    def _register(method):
        get_ipython().register_magic_function(partial(_wraps_magic, method, **kwargs), magic_kind='line_cell', magic_name=name)

    return _register