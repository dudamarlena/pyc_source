# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/guisimconflineedit.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 17045 bytes
"""
:class:`QLineEdit`-based simulation configuration widget subclasses.
"""
from PySide2.QtCore import QCoreApplication, Signal, Slot
from PySide2.QtWidgets import QLineEdit, QPushButton
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.path import pathnames
from betse.util.type.types import type_check, StrOrNoneTypes
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditscalar import QBetseeSimConfEditScalarWidgetMixin
from betsee.util.widget.abc.guiclipboardabc import QBetseeClipboardScalarWidgetMixin
from betsee.util.widget.stock.label.guilabelimage import QBetseeLabelImage

class QBetseeSimConfLineEdit(QBetseeClipboardScalarWidgetMixin, QBetseeSimConfEditScalarWidgetMixin, QLineEdit):
    __doc__ = '\n    Simulation configuration-specific line edit widget, interactively editing\n    single-line strings backed by external simulation configuration files.\n    '

    def setText(self, text_new):
        super().setText(text_new)
        self._set_alias_to_widget_value_if_safe()

    @property
    def undo_synopsis(self) -> str:
        return QCoreApplication.translate('QBetseeSimConfLineEdit', 'edits to a text box')

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        return self.editingFinished

    @property
    def widget_value(self) -> str:
        return self.text()

    @widget_value.setter
    @type_check
    def widget_value(self, widget_value):
        if not isinstance(widget_value, str):
            widget_value = str(widget_value)
        super().setText(widget_value)

    def _reset_widget_value(self) -> None:
        self.widget_value = ''


class QBetseeSimConfPathnameLineEditABC(QBetseeSimConfLineEdit):
    __doc__ = '\n    Abstract base class of all simulation configuration-specific pathname line\n    edit widget subclasses, interactively editing pathnames backed by external\n    simulation configuration files.\n    '

    @type_check
    def _init_safe(self, push_btn, *args, **kwargs):
        """
        Finalize the initialization of this line edit, associated with all
        passed **sibling buddy widgets** (i.e., widgets spatially adjacent to
        this line edit, whose initialization is finalized by this method in a
        manner informing these widgets of their association to this line edit).

        Parameters
        ----------
        push_btn : QPushButton
            Push button "buddy" associated with this line edit. To display a
            path dialog selecting this pathname when this button is clicked,
            this method connects the :meth:`QPushButton.clicked` signal of this
            button to the :meth:`_set_text_to_pathname_selected` slot of this
            line edit. By convention, this button is typically labelled
            "Browse..." and situated to the right of this line edit.

        All remaining parameters are passed as is to the superclass
        :meth:`QBetseeSimConfEditScalarWidgetMixin._init_safe` method.
        """
        (super()._init_safe)(*args, **kwargs)
        push_btn.clicked.connect(self._set_text_to_pathname_selected)

    @Slot()
    def _set_text_to_pathname_selected(self) -> None:
        """
        Slot setting the text displayed by this line edit to the possibly
        non-existing pathname selected by a subclass-specific path dialog
        satisfying various constraints (e.g., image, subdirectory).

        This slot is connected to the :attr:`clicked` signal of the push button
        associated with this line edit at widget finalization time, for safety.
        """
        old_pathname = self.text()
        new_pathname = self._select_pathname(old_pathname)
        if new_pathname is not None:
            self.setText(new_pathname)

    @type_check
    def _select_pathname(self, init_pathname: str) -> StrOrNoneTypes:
        """
        Possibly non-existing pathname interactively selected by the user on
        clicking the push button buddy associated with this line edit from a
        subclass-specific dialog displayed by this method if the user confirmed
        this dialog *or* ``None`` otherwise (i.e., if the user sadly cancelled
        this dialog).

        Parameters
        ----------
        init_pathname : str
            Pathname of the path to be initially displayed by this dialog
            (e.g., as externally specified by this simulation configuration).

        Returns
        ----------
        StrOrNoneTypes
            Either:

            * If this dialog was confirmed, the possibly non-existing pathname
              selected from this dialog.
            * Else, ``None``.
        """
        raise BetseMethodUnimplementedException()


class QBetseeSimConfPathnameImageLineEdit(QBetseeSimConfPathnameLineEditABC):
    __doc__ = '\n    Simulation configuration-specific **image filename** (i.e., filenames with\n    filetypes recognized by Pillow, the third-party image processing framework\n    leveraged by BETSE itself) line edit widget, interactively editing image\n    filenames backed by external simulation configuration files.\n\n    Attributes\n    ----------\n    _image_label : QLabel\n        Label "buddy" associated with this line edit. To preview the image\n        whose filename is the text displayed by this line edit, this label\'s\n        pixmap is read from this filename. By convention, this label is\n        typically situated below this line edit.\n\n    See Also\n    ----------\n    :func:`guifile.select_image_read`\n        Further details.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._image_label = None

    @type_check
    def _init_safe(self, image_label, *args, **kwargs):
        """
        Finalize the initialization of this line edit, associated with all
        passed **sibling buddy widgets** (i.e., widgets spatially adjacent to
        this line edit, whose initialization is finalized by this method in a
        manner informing these widgets of their association to this line edit).

        Parameters
        ----------
        image_label : QBetseeLabelImage
            Label "buddy" associated with this line edit. To preview the image
            whose filename is the text displayed by this line edit, this
            label's pixmap is read from this filename. By convention, this
            label is typically situated below this line edit. To preserve this
            image's aspect ratio, this widget is required to be an instance of
            the application-specific :class:`QBetseeLabelImage` class -- *not*
            the application-agnostic :class:`QLabel` class, which fails to
            preserve this image's aspect ratio.

        All remaining parameters are passed as is to the superclass
        :meth:`QBetseeSimConfPathnameLineEditABC._init_safe` method.
        """
        self._init_label(image_label)
        (super()._init_safe)(*args, **kwargs)

    @type_check
    def _init_label(self, image_label: QBetseeLabelImage) -> None:
        """
        Finalize the initialization of the passed label "buddy" associated with
        this line edit.

        See Also
        ----------
        :meth:`_init_safe`
            Further details.
        """
        self._image_label = image_label
        self._image_label.init_if_needed()
        self._image_label.setWordWrap(True)

    def _get_widget_from_alias_value(self):
        image_filename = super()._get_widget_from_alias_value()
        self._image_label.setVisible(self._is_sim_open)
        self._preview_image_if_sim_open(image_filename)
        return image_filename

    def _get_alias_from_widget_value(self):
        image_filename = super()._get_alias_from_widget_value()
        self._preview_image_if_sim_open(image_filename)
        return image_filename

    @type_check
    def _preview_image_if_sim_open(self, image_filename: str) -> None:
        """
        Display a preview of the image with the passed filename as the pixmap
        of the label associated with this line edit if this image is
        previewable *or* log and/or display a non-fatal warning otherwise.

        If no simulation configuration is open, this method safely reduces to a
        noop without erroneously handling this image.

        Parameters
        ----------
        image_filename : str
            Absolute or relative filename of the image to be previewed.
        """
        self._image_label.clear()
        if not self._is_sim_open:
            self._image_label.setText(QCoreApplication.translate('QBetseeSimConfPathnameImageLineEdit', 'N/A'))
            return
        image_filename_absolute = image_filename if pathnames.is_absolute(image_filename) else pathnames.join(self._sim_conf.dirname, image_filename)
        self._image_label.load_image(image_filename_absolute)

    @type_check
    def _select_pathname(self, init_pathname: str) -> StrOrNoneTypes:
        from betsee.util.path import guifile
        return guifile.select_image_read(init_pathname=init_pathname,
          parent_dirname=(self._sim_conf.dirname))


class QBetseeSimConfPathnameSubdirLineEdit(QBetseeSimConfPathnameLineEditABC):
    __doc__ = '\n    Simulation configuration-specific **subdirectory pathname** (i.e.,\n    pathnames of subdirectories of top-level simulation configuration\n    directories) line edit widget, interactively editing subdirectory pathnames\n    backed by external simulation configuration files.\n\n    For relocatability (i.e., to permit end users to trivially move simulation\n    configurations to different directories), this line edit displays only the\n    relative pathname of these subdirectories with respect to their parent\n    directories; their absolute pathnames are *not* displayed.\n\n    See Also\n    ----------\n    :func:`guidir.select_subdir`\n        Further details.\n    '

    @type_check
    def _select_pathname(self, init_pathname: str) -> StrOrNoneTypes:
        from betsee.util.path import guidir
        pathnames.die_if_absolute(init_pathname)
        return guidir.select_subdir(init_pathname=init_pathname,
          parent_dirname=(self._sim_conf.dirname))