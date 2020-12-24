# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/app/guiappsplash.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 4100 bytes
"""
Submodule providing the startup splash progress visualizing the current progress
of this application loading.
"""
from PySide2.QtCore import Qt, QPixmap
from PySide2.QtWidgets import QSplashScreen
from betse.util.type.types import type_check
from betsee.util.app import guiapp
GUI_APP_SPLASH = None

class QBetseeSplashScreen(QSplashScreen):
    __doc__ = '\n    :class:`QSplashScreen`-based widget displaying a non-modal splash screen,\n    typically used to present a multi-threaded graphical progress bar during\n    time-consuming application startup.\n    '

    @type_check
    def __init__(self, image_uri):
        """
        Initialize this splash screen with the passed properties.

        Parameters
        ----------
        image_uri : str
            Qt-specific Uniform Resource Identifier (URI) of the single image to
            be displayed by this splash screen (e.g., ``://image/splash.svg``).
        """
        super().__init__()
        gui_app = guiapp.get_app()
        self.setPixmap(QPixmap(image_uri))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAutoFillBackground(False)
        self.show()
        gui_app.processEvents()

    @type_check
    def set_info(self, info: str) -> None:
        """
        Display the passed human-readable single-line string as the current
        message for this splash screen, replacing the prior such string if any.
        """
        gui_app = guiapp.get_app()
        self.showMessage(info)
        gui_app.processEvents()