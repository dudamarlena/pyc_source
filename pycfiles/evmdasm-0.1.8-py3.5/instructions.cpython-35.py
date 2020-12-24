# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\instructions.py
# Compiled at: 2018-10-08 16:43:40
# Size of source mod 2**32: 4511 bytes
import logging, itertools
from . import utils
logger = logging.getLogger(__name__)

class Instruction(object):
    __doc__ = ' Base Instruction class\n\n        doubly linked\n    '

    def __init__(self, opcode, name, length_of_operand=0, description=None, args=None, returns=None, gas=-1, category=None, pops=None, pushes=None, fork=''):
        self._opcode, self._name, self._length_of_operand = opcode, name, length_of_operand
        self._gas = gas
        self._description = description
        self._args = args or []
        self._returns = returns or []
        self._category = category
        self._pops = pops
        self._pushes = pushes
        self._fork = fork
        self._opcode_bytes = self._opcode.to_bytes(1, byteorder='big')
        self._operand_bytes = b'\x00' * length_of_operand
        self._operand = '\x00' * length_of_operand
        self.address = None
        self.next = None
        self.previous = None

    def __repr__(self):
        return '<%s name=%s address=%s size=%d %s>' % (self.__class__.__name__,
         self.name, hex(self.address) if self.address else str(self.address), self.size,
         'operand=%r' % self.operand if self.operand else '')

    def __str__(self):
        return '%s %s' % (self.name, '0x%s' % self.operand if self.operand else '')

    def __len__(self):
        return self.size

    @property
    def opcode(self):
        return self._opcode

    @property
    def name(self):
        return self._name

    @property
    def opcode(self):
        return self._opcode

    @property
    def length_of_operand(self):
        return self._length_of_operand

    @property
    def operand_length(self):
        return self._length_of_operand

    @property
    def gas(self):
        return self._gas

    @property
    def description(self):
        return self._description

    @property
    def args(self):
        return self._args

    @property
    def returns(self):
        return self._returns

    @property
    def category(self):
        return self._category

    @property
    def opcode_bytes(self):
        return self._opcode_bytes

    @property
    def operand_bytes(self):
        return self._operand_bytes

    @operand_bytes.setter
    def operand_bytes(self, b):
        self._operand_bytes = b
        self._operand = ''.join('%0.2x' % _ for _ in self._operand_bytes)
        return self

    @property
    def operand(self):
        return self._operand

    @operand.setter
    def operand(self, s):
        self._operand = s
        self._operand_bytes = utils.str_to_bytes(s)
        return self

    @property
    def size(self):
        return self.length_of_operand + 1

    @property
    def pops(self):
        if self._pops is not None:
            return self._pops
        return len(self.args)

    @property
    def pushes(self):
        if self._pushes is not None:
            return self._pushes
        return len(self.returns)

    @property
    def fork(self):
        return self._fork

    def clone(self, _template=None):
        _template = self.__class__ if _template is None else _template
        return _template(opcode=self.opcode, name=self.name, length_of_operand=self.length_of_operand, description=self.description, args=self.args, returns=self.returns, gas=self.gas, category=self.category, pops=self._pops, pushes=self._pushes, fork=self._fork)

    def consume(self, bytecode):
        m = self.clone()
        m.operand_bytes = bytes(_ for _ in itertools.islice(bytecode, m.length_of_operand))
        return m

    def serialize(self):
        return '%0.2x' % self.opcode + utils.bytes_to_str(self.operand_bytes, prefix='')

    def skip_to(self, names):
        res = self.next
        while res:
            if any(res.name == name for name in names):
                return res
            res = res.next