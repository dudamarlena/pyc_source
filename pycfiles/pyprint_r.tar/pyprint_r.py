# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/sasha/workspace/print_r/pyprint_r/pyprint_r.py
# Compiled at: 2012-03-05 15:34:52
"""
- print_r()
- string print_r (mixed object [, bool view = False])
- Prints human-readable information about the object
- @author: Alexander Guinness
- @version: 1.1
- @params: {mixed} The Object to be printed
- @params: {view} Optional boolean parameter to set an alternative view
- @return string represented by standard output function print()
- @license: PSF, MIT
- @date: 2/27/12 9:28 PM
"""
__all__ = [
 'print_r']

class main:

    def __init__(self, data, view):
        """
                - __init__ (mixed data [, bool view = False])
                """
        self.data = data
        self.view = view

    def __str__(self):
        return self.build(self.data)

    def build(self, data, indent=''):
        """
                - string build (mixed data [, str indent = ''])
                """
        output = []

        def get_depth(item):
            return self.set_depth(item, output, indent)

        if isinstance(data, dict):
            get_depth(data.items())
        else:
            if isinstance(data, list):
                get_depth(enumerate(data))
            else:
                if isinstance(data, str):
                    output.extend(['"', data, '"'])
                else:
                    if '__dict__' in dir(data) and type(data) is not type:
                        get_depth(data.__dict__.items())
                    else:
                        output.append(data)
        return ''.join(map(str, output))

    def set_depth(self, item, output, indent):
        """
                - void set_depth (mixed item, dict output, str indent)
                """
        is_list = isinstance(item, enumerate) and 1 or 0
        brace = [
         [
          '{', '}'], ['[', ']']][is_list]
        block = [brace[0], '\n']
        for key, value in sorted(item):
            block.extend([indent, self.get_view(key, is_list), self.build(value, indent + '\t'), ',', '\n'])

        block.pop(-2)
        output.extend([''.join(block), indent, brace[1]])

    def get_view(self, key, is_list):
        """
                - string get_view (mixed key, bool is_list)
                """
        return ''.join(map(str, (self.view or is_list) and ['\t[', key, '] => '] or ['\t', key, ': ']))


def print_r(data, view=0):
    return print(main(data, view))