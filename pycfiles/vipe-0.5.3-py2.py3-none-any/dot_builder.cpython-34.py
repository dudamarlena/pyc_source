# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/dot_builder.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 5327 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import io, re

class DotBuilder:
    __doc__ = "Tool for creating description of the graph using GraphViz's dot format.\n    "
    _DotBuilder__whitespace_pattern = re.compile('\\s+')

    def __init__(self, vertical_orientation=True):
        """Args:
            vertical_orientation (bool): True if the graph should be drawn
                from top to bottom, False if it should be drawn from left to
                right.
        """
        self._DotBuilder__s = io.StringIO()
        self._DotBuilder__build_finished = False
        self._DotBuilder__print('digraph {')
        if not vertical_orientation:
            self._DotBuilder__print('rankdir=LR')

    def add_edge(self, start, start_output_port, end, end_input_port, label=None):
        """
        Args:
            start (string): label of the start node
            start_output_port (string): name of the start node's output port.
                If None, the node will be connected directly, not through
                its port (if any).
            end (string): label of the end node
            end_input_port (string): name of the end node's input port.
                If None, the node will be connected directly, not through
                its port (if any).
            label (string): label of the edge.
        """
        assert not self._DotBuilder__build_finished
        connection_text = '{} -> {}'.format(self._DotBuilder__build_edge_point(start, start_output_port), self._DotBuilder__build_edge_point(end, end_input_port))
        parameters = []
        if label is not None:
            parameters.append('label="{}"'.format(self._DotBuilder__normalize_label(label)))
        if len(parameters) == 0:
            self._DotBuilder__print(connection_text)
        else:
            self._DotBuilder__print('{}[{}]'.format(connection_text, ' '.join(parameters)))

    @staticmethod
    def __build_edge_point(node, port):
        text = ['"{}"'.format(node)]
        if port is not None:
            text.append(':')
            text.append('"{}"'.format(port))
        return ''.join(text)

    def add_node(self, name, labels=None, color=None, shape=None, width=None, height=None, use_raw_labels=False):
        """
        Args:
            labels (List[string]): list of labels to be printed in the node.
            Each label is placed in a separate line.
            color (string): value taken from
                http://graphviz.org/doc/info/colors.html
            shape (string): value taken from
                http://graphviz.org/doc/info/shapes.html
            width (float): width of the node in inches. See
                http://graphviz.org/doc/info/attrs.html#d:width for details.
            height (float): height of the node in inches. See
                http://graphviz.org/doc/info/attrs.html#d:height for details.
            use_raw_labels (bool): if True, the labels given as the input
                is not preprocessed.
        """
        assert not self._DotBuilder__build_finished
        if labels is None and color is None and shape is None and width is None and height is None:
            return
        params = []
        if labels is not None:
            text = []
            for label in labels:
                processed_label = label
                if not use_raw_labels:
                    processed_label = self._DotBuilder__normalize_label(label)
                text.append(processed_label)

            final_label_text = '\\n'.join(text)
            if not use_raw_labels:
                final_label_text = '"{}"'.format(final_label_text)
            params.append('label={}'.format(final_label_text))
        if color is not None:
            params.append('fillcolor={},style=filled'.format(color))
        if shape is not None:
            params.append('shape={}'.format(shape))
        if width is not None or height is not None:
            params.append('fixedsize=true')
            if width is not None:
                params.append('width={}'.format(width))
            if height is not None:
                params.append('height={}'.format(height))
        self._DotBuilder__print('"{}" [{}]'.format(name, ' '.join(params)))

    def get_result(self):
        """
        Returns:
            string: graph description in dot format
        """
        if self._DotBuilder__build_finished is False:
            self._DotBuilder__build_finished = True
            self._DotBuilder__print('}')
        return self._DotBuilder__s.getvalue()

    def __print(self, text):
        print(text, file=self._DotBuilder__s)

    @staticmethod
    def __normalize_label(label):
        text = label
        text = text.replace('"', "'")
        text = re.sub(DotBuilder._DotBuilder__whitespace_pattern, ' ', text)
        return text