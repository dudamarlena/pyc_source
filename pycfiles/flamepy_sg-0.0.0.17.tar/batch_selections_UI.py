# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stefan/XenDrive/___VFX/FLAME_STUFF/FLAME_DEV/PYTHON/flame_python_projects/FlamePy_sg/flamepy_sg/scripts/batch_selections/batch_selections_UI.py
# Compiled at: 2018-05-19 02:59:28
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui
import os, traceback, subprocess as sb
from flamepy_sg.scripts.customprints.ansi_colors import sg_colors
from flamepy_sg.modules import yaml
from flamepy_sg.scripts.batch_snippets.connected_duplicate import main as _dupli
from flamepy_sg.scripts.batch_snippets.matte_cleaner import main as _cleaner
print sg_colors.green1 + '--- From save_load_selection_UI.py ---' + sg_colors.endc
absolute_path = os.path.realpath(__file__)
root_path = ('/').join(absolute_path.split('/')[0:-3])

def actions_side_callback(passed_data):
    file_path = ('{root}/scripts/text_files/Expressions_particles_reformated.txt').format(root=root_path)
    print sg_colors.grey3 + file_path + sg_colors.endc
    sb.call(['open', file_path])


def load_side_callback(passed_data):
    import flame
    flame.batch.selected_nodes = passed_data
    flame.batch.frame_selected()


def load_selections(path):
    with open(path, 'r') as (saved_selections):
        return yaml.load(saved_selections)
        print yaml.load(saved_selections)


def save_selection(path, data):
    with open(path, 'w') as (saved_selections):
        saved_selections.write(yaml.safe_dump(data))
    print (
     sg_colors.grey3, 'from save_selection() print data: ', data, sg_colors.endc)


class SelectionsRow(QWidget):
    _signal = Signal()

    def __init__(self, name, data, actions_callback, load_callback, graphSelected, row_id, parent=None):
        super(SelectionsRow, self).__init__(parent=parent)
        self.row_id = row_id
        self.name = name
        self.data = data
        self.actions_callback = actions_callback
        self.load_callback = load_callback
        self.graphSelected = graphSelected
        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.name = QLineEdit(self.name)
        self.store_button = QPushButton()
        self.load_button = QPushButton()
        self.actions_button = QPushButton()
        self.remove_button = QPushButton()
        self.store_button.setFlat(True)
        self.load_button.setFlat(True)
        self.actions_button.setFlat(True)
        self.remove_button.setFlat(True)
        self.store_button.setIcon(QIcon(('{root}/scripts/batch_selections/icons/add_grey1_24dp.png').format(root=root_path)))
        self.load_button.setIcon(QIcon(('{root}/scripts/batch_selections/icons/load_grey1_24dp.png').format(root=root_path)))
        self.actions_button.setIcon(QIcon(('{root}/scripts/batch_selections/icons/robot_grey1_24dp.png').format(root=root_path)))
        self.remove_button.setIcon(QIcon(('{root}/scripts/batch_selections/icons/del_grey1_24dp.png').format(root=root_path)))
        self.menu = QtGui.QMenu(self)
        self.menu.addAction('Frame selection', self.exec_load_callback)
        self.menu.addAction('Duplicate', _dupli)
        self.menu.addAction('Matte Cleaner', _cleaner)
        self.menu.addAction('open file dummy', self.exec_action_callback)
        self.actions_button.setMenu(self.menu)
        self.remove_button.clicked.connect(self.remove)
        self.load_button.clicked.connect(self.exec_load_callback)
        self.store_button.clicked.connect(self.store)
        self.name.returnPressed.connect(self.store)
        self._layout.addWidget(self.name)
        self._layout.addWidget(self.store_button)
        self._layout.addWidget(self.load_button)
        self._layout.addWidget(self.actions_button)
        self._layout.addWidget(self.remove_button)

    def remove(self):
        self.data = {}
        self.name.setText('')
        self._signal.emit()
        print sg_colors.green1 + '--- def remove(self) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc

    def value(self):
        return {'name': self.name.text(), 'data': self.data}

    def store(self, *args, **kwargs):
        try:
            self.data = self.graphSelected()
            if not self.name.text():
                self.name.setText('selection_' + str(self.row_id + 1).zfill(2))
            self._signal.emit()
        except:
            traceback.print_exc()

        print sg_colors.green1 + '--- def store(self) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc

    def exec_action_callback(self):
        try:
            self.actions_callback(self.data)
        except:
            traceback.print_exc()

        print sg_colors.green1 + '--- def exec_action_callback(self) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc

    def exec_load_callback(self):
        try:
            self.load_callback(self.data)
        except:
            traceback.print_exc()

        print sg_colors.green1 + '--- def exec_action_callback(self) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc


class SelectionsWidget(QWidget):
    print sg_colors.green1 + '--- class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get('path')
        self.slots = kwargs.get('slots', 10)
        self.graphSelected = kwargs.get('graphSelected')
        super(SelectionsWidget, self).__init__(parent=kwargs.get('parent'))
        self.mainLayout = QGridLayout(self)
        self.templateLayout = QVBoxLayout()
        self.templateLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(self.templateLayout, 0, 0)
        self.setWindowTitle('Selections')
        self.move(800, 150)
        self._rows = []
        if self.path and os.path.isfile(self.path):
            data = load_selections(self.path)
            self.create_ui(data)

    def create_ui(self, data):
        print sg_colors.green1 + '--- def create_ui(self, data) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc
        for row in self._rows:
            row.deleteLater()

        self.slots = max(len(data), self.slots)
        for i in range(self.slots):
            if i < len(data):
                entry = data[i]
            else:
                entry = {'name': '', 'data': []}
            import flame
            print sg_colors.grey3, 'CURRENT NODES:', flame.batch.selected_nodes, sg_colors.endc
            row = SelectionsRow(entry['name'], entry['data'], actions_side_callback, load_side_callback, self.graphSelected, row_id=i)
            row._signal.connect(self.save)
            self._rows.append(row)
            self.mainLayout.addWidget(row)
            print sg_colors.endc

    def save(self):
        print sg_colors.green1 + '--- def save(self) in class SelectionsWidget(QWidget): inside CustomUiaction_selections.py ---' + sg_colors.endc
        yaml_data = []
        for row in self._rows:
            _value = row.value()
            if _value['data'] and _value['name']:
                yaml_data.append(_value)
            elif _value['data'] and not _value['name']:
                print sg_colors.grey3 + 'Skippin row with data that has no name' + sg_colors.endc

        save_selection(self.path, yaml_data)
        with open(self.path, 'r') as (saved_selections):
            print sg_colors.grey3 + '-' * 80 + sg_colors.endc
            print yaml.load(saved_selections)