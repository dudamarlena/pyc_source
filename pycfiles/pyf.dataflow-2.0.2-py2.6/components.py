# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/dataflow/components.py
# Compiled at: 2010-08-11 04:35:42
from pyf.dataflow.core import runner, component
from pyf.dataflow.merging import merge_iterators
import itertools, operator, logging
logger = logging.getLogger()
from collections import deque
from itertools import repeat, chain, izip
try:
    from itertools import izip_longest
except ImportError, AttributeError:

    def izip_longest(*args, **kwds):
        """ Function only available in Python 2.6.
        Reimplemented in Python 2.5 for consistency reason.
        See http://docs.python.org/library/itertools.html#itertools.izip_longest
        """
        fillvalue = kwds.get('fillvalue')

        def sentinel(counter=([fillvalue] * (len(args) - 1)).pop):
            yield counter()

        fillers = repeat(fillvalue)
        iters = [ chain(it, sentinel(), fillers) for it in args ]
        try:
            for tup in izip(*iters):
                yield tup

        except IndexError:
            pass


class groupby(object):

    def __init__(self, iterable, key=None, use_buffer=False):
        if key is None:
            key = lambda x: x
        self.__use_buffer = use_buffer
        self.keyfunc = key
        self.it = iter(iterable)
        self.it_next = self.it.next
        self.tgtkey = self.currkey = self.currvalue = object()
        if use_buffer:
            self.deques = list()
        return

    def __iter__(self):
        return self

    def next(self):
        while self.currkey == self.tgtkey:
            self.currvalue = self.it_next()
            self.currkey = self.keyfunc(self.currvalue)
            if self.__use_buffer and self.currkey == self.tgtkey:
                if len(self.deques) > 0:
                    self.deques[(-1)].append(self.currvalue)

        self.tgtkey = self.currkey
        if self.__use_buffer:
            deq = deque()
            self.deques.append(deq)
            deq.append(self.currvalue)
            return (
             self.currkey,
             self._buffer_grouper(self.tgtkey, deq))
        else:
            return (
             self.currkey, self._grouper(self.tgtkey))

    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue
            self.currvalue = self.it_next()
            self.currkey = self.keyfunc(self.currvalue)

    def _buffer_grouper(self, tgtkey, grp_deque):
        while True:
            if grp_deque:
                yield grp_deque.popleft()
                continue
            else:
                if self.currkey != tgtkey:
                    break
                self.currvalue = self.it_next()
                self.currkey = self.keyfunc(self.currvalue)
                if not self.currkey == tgtkey:
                    break
                yield self.currvalue

        self.deques.remove(grp_deque)


@component('IN', 'OUTA')
def splitm(source, out, size=3):
    """ Splits a data source in n sources (size kwarg)"""
    yield (
     out.size(), size)
    for row in source:
        for i in range(size):
            yield (
             out(i), row)


@component('INA', 'OUT')
def sum(sources, out):
    """ yields a sum for data sources for each row.
    can also be used to concatenate lists """
    for row in itertools.izip(*sources):
        yield reduce(operator.add, row)


@component('IN', 'OUT')
def inc(value, out, step=1):
    """ increments each value with step kwarg 
    usefull to add a column to a table if passing lists as values,
    and list as step """
    for line in value:
        yield (
         out, line + step)


@component('INA', 'OUT')
def all_true_longest(sources, out):
    """ A function that verifies that all the sources still flowing are true.
    If a source doesn't have an item (too short), it is assumed as true.
    If all the sources are true, return true, else return False.
    Useful to check that everything worked in the end of the dataflow chain.
    """
    for row in izip_longest(*sources, **dict(fillvalue=True)):
        cur_state = True
        for item in row:
            cur_state = cur_state and item

        yield cur_state


@component('INA', 'OUT')
def status_lookup(sources, out, buffer_num_getters=None, clear_each=10, fillvalue=True):
    """ A function that yields statuses (True/False) and statuses from sources.
    
    It uses a list of buffer getters (functions) to know if there is any result
    left in buffer for a particular source.
    
    Every "clear_each" (nth) iteration it checks for the buffer and consumes it.
    
    This component is especially useful to synchronise sources so they consume
    their own sources in a pseudo synchronous way (useful in tree shapes).
    
    About performance :
    With clear_each set as 1 you can achieve a great memory consumption perf but
    this will reduce the performance of your loop.
    For relatively small records, a value of 10 to 100 is recommended.
    """
    if buffer_num_getters is None:
        raise ValueError('You should set getters for the buffer count')
    yield fillvalue
    sources = list(sources)
    burnt_sources = list()
    iteration = 0
    continue_sources = True
    while continue_sources:
        iteration += 1
        for (num, source) in enumerate(sources):
            continue_source = True
            try:
                while continue_source:
                    yield source.next()
                    if not iteration % clear_each:
                        if buffer_num_getters[num] is None or buffer_num_getters[num]() < 1:
                            continue_source = False
                    else:
                        continue_source = False

            except StopIteration:
                if num not in burnt_sources:
                    burnt_sources.append(num)
                continue_source = False
                yield fillvalue

        if len(burnt_sources) >= len(sources):
            continue_sources = False

    yield fillvalue
    return


@component('INA', 'OUT')
def all_true(sources, out):
    """ A function that verifies that all the sources are true.
    If all the sources are true, return true, else return False.
    Useful to check that everything worked in the end of the dataflow chain
    and to synchronize chain sizes.
    """
    for row in itertools.izip(*sources):
        yield reduce(operator.and_, row)


@component('IN', 'OUT')
def bufferize(source, out, chunk_size=20):
    """ Group items in buffers. Useful to write N items at once.
    IN: source, an iterator
    OUT: an iterator of groups
    kwarg chunk_size: size of the groups
    """
    buffer = list()
    for (i, v) in enumerate(source):
        buffer.append(v)
        if not (i + 1) % chunk_size and not i == 0:
            yield buffer
            buffer = list()

    if len(buffer):
        yield buffer


@component('OUT')
def generator_component(out, generator=None):
    for item in generator:
        yield item


def generator_to_component(generator):

    @component('OUT')
    def gencomponent(out, generator=generator):
        for item in generator:
            yield item

    return gencomponent


@component('IN', 'OUT')
def filter_values(values, out, comp=lambda x: True, add_ellipsis=False):
    for item in values:
        if comp(item):
            yield item
        elif add_ellipsis:
            yield Ellipsis


@component('INA', 'OUT')
def zip_merging(sources, out):
    for row in itertools.izip(*sources):
        yield row


@component('INA', 'OUT')
def linear_merging(sources, out, ports=None):
    for row in izip_longest(fillvalue=Ellipsis, *sources):
        for item in row:
            yield item


@component('INA', 'OUT')
def linear_merging_python(sources, out, ports=None):
    burnt_sources = list()
    sources = list(sources)
    while True:
        for source in sources:
            if source not in burnt_sources:
                try:
                    yield source.next()
                except StopIteration:
                    burnt_sources.append(source)

        if len(burnt_sources) >= len(sources):
            break


@component('INA', 'OUT')
def ordered_key_merging(sources, out, key=None):
    for row in merge_iterators(list(sources), key=key):
        yield row