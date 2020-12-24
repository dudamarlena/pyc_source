# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/mixin/guisimconfwdg.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 3699 bytes
"""
Abstract base classes of all simulation configuration widget subclasses
instantiated in pages of the top-level stack.
"""
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeWidgetMixinSimConf(QBetseeObjectMixin):
    __doc__ = '\n    Abstract base class of all **non-editable simulation configuration widget**\n    (i.e., widget *not* interactively editing simulation configuration values\n    stored in external YAML files) subclasses.\n\n    Design\n    ----------\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be subclassed *first* rather than *last* in subclasses.\n\n    Attributes\n    ----------\n    _sim_conf : QBetseeSimConf\n        High-level state of the currently open simulation configuration, which\n        depends on the state of this low-level simulation configuration widget.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._sim_conf = None

    @type_check
    def _init_safe(self, sim_conf: 'betsee.gui.simconf.guisimconf.QBetseeSimConf') -> None:
        """
        Finalize the initialization of this widget.

        Design
        ----------
        Subclasses should typically override this method with a
        subclass-specific implementation that (in order):

        #. Calls this superclass implementation, which sets instance variables
           typically required by subclass slots.
        #. Connects all relevant signals and slots.

        Connecting these signals and slots earlier in the :meth:`__init__`
        method is *not* recommended, even for slots that Qt technically should
        *never* invoke at that time. Why? Because Qt actually appears to
        erroneously emit signals documented as emitted only by external user
        action (e.g., :meth:`QLineEdit.editingFinished`) on internal code-based
        action (e.g., startup construction of the main window).

        Parameters
        ----------
        sim_conf : QBetseeSimConf
            High-level state of the currently open simulation configuration.
        """
        logs.log_debug('Initializing non-editable widget "%s"...', self.obj_name)
        self._sim_conf = sim_conf