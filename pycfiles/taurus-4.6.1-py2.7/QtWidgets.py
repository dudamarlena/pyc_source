# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtWidgets.py
# Compiled at: 2019-08-19 15:09:29
"""
Provides widget classes and functions.
.. warning:: Only PyQt4/PySide QtGui classes compatible with PyQt5.QtWidgets
    are exposed here. Therefore, you need to treat/use this package as if it
    were the ``PyQt5.QtWidgets`` module.
"""
from . import PYQT5, PYSIDE2, PYQT4, PYSIDE, PythonQtError
from taurus.core.util import log as __log
if PYQT5:
    from PyQt5.QtWidgets import *
elif PYSIDE2:
    from PySide2.QtWidgets import *
elif PYQT4:
    __log.warning('Using QtWidgets with PyQt4 is not supported and may fail ' + 'in many cases. Use at your own risk ' + '(or use a Qt5 binding)')
    from PyQt4.QtGui import *
    QStyleOptionViewItem = QStyleOptionViewItemV4
    del QStyleOptionViewItemV4
    try:
        del QGlyphRun
        del QMatrix2x2
        del QMatrix2x3
        del QMatrix2x4
        del QMatrix3x2
        del QMatrix3x3
        del QMatrix3x4
        del QMatrix4x2
        del QMatrix4x3
        del QMatrix4x4
        del QQuaternion
        del QRadialGradient
        del QRawFont
        del QRegExpValidator
        del QStaticText
        del QTouchEvent
        del QVector2D
        del QVector3D
        del QVector4D
        del qFuzzyCompare
    except NameError:
        pass

    del QAbstractTextDocumentLayout
    del QActionEvent
    del QBitmap
    del QBrush
    del QClipboard
    del QCloseEvent
    del QColor
    del QConicalGradient
    del QContextMenuEvent
    del QCursor
    del QDesktopServices
    del QDoubleValidator
    del QDrag
    del QDragEnterEvent
    del QDragLeaveEvent
    del QDragMoveEvent
    del QDropEvent
    del QFileOpenEvent
    del QFocusEvent
    del QFont
    del QFontDatabase
    del QFontInfo
    del QFontMetrics
    del QFontMetricsF
    del QGradient
    del QHelpEvent
    del QHideEvent
    del QHoverEvent
    del QIcon
    del QIconDragEvent
    del QIconEngine
    del QImage
    del QImageIOHandler
    del QImageReader
    del QImageWriter
    del QInputEvent
    del QInputMethodEvent
    del QKeyEvent
    del QKeySequence
    del QLinearGradient
    del QMouseEvent
    del QMoveEvent
    del QMovie
    del QPaintDevice
    del QPaintEngine
    del QPaintEngineState
    del QPaintEvent
    del QPainter
    del QPainterPath
    del QPainterPathStroker
    del QPalette
    del QPen
    del QPicture
    del QPictureIO
    del QPixmap
    del QPixmapCache
    del QPolygon
    del QPolygonF
    del QRegion
    del QResizeEvent
    del QSessionManager
    del QShortcutEvent
    del QShowEvent
    del QStandardItem
    del QStandardItemModel
    del QStatusTipEvent
    del QSyntaxHighlighter
    del QTabletEvent
    del QTextBlock
    del QTextBlockFormat
    del QTextBlockGroup
    del QTextBlockUserData
    del QTextCharFormat
    del QTextCursor
    del QTextDocument
    del QTextDocumentFragment
    del QTextDocumentWriter
    del QTextFormat
    del QTextFragment
    del QTextFrame
    del QTextFrameFormat
    del QTextImageFormat
    del QTextInlineObject
    del QTextItem
    del QTextLayout
    del QTextLength
    del QTextLine
    del QTextList
    del QTextListFormat
    del QTextObject
    del QTextObjectInterface
    del QTextOption
    del QTextTable
    del QTextTableCell
    del QTextTableCellFormat
    del QTextTableFormat
    del QTransform
    del QValidator
    del QWhatsThisClickedEvent
    del QWheelEvent
    del QWindowStateChangeEvent
    del qAlpha
    del qBlue
    del qGray
    del qGreen
    del qIsGray
    del qRed
    del qRgb
    del qRgba
    del QIntValidator
    del QStringListModel
    del QAbstractPrintDialog
    del QPageSetupDialog
    del QPrintDialog
    del QPrintEngine
    del QPrintPreviewDialog
    del QPrintPreviewWidget
    del QPrinter
    del QPrinterInfo
    del QItemSelection
    del QItemSelectionModel
    del QItemSelectionRange
    del QSortFilterProxyModel
    QHeaderView.sectionsClickable = QHeaderView.isClickable
    QHeaderView.sectionsMovable = QHeaderView.isMovable
    QHeaderView.sectionResizeMode = QHeaderView.resizeMode
    QHeaderView.setSectionsClickable = QHeaderView.setClickable
    QHeaderView.setSectionsMovable = QHeaderView.setMovable
    QHeaderView.setSectionResizeMode = QHeaderView.setResizeMode
elif PYSIDE:
    __log.warning('Using QtWidgets with PySide is not supported and may fail ' + 'in many cases. Use at your own risk ' + '(or use a Qt5 binding)')
    from PySide.QtGui import *
    QStyleOptionViewItem = QStyleOptionViewItemV4
    del QStyleOptionViewItemV4
    del QAbstractTextDocumentLayout
    del QActionEvent
    del QBitmap
    del QBrush
    del QClipboard
    del QCloseEvent
    del QColor
    del QConicalGradient
    del QContextMenuEvent
    del QCursor
    del QDesktopServices
    del QDoubleValidator
    del QDrag
    del QDragEnterEvent
    del QDragLeaveEvent
    del QDragMoveEvent
    del QDropEvent
    del QFileOpenEvent
    del QFocusEvent
    del QFont
    del QFontDatabase
    del QFontInfo
    del QFontMetrics
    del QFontMetricsF
    del QGradient
    del QHelpEvent
    del QHideEvent
    del QHoverEvent
    del QIcon
    del QIconDragEvent
    del QIconEngine
    del QImage
    del QImageIOHandler
    del QImageReader
    del QImageWriter
    del QInputEvent
    del QInputMethodEvent
    del QKeyEvent
    del QKeySequence
    del QLinearGradient
    del QMatrix2x2
    del QMatrix2x3
    del QMatrix2x4
    del QMatrix3x2
    del QMatrix3x3
    del QMatrix3x4
    del QMatrix4x2
    del QMatrix4x3
    del QMatrix4x4
    del QMouseEvent
    del QMoveEvent
    del QMovie
    del QPaintDevice
    del QPaintEngine
    del QPaintEngineState
    del QPaintEvent
    del QPainter
    del QPainterPath
    del QPainterPathStroker
    del QPalette
    del QPen
    del QPicture
    del QPictureIO
    del QPixmap
    del QPixmapCache
    del QPolygon
    del QPolygonF
    del QQuaternion
    del QRadialGradient
    del QRegExpValidator
    del QRegion
    del QResizeEvent
    del QSessionManager
    del QShortcutEvent
    del QShowEvent
    del QStandardItem
    del QStandardItemModel
    del QStatusTipEvent
    del QSyntaxHighlighter
    del QTabletEvent
    del QTextBlock
    del QTextBlockFormat
    del QTextBlockGroup
    del QTextBlockUserData
    del QTextCharFormat
    del QTextCursor
    del QTextDocument
    del QTextDocumentFragment
    del QTextFormat
    del QTextFragment
    del QTextFrame
    del QTextFrameFormat
    del QTextImageFormat
    del QTextInlineObject
    del QTextItem
    del QTextLayout
    del QTextLength
    del QTextLine
    del QTextList
    del QTextListFormat
    del QTextObject
    del QTextObjectInterface
    del QTextOption
    del QTextTable
    del QTextTableCell
    del QTextTableCellFormat
    del QTextTableFormat
    del QTouchEvent
    del QTransform
    del QValidator
    del QVector2D
    del QVector3D
    del QVector4D
    del QWhatsThisClickedEvent
    del QWheelEvent
    del QWindowStateChangeEvent
    del qAlpha
    del qBlue
    del qGray
    del qGreen
    del qIsGray
    del qRed
    del qRgb
    del qRgba
    del QIntValidator
    del QStringListModel
    del QAbstractPrintDialog
    del QPageSetupDialog
    del QPrintDialog
    del QPrintEngine
    del QPrintPreviewDialog
    del QPrintPreviewWidget
    del QPrinter
    del QPrinterInfo
    del QItemSelection
    del QItemSelectionModel
    del QItemSelectionRange
    del QSortFilterProxyModel
    QHeaderView.sectionsClickable = QHeaderView.isClickable
    QHeaderView.sectionsMovable = QHeaderView.isMovable
    QHeaderView.sectionResizeMode = QHeaderView.resizeMode
    QHeaderView.setSectionsClickable = QHeaderView.setClickable
    QHeaderView.setSectionsMovable = QHeaderView.setMovable
    QHeaderView.setSectionResizeMode = QHeaderView.setResizeMode
else:
    raise PythonQtError('No Qt bindings could be found')