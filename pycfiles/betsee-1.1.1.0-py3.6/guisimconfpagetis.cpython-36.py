# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/page/space/guisimconfpagetis.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 10459 bytes
"""
**Tissue simulation configuration pager** (i.e., :mod:`PySide2`-based
controller for stack widget pages specific to tissue profiles) functionality.
"""
from PySide2.QtWidgets import QMainWindow
from betse.science.config.model.conftis import SimConfTissueABC
from betse.science.enum import enumion
from betse.util.type.obj import objects
from betse.util.type.iterable import sequences
from betse.util.type.types import type_check
from betsee.util.widget.abc.control.guictlpageabc import QBetseePagerABC, QBetseePagerItemizedMixin

class QBetseeSimConfPagerTissueABC(QBetseePagerABC):
    __doc__ = '\n    Abstract base class of all **tissue simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of a\n    stack widget page applicable to tissue profiles of a particular type with\n    corresponding settings of the current simulation configuration) subclasses.\n    '

    @type_check
    def init(self, main_window, widget_name_prefix, tissue_profile, is_reinitable=False):
        """
        Initialize this pager against the passed parent main window.

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., simulation configuration stack widget) of this window
        may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this pager.
        widget_name_prefix : str
            Substring prefixing the name of all instance variables of the
            passed ``main_window`` whose values are all child widgets of the
            page controlled by this pager.
        tissue_profile : SimConfTissueABC
            Current YAML-backed tissue profile subconfiguration (i.e.,
            :class:`SimConfTissueABC` instance) associated with this page.
        is_reinitable : bool
            ``True`` only if this method may be safely called multiple times.
            Defaults to ``False``.
        """
        super().init(main_window=main_window, is_reinitable=is_reinitable)
        tissue_profile_cls = type(tissue_profile)
        widget_name = main_window.get_widget(widget_name=(widget_name_prefix + 'name'))
        widget_image_filename = main_window.get_widget(widget_name=(widget_name_prefix + 'image_line'))
        widget_image_label = main_window.get_widget(widget_name=(widget_name_prefix + 'image_label'))
        widget_image_btn = main_window.get_widget(widget_name=(widget_name_prefix + 'image_btn'))
        widget_name.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(tissue_profile_cls.name),
          sim_conf_alias_parent=tissue_profile,
          is_reinitable=is_reinitable)
        widget_image_filename.init(sim_conf=(main_window.sim_conf),
          sim_conf_alias=(tissue_profile_cls.picker_image_filename),
          sim_conf_alias_parent=tissue_profile,
          push_btn=widget_image_btn,
          image_label=widget_image_label,
          is_reinitable=is_reinitable)
        for ion_name in enumion.iter_ion_names():
            ion_widget = main_window.get_widget(widget_name=('{}mem_{}'.format(widget_name_prefix, ion_name)))
            ion_descriptor = objects.get_attr(obj=tissue_profile_cls,
              attr_name=('Dm_' + ion_name))
            ion_widget.init(sim_conf=(main_window.sim_conf),
              sim_conf_alias=ion_descriptor,
              sim_conf_alias_parent=tissue_profile,
              is_reinitable=is_reinitable)


class QBetseeSimConfPagerTissueDefault(QBetseeSimConfPagerTissueABC):
    __doc__ = '\n    **Default tissue simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for the default tissue profile with corresponding\n    settings of the current simulation configuration).\n    '

    @type_check
    def init(self, main_window):
        super().init(main_window=main_window,
          widget_name_prefix='sim_conf_tis_default_',
          tissue_profile=(main_window.sim_conf.p.tissue_default))


class QBetseeSimConfPagerTissueCustom(QBetseePagerItemizedMixin, QBetseeSimConfPagerTissueABC):
    __doc__ = '\n    **Custom tissue simulation configuration pager** (i.e.,\n    :mod:`PySide2`-based controller connecting all editable widgets of the\n    stack widget page for the currently selected custom tissue profile with\n    corresponding settings of the current simulation configuration).\n\n    **This controller implements the well-known flyweight design pattern.**\n    Specifically, this single controller is shared between the zero or more\n    custom tissue profiles configured for this simulation and hence *cannot* be\n    implicitly initialized at application startup. Instead, this controller is\n    explicitly reinitialized in an on-the-fly manner immediately before this\n    page is displayed to edit a single such profile.\n    '

    @type_check
    def init(self, main_window: QMainWindow) -> None:
        pass

    @type_check
    def reinit(self, main_window, list_item_index):
        tissue_profile = sequences.get_index(sequence=(main_window.sim_conf.p.tissue_profiles),
          index=list_item_index)
        super().init(main_window=main_window,
          widget_name_prefix='sim_conf_tis_custom_',
          tissue_profile=tissue_profile,
          is_reinitable=True)