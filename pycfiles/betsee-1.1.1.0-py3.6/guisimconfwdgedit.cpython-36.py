# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/mixin/guisimconfwdgedit.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 13324 bytes
"""
Abstract base classes of all editable simulation configuration widget
subclasses instantiated in pages of the top-level stack.
"""
from PySide2.QtCore import QCoreApplication, Slot
from betse.lib.yaml.abc.yamlabc import YamlABCOrNoneTypes
from betse.lib.yaml.yamlalias import YamlAliasABC
from betse.util.io.log import logs
from betse.util.type.descriptor.datadescs import DataDescriptorBound
from betse.util.type.types import type_check, ClassOrNoneTypes
from betsee.guiexception import BetseePySideWidgetException
from betsee.util.widget.mixin.guiwdgeditmixin import QBetseeEditWidgetMixin

class QBetseeSimConfEditWidgetMixin(QBetseeEditWidgetMixin):
    __doc__ = '\n    Abstract base class of all **editable simulation configuration widget**\n    (i.e., widget interactively editing simulation configuration values stored\n    in external YAML files) subclasses.\n\n    Design\n    ----------\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be subclassed *first* rather than *last* in subclasses.\n\n    Attributes\n    ----------\n    _sim_conf : QBetseeSimConf\n        High-level state of the currently open simulation configuration, which\n        depends on the state of this low-level simulation configuration widget.\n    _sim_conf_alias : DataDescriptorBound\n        high-level object wrapping the low-level data descriptor of the\n        :class:`betse.science.parameters.Parameters` class, itself wrapping the\n        lower-level simulation configuration option edited by this widget.\n    _sim_conf_alias_type : ClassOrNoneTypes\n        Class or tuple of classes that the value to which\n        :attr:`_sim_conf_alias` evaluates is required to be an instance of if\n        any *or* ``None`` otherwise.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._sim_conf = None
        self._sim_conf_alias = None
        self._sim_conf_alias_type = None

    @type_check
    def _init_safe(self, sim_conf, sim_conf_alias, sim_conf_alias_parent=None, *args, **kwargs):
        """
        Finalize the initialization of this widget.

        Parameters
        ----------
        sim_conf : QBetseeSimConf
            High-level state of the currently open simulation configuration.
        sim_conf_alias : YamlAliasABC
            Low-level data descriptor bound to the simulation configuration
            setting edited by this widget -- typically a
            :class:`betse.science.params.Parameters`-specific class variable
            assigned the return value of the
            :func:`betse.science.config.confabc.yaml_alias` function.
        sim_conf_alias_parent : YamlABCOrNoneTypes
            YAML-backed simulation subconfiguration whose class declares the
            passed data descriptor. Defaults to ``None``, in which case this
            parameter defaults to ``sim_conf.p`` (i.e., the top-level
            YAML-backed simulation configuration).

        All remaining parameters are passed as is to the
        :meth:`QBetseeEditWidgetMixin._init_safe` method.

        See Also
        ----------
        :meth:`QBetseeWidgetMixinSimConf._init_safe`
            Further details.
        """
        (super()._init_safe)(args, undo_stack=sim_conf.undo_stack, **kwargs)
        logs.log_debug('Initializing editable widget "%s"...', self.obj_name)
        if sim_conf_alias_parent is None:
            sim_conf_alias_parent = sim_conf.p
        self._sim_conf = sim_conf
        self._sim_conf_alias = DataDescriptorBound(obj=sim_conf_alias_parent,
          data_desc=sim_conf_alias)
        self._sim_conf_alias_type = sim_conf_alias.expr_alias_cls
        self._die_if_sim_conf_alias_type_invalid()
        self._sim_conf.set_filename_signal.connect(self._set_filename)
        if self._sim_conf.is_open:
            logs.log_debug('Repopulating dynamic editable widget "%s"...', self.obj_name)
            self._set_filename(self._sim_conf.filename)

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        """
        Type of the simulation configuration setting edited by this widget if
        this widget is strictly constrained to values of only a single type
        *or* ``None`` otherwise (i.e., if this widget permissively displays
        values satisfying any one of several different types).

        By default, this method returns ``None``.

        Caveats
        ----------
        **Subclasses must override either this or the comparable
        :meth:`_die_if_sim_conf_alias_type_invalid` method.** Specifically, any
        subclass *not* already overriding this method must override the
        :meth:`_die_if_sim_conf_alias_type_invalid` method instead.
        Non-compliant subclasses overriding neither method will fail to
        validate the type of the current value of this simulation
        configuration setting, inviting subtle runtime type errors.

        See Also
        ----------
        :meth:`QBetseeSimConfEditScalarWidgetMixin.widget_value`
            Downstream property whose docstring documents the distinction
            between the following two related types:

            * The low-level type of all possible values of this simulation
              configuration setting returned by this method.
            * The high-level type of all possible :mod:`PySide2`-specific
              scalar values displayed by this widget *not* returned by this
              method.
        """
        pass

    def _die_if_sim_conf_alias_type_invalid(self) -> None:
        """
        Raise an exception if the types of low-level values exposed by the
        simulation configuration alias associated with this widget are
        unsupported by this widget's subclass.
        """
        if self._sim_conf_alias_type_strict is None:
            return
        else:
            is_sim_conf_alias_type_invalid = None
            if self._sim_conf_alias_type is tuple:
                is_sim_conf_alias_type_invalid = self._sim_conf_alias_type_strict not in self._sim_conf_alias_type
            else:
                is_sim_conf_alias_type_invalid = not issubclass(self._sim_conf_alias_type, self._sim_conf_alias_type_strict)
        if is_sim_conf_alias_type_invalid:
            raise BetseePySideWidgetException(QCoreApplication.translate('QBetseeSimConfEditWidgetMixin', 'Widget "{0}" YAML alias type {1!r} != {2!r} (i.e., expected a type compatible with {2!r} but received an incompatible type {1!r}).'.format(self.obj_name, self._sim_conf_alias_type, self._sim_conf_alias_type_strict)))

    @property
    def _is_sim_open(self) -> bool:
        """
        ``True`` only if a simulation configuration file is currently open.
        """
        return self._sim_conf is not None and self._sim_conf.is_open

    @Slot(str)
    def _set_filename(self, filename: str) -> None:
        """
        Slot signalled on the opening of a new simulation configuration *and*
        closing of an open simulation configuration.

        Design
        ----------
        Subclasses are recommended to override this method by (in order):

        #. Calling this superclass implementation.
        #. If this filename is non-empty, populating this widget's contents
           with the current value of the simulation configuration alias
           associated with this widget.

        Parameters
        ----------
        filename : str
            Either:

            * If the user opened a new simulation configuration file, the
              non-empty absolute filename of that file.
            * If the user closed an open simulation configuration file, the
              empty string.
        """
        pass

    def _update_sim_conf_dirty(self) -> None:
        """
        Update the dirty state for the current simulation configuration if this
        widget has been initialized with such a configuration *or* noop
        otherwise.

        This method is intended to be called by subclass slots on completion of
        user edits to the contents of this widget. In response, this method
        notifies all connected slots that this simulation configuration has
        received new unsaved changes.
        """
        if self._sim_conf is None:
            return
        is_dirty = self._is_undo_stack_dirty()
        logs.log_debug('Setting simulation configuration dirty bit from editable widget "%s" to "%r"...', self.obj_name, is_dirty)
        self._sim_conf.set_dirty_signal.emit(is_dirty)