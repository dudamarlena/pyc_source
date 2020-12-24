# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/shaders/multiprogram.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 3951 bytes
import weakref
from .program import ModularProgram

class MultiProgram(object):
    __doc__ = 'A collection of ModularPrograms that emulates the API of a single\n    ModularProgram. \n\n    A single Visual is often drawn in many different ways--viewed under\n    different transforms, with different clipping boundaries, or with different\n    colors as in picking and anaglyph stereo. Each draw may require a different\n    program. To simplify this process, MultiProgram exposes an API that looks\n    very much like a single ModularProgram, but internally manages many\n    programs.\n    '

    def __init__(self, vcode='', fcode=''):
        self._vcode = vcode
        self._fcode = fcode
        self._programs = weakref.WeakValueDictionary()
        self._set_items = {}
        self._next_prog_id = 0
        self._vert = MultiShader(self, 'vert')
        self._frag = MultiShader(self, 'frag')

    def add_program(self, name=None):
        """Create a program and add it to this MultiProgram.
        
        It is the caller's responsibility to keep a reference to the returned 
        program.
        
        The *name* must be unique, but is otherwise arbitrary and used for 
        debugging purposes.
        """
        if name is None:
            name = 'program' + str(self._next_prog_id)
            self._next_prog_id += 1
        if name in self._programs:
            raise KeyError("Program named '%s' already exists." % name)
        prog = ModularProgram(self._vcode, self._fcode)
        for key, val in self._set_items.items():
            prog[key] = val

        self.frag._new_program(prog)
        self.vert._new_program(prog)
        self._programs[name] = prog
        return prog

    @property
    def vert(self):
        """A wrapper around all vertex shaders contained in this MultiProgram.
        """
        return self._vert

    @vert.setter
    def vert(self, code):
        self._vcode = code
        for p in self._programs.values():
            p.vert = code

    @property
    def frag(self):
        """A wrapper around all fragmet shaders contained in this MultiProgram.
        """
        return self._frag

    @frag.setter
    def frag(self, code):
        self._fcode = code
        for p in self._programs.values():
            p.frag = code

    def __contains__(self, key):
        return any((key in p for p in self._programs.values()))

    def __getitem__(self, key):
        return self._set_items[key]

    def __setitem__(self, key, value):
        self._set_items[key] = value
        for program in self._programs.values():
            program[key] = value

    def __iter__(self):
        for p in self._programs.values():
            yield p

    def bind(self, data):
        for name in data.dtype.names:
            self[name] = data[name]


class MultiShader(object):
    __doc__ = "Emulates the API of a MainFunction while wrapping all vertex or fragment\n    shaders in a MultiProgram.\n    \n    Example::\n    \n        mp = MultiProgram(vert, frag)\n        mp.add_program('p1')\n        mp.add_program('p2')\n        \n        # applies to all programs\n        mp.vert['u_scale'] = (1, 2)\n        \n        # applies to one program\n        mp.get_program('p1').frag['u_color'] = (1, 1, 1, 1)  \n    "

    def __init__(self, program, shader):
        self._program = program
        self._shader = shader
        self._set_items = {}

    def __getitem__(self, key):
        return self._set_items[key]

    def __setitem__(self, key, value):
        self._set_items[key] = value
        for p in self._program._programs.values():
            getattr(p, self._shader)[key] = value

    def _new_program(self, p):
        """New program was added to the multiprogram; update items in the
        shader.
        """
        for k, v in self._set_items.items():
            getattr(p, self._shader)[k] = v