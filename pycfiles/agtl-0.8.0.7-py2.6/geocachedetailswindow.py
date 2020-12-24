# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/geocachedetailswindow.py
# Compiled at: 2011-04-23 08:43:29
import logging, geocaching, re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from showimagedialog import QtShowImageDialog
from ui_geocachedetailswindow import Ui_GeocacheDetailsWindow
from os import path, extsep
d = lambda x: x.decode('utf-8')
logger = logging.getLogger('qtgeocachewindow')

class QtGeocacheDetailsWindow(QMainWindow, Ui_GeocacheDetailsWindow):
    download_details = pyqtSignal()
    ICONS = {geocaching.GeocacheCoordinate.LOG_TYPE_FOUND: 'emoticon_grin', 
       geocaching.GeocacheCoordinate.LOG_TYPE_NOTFOUND: 'cross', 
       geocaching.GeocacheCoordinate.LOG_TYPE_NOTE: 'comment', 
       geocaching.GeocacheCoordinate.LOG_TYPE_MAINTENANCE: 'wrench', 
       geocaching.GeocacheCoordinate.LOG_TYPE_PUBLISHED: 'accept', 
       geocaching.GeocacheCoordinate.LOG_TYPE_DISABLED: 'delete', 
       geocaching.GeocacheCoordinate.LOG_TYPE_NEEDS_MAINTENANCE: 'error', 
       geocaching.GeocacheCoordinate.LOG_TYPE_WILLATTEND: 'calendar_edit', 
       geocaching.GeocacheCoordinate.LOG_TYPE_ATTENDED: 'group', 
       geocaching.GeocacheCoordinate.LOG_TYPE_UPDATE: 'asterisk_yellow'}

    def __init__(self, core, parent=None):
        QMainWindow.__init__(self, parent)
        self.core = core
        self.setupUi(self)
        self.actionDownload_Details.triggered.connect(self.__download_details)
        self.core.connect('cache-changed', self.__cache_changed)

    def __download_details(self):
        self.core.update_coordinates([self.current_geocache])

    def __cache_changed(self, caller, geocache):
        if geocache.name == self.current_geocache.name:
            self.show_geocache(geocache)

    def show_geocache(self, geocache):
        self.current_geocache = geocache
        self.setWindowTitle('Geocache Details: %s' % d(geocache.title))
        labels = (
         (
          self.labelFullName, geocache.title),
         (
          self.labelID, geocache.name),
         (
          self.labelType, geocache.type),
         (
          self.labelSize, geocache.get_size_string()),
         (
          self.labelTerrain, geocache.get_terrain()),
         (
          self.labelDifficulty, geocache.get_difficulty()),
         (
          self.labelOwner, geocache.owner),
         (
          self.labelStatus, geocache.get_status()))
        for (label, text) in labels:
            label.setText(d(text))

        if geocache.desc != '' and geocache.shortdesc != '':
            showdesc = '<b>%s</b><br />%s' % (geocache.shortdesc, geocache.desc)
        elif geocache.desc == '' and geocache.shortdesc == '':
            showdesc = '<i>No description available</i>'
        elif geocache.desc == '':
            showdesc = geocache.shortdesc
        else:
            showdesc = geocache.desc
        showdesc = d(showdesc)
        showdesc = re.sub('\\[\\[img:([^\\]]+)\\]\\]', lambda a: "<img src='%s' />" % self.get_path_to_image(a.group(1)), showdesc)
        self.labelDescription.setText(showdesc)
        logs = []
        for l in geocache.get_logs():
            logs.append(self.__get_log_line(l))

        self.labelLogs.setText(('').join(logs))
        hint = d(geocache.hints).strip()
        if len(hint) > 0:
            self.pushButtonShowHint.clicked.connect(lambda : self.__show_hint(hint))
        else:
            self.pushButtonShowHint.hide()
        self.listWidgetImages.clear()
        images = geocache.get_images()
        if len(images) > 0:
            i = 0
            for (filename, description) in images.items():
                file = self.get_path_to_image(filename)
                icon = QIcon(file)
                m = QListWidgetItem(icon, d(description), self.listWidgetImages)
                m.setData(Qt.UserRole, QVariant(i))
                i += 1

            self.listWidgetImages.itemClicked.connect(lambda item: self.__show_image(item.icon().pixmap(QApplication.desktop().size())))
        else:
            self.tabImages.deleteLater()

    def __get_log_line(self, log):
        icon = '%s%spng' % (path.join(self.core.dataroot, self.ICONS[log['type']]), extsep)
        date = '%4d-%02d-%02d' % (int(log['year']), int(log['month']), int(log['day']))
        finder = d(log['finder'])
        line1 = "<tr><td><img src='%s'>%s</td><td align='right'>%s</td></tr>" % (icon, finder, date)
        line2 = "<tr><td colspan='2'>%s</td></tr>" % log['text'].strip()
        line3 = "<tr>td colspan='2'><hr></td></tr>"
        return ('').join((line1, line2, line3))

    def __show_hint(self, text):
        QMessageBox.information(self, 'Hint, Hint!', text)

    def get_path_to_image(self, image):
        return path.join(self.core.settings['download_output_dir'], image)

    def __show_image(self, pixmap):
        m = QtShowImageDialog(self)
        m.show_image(pixmap)
        m.show()