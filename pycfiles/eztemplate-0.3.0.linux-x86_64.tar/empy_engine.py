# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/eztemplate/engines/empy_engine.py
# Compiled at: 2016-02-28 15:28:59
"""Provide the empy templating engine."""
from __future__ import absolute_import
from __future__ import print_function
import os.path, em
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from . import Engine

class SubsystemWrapper(em.Subsystem):
    """Wrap EmPy's Subsystem class.

    Allows to open files relative to a base directory.
    """

    def __init__(self, basedir=None, **kwargs):
        """Initialize Subsystem plus a possible base directory."""
        em.Subsystem.__init__(self, **kwargs)
        self.basedir = basedir

    def open(self, name, *args, **kwargs):
        """Open file, possibly relative to a base directory."""
        if self.basedir is not None:
            name = os.path.join(self.basedir, name)
        return em.Subsystem.open(self, name, *args, **kwargs)


class EmpyEngine(Engine):
    """Empy templating engine."""
    handle = 'empy'

    def __init__(self, template, dirname=None, **kwargs):
        """Initialize empy template."""
        super(EmpyEngine, self).__init__(**kwargs)
        if dirname is not None:
            em.theSubsystem = SubsystemWrapper(basedir=dirname)
        self.output = StringIO()
        self.interpreter = em.Interpreter(output=self.output)
        self.template = template
        return

    def apply(self, mapping):
        """Apply a mapping of name-value-pairs to a template."""
        self.output.seek(0)
        self.output.truncate(0)
        self.interpreter.string(self.template, locals=mapping)
        return self.output.getvalue()