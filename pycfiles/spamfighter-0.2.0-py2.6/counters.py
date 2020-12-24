# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/counters.py
# Compiled at: 2009-01-30 08:10:10
"""
Счетчики, анализирующие нагрузку на сервер.
"""
from zope.interface import Interface, implements
from twisted.internet import reactor
from spamfighter.utils.time import time

class ICounter(Interface):
    """
    Счетчик, аккумулирующий информацию по группе одиночных счетчиков L{IAtomCounter}.

    Счетчик обладает возможностью инкремента и показа текущей информации.
    """

    def __str__():
        u"""
        Представить текущее состояние счетчика в понятном человеку виде.

        @rtype: C{str}
        """
        pass

    def increment(value=1):
        u"""
        Инкрементировать значение счетчика (при этом инкрементируются все одинарные счетчики).

        @param value: значение инкремента
        """
        pass


class IAtomCounter(Interface):
    """
    Одиночный счетчик (одно значение). Счетчик рассчитывает своё
    значение для определенного периода времени.
    """

    def period():
        u"""
        Период времени, за который собирается значение счетчика.

        @return: период времени, секунды
        @rtype: C{int}
        """
        pass

    def value():
        u"""
        Текущее значение счетчика для данного периода.
        """
        pass

    def increment(value=1):
        u"""
        Увеличить значение счетчика на указанное значение.

        @param value: значение инкремента
        """
        pass

    def label():
        u"""
        Подпись счетчика, описывающая период его работы.

        @rtype: C{str}
        """
        pass

    def count():
        u"""
        Число увеличений счетчика.

        @rtype: C{int}
        """
        pass


class AtomCounterPeriod(object):
    """
    Одиночный счетчик, рассчитывающий своё значение за конечный 
    период времени. Состоит из двух значений, одно "теневое", которое
    в течение периода времени увеличивается, и другое "текущее", которое
    возвращается по запросу в течение того же периода времени, затем
    части счетчика меняются местами.

    @ivar counter: значение текущего и теневого счетчика
    @type counter: C{list(x,x)}
    @ivar active: номер теневого счетчика
    @type active: C{int}
    @ivar _period: период счетчика, секунд
    @type _period: C{int}
    """
    implements(IAtomCounter)

    def __init__(self, period):
        u"""
        Конструктор.

        @param period: период счетчика, секунд
        @type period: C{int}
        """
        self.counter = [
         0, 0]
        self.increments = [0, 0]
        self.active = 0
        self._period = period
        reactor.callLater(self._period, self.exchangeCounters)

    def value(self):
        u"""
        Текущее значение счетчика для данного периода.
        """
        return self.counter[(1 - self.active)]

    def count(self):
        u"""
        Число увеличений счетчика.

        @rtype: C{int}
        """
        return max(1, self.increments[(1 - self.active)])

    def period(self):
        u"""
        Период времени, за который собирается значение счетчика.

        @return: период времени, секунды
        @rtype: C{int}
        """
        return self._period

    def exchangeCounters(self):
        u"""
        Поменять местами теневой и текущий счетчик.
        """
        self.active = 1 - self.active
        self.counter[self.active] = 0
        self.increments[self.active] = 0
        reactor.callLater(self._period, self.exchangeCounters)

    def increment(self, value=1):
        u"""
        Увеличить значение счетчика на указанное значение.

        @param value: значение инкремента
        """
        self.counter[self.active] += value
        self.increments[self.active] += 1

    def label(self):
        u"""
        Подпись счетчика, описывающая период его работы.

        @rtype: C{str}
        """
        if self._period <= 60:
            return 'за %d секунд' % self._period
        return 'за %d минут' % (self._period // 60)

    def __getstate__(self):
        return {'period': self._period}

    def __setstate__(self, state):
        self.__init__(state['period'])


class AtomCounterEternal(object):
    """
    Одиночный счетчик за "весь период" (с момента создания счетчика).

    @ivar counter: значение счетчика
    @ivar start: время создания счетчика, секунды UTC
    @type start: C{int}
    """
    implements(IAtomCounter)

    def __init__(self):
        u"""
        Конструктор.
        """
        self.counter = 0
        self.increments = 0
        self.start = time()

    def value(self):
        u"""
        Текущее значение счетчика для данного периода.
        """
        return self.counter

    def count(self):
        u"""
        Число увеличений счетчика.

        @rtype: C{int}
        """
        return max(1, self.increments)

    def period(self):
        u"""
        Период времени, за который собирается значение счетчика.

        @return: период времени, секунды
        @rtype: C{int}
        """
        period = time() - self.start
        if period == 0:
            period = 1
        return period

    def increment(self, value=1):
        u"""
        Увеличить значение счетчика на указанное значение.

        @param value: значение инкремента
        """
        self.counter += value
        self.increments += 1

    def label(self):
        u"""
        Подпись счетчика, описывающая период его работы.

        @rtype: C{str}
        """
        return 'за всё время'

    def __getstate__(self):
        return 1

    def __setstate__(self, state):
        self.__init__()


class Counter(object):
    """
    Набор одиночных счетчиков, вместе рассчитывающих одно значение
    для нескольких периодов.

    @ivar counter: набор одиночных счетчиков
    @type counter: C{list(}L{IAtomCounter}C{)}
    """
    implements(ICounter)

    def increment(self, value=1):
        u"""
        Увеличить значение счетчика на указанное значение.

        @param value: значение инкремента
        """
        for counter in self.counters:
            counter.increment(value)

    def __str__(self):
        u"""
        Представить текущее состояние счетчика в понятном человеку виде.

        @rtype: C{str}
        """
        return (', ').join([ self.format() % value for value in self.values() ])

    def format(self):
        u"""
        Строка формата для вывода значения счетчика.
        """
        raise NotImplementedError

    def values(self):
        u"""
        Получить значения счетчиков в виде массива значений.
        """
        return [ (counter.label(), counter.value()) for counter in self.counters ]


class SpeedCounter(Counter):
    """
    Счетчик, измеряющий "скорость" величины (отношение ко времени).
    """

    def values(self):
        u"""
        Получить значения счетчиков в виде массива значений.
        """
        return [ (counter.label(), counter.value() * 1.0 / counter.period()) for counter in self.counters ]


class AverageCounter(Counter):
    """
    Счетчик, измеряющий среднее значение величины.
    """

    def values(self):
        u"""
        Получить значения счетчиков в виде массива значений.
        """
        return [ (counter.label(), counter.value() * 1.0 / counter.count()) for counter in self.counters ]


class RequestCounter(Counter):
    """
    Счетчик числа запросов.
    """

    def __init__(self):
        u"""
        Конструктор.
        """
        self.counters = [
         AtomCounterEternal(), AtomCounterPeriod(1800), AtomCounterPeriod(300), AtomCounterPeriod(60)]

    def format(self):
        u"""
        Строка формата для вывода значения счетчика.
        """
        return '%s: %d запросов'


class RequestPerSecondCounter(SpeedCounter):
    """
    Счетчик числа запросов в секунду.
    """

    def __init__(self):
        u"""
        Конструктор.
        """
        self.counters = [
         AtomCounterEternal(), AtomCounterPeriod(1800), AtomCounterPeriod(300), AtomCounterPeriod(60)]

    def format(self):
        u"""
        Строка формата для вывода значения счетчика.
        """
        return '%s: %.1f запросов/c'


class AverageServiceTimeCounter(AverageCounter):
    """
    Счетчик среднего времени обслуживания.
    """

    def __init__(self):
        u"""
        Конструктор.
        """
        self.counters = [
         AtomCounterEternal(), AtomCounterPeriod(1800), AtomCounterPeriod(300), AtomCounterPeriod(60)]

    def format(self):
        u"""
        Строка формата для вывода значения счетчика.
        """
        return '%s: среднее время обслуживания %.3f cек'