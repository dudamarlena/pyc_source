# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/mixin/guisimconfwdgeditenum.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 7139 bytes
"""
Abstract base classes of all editable enumerative simulation configuration
widget subclasses instantiated in pages of the top-level stacked widget.
"""
from PySide2.QtCore import QCoreApplication, QObject
from betse.util.type.iterable.mapping import mappings
from betse.util.type.types import type_check, ClassOrNoneTypes, EnumClassType, MappingType
from betsee.guiexception import BetseePySideWidgetEnumException
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditscalar import QBetseeSimConfEditScalarWidgetMixin

class QBetseeSimConfEditEnumWidgetMixin(QBetseeSimConfEditScalarWidgetMixin):
    __doc__ = '\n    Abstract base class of all **editable enumerative simulation configuration\n    widget** (i.e., widget interactively selecting between the mutually\n    exclusive members of a simulation configuration enumeration stored in\n    external YAML files) subclasses.\n\n    Attributes\n    ----------\n    _enum_member_to_widget_value : MappingType\n        Dictionary mapping from each member of the enumeration constraining\n        this widget to the corresponding mutually exclusive value displayed by\n        this widget.\n    _widget_value_to_enum_member : MappingType\n        Dictionary mapping from each mutually exclusive value displayed by this\n        widget to the corresponding member of the enumeration constraining this\n        widget.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._enum_member_to_widget_value = None
        self._widget_value_to_enum_member = None

    @type_check
    def _init_safe(self, enum_member_to_widget_value, *args, **kwargs):
        """
        Finalize the initialization of this widget.

        Parameters
        ----------
        enum_member_to_widget_value : MappingType
            Dictionary mapping from each member of the enumeration encapsulated
            by the passed ``sim_conf_alias`` parameter to the corresponding
            mutually exclusive value displayed by this widget.

        All remaining parameters are passed as is to the superclass method.

        Raises
        ----------
        BetseMappingException
            If this dictionary is *not* safely invertible (i.e., if any value
            of this dictionary is non-uniquely assigned to two or more keys).
        BetseePySideRadioButtonException
            If the number of members in this enumeration differs from the
            number of members mapped by (i.e., of keys in) this dictionary.
        """
        (super()._init_safe)(*args, **kwargs)
        self._enum_member_to_widget_value = enum_member_to_widget_value
        self._widget_value_to_enum_member = mappings.invert_map_unique(enum_member_to_widget_value)
        enum_type = self._sim_conf_alias.data_desc.expr_alias_cls
        if len(enum_type) != len(enum_member_to_widget_value):
            raise BetseePySideWidgetEnumException(QCoreApplication.translate('QBetseeSimConfEditEnumWidgetMixin', 'Number of enumeration members {0} differs from number of mapped enumeration members {1}.'.format(len(enum_type), len(enum_member_to_widget_value))))

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        return EnumClassType

    def _get_alias_from_widget_value(self) -> object:
        widget_value = self.widget_value
        if widget_value not in self._widget_value_to_enum_member:
            widget_value_label = widget_value
            if isinstance(widget_value, QObject):
                widget_value_label = widget_value.objectName()
            raise BetseePySideWidgetEnumException(QCoreApplication.translate('QBetseeSimConfEditEnumWidgetMixin', 'Widget value "{0}" unrecognized.'.format(widget_value_label)))
        return self._widget_value_to_enum_member[widget_value]

    def _get_widget_from_alias_value(self) -> object:
        enum_member = self._sim_conf_alias.get()
        if enum_member not in self._enum_member_to_widget_value:
            raise BetseePySideWidgetEnumException(QCoreApplication.translate('QBetseeSimConfEditEnumWidgetMixin', 'Enumeration member "{0}" unrecognized.'.format(str(enum_member))))
        return self._enum_member_to_widget_value[enum_member]