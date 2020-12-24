# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/environments/houdiniEnv.py
# Compiled at: 2012-10-23 06:33:01
import os, hou, re
from oyProjectManager import utils
from oyProjectManager.models.asset import Asset
from oyProjectManager.models.entity import EnvironmentBase
from oyProjectManager.models.project import Project
from oyProjectManager.models.repository import Repository
from oyProjectManager.models.sequence import Sequence
from oyProjectManager.models.version import Version
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Houdini(EnvironmentBase):
    """the houdini environment class
    """
    name = 'Houdini'

    def save_as(self, version):
        """the save action for houdini environment
        """
        if not version:
            return
        assert isinstance(version, Version)
        version.extension = 'hip'
        try:
            os.makedirs(os.path.dirname(version.full_path))
        except OSError:
            pass

        hou.hipFile.save(file_name=str(version.full_path))
        self.set_environment_variables(version)
        self.set_render_filename(version)
        hou.hipFile.save(file_name=str(version.full_path))
        self.set_environment_variables(version)
        return True

    def open_(self, version, force=False):
        """the open action for houdini environment
        """
        if not version:
            return
        if hou.hipFile.hasUnsavedChanges() and not force:
            raise RuntimeError
        hou.hipFile.load(file_name=str(version.full_path), suppress_save_prompt=True)
        self.set_environment_variables(version)
        return (
         True, [])

    def post_open(self, version):
        """just skip it
        """
        pass

    def import_(self, version):
        """the import action for houdini environment
        """
        hou.hipFile.merge(str(version.fullPath))
        return True

    def get_current_version(self):
        """Returns the currently opened Version instance
        """
        version = None
        full_path = hou.hipFile.name()
        if full_path != 'untitled.hip':
            version = self.get_version_from_full_path(full_path)
        return version

    def get_version_from_recent_files(self):
        """returns the version from the recent files
        """
        version = None
        recent_files = self.get_recent_file_list()
        for i in range(len(recent_files) - 1, 0, -1):
            version = self.get_version_from_full_path(recent_files[i])
            if version:
                break

        return version

    def get_last_version(self):
        """gets the file name from houdini environment
        """
        version = self.get_current_version()
        if version is None:
            version = self.get_version_from_recent_files()
        return version

    def set_environment_variables(self, version):
        """sets the environment variables according to the given Version
        instance
        """
        if not version:
            return
        logger.debug('version: %s' % version)
        logger.debug('version.path: %s' % version.path)
        logger.debug('version.filename: %s' % version.filename)
        logger.debug('version.full_path: %s' % version.full_path)
        logger.debug('version.full_path (calculated): %s' % os.path.join(version.path, version.filename).replace('\\', '/'))
        job = os.path.dirname(str(version.full_path))
        logger.debug('job: %s' % job)
        os.environ['JOB'] = job
        hou.hscript("set -g JOB = '" + job + "'")
        try:
            hou.allowEnvironmentVariableToOverwriteVariable('JOB', True)
        except AttributeError:
            hou.allowEnvironmentToOverwriteVariable('JOB', True)

    def get_recent_file_list(self):
        """returns the recent HIP files list from the houdini
        """
        fHist = FileHistory()
        return fHist.get_recent_files('HIP')

    def get_frame_range(self):
        """returns the frame range of the
        """
        timeInfo = hou.hscript('tset')[0].split('\n')
        pattern = '[-0-9\\.]+'
        start_frame = int(hou.timeToFrame(float(re.search(pattern, timeInfo[2]).group(0))))
        duration = int(re.search(pattern, timeInfo[0]).group(0))
        end_frame = start_frame + duration - 1
        return (
         start_frame, end_frame)

    def set_frame_range(self, start_frame=1, end_frame=100, adjust_frame_range=False):
        """sets the frame range
        """
        current_frame = hou.frame()
        if current_frame < start_frame:
            hou.setFrame(start_frame)
        else:
            if current_frame > end_frame:
                hou.setFrame(end_frame)
            hou.hscript('tset `(' + str(start_frame) + '-1)/$FPS` `' + str(end_frame) + '/$FPS`')
            output_nodes = self.get_output_nodes()
            for output_node in output_nodes:
                output_node.setParms({'trange': 0, 'f1': start_frame, 'f2': end_frame, 'f3': 1})

    def get_output_nodes(self):
        """returns the rop nodes in the scene
        """
        ropContext = hou.node('/out')
        outNodes = ropContext.children()
        exclude_node_types = [
         hou.nodeType(hou.nodeTypeCategories()['Driver'], 'wedge')]
        new_out_nodes = [ node for node in outNodes if node.type() not in exclude_node_types
                        ]
        return new_out_nodes

    def get_fps(self):
        """returns the current fps
        """
        return int(hou.fps())

    def set_render_filename(self, version):
        """sets the render file name
        """
        render_output_folder = version.output_path
        base_name = version.base_name
        take_name = version.take_name
        version_string = 'v%03d' % version.version_number
        user_initials = version.created_by.initials
        output_filename = os.path.join(render_output_folder, '`$OS`', base_name + '_' + take_name + '_`$OS`_' + version_string + '_' + user_initials + '.$F4.exr')
        output_filename = output_filename.replace('\\', '/')
        job = hou.getenv('JOB')
        while '$' in job:
            job = os.path.expandvars(job)

        job_relative_output_file_path = '$JOB/' + utils.relpath(job, output_filename, '/', '..')
        output_nodes = self.get_output_nodes()
        for output_node in output_nodes:
            if output_node.type().name() == 'ifd':
                try:
                    output_node.setParms({'vm_picture': str(job_relative_output_file_path)})
                except hou.PermissionError:
                    pass

                output_node.setParms({'vm_image_exr_compression': 'zips'})
                output_file_full_path = output_node.evalParm('vm_picture')
                output_file_path = os.path.dirname(output_file_full_path)
                flat_output_file_path = output_file_path
                while '$' in flat_output_file_path:
                    flat_output_file_path = os.path.expandvars(flat_output_file_path)

                try:
                    os.makedirs(flat_output_file_path)
                except OSError:
                    pass

    def set_fps(self, fps=25):
        """sets the time unit of the environment
        """
        if fps <= 0:
            return
        start_frame, end_frame = self.get_frame_range()
        hou.setFps(fps)
        self.set_frame_range(start_frame, end_frame)

    def replace_paths(self):
        """replaces all the paths in all the path related nodes
        """
        pass


class FileHistory(object):
    """A Houdini recent file history parser
    
    Holds the data in a dictionary, where the keys are the file types and the
    values are string list of recent file paths of that type
    """

    def __init__(self):
        self._history_file_name = 'file.history'
        self._history_file_path = ''
        if os.name == 'nt':
            self._history_file_path = os.path.dirname(os.getenv('POSE'))
        else:
            self._history_file_path = os.getenv('HIH')
        self._history_file_full_path = os.path.join(self._history_file_path, self._history_file_name)
        self._buffer = []
        self._history = dict()
        self._read()
        self._parse()

    def _read(self):
        """reads the history file to a buffer
        """
        try:
            history_file = open(self._history_file_full_path)
        except IOError:
            self._buffer = []
            return

        self._buffer = history_file.readlines()
        self._buffer = [ line.strip() for line in self._buffer ]
        history_file.close()

    def _parse(self):
        """parses the data in self._buffer
        """
        self._history = dict()
        buffer_list = self._buffer
        key_name = ''
        path_list = []
        len_buffer = len(buffer_list)
        for i in range(len_buffer):
            if buffer_list[i] == '{':
                key_name = buffer_list[(i - 1)]
                path_list = []
                for j in range(i + 1, len_buffer):
                    current_element = buffer_list[j]
                    if current_element != '}':
                        path_list.append(current_element)
                    else:
                        i = j + 1
                        break

                self._history[key_name] = path_list

    def get_recent_files(self, type_name=''):
        """returns the file list of the given file type
        """
        if type_name == '' or type_name is None:
            return []
        return self._history.get(type_name, [])
        return