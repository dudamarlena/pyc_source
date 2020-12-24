# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/connect.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 1141 bytes
from deephyper.search.nas.model.space.op import Operation

class Connect(Operation):
    __doc__ = 'Connection node.\n\n    Represents a possibility to create a connection between n1 -> n2.\n\n    Args:\n        graph (nx.DiGraph): a graph\n        n1 (Node): starting node\n        n2 (Node): arrival node\n    '

    def __init__(self, struct, n1, n2, *args, **kwargs):
        self.struct = struct
        self.n1 = n1
        self.n2 = n2

    def __str__(self):
        if type(self.n1) is list:
            if len(self.n1) > 0:
                ids = str(self.n1[0].id)
                for n in self.n1[1:]:
                    ids += ',' + str(n.id)

            else:
                ids = 'None'
        else:
            ids = self.n1.id
        return f"{type(self).__name__}_{ids}->{self.n2.id}"

    def init(self):
        """Set the connection in the structur graph from [n1] -> n2.
        """
        if type(self.n1) is list:
            for n in self.n1:
                self.struct.connect(n, self.n2)

        else:
            self.struct.connect(self.n1, self.n2)

    def __call__(self, value, *args, **kwargs):
        return value