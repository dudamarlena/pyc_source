# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/canvas_launcher/splash.py
# Compiled at: 2020-01-08 09:31:39
# Size of source mod 2**32: 555 bytes
from silx.gui import qt
from tomwer.gui import icons

def splash_screen():
    """

    :return: splash screen for orange-canvas
    :rtype: tuple(QPixmap, QRect),

    note: QRect is used by orange to define a mask to display the message.
          In our case we overwrite the QSplashScreen so we don't need this.
    """
    pixmap = icons.getQPixmap('tomwer')
    return (pixmap, qt.QRect(0, 0, 0, 0))


def getIcon():
    """

    :return: application icon
    :rtype: QIcon
    """
    pixmap = icons.getQPixmap('tomwer')
    return qt.QIcon(pixmap)