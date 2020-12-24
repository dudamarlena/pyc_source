# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/agent/aggregate.py
# Compiled at: 2014-10-18 19:15:55
import logging
from pyage.core.address import Addressable
from pyage.core.inject import Inject
logger = logging.getLogger(__name__)

class ForamAggregateAgent(Addressable):

    @Inject('forams', 'environment')
    def __init__(self):
        super(ForamAggregateAgent, self).__init__()
        for foram in self.forams.values():
            foram.parent = self
            self.environment.add_foram(foram)

    def step(self):
        for foram in self.forams.values():
            foram.step()

        self.environment.tick(self.parent.steps)

    def remove_foram(self, address):
        foram = self.forams[address]
        del self.forams[address]
        foram.parent = None
        return foram

    def add_foram(self, foram):
        foram.parent = self
        self.forams[foram.get_address()] = foram