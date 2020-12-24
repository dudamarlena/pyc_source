# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/project_properties.py
# Compiled at: 2012-10-19 18:33:24
import os, logging
from sqlalchemy.sql.expression import distinct
from oyProjectManager import conf
from oyProjectManager import db
from oyProjectManager.models.auth import Client
from oyProjectManager.models.project import Project
logger = logging.getLogger(__name__)
qt_module_key = 'PREFERRED_QT_MODULE'
qt_module = 'PyQt4'
if os.environ.has_key(qt_module_key):
    qt_module = os.environ[qt_module_key]
if qt_module == 'PySide':
    from PySide import QtGui, QtCore
    from oyProjectManager.ui import project_properties_UI_pyside as project_properties_UI
elif qt_module == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
    from oyProjectManager.ui import project_properties_UI_pyqt4 as project_properties_UI

class MainDialog(QtGui.QDialog, project_properties_UI.Ui_Dialog):
    """Dialog to edit project properties
    
    If a :class:`~oyProjectManager.models.project.Project` instance is also
    passed it will edit the given project.
    
    If no Project is passed then it will create and return a new one.
    """

    def __init__(self, parent=None, project=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        if db.session is None:
            db.setup()
        self.resolution_presets = conf.resolution_presets
        self.project = project
        self._setup_signals()
        self._setup_defaults()
        self.update_UI_from_project(self.project)
        return

    def _setup_signals(self):
        """sets up signals
        """
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), self.close)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.button_box_ok_clicked)
        QtCore.QObject.connect(self.name_lineEdit, QtCore.SIGNAL('textChanged(QString)'), self.name_edited)

    def set_resolution_to_default(self):
        index = self.resolution_comboBox.findText(conf.default_resolution_preset)
        self.resolution_comboBox.setCurrentIndex(index)

    def _setup_defaults(self):
        """sets up the default values
        """
        self.resolution_comboBox.addItems(sorted(conf.resolution_presets.keys()))
        self.set_resolution_to_default()
        clients = map(lambda x: x.name, Client.query().order_by(Client.name.asc()).all())
        self.clients_comboBox.clear()
        self.clients_comboBox.addItems(clients)
        self.fps_spinBox.setValue(conf.default_fps)
        self.active_checkBox.setChecked(True)
        if self.project is not None:
            self.code_lineEdit.setEnabled(False)
        self.shot_number_padding_spinBox.setValue(conf.shot_number_padding)
        self.shot_number_prefix_lineEdit.setText(conf.shot_number_prefix)
        self.revision_number_padding_spinBox.setValue(conf.rev_number_padding)
        self.revision_number_prefix_lineEdit.setText(conf.rev_number_prefix)
        self.version_number_padding_spinBox.setValue(conf.ver_number_padding)
        self.version_number_prefix_lineEdit.setText(conf.ver_number_prefix)
        self.structure_textEdit.setText(conf.project_structure)
        return

    def update_UI_from_project(self, project):
        """Updates the UI with the info from the given project instance
        
        :param project: The :class:`~oyProjectManager.models.project.Project`
          instance which the UI data will be read from.
        """
        if project is None:
            return
        else:
            self.name_lineEdit.setText(project.name)
            self.code_lineEdit.setText(project.code)
            if project.client:
                index = self.clients_comboBox.findText(project.client.name)
                if index != -1:
                    self.clients_comboBox.setCurrentIndex(index)
            self.fps_spinBox.setValue(project.fps)
            self.active_checkBox.setChecked(project.active)
            self.shot_number_prefix_lineEdit.setText(project.shot_number_prefix)
            self.shot_number_padding_spinBox.setValue(project.shot_number_padding)
            self.revision_number_prefix_lineEdit.setText(project.rev_number_prefix)
            self.revision_number_padding_spinBox.setValue(project.rev_number_padding)
            self.version_number_prefix_lineEdit.setText(project.ver_number_prefix)
            self.version_number_padding_spinBox.setValue(project.ver_number_padding)
            self.structure_textEdit.setText(project.structure)
            preset_key = None
            for key in conf.resolution_presets.keys():
                if conf.resolution_presets[key] == [project.width,
                 project.height,
                 project.pixel_aspect]:
                    preset_key = key
                    break

            if preset_key is not None:
                index = self.resolution_comboBox.findText(preset_key)
                self.resolution_comboBox.setCurrentIndex(index)
            else:
                self.resolution_comboBox.setCurrentIndex(self.resolution_comboBox.count() - 1)
            return

    def button_box_ok_clicked(self):
        """runs when the ok button clicked
        """
        name = self.name_lineEdit.text()
        code = self.code_lineEdit.text()
        if code == '':
            QtGui.QMessageBox.critical(self, 'Error', 'Code field can not be empty,\nPlease enter a proper Code!!!')
            return
        else:
            client_name = self.clients_comboBox.currentText()
            client = Client.query().filter(Client.name == client_name).first()
            if not client:
                client = Client(name=client_name)
                client.save()
            resolution_name = self.resolution_comboBox.currentText()
            resolution_data = conf.resolution_presets[resolution_name]
            fps = self.fps_spinBox.value()
            active = self.active_checkBox.isChecked()
            shot_number_padding = self.shot_number_padding_spinBox.value()
            shot_number_prefix = self.shot_number_prefix_lineEdit.text()
            rev_number_padding = self.revision_number_padding_spinBox.value()
            rev_number_prefix = self.revision_number_prefix_lineEdit.text()
            ver_number_padding = self.version_number_padding_spinBox.value()
            ver_number_prefix = self.version_number_prefix_lineEdit.text()
            structure_code = self.structure_textEdit.toPlainText()
            is_new_project = False
            if self.project is None:
                logger.debug('no project is given creating new one')
                self.project = Project(name=name, code=code)
                is_new_project = True
            else:
                logger.debug('updating the given project')
            self.project.name = name
            self.project.client = client
            self.project.fps = fps
            self.project.width = resolution_data[0]
            self.project.height = resolution_data[1]
            self.project.pixel_aspect = resolution_data[2]
            self.project.active = active
            self.project.shot_number_padding = shot_number_padding
            self.project.shot_number_prefix = shot_number_prefix
            self.project.rev_number_padding = rev_number_padding
            self.project.rev_number_prefix = rev_number_prefix
            self.project.ver_number_padding = ver_number_padding
            self.project.ver_number_prefix = ver_number_prefix
            self.project.structure = structure_code
            if is_new_project:
                self.project.create()
            else:
                self.project.save()
            self.close()
            return

    def name_edited(self, new_name):
        """called by the ui event when the text in project name lineEdit
        changed, it updates the code field if the code field is empty
        :param new_name: the changed name
        """
        import re
        new_code = re.sub('([^A-Z0-9]+)([\\-\\s]*)', '_', new_name.upper())
        self.code_lineEdit.setText(new_code)