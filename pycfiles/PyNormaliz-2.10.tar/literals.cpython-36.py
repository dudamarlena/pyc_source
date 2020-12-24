# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/grammar/literals.py
# Compiled at: 2019-05-05 04:54:54
# Size of source mod 2**32: 2731 bytes
from enum import Enum
import logging
logger = logging.getLogger(__name__)
OMMIT = '...'

class CodeMode(Enum):
    QUERY = ''
    PYTHON = '%python'
    KERAS = '%keras'
    SQL = '%sql'


class AOP(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    EXP = '**'

    def __str__(self):
        return self.value


class COP(Enum):
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQ = '=='
    NE = '!='
    LK = '~'
    IN = 'in'
    NI = 'not in'

    def negate(self):
        if self is COP.GT:
            return COP.LE
        else:
            if self is COP.GE:
                return COP.LT
            else:
                if self is COP.LT:
                    return COP.GE
                else:
                    if self is COP.LE:
                        return COP.GT
                    if self is COP.EQ:
                        return COP.NE
                    if self is COP.NE:
                        return COP.EQ
                if self is COP.IN:
                    return COP.NI
            if self is COP.NI:
                return COP.IN
        msg = 'Negated {} is not supported currently'.format(self)
        logger.error(msg)
        raise NotImplementedError(msg)

    def __str__(self):
        return self.value


class LOP(Enum):
    AND = 'and'
    OR = 'or'
    XOR = 'xor'
    NOT = 'not'
    IMP = 'imp'
    EQV = 'eqv'

    @classmethod
    def parse(cls, token):
        token = token.lower()
        if token == '!' or token == 'not':
            return cls.NOT
        if token == '&' or token == 'and':
            return cls.AND
        if token == '|' or token == 'or':
            return cls.OR
        if token == '^' or token == 'xor':
            return cls.XOR
        if token == '=>' or token == 'imp':
            return cls.IMP
        if token == '<=>' or token == '<=>':
            return cls.EQV

    def negate(self):
        if self is LOP.AND:
            return LOP.OR
        if self is LOP.OR:
            return LOP.AND
        msg = 'Negation only supports AND/OR for now'
        logger.error(msg)
        raise NotImplementedError(msg)

    def __str__(self):
        if self is LOP.XOR or self is LOP.IMP or self is LOP.EQV:
            msg = 'String representation only supports AND/OR/NOT for now'
            logger.error(msg)
            raise NotImplementedError(msg)
        return self.value


class MOP(Enum):
    HISTORY = 'history'
    DESCRIBE = 'describe'
    REDO = 'redo'
    UNDO = 'undo'
    DEL = 'del'


class ConstantType(Enum):
    NULL = 'none'
    BOOL = 'bool'
    INT = 'integer'
    FLT = 'float'
    STR = 'string'
    PTN = 'pattern'
    UID = 'uuid'
    URL = 'url'
    DTM = 'datetime'
    ANY = 'object'


class ImplType(Enum):
    DEF = ':='
    OR_DEF = '|='
    AND_DEF = '&='