# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/low_score_nodes_remover.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2434 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import copy

class LowScoreNodesRemover:
    _LowScoreNodesRemover__lowest_acceptable_score = -2

    def __init__(self, importance_score_map):
        """Args:
            importance_score_map (ImportanceScoreMap):
        """
        self._LowScoreNodesRemover__score_map = importance_score_map

    def run(self, pipeline):
        """Remove nodes with importance score value below a threshold.

        Apart from the low score, another condition must hold for a given node
        to be removed. Namely, given node has to lack either input or output
        ports. This condition is a substitute of removing nodes with either
        no incoming or no outcoming connections. We could later implement a
        more precise solution where existing connections are checked
        (this makes sense because there might be a situation that we have a
        port, but it is not connected to anything)

        Note that we focus here on removing nodes with either incoming or
        outcoming connections missing and this is because removing such nodes
        from a graph is easy. However, if required, we might
        implement a solution that removes also nodes with both
        incoming and outcoming connections present.

        Args:
            pipeline (Pipeline): input pipeline.

        Return:
            Pipeline: a copy of the input pipeline with some nodes removed.
        """
        result = copy.deepcopy(pipeline)
        names = list(result.nodes.keys())
        for name in names:
            node = result.nodes[name]
            if self._LowScoreNodesRemover__score_map.get_score(node.importance) < self._LowScoreNodesRemover__lowest_acceptable_score:
                if len(node.output_ports) == 0 or len(node.input_ports) == 0:
                    del result.nodes[name]
                else:
                    continue

        return result