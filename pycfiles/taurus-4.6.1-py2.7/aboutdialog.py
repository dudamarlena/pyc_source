# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/help/aboutdialog.py
# Compiled at: 2019-08-19 15:09:29
"""
This module provides a simple dialog to display typical About
<application> dialog. It will create a Dialog with the title being
*Dialog + <app name>* and a default text combining the application
name and version, organization name and domain.

This behaviour can be changed by setting the dialog window title
(:meth:`~AboutDialog.setWindowTitle`) and content
(:meth:`~AboutDialog.setText`, :meth:`~AboutDialog.setHtml`)

Example usage::

    from taurus.external.qt import Qt
    from taurus.qt.qtgui.help import AboutDialog

    app = Qt.QApplication([])
    app.setApplicationName("Example GUI")
    app.setApplicationVersion("1.2.3")
    app.setOrganizationName("Taurus")
    app.setOrganizationDomain("http://www.taurus-scada.org/")
    about_dialog = AboutDialog()
    pixmap = Qt.QIcon.fromTheme("folder-open").pixmap(64, 64)
    about_dialog.setPixmap(pixmap)
    about_dialog.exec_()

    """
__all__ = [
 'AboutDialog']
from taurus.external.qt import Qt
from taurus.qt.qtgui.util.ui import UILoadable

@UILoadable
class AboutDialog(Qt.QDialog):
    """
    Simple dialog to display typical About <application> dialog.
    It will create a Dialog with the title being
    *Dialog + <app name>* and a default text combining the application
    name and version, organization name and domain.

    This behaviour can be changed by setting the dialog window title
    (:meth:`~AboutDialog.setWindowTitle`) and content
    (:meth:`~AboutDialog.setText`, :meth:`~AboutDialog.setHtml`)

    Example usage::

        from taurus.external.qt import Qt
        from taurus.qt.qtgui.help import AboutDialog

        app = Qt.QApplication([])
        app.setApplicationName("Example GUI")
        app.setApplicationVersion("1.2.3")
        app.setOrganizationName("Taurus")
        app.setOrganizationDomain("http://www.taurus-scada.org/")
        about_dialog = AboutDialog()
        pixmap = Qt.QIcon.fromTheme("folder-open").pixmap(64, 64)
        about_dialog.setPixmap(pixmap)
        about_dialog.exec_()

    """
    _Template = '<html><body><p><b>{0}</b></p><p>{1}</p><p>{2}</p><p><a href="{3}">{2}</a></p>(c) Copyright {2}'

    def __init__(self, parent=None):
        Qt.QDialog.__init__(self, parent)
        self.loadUi()
        self.text_browser.setFrameStyle(Qt.QFrame.NoFrame)
        palette = Qt.QPalette()
        palette.setColor(Qt.QPalette.Base, palette.color(Qt.QPalette.Background))
        self.text_browser.setPalette(palette)
        self.logo_widget.setAlignment(Qt.Qt.AlignHCenter | Qt.Qt.AlignTop)
        name = Qt.qApp.applicationName()
        version = Qt.qApp.applicationVersion()
        org = Qt.qApp.organizationName()
        org_domain = Qt.qApp.organizationDomain()
        self.setWindowTitle('About ' + Qt.qApp.applicationName())
        self.setHtml(self._Template.format(name, version, org, org_domain))

    def setText(self, text):
        """
        Sets the dialog text.

        :param text: new text
        :type text: str
        """
        self.text_browser.setText(text)

    def getHtml(self):
        """
        Gets the current dialog HTML text.

        :return: the current dialog HTML text.
        :rtype: str
        """
        return self.text_browser.toHtml()

    @Qt.Slot(str)
    def setHtml(self, html):
        """
        Sets the dialog HTML text.

        :param text: new HTML text
        :type text: str
        """
        self.text_browser.setHtml(html)

    def resetHtml(self):
        """
        Resets the dialog HTML to an empty HTML document
        """
        self.setHtml('<html><body></body></html>')

    def getSource(self):
        """
        Gets the current dialog document source.

        :return: the current dialog document source.
        :rtype: Qt.QUrl
        """
        return self.text_browser.source()

    @Qt.Slot(Qt.QUrl)
    def setSource(self, source):
        """
        Sets the dialog document source.

        :param text: new document source
        :type text: Qt.QUrl
        """
        self.text_browser.setSource(source)

    @Qt.Slot(Qt.QPixmap)
    def setPixmap(self, pixmap):
        """
        Sets the dialog pixmap

        :param text: new pixmap
        :type text: Qt.QPixmap
        """
        self.logo_widget.setPixmap(pixmap)

    def getPixmap(self):
        """
        Gets the current pixmap.

        :return: the current dialog pixmap
        :rtype: Qt.QPixmap
        """
        pixmap = self.logo_widget.getPixmap()
        if pixmap is None:
            pixmap = Qt.QPixmap()
        return pixmap

    def resetPixmap(self):
        """
        Resets the dialog pixmap to a Null pixmap.
        """
        self.setPixmap(Qt.QPixmap())

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return {'group': 'Taurus Help', 'icon': Qt.QIcon.fromTheme('help'), 
           'module': 'taurus.qt.qtgui.help', 
           'container': False}

    pixmap = Qt.Property('QPixmap', getPixmap, setPixmap, resetPixmap)
    html = Qt.Property('QString', getHtml, setHtml, resetHtml)
    source = Qt.Property('QUrl', getSource, setSource)


def main():
    app = Qt.QApplication([])
    app.setApplicationName('Example GUI')
    app.setApplicationVersion('1.2.3')
    app.setOrganizationName('Taurus')
    app.setOrganizationDomain('http://www.taurus-scada.org/')
    about_dialog = AboutDialog()
    pixmap = Qt.QIcon.fromTheme('folder-open').pixmap(64, 64)
    about_dialog.setPixmap(pixmap)
    about_dialog.exec_()


if __name__ == '__main__':
    main()