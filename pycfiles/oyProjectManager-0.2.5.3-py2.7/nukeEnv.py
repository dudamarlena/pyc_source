# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/environments/nukeEnv.py
# Compiled at: 2013-01-11 02:44:37
import os, platform, jinja2, nuke
from oyProjectManager import utils
from oyProjectManager.models.entity import EnvironmentBase

class Nuke(EnvironmentBase):
    """the nuke environment class
    """
    name = 'Nuke'

    def __init__(self, version=None, name='', extensions=None):
        """nuke specific init
        """
        self._root = self.get_root_node()
        self._main_output_node_name = 'MAIN_OUTPUT'

    def get_root_node(self):
        """returns the root node of the current nuke session
        """
        return nuke.toNode('root')

    def save_as(self, version):
        """"the save action for nuke environment
        
        uses Nukes own python binding
        """
        version.extension = '.nk'
        self.project_directory = os.path.dirname(version.path)
        self.create_main_write_node(version)
        self.replace_external_paths()
        try:
            os.makedirs(version.path)
        except OSError:
            pass

        if version.type.type_for == 'Shot':
            self.set_frame_range(version.version_of.start_frame, version.version_of.end_frame)
        nuke.scriptSaveAs(version.full_path)
        return True

    def export_as(self, version):
        """the export action for nuke environment
        """
        version.extension = '.nk'
        nuke.nodeCopy(version.fullPath)
        return True

    def open_(self, version, force=False):
        """the open action for nuke environment
        """
        nuke.scriptOpen(version.full_path)
        self.project_directory = os.path.dirname(version.path)
        self.replace_external_paths()
        return (
         True, [])

    def post_open(self, version):
        """the post open action for the nuke environment
        """
        pass

    def import_(self, version):
        """the import action for nuke environment
        """
        nuke.nodePaste(version.full_path)
        return True

    def get_current_version(self):
        """Finds the Version instance from the current open file.
        
        If it can't find any then returns None.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        full_path = self._root.knob('name').value()
        return self.get_version_from_full_path(full_path)

    def get_version_from_recent_files(self):
        """It will try to create a
        :class:`~oyProjectManager.models.version.Version` instance by looking at
        the recent files list.
        
        It will return None if it can not find one.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        i = 1
        while True:
            try:
                full_path = nuke.recentFile(i)
            except RuntimeError:
                return

            i += 1
            version = self.get_version_from_full_path(full_path)
            if version is not None:
                return version

        return

    def get_version_from_project_dir(self):
        """Tries to find a Version from the current project directory
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        versions = self.get_versions_from_path(self.project_directory)
        version = None
        if versions:
            version = versions[0]
        return version

    def get_last_version(self):
        """gets the file name from nuke
        """
        version = self.get_current_version()
        if version is None:
            version = self.get_version_from_recent_files()
        if version is None:
            version = self.get_version_from_project_dir()
        return version

    def get_frame_range(self):
        """returns the current frame range
        """
        startFrame = int(self._root.knob('first_frame').value())
        endFrame = int(self._root.knob('last_frame').value())
        return (startFrame, endFrame)

    def set_frame_range(self, start_frame=1, end_frame=100, adjust_frame_range=False):
        """sets the start and end frame range
        """
        self._root.knob('first_frame').setValue(start_frame)
        self._root.knob('last_frame').setValue(end_frame)

    def set_fps(self, fps=25):
        """sets the current fps
        """
        self._root.knob('fps').setValue(fps)

    def get_fps(self):
        """returns the current fps
        """
        return int(self._root.knob('fps').getValue())

    def get_main_write_node(self):
        """Returns the main write node in the scene or None.
        """
        all_write_nodes = nuke.allNodes('Write')
        for write_node in all_write_nodes:
            if write_node.name().startswith(self._main_output_node_name):
                main_write_node = write_node
                return main_write_node

        return

    def create_main_write_node(self, version):
        """creates the default write node if there is no one created before.
        """
        main_write_node = self.get_main_write_node()
        if main_write_node is None:
            main_write_node = nuke.nodes.Write()
            main_write_node.setName(self._main_output_node_name)
        output_file_name = ''
        if version.type.type_for == 'Shot':
            output_file_name = version.project.code + '_'
            output_file_name += version.version_of.sequence.code + '_'
        output_file_name += version.base_name + '_' + version.take_name + '_' + version.type.code + '_' + 'Output_' + 'v%03d' % version.version_number + '.###.png'
        output_file_full_path = os.path.join(version.output_path, output_file_name).replace('\\', '/')
        main_write_node['file'].setValue(output_file_full_path)
        try:
            os.makedirs(os.path.dirname(output_file_full_path))
        except OSError:
            pass

        platform_system = platform.system()
        format_id = 11
        if platform_system == 'Darwin':
            format_id = 11
            if nuke.NUKE_VERSION_MAJOR + nuke.NUKE_VERSION_MINOR / 10.0 < 6.3:
                format_id = 12
        main_write_node['file_type'].setValue(format_id)
        main_write_node['channels'].setValue('rgb')
        return

    def replace_external_paths(self, mode=0):
        """replaces file paths with environment variable scripts
        """

        def repPath(path):
            return utils.relpath(self.project_directory, path, '/', '..')

        allNodes = nuke.allNodes()
        readNodes = [ node for node in allNodes if node.Class() == 'Read' ]
        writeNodes = [ node for node in allNodes if node.Class() == 'Write' ]
        readGeoNodes = [ node for node in allNodes if node.Class() == 'ReadGeo' ]
        readGeo2Nodes = [ node for node in allNodes if node.Class() == 'ReadGeo2' ]
        writeGeoNodes = [ node for node in allNodes if node.Class() == 'WriteGeo' ]

        def nodeRep(nodes):
            """helper function to replace path values
            """
            [ node['file'].setValue(repPath(os.path.expandvars(os.path.expanduser(node['file'].getValue())).replace('\\', '/'))) for node in nodes
            ]

        nodeRep(readNodes)
        nodeRep(writeNodes)
        nodeRep(readGeoNodes)
        nodeRep(readGeo2Nodes)
        nodeRep(writeGeoNodes)

    @property
    def project_directory(self):
        """The project directory.
        
        Set it to the project root, and set all your paths relative to this
        directory.
        """
        root = self.get_root_node()
        return root['project_directory'].getValue()

    @project_directory.setter
    def project_directory(self, project_directory_in):
        project_directory_in = project_directory_in.replace('\\', '/')
        root = self.get_root_node()
        root['project_directory'].setValue(project_directory_in)

    def create_slate_info(self):
        """Returns info about the current shot which will contribute to the
        shot slate
        
        :return: string
        """
        version = self.get_current_version()
        shot = version.version_of
        template = jinja2.Template("Show: {{shot.project.name}}\nShot: {{shot.number}}\nFrame Range: {{shot.start_frame}}-{{shot.end_frame}}\nHandles: +{{shot.handle_at_start}}, -{{shot.handle_at_end}}\nArtist: {{version.created_by.name}}\nVersion: v{{'%03d'|format(version.version_number)}}\nStatus: WIP\n        ")
        template_vars = {'shot': shot, 
           'version': version}
        return template.render(**template_vars)