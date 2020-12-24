# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/pager/guisimconfpagerion.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 3106 bytes
"""
:mod:`PySide2`-based stack widget page controllers specific to ions.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QMainWindow
from betse.science.parameters import Parameters
from betse.science.config.confenum import IonProfileType
from betse.util.type.types import type_check
from betse.util.type.mapping.mapcls import OrderedArgsDict
from betsee.util.widget.abc.guicontrolabc import QBetseeControllerABC

class QBetseeSimConfIonStackedWidgetPager(QBetseeControllerABC):
    __doc__ = '\n    :mod:`PySide2`-based stack widget page controller, connecting all editable\n    widgets of the ion page with the corresponding low-level settings of the\n    current simulation configuration.\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window)
        sim_conf = main_window.sim_conf
        main_window.sim_conf_ion_profile.init(sim_conf=sim_conf,
          sim_conf_alias=(Parameters.ion_profile),
          enum_member_to_item_text=(OrderedArgsDict(IonProfileType.BASIC, QCoreApplication.translate('QBetseeSimConfIonStackedWidgetPage', 'Basic'), IonProfileType.BASIC_CA, QCoreApplication.translate('QBetseeSimConfIonStackedWidgetPage', 'Basic + Ca2+'), IonProfileType.MAMMAL, QCoreApplication.translate('QBetseeSimConfIonStackedWidgetPage', 'Mammal'), IonProfileType.AMPHIBIAN, QCoreApplication.translate('QBetseeSimConfIonStackedWidgetPage', 'Amphibian'), IonProfileType.CUSTOM, QCoreApplication.translate('QBetseeSimConfIonStackedWidgetPage', 'Custom'))))
        main_window.sim_conf_ion_custom.setVisible(False)