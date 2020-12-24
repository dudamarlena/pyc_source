# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/create_asset_dialog.py
# Compiled at: 2012-09-24 08:16:34
import os, logging
from sqlalchemy.sql.expression import distinct
import oyProjectManager
from oyProjectManager import config, db
from oyProjectManager.models.asset import Asset
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
conf = config.Config()
qt_module_key = 'PREFERRED_QT_MODULE'
qt_module = 'PyQt4'
if os.environ.has_key(qt_module_key):
    qt_module = os.environ[qt_module_key]
if qt_module == 'PySide':
    from PySide import QtGui, QtCore
    from oyProjectManager.ui import create_asset_dialog_UI_pyside as create_asset_dialog_UI
elif qt_module == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
    from oyProjectManager.ui import create_asset_dialog_UI_pyqt4 as create_asset_dialog_UI

class create_asset_dialog(QtGui.QDialog, create_asset_dialog_UI.Ui_create_asset):
    """Called upon asset creation
    """

    def __init__(self, parent=None):
        logger.debug('initializing create_asset_dialog')
        super(create_asset_dialog, self).__init__(parent)
        self.setupUi(self)
        self.ok = False
        self._setup_signals()
        self._setup_defaults()

    def _setup_signals(self):
        """setting up the signals
        """
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.buttonBox_accepted)

    def _setup_defaults(self):
        """setting up the defaults
        """
        all_types = map(lambda x: x[0], db.query(distinct(Asset.type)).all())
        if conf.default_asset_type_name not in all_types:
            all_types.append(conf.default_asset_type_name)
        logger.debug('all_types: %s' % all_types)
        self.asset_types_comboBox.addItems(all_types)

    def buttonBox_accepted(self):
        """runs when the buttonbox.OK is clicked
        """
        self.ok = True
        self.close()

    def buttonBox_rejected(self):
        """runs when the buttonbox.Cancel is clicked
        """
        self.ok = False
        self.close()