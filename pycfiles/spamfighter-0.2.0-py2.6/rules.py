# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/rules.py
# Compiled at: 2009-01-30 08:10:10
"""
Обслуживание правил для анализа сообщений.
"""
import types
from functools import partial

class DuplicateRuleError(Exception):
    """
    Правило с таким именем уже было зарегистриовано.
    """
    pass


class RuleNotFoundError(Exception):
    """
    Правило с таким именем не найдено.
    """
    pass


class RulesFactory(object):
    """
    Фабрика правил анализа сообщений. Регистрирует правила
    и выдает их по требованию.

    Правило анализа сообщений может быть:
     - функцией
     - классом

    В случае функции правило должно иметь вид::
      def rule(domain, message, arg1, arg2=33)

    где:
     - C{domain} (L{spamfighter.interfaces.IDomain}) - текущий домен;
     - C{message} (L{spamfighter.interfaces.IMessage}) - обрабатываемое сообщение;
     - C{arg1}, C{arg2} - дополнительные параметры правил анализа;
     - именем правила будет имя функции (C{rule}).

    Класс должен иметь следующий вид::
      class Rule(object):
          def __init__(self, arg1, arg2=33):
             ...
          def analyze(domain, message):
             ...

    Смысл полей аналогично случаю функции, именем правила будет имя класса.

    @ivar rules: хэш по имени зарегистрированных правил
    @type rules: C{dict}
    """

    def __init__(self):
        u"""
        Конструктор.
        """
        self.rules = {}

    def registerRule(self, rule):
        u"""
        Добавить новое правило (зарегистрировать).

        @param rule: новое правило
        @type rule: C{func} или C{class}
        @raise DuplicateRuleError: если правило с таким же именем уже было зарегистрировано
        """
        if type(rule) is types.FunctionType:
            name = rule.func_name
            info = {'class': None, 'method': rule}
        else:
            name = rule.__name__
            info = {'class': rule, 'method': rule.analyze}
        if self.rules.has_key(name):
            raise DuplicateRuleError, name
        self.rules[name] = info
        return

    def unregisterRule(self, rule):
        u"""
        Удалить ранее зарегистрированное правило.

        @param rule: новое правило
        @type rule: C{func} или C{class}
        @raise RuleNotFoundError: правило с указанным имененем не обнаружено
        """
        if type(rule) is types.FunctionType:
            name = rule.func_name
        else:
            name = rule.__name__
        if not self.rules.has_key(name):
            raise RuleNotFoundError, name
        del self.rules[name]

    def instanciateRule(self, name, **kwargs):
        u"""
        Инстанциировать правило, создать его экземпляр с указанными параметрами.

        Возвращает функцию, в которой должно остаться только два свободных параметра:
        домен и сообщение.

        @param name: имя правила
        @type name: C{str}
        @return: инстанциированное правило
        @rtype: C{func}
        @raise RuleNotFoundError: правило с указанным имененем не обнаружено
        """
        if not self.rules.has_key(name):
            raise RuleNotFoundError, name
        if self.rules[name]['class'] is None:
            return partial(self.rules[name]['method'], **kwargs)
        else:
            return partial(self.rules[name]['method'], self.rules[name]['class'](**kwargs))
            return

    def getRuleNames(self):
        u"""
        Получить имена всех правил.

        @return: список имен правил
        @rtype: C{list(str)}
        """
        return self.rules.keys()


factory = RulesFactory()

def ruleTrue(domain, message):
    u"""
    Правило, которое всегда возвращает истину.
    """
    return True


def ruleFalse(domain, message):
    u"""
    Правило, которое всегда возвращает ложь.
    """
    return False


factory.registerRule(ruleTrue)
factory.registerRule(ruleFalse)