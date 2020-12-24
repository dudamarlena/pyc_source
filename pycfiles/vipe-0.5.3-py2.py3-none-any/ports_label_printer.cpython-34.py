# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/ports_label_printer.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 3186 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from io import StringIO

class PortName:

    def __init__(self, label, internal_name):
        """Args:
            label (string): name of the label to be displayed
            internal_name (string): name of the label used internally in the
                definition of the dot format. It is unique for given node.
        """
        self.label = label
        self.internal_name = internal_name


class PortsLabelPrinter:
    __doc__ = "Creates a dot format label that shows node's ports."

    def __init__(self):
        self._PortsLabelPrinter__s = None

    def __pr(self, text):
        print(text, file=self._PortsLabelPrinter__s)

    def run(self, labels, input_port_names, output_port_names, color):
        """Args:
            labels (List[string]): list of labels to be printed in the node.
                Each label is placed in a separate line.
            input_port_names (List[PortName]): input port names
            output_port_names (List[PortName]): output port names
            color (string): value taken from
                http://graphviz.org/doc/info/colors.html
        """
        self._PortsLabelPrinter__s = StringIO()
        height = max(len(input_port_names), len(output_port_names), len(labels))
        self._PortsLabelPrinter__pr('<')
        self._PortsLabelPrinter__pr('<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">')
        self._PortsLabelPrinter__pr('  <TR>')
        self._PortsLabelPrinter__print_ports(input_port_names, height, True)
        self._PortsLabelPrinter__pr('    <TD ROWSPAN="{}" BGCOLOR="{}" BORDER="1">{}</TD>'.format(height, color, '<BR/>'.join(labels)))
        self._PortsLabelPrinter__print_ports(output_port_names, height, False)
        self._PortsLabelPrinter__pr('  </TR>')
        self._PortsLabelPrinter__pr('</TABLE>>')
        return self._PortsLabelPrinter__s.getvalue()

    def __print_ports(self, port_names, height, are_input_ports):
        if len(port_names) == 0:
            return
        self._PortsLabelPrinter__pr('    <TD ROWSPAN="{}">'.format(height))
        self._PortsLabelPrinter__pr('      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">')
        for port in port_names:
            label = None
            align = None
            if are_input_ports:
                label = '&#9654; {}'.format(port.label)
                align = 'LEFT'
            else:
                label = '{} &#9654;'.format(port.label)
                align = 'RIGHT'
            self._PortsLabelPrinter__pr('        <TR><TD ALIGN="{}" PORT="{}">{}</TD></TR>'.format(align, port.internal_name, label))

        for _ in range(height - len(port_names)):
            self._PortsLabelPrinter__pr('        <TR><TD BORDER="0"> </TD></TR>')

        self._PortsLabelPrinter__pr('      </TABLE>')
        self._PortsLabelPrinter__pr('    </TD>')