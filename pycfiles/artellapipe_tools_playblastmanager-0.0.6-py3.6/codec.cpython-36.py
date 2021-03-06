# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/tools/playblastmanager/plugins/codec.py
# Compiled at: 2020-03-13 14:13:04
# Size of source mod 2**32: 3820 bytes
"""
Module that contains implementation for Playblast Codec Plugin
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtWidgets import *
import tpDcc as tp
from artellapipe.tools.playblastmanager.core import plugin

class CodecWidget(plugin.PlayblastPlugin, object):
    id = 'Codec'
    collapsed = True

    def __init__(self, project, config, parent=None):
        super(CodecWidget, self).__init__(project=project, config=config, parent=parent)

    def get_main_layout(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        return main_layout

    def ui(self):
        super(CodecWidget, self).ui()
        self.format = QComboBox()
        self.compression = QComboBox()
        self.quality = QSpinBox()
        self.quality.setMinimum(0)
        self.quality.setMaximum(100)
        self.quality.setValue(100)
        self.quality.setToolTip('Compression quality percentage')
        for widget in [self.format, self.compression, self.quality]:
            self.main_layout.addWidget(widget)

        self.format.currentIndexChanged.connect(self._on_format_changed)
        self.refresh()
        index = self.format.findText('qt')
        if index != -1:
            self.format.setCurrentIndex(index)
            index = self.compression.findText('H.264')
            if index != -1:
                self.compression.setCurrentIndex(index)

    def setup_signals(self):
        self.compression.currentIndexChanged.connect(self.optionsChanged)
        self.format.currentIndexChanged.connect(self.optionsChanged)
        self.quality.valueChanged.connect(self.optionsChanged)

    def get_inputs(self, as_preset=False):
        """
        Overrides base ArtellaPlayblastPlugin get_inputs function
        Returns a dict with proper input variables as keys of the dictionary
        :return: dict
        """
        return self.get_outputs()

    def get_outputs(self):
        """
         Overrides base ArtellaPlayblastPlugin get_outputs function
         Returns the outputs variables of the Playblast widget as dict
         :return: dict
         """
        return {'format':self.format.currentText(), 
         'compression':self.compression.currentText(), 
         'quality':self.quality.value()}

    def apply_inputs(self, attrs_dict):
        """
        Overrides base ArtellaPlayblastPlugin apply_inputs function
        Applies the given dict of attributes to the widget
        :param attrs_dict: dict
        """
        codec_format = attrs_dict.get('format', 0)
        compression = attrs_dict.get('compression', 4)
        quality = attrs_dict.get('quality', 100)
        try:
            self.format.setCurrentIndex(self.format.findText(codec_format))
            self.compression.setCurrentIndex(self.compression.findText(compression))
        except Exception:
            self.format.setCurrentIndex(codec_format)
            self.compression.setCurrentIndex(compression)

        self.quality.setValue(int(quality))

    def refresh(self):
        """
        Function that refreshes plugin UI
        """
        self.format.clear()
        self.format.addItems(sorted(tp.Dcc.get_playblast_formats()))

    def _on_format_changed(self):
        """
        Refresh available compressions
        """
        playblast_format = self.format.currentText()
        self.compression.clear()
        self.compression.addItems(tp.Dcc.get_playblast_compressions(playblast_format=playblast_format))