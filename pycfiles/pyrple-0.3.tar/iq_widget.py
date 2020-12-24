# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/iq_widget.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = '\nA widget for the iq modules\n'
from .base_module_widget import ModuleWidget
from qtpy import QtCore, QtWidgets

class IqWidget(ModuleWidget):
    """
    Widget for the IQ module
    """

    def init_gui(self):
        super(IqWidget, self).init_gui()
        for key, widget in self.attribute_widgets.items():
            layout = widget.layout_v
            self.attribute_layout.removeWidget(widget)

        self.attribute_widgets['bandwidth'].widget.set_max_cols(2)
        self.attribute_layout.addWidget(self.attribute_widgets['input'])
        self.attribute_layout.addWidget(self.attribute_widgets['acbandwidth'])
        self.attribute_layout.addWidget(self.attribute_widgets['frequency'])
        self.attribute_widgets['frequency'].layout_v.insertWidget(3, self.attribute_widgets['phase'])
        self.attribute_layout.addWidget(self.attribute_widgets['bandwidth'])
        self.attribute_layout.addWidget(self.attribute_widgets['quadrature_factor'])
        self.attribute_widgets['quadrature_factor'].widget.per_second = 10
        self.attribute_layout.addWidget(self.attribute_widgets['gain'])
        self.attribute_layout.addWidget(self.attribute_widgets['amplitude'])
        self.attribute_layout.addWidget(self.attribute_widgets['output_signal'])
        self.attribute_widgets['output_signal'].layout_v.insertWidget(3, self.attribute_widgets['output_direct'])
        self.attribute_layout.setStretch(0, 0)
        self.attribute_layout.addStretch(1)