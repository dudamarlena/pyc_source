# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/ide/settings.py
# Compiled at: 2017-11-20 08:10:46
# Size of source mod 2**32: 1333 bytes
from enum import IntEnum
from PyQt5.QtCore import QObject, Q_ENUMS
from PyQt5.QtQml import QQmlEngine, QJSEngine
from ifj2017.interpreter.instruction import Instruction
ICON_SIZES = (16, 24, 32, 48, 256)
EXPRESSION_SPLITTERS = set(' \n\t')

class Expression(QObject):

    class ExpressionTypes(IntEnum):
        Instruction = 0
        Variable = 1
        Types = 2
        Header = 3

    Q_ENUMS(ExpressionTypes)

    @staticmethod
    def singletonProvider(engine: QQmlEngine, script_engine: QJSEngine) -> QObject:
        return Expression()


INSTRUCTIONS = tuple(sorted(list(Instruction._commands.keys())))
IDENTIFIER_PATTERN = '[\\w_\\-\\$&%*]+'
SEARCH_FORMAT = 'yellow'
HIGHLIGHT_RULES = (
 (
  (''.join(('(?i)', instruction)) for instruction in INSTRUCTIONS), '#1d73a3'),
 (('[LGT]F@',), '#930c80'),
 (
  (
   '(?<=[LGT]F@){identifier}'.format(identifier=IDENTIFIER_PATTERN),), 'black'),
 (
  (
   '(?i)(call|label|JUMP|jumpifeq|jumpifneq|jumpifeqs|jumpifneqs)(\\s+)({identifier})'.format(identifier=IDENTIFIER_PATTERN),), ('#1d73a3', None, '#4c4c4c')),
 (('(float|int)(@)(-?[0-9.]+)', '(bool)(@)((?i)(true|false))', '(string)@(.*)'), '#1ed3a8'),
 (('#.*$',), 'gray'),
 (
  ('([nN])([yY])([aA])([nN])', ), '#ED1869 #F2BC1F #39BFC1 #672980'.split()))