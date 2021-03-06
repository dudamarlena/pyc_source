# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tlp/instance.py
# Compiled at: 2020-05-13 17:51:52
# Size of source mod 2**32: 6927 bytes
import enum
from typing import Dict, Iterator, Union
from tlp import util
from tlp.verilog import ast
from tlp.verilog import xilinx as rtl
from .task import Task

class Instance:
    __doc__ = 'Instance of a child Task in an upper-level task.\n\n  A task can be instantiated multiple times in the same upper-level task.\n  Each object of this class corresponds to such a instance of a task.\n\n  Attributes:\n    task: Task, corresponding task of this instance.\n    instance_id: int, index of the instance of the same task.\n    step: int, bulk-synchronous step when instantiated.\n    args: a dict mapping arg names to Arg.\n\n  Properties:\n    name: str, instance name, unique in the parent module.\n\n  '

    class Arg:

        class Cat(enum.Enum):
            INPUT = 1
            OUTPUT = 2
            SCALAR = 4
            STREAM = 8
            MMAP = 16
            ASYNC = 32
            ASYNC_MMAP = MMAP | ASYNC
            ISTREAM = STREAM | INPUT
            OSTREAM = STREAM | OUTPUT

        def __init__(self, cat: Union[(str, Cat)], port: str):
            if isinstance(cat, str):
                self.cat = {'istream':Instance.Arg.Cat.ISTREAM,  'ostream':Instance.Arg.Cat.OSTREAM, 
                 'scalar':Instance.Arg.Cat.SCALAR, 
                 'mmap':Instance.Arg.Cat.MMAP, 
                 'async_mmap':Instance.Arg.Cat.ASYNC_MMAP}[cat]
            else:
                self.cat = cat
            self.port = port
            self.width = None

    def __init__(self, task: Task, instance_id: int, **kwargs):
        self.task = task
        self.instance_id = instance_id
        self.step = kwargs.pop('step')
        self.args = {rtl.sanitize_array_name(k):(Instance.Arg)(**v) for k, v in kwargs.pop('args').items()}

    @property
    def name(self) -> str:
        return util.get_instance_name((self.task.name, self.instance_id))

    @property
    def is_autorun(self) -> bool:
        return self.step < 0

    @property
    def state(self) -> ast.Identifier:
        """State of this instance."""
        return ast.Identifier(f"{self.name}__state")

    def set_state(self, new_state: ast.Node) -> ast.NonblockingSubstitution:
        return ast.NonblockingSubstitution(left=(self.state), right=new_state)

    def is_state(self, state: ast.Node) -> ast.Eq:
        return ast.Eq(left=(self.state), right=state)

    @property
    def rst_n(self) -> ast.Identifier:
        """The handshake synchronous active-low reset signal."""
        return ast.Identifier(f"{self.name}__{rtl.HANDSHAKE_RST_N}")

    @property
    def start(self) -> ast.Identifier:
        """The handshake start signal.

    This signal is asserted until the ready signal is asserted when the instance
    of task starts.

    Returns:
      The ast.Identifier node of this signal.
    """
        return ast.Identifier(f"{self.name}__{rtl.HANDSHAKE_START}")

    @property
    def done(self) -> ast.Identifier:
        """The handshake done signal.

    This signal is asserted for 1 cycle when the instance of task finishes.

    Returns:
      The ast.Identifier node of this signal.
    """
        return ast.Identifier(f"{self.name}__{rtl.HANDSHAKE_DONE}")

    @property
    def is_done(self) -> ast.Identifier:
        """Signal used to determine the upper-level state."""
        return ast.Identifier(f"{self.name}__is_done")

    @property
    def idle(self) -> ast.Identifier:
        """Whether this isntance is idle."""
        return ast.Identifier(f"{self.name}__{rtl.HANDSHAKE_IDLE}")

    @property
    def ready(self) -> ast.Identifier:
        """Whether this isntance is ready to take new input."""
        return ast.Identifier(f"{self.name}__{rtl.HANDSHAKE_READY}")

    def get_signal(self, signal: str) -> ast.Identifier:
        if signal not in frozenset({'done', 'idle', 'ready'}):
            raise ValueError('signal should be one of (done, idle, ready), got {}'.format(signal))
        return getattr(self, signal)

    @property
    def handshake_signals(self) -> Iterator[Union[(ast.Wire, ast.Reg)]]:
        """All handshake signals used for this instance.

    Yields:
      Union[ast.Wire, ast.Reg] of signals.
    """
        yield ast.Wire(name=(self.start.name), width=None)
        if not self.is_autorun:
            yield ast.Reg(name=(self.state.name), width=(ast.make_width(2)))
            yield from (ast.Wire(name=(rtl.wire_name(self.name, suffix)), width=None) for suffix in rtl.HANDSHAKE_OUTPUT_PORTS)

    def get_instance_arg(self, arg: str) -> str:
        return f"{self.name}___{arg}"


class Port:

    def __init__(self, obj):
        self.cat = {'istream':Instance.Arg.Cat.ISTREAM, 
         'ostream':Instance.Arg.Cat.OSTREAM, 
         'scalar':Instance.Arg.Cat.SCALAR, 
         'mmap':Instance.Arg.Cat.MMAP, 
         'async_mmap':Instance.Arg.Cat.ASYNC_MMAP}[obj['cat']]
        self.name = rtl.sanitize_array_name(obj['name'])
        self.ctype = obj['type']
        self.width = obj['width']