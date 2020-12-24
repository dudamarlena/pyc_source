# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/pager/guisimconfpagertis.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 4444 bytes
"""
:mod:`PySide2`-based stack widget page controllers specific to tissue settings.
"""
from PySide2.QtWidgets import QMainWindow
from betse.lib.yaml.abc.yamlabc import YamlABC
from betse.science.config.model.conftis import SimConfTissueDefault
from betse.util.type.obj import objects
from betse.util.type.types import type_check
from betsee.util.widget.abc.guicontrolabc import QBetseeControllerABC

class QBetseeSimConfTissueDefaultStackedWidgetPager(QBetseeControllerABC):
    __doc__ = '\n    :mod:`PySide2`-based stack widget page controller, connecting all editable\n    widgets of the tissue page with the corresponding low-level settings of the\n    current simulation configuration.\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf = main_window.sim_conf
        tissue_default = sim_conf.p.tissue_default
        main_window.sim_conf_tis_default_name.init(sim_conf=sim_conf,
          sim_conf_alias=(SimConfTissueDefault.name),
          sim_conf_alias_parent=tissue_default)
        main_window.sim_conf_tis_default_image_line.init(sim_conf=sim_conf,
          sim_conf_alias=(SimConfTissueDefault.picker_image_filename),
          sim_conf_alias_parent=tissue_default,
          push_btn=(main_window.sim_conf_tis_default_image_btn),
          image_label=(main_window.sim_conf_tis_default_image_label))
        self._init_widgets_ion(main_window=main_window,
          page_conf=tissue_default)

    def _init_widgets_ion(self, main_window: QMainWindow, page_conf: YamlABC) -> None:
        """
        Initialize all ion-specific widgets on this page.

        Attributes
        ----------
        main_window : QMainWindow
            Main window singleton.
        page_conf : YamlABC
            YAML-backed simulation subconfiguration specific to this page.
        """
        ION_NAMES = {
         'Na', 'K', 'Cl', 'Ca', 'M', 'P'}
        sim_conf = main_window.sim_conf
        for ion_name in ION_NAMES:
            ion_widget_name = 'sim_conf_tis_default_mem_' + ion_name
            ion_descriptor_name = 'Dm_' + ion_name
            ion_widget = objects.get_attr(obj=main_window,
              attr_name=ion_widget_name)
            ion_descriptor = objects.get_attr(obj=SimConfTissueDefault,
              attr_name=ion_descriptor_name)
            ion_widget.init(sim_conf=sim_conf,
              sim_conf_alias=ion_descriptor,
              sim_conf_alias_parent=page_conf)