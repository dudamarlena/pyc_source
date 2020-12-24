# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/label/guilabelimage.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 19564 bytes
"""
**Image label** (i.e., :mod:`QLabel`-based widgets natively preserving the
aspect ratios of all images added to these widgets) facilities.
"""
from PySide2.QtCore import Qt, QCoreApplication, QSize
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QFrame, QLabel, QScrollArea
from betse.lib.pil import pils
from betse.util.io.log import logs
from betse.util.path import pathnames, paths
from betse.util.type.cls import classes
from betse.util.type.text import mls
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeLabelImage(QBetseeObjectMixin, QLabel):
    __doc__ = "\n    :mod:`QLabel`-based widget preserving the aspect ratio of the optional\n    **pixmap** (i.e., in-memory image) added to this widget.\n\n    By default, pixmaps added to :class:`QLabel` widgets are stretched to fit\n    layout requirements -- commonly resulting in unappealing deformation of\n    pixmaps added to these widgets. This derivative widget corrects this\n    harmful behaviour by constraining the aspect ratio of this widget to be\n    equal to the aspect ratio of the contained pixmap if any. To do so:\n\n    * The width of this widget is always preserved as is.\n    * The height of this widget is dynamically set to be the width of this\n      widget multiplied by the aspect ratio of the contained pixmap if any,\n      thus constraining the aspect ratio of this widget to be the same.\n\n    This widget supports all image filetypes supported by standard Qt widgets.\n    Specifically, all images whose filetypes are in the system-specific set\n    returned by the\n    :func:`betse.util.path.guifiletype.get_image_read_filetypes` function are\n    explicitly supported.\n\n    Caveats\n    ----------\n    This widget *must* be contained in a :class:`QScrollArea` widget.\n    Equivalently, some transitive parent widget of this widget *must* be a\n    :class:`QScrollArea` widget. If this is *not* the case when the\n    :meth:`_init_safe` method finalizing this widget's initialization is\n    called, that method explicitly raises an exception.\n\n    Why? Because size hints for widgets residing outside of\n    :class:`QScrollArea` widgets are typically silently ignored. This widget\n    declares a size hint preserving the aspect ratio of its pixmap. If this\n    size hint is silently ignored, this pixmap's aspect ratio will typically be\n    silently violated. Since this widget type exists *only* to preserve this\n    aspect ratio, this constitutes a fatal error.\n\n    Recursion\n    ----------\n    There exists circumstantial online evidence that this widget can\n    *effectively* induces infinite recursion in edge cases. Specifically, `it\n    has been asserted elsewhere <recursion claim_>`__ that:\n\n    * :meth:`QBetseeLabelImage.resizeEvent` calls\n      :meth:`QBetseeLabelImage.setPixmap`.\n    * :meth:`QBetseeLabelImage.setPixmap` calls\n      :meth:`QLabel.setPixmap`.\n    * :meth:`QLabel.setPixmap` calls :meth:`QLabel.updateLabel`.\n    * :meth:`QLabel.updateLabel` calls :meth:`QLabel.updateGeometry`.\n    * :meth:`QLabel.updateGeometry` may conditionally call\n      :meth:`QLabel.resize` in edge cases.\n    * :meth:`QLabel.resize` queues a new resize event for this label.\n    * The Qt event loop processes this event by calling\n      :meth:`QLabel.resizeEvent`, completing the recursive cycle.\n\n    Technically speaking, no recursive cycle exists. Due to indirection\n    introduced by event handling, the :meth:`QLabel.resize` and\n    :meth:`QLabel.resizeEvent` methods are called in different branches of the\n    call stack. Ergo, the above call chain should noticeably degrade\n    application performance *without* fatally exhausting the stack. Sadly,\n    since these methods are called sequentially rather than recursively,\n    detecting and guarding against this edge case is infeasible. (It could be\n    worse.)\n\n    Practically speaking, we were unable to replicate this worst-case issue.\n    Since we cannot replicate it, we cannot resolve it. We have elected instead\n    to do nothing, accepting that this may become a demonstrable issue later.\n\n    .. _recursion claim:\n        https://stackoverflow.com/a/41403419/2809027\n\n    Attributes\n    ----------\n    _pixmap : (QPixmap, NoneType)\n        Pixmap added to this widget by an external call to the\n        :meth:`setPixmap` method if that method has been called *or* ``None``\n        otherwise.\n\n    See Also\n    ----------\n    https://stackoverflow.com/a/22618496/2809027\n        StackOverflow answer inspiring this implementation.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._pixmap = None
        self.setFrameShape(QFrame.StyledPanel)
        self.setScaledContents(False)

    def _init_safe(self, *args, **kwargs):
        """
        Finalize the initialization of this widget.

        Raises
        ----------
        BetseePySideWidgetException
            If this widget is *not* contained in a :class:`QScrollArea` widget.
            See the class docstring for commentary.
        """
        from betsee.util.widget import guiwdg
        (super()._init_safe)(*args, **kwargs)
        guiwdg.die_unless_widget_parent_satisfies(widget=self,
          predicate=(lambda widget_parent: isinstance(widget_parent, QScrollArea)))

    @property
    def _is_pixmap(self) -> bool:
        """
        ``True`` only if this label has a pixmap that is *not* the null pixmap.
        """
        return self._pixmap is not None and not self._pixmap.isNull()

    def sizeHint(self) -> QSize:
        """
        Preferred size for this label, defined in a manner preserving both this
        label's existing width *and* this label's pixmap's aspect ratio.

        If this property is *not* overridden in this manner, the
        :meth:`setPixmap` method rescaling this pixmap and hence this label
        gradually increase the size of this label to this preferred size over a
        lengthy (and hence unacceptable) period of nearly ten seconds. Hence,
        overriding this is non-optional.
        """
        label_width = self.width()
        return QSize(label_width, self.heightForWidth(label_width))

    def heightForWidth(self, label_width_new: int) -> int:
        """
        Preferred height for this widget given the passed width if this
        widget's height depend on its width *or* -1 otherwise (i.e., if this
        widget's height is independent of its width).

        Parameters
        ----------
        label_width_new : int
            Width that this widget is being externally resized to.

        Returns
        ----------
        int
            Either:

            * If this widget contains a **non-null pixmap** (i.e., if the
              :meth:`setPixmap` method of this widget has been passed a pixmap
              whose :meth:`QPixmap.isNull` method returns ``False``), the
              returned height is guaranteed to preserve the aspect ratio of
              this pixmap with respect to the passed width.
            * Else (i.e., if this widget either contains no pixmap *or*
              contains the null pixmap), the returned height is this widget's
              current height unmodified.
        """
        if self._is_pixmap:
            return round(self._pixmap.height() * label_width_new / self._pixmap.width())
        else:
            return self.height()

    @type_check
    def setPixmap(self, pixmap):
        """
        Set this label's pixmap to the passed pixmap, internally rescaled to
        this label's current size.

        Under ideal circumstances, this label's current size is identical to
        this label's **preferred size** (i.e., the size returned by the
        :meth:`sizeHint` method). Since the latter is overridden by this
        widget to preserve the aspect ratio of this pixmap, this pixmap's new:

        * Width will be the current width of this label.
        * Height will be a function of this width preserving the aspect ratio
          of this pixmap.

        For aesthetics, this pixmap is rescaled with smooth bilinear filtering
        rather than with the default non-smooth transition.

        Parameters
        ----------
        pixmap : QPixmap
            Pixmap to be set as this label's pixmap
        """
        self._pixmap = pixmap
        pixmap_size_old = pixmap.size()
        pixmap_size_new = self.sizeHint()
        logs.log_debug('Rescaling label pixmap from %dx%d to %dx%d...', pixmap_size_old.width(), pixmap_size_old.height(), pixmap_size_new.width(), pixmap_size_new.height())
        pixmap_rescaled = pixmap.scaled(pixmap_size_new, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super().setPixmap(pixmap_rescaled)

    def resizeEvent(self, *args, **kwargs):
        (super().resizeEvent)(*args, **kwargs)
        if self._is_pixmap:
            logs.log_debug('Rescaling pixmap after resizing label...')
            self.setPixmap(self._pixmap)

    @type_check
    def load_image(self, filename: str) -> None:
        """
        Load the image with the passed filename as this label's pixmap in a
        sensible manner preserving the aspect ratio of this image.

        For safety, this method preferentially displays otherwise fatal errors
        resulting from this loading process as non-fatal warnings set as this
        label's text. Since this widget is typically *only* leveraged as an
        image previewer, the failure to preview arbitrary user-defined images
        of dubious origin, quality, and contents and possibly unsupported
        filetype should *not* halt the entire application. Ergo, it doesn't.

        Parameters
        ----------
        filename : str
            Absolute or relative filename of the image to be loaded.
        """
        from betsee.util.path import guifiletype
        basename = pathnames.get_basename(filename)
        filetype = pathnames.get_filetype_undotted_or_none(filename)
        logs.log_debug('Previewing image "%s"...', basename)
        try:
            if not paths.is_readable(filename):
                self._warn(QCoreApplication.translate('QBetseeLabelImage', 'Image "{0}" not found or unreadable.'.format(filename)))
                return
            else:
                if filetype is None:
                    self._warn(QCoreApplication.translate('QBetseeLabelImage', 'Image "{0}" has no filetype.'.format(filename)))
                    return
                filetypes_pil = pils.get_filetypes()
                filetypes_qt = guifiletype.get_image_read_filetypes()
                if filetype not in filetypes_pil:
                    self._warn(QCoreApplication.translate('QBetseeLabelImage', 'Image filetype "{0}" unrecognized by Pillow.'.format(filetype)))
                    return
                if filetype not in filetypes_qt:
                    self._warn(QCoreApplication.translate('QBetseeLabelImage', 'Image filetype "{0}" not previewable.'.format(filetype)))
                    return
            pixmap = QPixmap(filename)
            self.setPixmap(pixmap)
        except Exception as exception:
            exception_type = classes.get_name_unqualified(exception)
            exception_message = str(exception)
            self._warn(QCoreApplication.translate('QBetseeLabelImage', 'Image "{0}" preview failed with "{1}": {2}'.format(basename, exception_type, exception_message)))

    @type_check
    def _warn(self, warning: str) -> None:
        """
        Set the passed human-readable message as this label's text, log this
        message as a warning, and remove this label's existing pixmap if any.

        For clarity, this message is embedded in rich text (i.e., HTML)
        visually accentuating this message in a manner indicative of warnings
        -- notably, with boldened red text.

        Caveats
        ----------
        **This message is logged as is and hence assumed to be plaintext.** All
        HTML syntax (e.g., ``&amp;``, ``<table>``) embedded in this message is
        escaped for safety, preventing this message from being erroneously
        misinterpreted as rich text.

        Parameters
        ----------
        warning : str
            Human-readable warning message to be displayed as this label's
            text.
        """
        logs.log_warning(warning)
        self.clear()
        warning_escaped = mls.escape_ml(warning)
        self._image_label.setText(QCoreApplication.translate('QBetseeLabelImage', '<span style="color: #aa0000;"><b>Warning:</b> {0}</span>'.format(warning_escaped)))
        self.adjustSize()