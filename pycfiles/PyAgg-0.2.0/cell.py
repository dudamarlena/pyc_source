# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/cell.py
# Compiled at: 2014-12-10 17:22:55
import logging
from pyage.core.inject import Inject
from pyage.core.address import Addressable
logger = logging.getLogger(__name__)

class Cell(Addressable):

    @Inject('algae_limit', 'cell_capacity')
    def __init__(self, algae=0):
        super(Cell, self).__init__()
        self._algae = algae
        self.forams = set()
        self._neighbours = []

    def insert_foram(self, foram):
        logger.info('inserting %s into %s' % (foram, self))
        if self.is_full():
            raise ValueError('cannot insert foram to full cell')
        self.forams.add(foram)
        foram.cell = self

    def remove_foram(self, foram):
        self.forams.remove(foram)
        foram.cell = None
        return foram

    def is_empty(self):
        return not self.forams

    def is_full(self):
        return len(self.forams) >= self.cell_capacity

    def take_algae(self, demand):
        to_let = min(demand, self._algae)
        self._algae -= to_let
        return to_let

    def get_algae(self):
        return self._algae

    def add_algae(self, algae):
        self._algae += algae
        self._algae = min(self._algae, self.algae_limit)

    def available_food(self):
        return self._algae + sum(map(lambda c: c.get_algae(), self._neighbours))

    def add_neighbour(self, cell):
        self._neighbours.append(cell)

    def get_neighbours(self):
        return self._neighbours

    def to_shadow(self):
        return (
         self.get_address(), self.available_food(), self._algae, self.is_full(),
         [ cell.get_address() for cell in self.get_neighbours()
         ])

    def __repr__(self):
        return '(%d, %s, %d)' % (self._algae, self.forams, self.available_food())