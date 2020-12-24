# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/pragma.py
# Compiled at: 2018-11-21 11:13:57
# Size of source mod 2**32: 2438 bytes


class Pragma(object):
    __doc__ = 'Allow the addition and removal of translation flags during the translation process.\n\t\n\tUsage is straightforward; to add "flag" to the current set of flags:\n\t\n\t\t: pragma flag\n\t\n\tTo subsequently remove a flag:\n\t\n\t\t: pragma !flag\n\t\n\tMultiple flags may be whitespace separated and can mix addition and removal:\n\t\n\t\t: pragma flag !other_flag\n\t\n\tNo flag may contain whitespace.\n\t\n\tBuilt-in flags include:\n\t\n\t\t`init`: The module scope has been prepared. Unsetting this is unwise.\n\t\t\n\t\t`text`: Text fragments have been utilized within the current function scope.\n\t\t\n\t\t`dirty`: It is known to the engine that the current buffer contains content which will need to be flushed.\n\t\t\n\t\t`buffer`: Enabled by default, its presence tells cinje to use a buffer with explicit flushing. When removed\n\t\t\t\tbuffering is disabled and every fragment is flushed as it is encounered and `: use` / `: using`\n\t\t\t\tbehaviour is altered to `yield from` instead of adding the child template to the buffer.\n\t\t\t\t\n\t\t\t\tIt is potentially very useful to disable this in the context of `: use` and `: using` to make child\n\t\t\t\ttemplate `: flush` statements effective.\n\t\t\n\t\t`using`: Indicates the `_using_stack` variable is available at this point in the translated code, i.e. to\n\t\t\t\ttrack nested `: using` statements.\n\t\n\tIn Python 3 runtimes with function annotation support, you can declare flags as the return type annotation:\n\t\n\t\t: def my_function argument, other_argument -> \'flag !other_flag\'\n\t\n\tFlags declared this way will have their effect reversed automatically at the close of the function scope.\n\t'
    priority = 25

    def match(self, context, line):
        """Match "pragma" command usage."""
        return line.kind == 'code' and line.stripped.startswith('pragma ')

    def __call__(self, context):
        flags = [i.lower().strip() for i in context.input.next().stripped.split()][1:]
        for flag in flags:
            if not flag.strip('!'):
                continue
            if flag[0] == '!':
                flag = flag[1:]
                if flag in context.flag:
                    context.flag.remove(flag)
                    continue
                if flag not in context.flag:
                    context.flag.add(flag)

        if False:
            yield None