# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/struct/nx_struct.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 2107 bytes
import networkx as nx

class NxStructure:
    __doc__ = 'A NxStructure is a structure based on a networkx graph.\n    '

    def __init__(self, *args, **kwargs):
        self.graph = nx.DiGraph()

    def draw_graphviz(self, path):
        with open(path, 'w') as (f):
            try:
                nx.nx_agraph.write_dot(self.graph, f)
            except:
                print("Error: can't create graphviz file...")

    def get_output_nodes(self):
        """Get nodes of 'graph' without successors.

        Return:
            list: the nodes without successors of a DiGraph.
        """
        nodes = list(self.graph.nodes())
        output_nodes = []
        for n in nodes:
            if len(list(self.graph.successors(n))) == 0:
                output_nodes.append(n)

        return output_nodes

    @staticmethod
    def create_tensor_aux(g, n, train=None):
        """Recursive function to create the tensors from the graph.

        Args:
            g (nx.DiGraph): a graph
            n (nx.Node): a node
            train (bool): True if the network is built for training, False if the network is built for validation/testing (for example False will deactivate Dropout).

        Return:
            the tensor represented by n.
        """
        try:
            if n._tensor != None:
                output_tensor = n._tensor
            else:
                pred = list(g.predecessors(n))
                if len(pred) == 0:
                    output_tensor = n.create_tensor(train=train)
                else:
                    tensor_list = list()
                    for s_i in pred:
                        tmp = NxStructure.create_tensor_aux(g,
                          s_i, train=train)
                        if type(tmp) is list:
                            tensor_list.extend(tmp)
                        else:
                            tensor_list.append(tmp)

                    output_tensor = n.create_tensor(tensor_list, train=train)
            return output_tensor
        except TypeError:
            raise RuntimeError(f"Failed to build tensors from :{n}")