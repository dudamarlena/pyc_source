# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/image_converter.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2456 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import subprocess, os.path

class ImageConverter:
    __doc__ = "Takes GraphViz's graph in dot format and generates some derivative data.\n    "

    def __init__(self, dot_graph, dot_program_path='/usr/bin/dot'):
        """
        Args:
            dot_graph (string): description of graph in GraphViz's dot format
            dot_program_path (string): path to the `dot` program installed
                in the system along with GraphViz library
        """
        if not os.path.isfile(dot_program_path):
            raise Exception('Given path to "dot" program ("{}") is incorrect. It does not exist or it does not correspond to a file. This might mean that GraphViz library is not installed in the system.')
        self._ImageConverter__dot_graph = dot_graph
        self._ImageConverter__dot_program_path = dot_program_path

    def to_image_map(self):
        """
        Returns:
            string: client-size image map ready to be embedded in
                HTML document. This is GraphViz's `cmapx` output
                (see http://www.graphviz.org/doc/info/output.html#a:cmapx).
        """
        raise NotImplementedError

    def to_image(self):
        """Convert the dot graph to a PNG image

        Return:
            byte string
        """
        p = subprocess.Popen([self._ImageConverter__dot_program_path, '-Tpng'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(self._ImageConverter__dot_graph.encode('utf-8'))
        if len(stderr) > 0:
            raise Exception('Error output produced while running dot program: {} '.format(str(stderr)))
        return stdout