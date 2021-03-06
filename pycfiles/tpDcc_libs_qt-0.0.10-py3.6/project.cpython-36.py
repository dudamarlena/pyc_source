# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/project.py
# Compiled at: 2020-04-26 16:40:12
# Size of source mod 2**32: 25027 bytes
"""
Module that contains generic functionality when dealing with projects
"""
from __future__ import print_function, division, absolute_import
import os, logging
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
import tpDcc as tp
from tpDcc.libs import qt
from tpDcc.libs.python import path, settings, folder, fileio
from tpDcc.core import project as core_project
from tpDcc.core import consts
from tpDcc.libs.qt.widgets import grid, search, directory, dividers
LOGGER = logging.getLogger()

class Project(QWidget, core_project.ProjectData):
    projectOpened = Signal(object)
    projectRemoved = Signal()
    projectImageChanged = Signal(str)

    def __init__(self, name, project_path, settings=None, options=None, parent=None):
        core_project.ProjectData.__init__(self, name=name, project_path=project_path, settings=settings,
          options=options)
        QWidget.__init__(self, parent=parent)
        self.setMaximumWidth(160)
        self.setMaximumHeight(200)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        main_frame.setLineWidth(1)
        main_frame.setLayout(widget_layout)
        self.main_layout.addWidget(main_frame)
        self.project_btn = QPushButton('', self)
        self.project_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.project_btn.setIconSize(QSize(120, 120))
        project_lbl = QLabel(self.name)
        project_lbl.setStyleSheet('background-color:rgba(0, 0, 0, 150);')
        project_lbl.setAlignment(Qt.AlignCenter)
        widget_layout.addWidget(self.project_btn)
        widget_layout.addWidget(project_lbl)
        self.setup_signals()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        remove_icon = tp.ResourcesMgr().icon(name='delete', extension='png')
        remove_action = QAction(remove_icon, 'Remove', menu)
        remove_action.setStatusTip(consts.DELETE_PROJECT_TOOLTIP)
        remove_action.setToolTip(consts.DELETE_PROJECT_TOOLTIP)
        remove_action.triggered.connect(self._on_remove_project)
        folder_icon = tp.ResourcesMgr().icon(name='open_folder', extension='png')
        folder_action = QAction(folder_icon, 'Open in Browser', menu)
        folder_action.setStatusTip(consts.OPEN_PROJECT_IN_EXPLORER_TOOLTIP)
        folder_action.setToolTip(consts.OPEN_PROJECT_IN_EXPLORER_TOOLTIP)
        folder_action.triggered.connect(self._on_open_in_browser)
        image_icon = tp.ResourcesMgr().icon(name='picture', extension='png')
        set_image_action = QAction(image_icon, 'Set Project Image', menu)
        set_image_action.setToolTip(consts.SET_PROJECT_IMAGE_TOOLTIP)
        set_image_action.setStatusTip(consts.SET_PROJECT_IMAGE_TOOLTIP)
        set_image_action.triggered.connect(self._on_set_project_image)
        for action in [remove_action, None, folder_action, None, set_image_action]:
            if action is None:
                menu.addSeparator()
            else:
                menu.addAction(action)

        menu.exec_(self.mapToGlobal(event.pos()))

    def setup_signals(self):
        self.project_btn.clicked.connect(self._on_open_project)

    @classmethod
    def create_project_from_data(cls, project_data_path):
        """
        Creates a new project using a project data JSON file
        :param project_data_path: str, path where project JSON data file is located
        :return: Project
        """
        if project_data_path is None or not path.is_file(project_data_path):
            tp.logger.warning('Project Data Path {} is not valid!'.format(project_data_path))
            return
        else:
            project_data = settings.JSONSettings()
            project_options = settings.JSONSettings()
            project_dir = path.get_dirname(project_data_path)
            project_name = path.get_basename(project_data_path)
            project_data.set_directory(project_dir, project_name)
            project_options.set_directory(project_dir, 'options.json')
            if not project_data or not project_data.has_settings():
                LOGGER.warning('No valid project data found on Project Data File: {}'.format(project_data_path))
            project_name = project_data.get('name')
            project_path = path.get_dirname(path.get_dirname(project_data_path))
            project_image = project_data.get('image')
            LOGGER.debug('New Project found [{}]: {}'.format(project_name, project_path))
            new_project = cls(name=project_name, project_path=project_path, settings=project_data, options=project_options)
            if project_image:
                new_project.set_image(project_image)
            return new_project

    def open(self):
        """
        Opens project
        """
        self._on_open_project()

    def set_image(self, encoded_image):
        from tpDcc.libs.qt.core import image
        if not encoded_image:
            return
        encoded_image = encoded_image.encode('utf-8')
        self.project_btn.setIcon(QIcon(QPixmap.fromImage(image.base64_to_image(encoded_image))))

    def remove(self):
        from tpDcc.libs.qt.core import qtutils
        if not path.is_dir(self.full_path):
            LOGGER.warning('Impossible to remove Project Path: {}'.format(self.full_path))
            return False
        project_name = self.name
        project_path = self.project_path
        result = qtutils.get_permission(message=('Are you sure you want to delete project: {}'.format(self.name)), title='Deleting Project',
          cancel=False)
        if not result:
            return
        else:
            valid_delete = folder.delete_folder(folder_name=project_name, directory=project_path)
            if valid_delete is None:
                return False
            return True

    def load_project_data(self):
        """
        Return dictionary data contained in the project
        :return: dict
        """
        if not self.settings:
            return
        else:
            return self.settings.data()

    def get_project_nodes(self):
        """
        Returns path where nodes should be stored
        :return: str
        """
        return [
         os.path.join(self.full_path, 'nodes'), os.path.join(self.full_path, 'components')]

    def _on_open_project(self):
        LOGGER.debug('Loading project "{}" ...'.format(self.full_path))
        self.projectOpened.emit(self)

    def _on_remove_project(self):
        valid_remove = self.remove()
        if valid_remove:
            self.projectRemoved.emit()

    def _on_open_in_browser(self):
        fileio.open_browser(self.full_path)

    def _on_set_project_image(self):
        image_file = tp.Dcc.select_file_dialog(title='Select Project Image File',
          pattern='PNG Files (*.png)')
        if image_file is None or not path.is_file(image_file):
            LOGGER.warning('Selected Image "{}" is not valid!'.format(image_file))
            return
        valid_change = self.set_project_image(image_file)
        if valid_change:
            self.projectImageChanged.emit(image_file)


class ProjectViewer(grid.GridWidget, object):
    projectOpened = Signal(object)

    def __init__(self, project_class, parent=None):
        self._settings = None
        self._project_class = project_class
        super(ProjectViewer, self).__init__(parent=parent)
        self.setShowGrid(False)
        self.setColumnCount(3)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)

    def set_settings(self, settings):
        """
        Set the settings used by this editor
        This settings come from the main UI settings
        :param settings: QtIniSettings
        """
        self._settings = settings
        self.update_projects()

    def add_project(self, project_widget):
        if project_widget is None:
            return
        row, col = self.first_empty_cell()
        project_widget.projectOpened.connect(self._on_open_project)
        project_widget.projectRemoved.connect(self._on_removed_project)
        project_widget.projectImageChanged.connect(self._on_updated_project_image)
        self.addWidget(row, col, project_widget)
        self.resizeRowsToContents()

    def get_project_by_name(self, project_name):
        for w in self.get_widgets():
            if w.name == project_name:
                return w

    def update_projects(self, project_path=None):
        self.clear()
        if not project_path:
            if self._settings is None:
                tp.logger.debug('No Projects Path defined yet ...')
                return
            if self._settings.has_setting('project_directory'):
                project_path = self._settings.get('project_directory')
        if project_path:
            if not path.is_dir(project_path):
                tp.logger.warning('Projects Path {} is not valid!'.format(project_path))
                return
            for root, dirs, files in os.walk(project_path):
                if consts.PROJECTS_NAME in files:
                    new_project = self._project_class.create_project_from_data(path.join_path(root, consts.PROJECTS_NAME))
                    if new_project is not None:
                        self.add_project(new_project)

    def _on_open_project(self, project):
        self.projectOpened.emit(project)

    def _on_removed_project(self):
        self.update_projects()

    def _on_updated_project_image(self, image_path):
        self.update_projects()


class ProjectWidget(QWidget, object):
    PROJECT_CLASS = Project
    projectOpened = Signal(object)

    def __init__(self, parent=None):
        super(ProjectWidget, self).__init__(parent=parent)
        self._settings = None
        self._history = None
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        self.setLayout(main_layout)
        self._tab_widget = QTabWidget()
        self._open_project = OpenProjectWidget(project_class=(self.PROJECT_CLASS))
        self._new_project = NewProjectWidget(project_class=(self.PROJECT_CLASS))
        self._tab_widget.addTab(self._open_project, 'Projects')
        self._tab_widget.addTab(self._new_project, 'New Project')
        main_layout.addWidget(self._tab_widget)
        self._open_project.projectOpened.connect(self._on_project_opened)
        self._new_project.projectCreated.connect(self._on_project_created)
        self._tab_widget.currentChanged.connect(self._on_tab_changed)

    def set_settings(self, settings):
        """
        Set the settings used by this editor
        This settings come from the main UI settings
        :param settings: QtIniSettings
        """
        self._settings = settings
        self._open_project.set_settings(settings)
        self._new_project.set_settings(settings)

    def set_projects_path(self, projects_path):
        """
        Sets the path where we want to search for projects
        :param projects_path: str
        """
        self._open_project.set_projects_path(projects_path)

    def get_project_by_name(self, project_name, force_update=True):
        """
        Returns project by its name
        :param project_name: str
        :param force_update: bool
        :return: Project
        """
        if force_update:
            self._open_project.get_projects_list().update_projects()
        projects_list = self._open_project.get_projects_list()
        return projects_list.get_project_by_name(project_name)

    def open_project(self, project_name):
        """
        Opens project with given name
        :param project_name: str
        :return: Project
        """
        project_found = self.get_project_by_name(project_name)
        if project_found:
            project_found.open()
            return project_found

    def _on_project_opened(self, project):
        self.projectOpened.emit(project)

    def _on_project_created(self, project):
        self._tab_widget.setCurrentIndex(0)

    def _on_tab_changed(self, index):
        if index == 0:
            self._open_project.update_projects()


class OpenProjectWidget(QWidget, object):
    projectOpened = Signal(object)

    def __init__(self, project_class, parent=None):
        super(OpenProjectWidget, self).__init__(parent=parent)
        self._settings = None
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)
        self.setLayout(main_layout)
        self.search_widget = search.SearchFindWidget()
        self.search_widget.set_placeholder_text('Filter Projects ...')
        self._projects_list = ProjectViewer(project_class=project_class)
        self._projects_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout1 = QHBoxLayout()
        buttons_layout1.setContentsMargins(0, 0, 0, 0)
        buttons_layout1.setSpacing(0)
        buttons_layout1.setAlignment(Qt.AlignLeft)
        self.browse_widget = directory.SelectFolder(label_text='Projects Path', use_app_browser=True, use_icon=True)
        buttons_layout1.addWidget(self.browse_widget)
        buttons_layout.addLayout(buttons_layout1)
        main_layout.addWidget(self.search_widget)
        main_layout.addWidget(dividers.Divider('PROJECTS', alignment=(Qt.AlignCenter)))
        main_layout.addWidget(self._projects_list)
        main_layout.addLayout(buttons_layout)
        self.browse_widget.directoryChanged.connect(self._on_directory_browsed)
        self._projects_list.projectOpened.connect(self._on_project_opened)
        self._update_ui()

    def get_projects_list(self):
        """
        Returns projects list widget
        :return: ProjectViewer
        """
        return self._projects_list

    def set_projects_path(self, projects_path):
        """
        Sets the path where we want to search for projects
        :param projects_path: str
        """
        self._on_directory_browsed(projects_path)
        self.update_projects(projects_path)

    def set_settings(self, settings):
        """
        Set the settings used by this editor
        This settings come from the main UI settings
        :param settings: QtIniSettings
        """
        self._settings = settings
        self._update_ui()
        self._projects_list.set_settings(settings)

    def update_projects(self, project_path=None):
        self._projects_list.update_projects(project_path=project_path)

    def _update_ui(self, project_path=None):
        """
        Update UI based on the stored settings if exists
        """
        if project_path or self._settings:
            if self._settings.has_setting('project_directory'):
                project_path = self._settings.get('project_directory')
                tp.logger.debug('Project Path stored in settings: {}'.format(project_path))
        if project_path:
            self.browse_widget.set_directory(directory=project_path)
            if self._settings:
                self.update_projects()
            else:
                self.update_projects(project_path=project_path)

    def _on_directory_browsed(self, dir):
        """
        Set the project directory
        :param dir: str
        """
        if not dir or not path.is_dir(dir):
            return
        else:
            if self._settings:
                self._settings.set('project_directory', dir)
                tp.logger.debug('Updated FactoRig Project Path: {}'.format(dir))
                self._update_ui()
            else:
                self._update_ui(dir)

    def _on_project_opened(self, project):
        self.projectOpened.emit(project)


class NewProjectWidget(QWidget, object):
    projectCreated = Signal(object)

    def __init__(self, project_class, parent=None):
        super(NewProjectWidget, self).__init__(parent=parent)
        self._settings = None
        self._selected_template = None
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        self.search_widget = search.SearchFindWidget()
        self.search_widget.set_placeholder_text('Filter Templates ...')
        self.templates_list = TemplatesViewer(project_class=project_class)
        self.templates_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_layout.setSpacing(1)
        project_line_layout = QHBoxLayout()
        project_line_layout.setContentsMargins(0, 0, 0, 0)
        project_line_layout.setSpacing(0)
        project_layout.addLayout(project_line_layout)
        self.project_line = QLineEdit()
        self.project_line.setPlaceholderText('Project Path')
        self.project_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.project_btn = directory.SelectFolderButton(text='...', use_app_browser=True)
        project_line_layout.addWidget(self.project_line)
        project_line_layout.addWidget(self.project_btn)
        self.name_line = QLineEdit()
        self.name_line.setPlaceholderText('Project Name')
        project_line_layout.addWidget(dividers.get_horizontal_separator_widget())
        project_line_layout.addWidget(self.name_line)
        self.create_btn = QPushButton('Create')
        project_line_layout.addSpacing(10)
        project_line_layout.addWidget(self.create_btn)
        main_layout.addWidget(self.search_widget)
        main_layout.addWidget(dividers.Divider('TEMPLATES', alignment=(Qt.AlignCenter)))
        main_layout.addWidget(self.templates_list)
        main_layout.addLayout(project_layout)
        self.templates_list.selectedTemplate.connect(self._on_selected_template)
        self.project_btn.directoryChanged.connect(self._on_directory_browsed)
        self.create_btn.clicked.connect(self._on_create)

    def set_settings(self, settings):
        """
        Set the settings used by this editor
        This settings come from the main UI settings
        :param settings: QtIniSettings
        """
        self._settings = settings
        self._update_ui()

    def _update_ui(self):
        """
        Update UI based on the stored settings if exists
        """
        if self._settings:
            if self._settings.has_setting('project_directory'):
                project_path = self._settings.get('project_directory')
                self.project_line.setText(project_path)
                self.project_btn.init_directory = project_path

    def _on_selected_template(self, template):
        self._selected_template = template

    def _on_directory_browsed(self, dir):
        if not dir or not path.is_dir(dir):
            return
        self.project_line.setText(str(dir))

    def _on_create(self):
        project_path = self.project_line.text()
        project_name = self.name_line.text()
        if not project_path or not path.is_dir(project_path) or not project_name:
            tp.logger.warning('Project Path: {} or Project Name: {} are not valid!'.format(project_path, project_name))
            return
        if self._selected_template is None:
            tp.logger.warning('No Template selected, please select one first ...')
            return
        new_project = self._selected_template.create_project(project_name=project_name, project_path=project_path)
        if new_project is not None:
            tp.logger.debug('Project {} created successfully on path {}'.format(new_project.name, new_project.project_path))
            self.name_line.setText('')
            self.projectCreated.emit(new_project)
            return new_project


class TemplateData(object):
    PROJECT_CLASS = None

    def __init__(self, name='New Template'):
        self._name = name

    def get_name(self):
        return self._name

    name = property(get_name)

    def create_project(self, project_name, project_path):
        if not self.PROJECT_CLASS:
            qt.logger.warning('Impossible to create because project class is not defined!')
            return
        else:
            new_project = self.PROJECT_CLASS(name=project_name, project_path=project_path)
            new_project.create_project()
            return new_project


class Template(QWidget):
    templateChecked = Signal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setMaximumWidth(160)
        self.setMaximumHeight(200)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(2, 2, 2, 2)
        widget_layout.setSpacing(0)
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        main_frame.setLineWidth(1)
        main_frame.setLayout(widget_layout)
        main_layout.addWidget(main_frame)
        self.project_btn = QPushButton('', self)
        self.project_btn.setCheckable(True)
        self.project_btn.setIcon(self.get_icon())
        self.project_btn.setIconSize(QSize(120, 120))
        project_lbl = QLabel(self.name)
        project_lbl.setStyleSheet('background-color:rgba(0, 0, 0, 150);')
        project_lbl.setAlignment(Qt.AlignCenter)
        widget_layout.addWidget(self.project_btn)
        widget_layout.addWidget(project_lbl)
        self.setup_signals()

    def setup_signals(self):
        self.project_btn.toggled.connect(self._on_selected_template)

    def get_icon(self):
        return tp.ResourcesMgr().icon(name='project', extension='png')

    def _on_selected_template(self, template):
        self.templateChecked.emit(self)


class BlankTemplateData(TemplateData, object):

    def __init__(self, name='Blank'):
        super(BlankTemplateData, self).__init__(name=name)

    def get_name(self):
        return self._name

    name = property(get_name)

    def create_project(self, project_name, project_path):
        new_project = super(BlankTemplateData, self).create_project(project_name=project_name, project_path=project_path)
        new_project.create_folder(consts.DATA_FOLDER)
        new_project.create_folder(consts.CODE_FOLDER)
        return new_project


class BlankTemplate(Template, BlankTemplateData):

    def __init__(self, parent=None):
        BlankTemplateData.__init__(self)
        Template.__init__(self, parent=parent)


class TemplatesViewer(grid.GridWidget, object):
    STANDARD_TEMPLATES = [
     BlankTemplate]
    selectedTemplate = Signal(object)

    def __init__(self, project_class, parent=None):
        self._project_class = project_class
        super(TemplatesViewer, self).__init__(parent=parent)
        self.setShowGrid(False)
        self.setColumnCount(3)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._init_standard_templates()

    def add_template(self, template_widget):
        if template_widget is None:
            return
        template_widget.PROJECT_CLASS = self._project_class
        row, col = self.first_empty_cell()
        self.addWidget(row, col, template_widget)
        self.resizeRowsToContents()

    def _init_standard_templates(self):
        for template in self.STANDARD_TEMPLATES:
            new_template = template()
            new_template.PROJECT_CLASS = self._project_class
            new_template.templateChecked.connect(self._on_template_selected)
            self.add_template(new_template)

    def _on_template_selected(self, template):
        self.selectedTemplate.emit(template)