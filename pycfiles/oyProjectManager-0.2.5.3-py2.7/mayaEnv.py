# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/environments/mayaEnv.py
# Compiled at: 2013-02-20 15:51:56
import logging, os
from pymel import core as pm
from oyProjectManager import conf
from oyProjectManager import utils
from oyProjectManager.models.entity import EnvironmentBase
from oyProjectManager.models.repository import Repository
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Maya(EnvironmentBase):
    """the maya environment class
    """
    name = 'Maya'
    time_to_fps = {'sec': 1, 
       '2fps': 2, 
       '3fps': 3, 
       '4fps': 4, 
       '5fps': 5, 
       '6fps': 6, 
       '8fps': 8, 
       '10fps': 10, 
       '12fps': 12, 
       'game': 15, 
       '16fps': 16, 
       '20fps': 20, 
       'film': 24, 
       'pal': 25, 
       'ntsc': 30, 
       '40fps': 40, 
       'show': 48, 
       'palf': 50, 
       'ntscf': 60, 
       '75fps': 75, 
       '80fps': 80, 
       '100fps': 100, 
       '120fps': 120, 
       '125fps': 125, 
       '150fps': 150, 
       '200fps': 200, 
       '240fps': 240, 
       '250fps': 250, 
       '300fps': 300, 
       '375fps': 375, 
       '400fps': 400, 
       '500fps': 500, 
       '600fps': 600, 
       '750fps': 750, 
       'millisec': 1000, 
       '1200fps': 1200, 
       '1500fps': 1500, 
       '2000fps': 2000, 
       '3000fps': 3000, 
       '6000fps': 6000}

    def save_as(self, version):
        """The save_as action for maya environment.
        
        It saves the given Version instance to the Version.full_path.
        """
        self.check_external_files()
        version.extension = '.ma'
        project = version.project
        current_workspace_path = pm.workspace.path
        workspace_path = os.path.dirname(version.path)
        logger.debug('current workspace: %s' % current_workspace_path)
        logger.debug('next workspace: %s' % workspace_path)
        if current_workspace_path != workspace_path:
            logger.debug('changing workspace detected!')
            logger.debug('converting paths to absolute, to be able to preserve external paths')
            self.replace_external_paths(mode=1)
        self.create_workspace_file(workspace_path)
        pm.workspace.open(workspace_path)
        self.create_workspace_folders(workspace_path)
        self.set_fps(project.fps)
        if version.version_number == 1:
            self.set_resolution(project.width, project.height, project.pixel_aspect)
            if version.type.type_for == 'Shot':
                self.set_frame_range(version.version_of.start_frame, version.version_of.end_frame)
        self.set_render_fileName(version)
        self.set_playblast_file_name(version)
        utils.createFolder(version.path)
        unknownNodes = pm.ls(type='unknown')
        pm.delete(unknownNodes)
        self.replace_external_paths(mode=1)
        pm.saveAs(version.full_path, type='mayaAscii')
        self.update_references_list(version)
        self.append_to_recent_files(version.full_path)
        return True

    def export_as(self, version):
        """the export action for maya environment
        """
        if len(pm.ls(sl=True)) < 1:
            raise RuntimeError('There is nothing selected to export')
        self.check_external_files()
        version.extension = '.ma'
        utils.createFolder(version.path)
        workspace_path = os.path.dirname(version.path)
        self.create_workspace_file(workspace_path)
        self.create_workspace_folders(workspace_path)
        pm.exportSelected(version.full_path, type='mayaAscii')
        version.save()
        return True

    def open_(self, version, force=False):
        """The open action for Maya environment.
        
        Opens the given Version file, sets the workspace etc.
        
        It also updates the referenced Version on open.
        
        :returns: list of :class:`~oyProjectManager.models.version.Version`
          instances which are referenced in to the opened version and those
          need to be updated
        """
        previous_workspace_path = pm.workspace.path
        new_workspace = os.path.dirname(version.path)
        pm.workspace.open(new_workspace)
        logger.info('opening file: %s' % version.full_path)
        try:
            pm.openFile(version.full_path, f=force, loadReferenceDepth='none')
        except RuntimeError as e:
            pm.workspace.open(previous_workspace_path)
            raise e

        self.set_playblast_file_name(version)
        self.append_to_recent_files(version.full_path)
        self.replace_external_paths(mode=1)
        to_update_list = self.check_referenced_versions()
        self.update_references_list(version)
        return (
         True, to_update_list)

    def post_open(self, version):
        """Runs after opening a file
        """
        self.load_referenced_versions()
        self.update_references_list(version)

    def import_(self, version):
        """Imports the content of the given Version instance to the current
        scene.
        
        :param version: The desired
          :class:`~oyProjectManager.models.version.Version` to be imported
        """
        pm.importFile(version.full_path)
        return True

    def reference(self, version):
        """References the given Version instance to the current Maya scene.
        
        :param version: The desired
          :class:`~oyProjectManager.models.version.Version` instance to be
          referenced.
        """
        namespace = os.path.basename(version.filename)
        repo = Repository()
        workspace_path = pm.workspace.path
        new_version_full_path = version.full_path
        if version.full_path.startswith(workspace_path):
            new_version_full_path = utils.relpath(workspace_path, version.full_path.replace('\\', '/'), '/', '..')
        new_version_full_path = repo.relative_path(new_version_full_path)
        ref = pm.createReference(new_version_full_path, gl=True, loadReferenceDepth='none', namespace=namespace, options='v=0')
        self.replace_external_paths(1)
        if not ref.isLoaded():
            ref.load()
        current_version = self.get_current_version()
        if current_version:
            current_version.references.append(version)
            current_version.save()
        return True

    def get_version_from_workspace(self):
        """Tries to find a version from the current workspace path
        """
        logger.debug('trying to get the version from workspace')
        workspace_path = pm.workspace.path
        logger.debug('workspace_path: %s' % workspace_path)
        versions = self.get_versions_from_path(workspace_path)
        version = None
        if len(versions):
            version = versions[0]
        logger.debug('version from workspace is: %s' % version)
        return version

    def get_current_version(self):
        """Finds the Version instance from the current Maya session.
        
        If it can't find any then returns None.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        version = None
        full_path = pm.env.sceneName()
        logger.debug('full_path : %s' % full_path)
        if full_path != '':
            logger.debug('trying to get the version from current file')
            version = self.get_version_from_full_path(full_path)
            logger.debug('version from current file: %s' % version)
        return version

    def get_version_from_recent_files(self):
        """It will try to create a
        :class:`~oyProjectManager.models.version.Version` instance by looking at
        the recent files list.
        
        It will return None if it can not find one.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        version = None
        logger.debug('trying to get the version from recent file list')
        try:
            recent_files = pm.optionVar['RecentFilesList']
        except KeyError:
            print 'no recent files'
            recent_files = None

        if recent_files is not None:
            for i in range(len(recent_files) - 1, -1, -1):
                version = self.get_version_from_full_path(recent_files[i])
                if version is not None:
                    break

            logger.debug('version from recent files is: %s' % version)
        return version

    def get_last_version(self):
        """Returns the last opened or the current Version instance from the
        environment.
        
        * It first looks at the current open file full path and tries to match
          it with a Version instance.
        * Then searches for the recent files list.
        * Still not able to find any Version instances, will return the version
          instance with the highest id which has the current workspace path in
          its path
        * Still not able to find any Version instances returns None
        
        :returns: :class:`~oyProjectManager.models.version.Version` instance or
            None
        """
        version = self.get_current_version()
        if version is None:
            version = self.get_version_from_recent_files()
        if version is None:
            version = self.get_version_from_workspace()
        return version

    def set_render_fileName(self, version):
        """sets the render file name
        """
        render_output_folder = version.output_path.replace('\\', '/')
        image_folder_from_ws = pm.workspace.fileRules['images']
        image_folder_from_ws_full_path = os.path.join(os.path.dirname(version.path), image_folder_from_ws).replace('\\', '/')
        render_file_full_path = render_output_folder + '/<Layer>/' + version.project.code + '_'
        if version.type.type_for == 'Shot':
            render_file_full_path += version.version_of.sequence.code + '_'
        render_file_full_path += version.base_name + '_' + version.take_name + '_<Layer>_<RenderPass>_<Version>'
        render_file_rel_path = utils.relpath(image_folder_from_ws_full_path, render_file_full_path, sep='/')
        if self.has_stereo_camera():
            render_file_rel_path += '_<Camera>'
        dRG = pm.PyNode('defaultRenderGlobals')
        dRG.setAttr('imageFilePrefix', render_file_rel_path)
        dRG.setAttr('renderVersion', 'v%03d' % version.version_number)
        dRG.setAttr('animation', 1)
        dRG.setAttr('outFormatControl', 0)
        dRG.setAttr('extensionPadding', 4)
        dRG.setAttr('imageFormat', 7)
        dRG.setAttr('pff', 1)
        self.set_output_file_format()

    def set_output_file_format(self):
        """sets the output file format
        """
        dRG = pm.PyNode('defaultRenderGlobals')
        if dRG.getAttr('currentRenderer') == 'mentalRay':
            dRG.setAttr('imageFormat', 51)
            dRG.setAttr('imfkey', 'exr')
            import pymel
            try:
                if pymel.versions.current() >= pymel.versions.v2012:
                    try:
                        mrG = pm.PyNode('mentalrayGlobals')
                    except pm.general.MayaNodeError:
                        pm.mel.miCreateDefaultNodes()
                        mrG = pm.PyNode('mentalrayGlobals')

                    mrG.setAttr('imageCompression', 4)
            except AttributeError as pm.general.MayaNodeError:
                pass

            try:
                miDF = pm.PyNode('miDefaultFramebuffer')
                miDF.setAttr('datatype', 16)
            except TypeError as pm.general.MayaNodeError:
                pass

    def set_playblast_file_name(self, version):
        """sets the playblast file name
        """
        playblast_path = os.path.join(version.output_path, 'Playblast')
        playblast_filename = version.version_of.project.code
        if version.type.type_for == 'Shot':
            playblast_filename += '_' + version.version_of.sequence.code
        playblast_filename += '_' + os.path.splitext(version.filename)[0]
        playblast_full_path = os.path.join(playblast_path, playblast_filename).replace('\\', '/')
        utils.mkdir(playblast_path)
        pm.optionVar['playblastFile'] = playblast_full_path

    def set_resolution(self, width, height, pixel_aspect=1.0):
        """Sets the resolution of the current scene
        
        :param width: The width of the output image
        :param height: The height of the output image
        :param pixel_aspect: The pixel aspect ratio
        """
        dRes = pm.PyNode('defaultResolution')
        dRes.width.set(width)
        dRes.height.set(height)
        dRes.pixelAspect.set(pixel_aspect)
        dRes.deviceAspectRatio.set(float(width) / float(height))

    def set_project(self, version):
        """Sets the project to the given version.
        
        The Maya version uses :class:`~oyProjectManager.models.version.Version`
        instances to set the project. Because the Maya workspace is related to
        the the Asset or Shot which can be derived from the Version instance
        very easily.
        """
        pm.workspace.open(os.path.dirname(version.path))
        self.set_fps(version.project.fps)

    def append_to_recent_files(self, path):
        """appends the given path to the recent files list
        """
        try:
            recentFiles = pm.optionVar['RecentFilesList']
        except KeyError:
            recentFiles = pm.OptionVarList([], 'RecentFilesList')

        recentFiles.appendVar(path)

    def check_external_files(self):
        """checks for external files in the current scene and raises
        RuntimeError if there are local files in the current scene, used as:
            
            - File Textures
            - Mentalray Textures
            - ImagePlanes
            - IBL nodes
            - References
        """

        def is_in_repo(path):
            """checks if the given path is in repository
            :param path: the path which wanted to be checked
            :return: True or False
            """
            assert isinstance(path, (str, unicode))
            path = os.path.expandvars(path)
            return path.startswith(os.environ[conf.repository_env_key].replace('\\', '/'))

        external_nodes = []
        for file_texture in pm.ls(type=pm.nt.File):
            path = file_texture.attr('fileTextureName').get()
            logger.debug('checking path: %s' % path)
            if path is not None and os.path.isabs(path) and not is_in_repo(path):
                logger.debug('is not in repo: %s' % path)
                external_nodes.append(file_texture)

        for mr_texture in pm.ls(type=pm.nt.MentalrayTexture):
            path = mr_texture.attr('fileTextureName').get()
            logger.debug('path of %s: %s' % (mr_texture, path))
            if path is not None and os.path.isabs(path) and not is_in_repo(path):
                external_nodes.append(mr_texture)

        for image_plane in pm.ls(type=pm.nt.ImagePlane):
            path = image_plane.attr('imageName').get()
            if path is not None and os.path.isabs(path) and not is_in_repo(path):
                external_nodes.append(image_plane)

        for ibl in pm.ls(type=pm.nt.MentalrayIblShape):
            path = ibl.attr('texture').get()
            if path is not None and os.path.isabs(path) and not is_in_repo(path):
                external_nodes.append(ibl)

        if external_nodes:
            pm.select(external_nodes)
            raise RuntimeError('There are external references in your scene!!!\n\nThe problematic nodes are:\n\n' + ('\n\t').join(map(lambda x: x.name(), external_nodes)) + '\n\nThese nodes are added in to your selection list,\nPlease correct them!\n\nYOUR FILE IS NOT GOING TO BE SAVED!!!')
        return

    def check_referenced_versions(self):
        """checks the referenced assets versions
        
        returns a list of Version instances and maya Reference objects in a
        tuple
        """
        version_tuple_list = self.get_referenced_versions()
        to_be_updated_list = []
        for version_tuple in version_tuple_list:
            version = version_tuple[0]
            if not version.is_latest_published_version():
                to_be_updated_list.append(version_tuple)

        return sorted(to_be_updated_list, key=lambda x: x[2])

    def get_referenced_versions(self):
        """Returns the versions those been referenced to the current scene
        
        Returns Version instances and the corresponding Reference instance as a
        tupple in a list, and a string showing the path of the Reference.
        Replaces all the relative paths to absolute paths.
        
        The returned tuple format is as follows:
        (Version, Reference, full_path)
        """
        valid_versions = []
        references = pm.listReferences()
        refs_and_paths = []
        for reference in references:
            temp_version_full_path = reference.path
            temp_version_full_path = os.path.expandvars(os.path.expanduser(os.path.normpath(temp_version_full_path))).replace('\\', '/')
            refs_and_paths.append((reference, temp_version_full_path))

        refs_and_paths = sorted(refs_and_paths, None, lambda x: x[1])
        prev_version = None
        prev_full_path = ''
        for reference, full_path in refs_and_paths:
            if full_path == prev_full_path:
                valid_versions.append((
                 prev_version, reference, prev_full_path))
            else:
                temp_version = self.get_version_from_full_path(full_path)
                if temp_version:
                    valid_versions.append((temp_version, reference, full_path))
                    prev_version = temp_version
                    prev_full_path = full_path

        return sorted(valid_versions, None, lambda x: x[2])

    def update_references_list(self, version=None):
        """updates the references list of the current version
        :param version: the version to be checked
        """
        if version is not None:
            reference_list = []
            reference_info = self.get_referenced_versions()
            for data in reference_info:
                if data[0] not in reference_list:
                    reference_list.append(data[0])

            version.references = reference_list
            version.save()
        return

    def update_versions(self, version_tuple_list):
        """update versions to the latest version
        """
        repo = Repository()
        repo_env_key = '$' + conf.repository_env_key
        previous_version_full_path = ''
        latest_version = None
        for version_tuple in version_tuple_list:
            version = version_tuple[0]
            reference = version_tuple[1]
            version_full_path = version_tuple[2]
            if version_full_path != previous_version_full_path:
                latest_version = version.latest_version()
                previous_version_full_path = version_full_path
            reference.replaceWith(latest_version.full_path.replace(repo.server_path, repo_env_key))

        return

    def get_frame_range(self):
        """returns the current playback frame range
        """
        start_frame = int(pm.playbackOptions(q=True, ast=True))
        end_frame = int(pm.playbackOptions(q=True, aet=True))
        return (start_frame, end_frame)

    def set_frame_range(self, start_frame=1, end_frame=100, adjust_frame_range=False):
        """sets the start and end frame range
        """
        pm.playbackOptions(ast=start_frame, aet=end_frame)
        if adjust_frame_range:
            pm.playbackOptions(min=start_frame, max=end_frame)
        dRG = pm.PyNode('defaultRenderGlobals')
        dRG.setAttr('startFrame', start_frame)
        dRG.setAttr('endFrame', end_frame)

    def get_fps(self):
        """returns the fps of the environment
        """
        return self.time_to_fps[pm.currentUnit(q=1, t=1)]

    def set_fps(self, fps=25):
        """sets the fps of the environment
        """
        current_time = pm.currentTime(q=1)
        pMin = pm.playbackOptions(q=1, min=1)
        pMax = pm.playbackOptions(q=1, max=1)
        pAst = pm.playbackOptions(q=1, ast=1)
        pAet = pm.playbackOptions(q=1, aet=1)
        time_unit = 'pal'
        for key in self.time_to_fps:
            if self.time_to_fps[key] == fps:
                time_unit = key
                break

        pm.currentUnit(t=time_unit, ua=0)
        pm.optionVar['workingUnitTime'] = time_unit
        pm.currentTime(current_time)
        pm.playbackOptions(ast=pAst, aet=pAet)
        pm.playbackOptions(min=pMin, max=pMax)

    def load_referenced_versions(self):
        """loads all the references
        """
        references = pm.listReferences()
        for reference in references:
            reference.load()

    def replace_versions(self, source_reference, target_file):
        """replaces the source reference with the target file
        
        the source_reference may should be in maya reference node
        """
        base_reference_node = source_reference.refNode
        previous_namespace = self.get_full_namespace_from_node_name(source_reference.nodes()[0])
        subReferences = self.get_all_sub_references(source_reference)
        if len(subReferences) > 0:
            allEdits = []
            for subRef in subReferences:
                allEdits += subRef.getReferenceEdits(orn=base_reference_node)

            source_reference.replaceWith(target_file)
            subReferences = self.get_all_sub_references(source_reference)
            newNS = self.get_full_namespace_from_node_name(subReferences[0].nodes()[0])
            allEdits = [ edit.replace(previous_namespace + ':', newNS + ':') for edit in allEdits ]
            for edit in allEdits:
                try:
                    pm.mel.eval(edit)
                except pm.MelError:
                    pass

        else:
            source_reference.replaceWith(target_file)
            subReferences = self.get_all_sub_references(source_reference)
            newNS = self.get_full_namespace_from_node_name(subReferences[0].nodes()[0])
            if previous_namespace != newNS:
                for subRef in self.get_all_sub_references(source_reference):
                    for node in subRef.nodes():
                        nodeNewName = node.longName()
                        nodeOldName = nodeNewName.replace(newNS + ':', previous_namespace + ':')
                        pm.referenceEdit(base_reference_node, changeEditTarget=(nodeOldName, nodeNewName))

                pm.referenceEdit(base_reference_node, applyFailedEdits=True)

    def get_all_sub_references(self, ref):
        """returns the recursive sub references as a list of FileReference
        objects for the given file reference
        """
        allRefs = []
        subRefDict = ref.subReferences()
        if len(subRefDict) > 0:
            for subRefData in subRefDict.iteritems():
                subRef = subRefData[1]
                allRefs.append(subRef)
                allRefs += self.get_all_sub_references(subRef)

        return allRefs

    def get_full_namespace_from_node_name(self, node):
        """dirty way of getting the namespace from node name
        """
        return (':').join(node.name().split(':')[:-1])

    def has_stereo_camera(self):
        """checks if the scene has a stereo camera setup
        returns True if any
        """
        if pm.pluginInfo('stereoCamera', q=True, l=True):
            return len(pm.ls(type='stereoRigTransform')) > 0
        else:
            return False

    def replace_external_paths(self, mode=0):
        """Replaces all the external paths
        
        replaces:
          references: to a path which starts with $REPO env variable in
                      absolute mode and a workspace relative path in relative
                      mode
          file      : to a path which starts with $REPO env variable in
                      absolute mode and a workspace relative path in relative
                      mode
        
        Absolute mode works best for now.
        
        .. note::
          After v0.2.2 the system doesn't care about the mentalrayTexture
          nodes because the lack of a good environment variable support from
          that node. Use regular maya file nodes with mib_texture_filter_lookup
          nodes to have the same sharp results.
        
        :param mode: Defines the process mode:
          if mode == 0 : replaces with relative paths
          if mode == 1 : replaces with absolute paths
        """
        logger.debug('replacing paths with mode: %i' % mode)
        repo = Repository()
        repo_env_key = '$' + conf.repository_env_key
        workspace_path = pm.workspace.path
        server_path = os.environ[conf.repository_env_key]
        if server_path.endswith('/'):
            server_path = server_path[:-1]
        for ref in pm.listReferences():
            unresolved_path = ref.unresolvedPath().replace('\\', '/')
            if not unresolved_path.startswith('$' + conf.repository_env_key):
                if not os.path.isabs(unresolved_path):
                    unresolved_path = os.path.join(workspace_path, unresolved_path)
                if unresolved_path.startswith(server_path):
                    new_ref_path = ''
                    if mode:
                        new_ref_path = ref.path.replace(server_path, repo_env_key)
                    else:
                        new_ref_path = utils.relpath(workspace_path, ref.path)
                    logger.info('replacing reference:', ref.path)
                    logger.info('replacing with:', new_ref_path)
                    ref.replaceWith(new_ref_path)

        for image_file in pm.ls(type='file'):
            file_texture_path = image_file.getAttr('fileTextureName')
            file_texture_path = file_texture_path.replace('\\', '/')
            logger.info('replacing file texture: %s' % file_texture_path)
            file_texture_path = os.path.normpath(os.path.expandvars(file_texture_path))
            file_texture_path = file_texture_path.replace('\\', '/')
            if not os.path.isabs(file_texture_path):
                file_texture_path = os.path.join(workspace_path, file_texture_path).replace('\\', '/')
            new_path = ''
            if mode:
                new_path = file_texture_path.replace(server_path, '$' + conf.repository_env_key)
            else:
                new_path = utils.relpath(workspace_path, file_texture_path, '/', '..')
            logger.info('with: %s' % new_path)
            image_file.setAttr('fileTextureName', new_path)

    def create_workspace_file(self, path):
        """creates the workspace.mel at the given path
        """
        content = conf.maya_workspace_file_content
        full_path = os.path.join(path, 'workspace.mel')
        try:
            os.makedirs(os.path.dirname(full_path))
        except OSError:
            pass

        workspace_file = file(full_path, 'w')
        workspace_file.write(content)
        workspace_file.close()

    def create_workspace_folders(self, path):
        """creates the workspace folders
        :param path: the root of the workspace
        """
        for key in pm.workspace.fileRules:
            rule_path = pm.workspace.fileRules[key]
            full_path = os.path.join(path, rule_path)
            print full_path
            try:
                os.makedirs(full_path)
            except OSError:
                pass