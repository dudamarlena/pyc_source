# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/tools/xgenmanager/widgets/xgenmanager.py
# Compiled at: 2020-03-08 13:20:42
# Size of source mod 2**32: 15172 bytes
"""
Tool that allows to import/export XGen data
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Enrique Velasco'
__license__ = 'MIT'
__maintainer__ = 'Enrique Velasco'
__email__ = 'enriquevelmai@hotmail.com'
import os, json, stat, shutil, logging
from functools import partial
from Qt.QtWidgets import *
import tpDcc as tp, artellapipe
from artellapipe.libs import artella
if tp.is_maya():
    import maya.cmds as mc, xgenm as xg, xgenm.xgGlobal as xgg
LOGGER = logging.getLogger()

class ControlXgenUi(artellapipe.ToolWidget, object):

    def __init__(self, project, config, settings, parent):
        self.shaders_dict = dict()
        self.scalps_list = list()
        self.collection_name = None
        self._project = project
        super(ControlXgenUi, self).__init__(project=project, config=config, settings=settings, parent=parent)

    def ui(self):
        super(ControlXgenUi, self).ui()
        self.ui = tp.ResourcesMgr().gui('xgenmanager')
        if not self.ui:
            LOGGER.error('Error while loading XGen Manager UI ...')
            return
        self.main_layout.addWidget(self.ui)
        self._populate_data()
        self._connect_componets_to_actions()

    def _populate_data(self):
        self.ui.collection_cbx.addItems(self._get_all_collections())
        self.ui.renderer_cbx.addItems(['None', 'Arnold Renderer'])
        self.ui.renderer_cbx.setCurrentIndex(1)
        self.ui.renderer_mode_cbx.addItems(['Live', 'Batch Render'])
        self.ui.renderer_mode_cbx.setCurrentIndex(1)
        self.ui.motion_blur_cbx.addItems(['Use Global Settings', 'On', 'Off'])
        self.ui.extra_depth_sbx.setValue(16)
        self.ui.extra_samples_sbx.setValue(0)
        characters_to_set = os.listdir(os.path.join(artellapipe.AssetsMgr().get_assets_path(), 'Characters'))
        characters_to_set.insert(0, '')
        self.ui.export_character_cbx.addItems(characters_to_set)
        self.ui.import_character_cbx.addItems(characters_to_set)

    def _connect_componets_to_actions(self):
        self.ui.export_go_btn.clicked.connect(self._do_export)
        self.ui.importer_go_btn.clicked.connect(self._do_import)
        self.ui.path_browse_btn.clicked.connect(self._save_file)
        self.ui.groom_file_browser_btn.clicked.connect(self._open_file)
        self.ui.geometry_scalpt_grp_btn.clicked.connect(partial(self._load_selection_to_line, self.ui.geometry_scalpt_grp_txf))
        self.ui.export_character_cbx.currentIndexChanged.connect(partial(self._set_path, self.ui.export_character_cbx, self.ui.path_txf))
        self.ui.import_character_cbx.currentIndexChanged.connect(partial(self._set_path, self.ui.import_character_cbx, self.ui.groom_package_txf))

    def _set_path(self, driver, setter, k):
        """
        Sets path to the text widget
        """
        asset_name = driver.currentText()
        if asset_name:
            save_path = os.path.join(artellapipe.AssetsMgr().get_assets_path(), 'Characters', asset_name, '__working__', 'groom', 'groom_package.groom')
            setter.setText(save_path)
            return
        setter.setText('')

    def _load_selection_to_line(self, qt_object):
        """
        Load selection into the given texfiled
        :param qt_object: QTexField object where to set the selected items
        """
        selection = mc.ls(sl=True)
        text_to_add = '"{}"'.format(selection[0])
        if len(selection) > 1:
            for obj in selection[1:]:
                text_to_add += ';"{}"'.format(obj)

        qt_object.setText(text_to_add)

    def _get_all_collections(self):
        """
        Get all collections in the maya scene
        :return: list, with the collection names
        """
        collections_list = list()
        for item in xg.palettes():
            collections_list.append(item)

        return collections_list

    def _open_file(self):
        """
        Open file dialog, and sets the path to the QTexField
        """
        file_path, _ext = QFileDialog.getOpenFileName(self, dir=(os.environ['HOME']), filter='Folder(.groom)')
        self.ui.groom_package_txf.setText(str(file_path))

    def _save_file(self):
        """
        Save file dialog, and sets the path to the QTexField
        :return:
        """
        file_path, _ext = QFileDialog.getSaveFileName(self, dir=(os.environ['HOME']), filter='Folder(.groom)')
        self.ui.path_txf.setText(str(file_path))

    def _do_export(self):
        """
        Executes the export of the choose collection
        """
        self.collection_name = self.ui.collection_cbx.currentText()
        self.shaders_dict = self._get_shaders()
        self.scalps_list = self._get_scalps()
        ptx_folder = self._get_root_folder()
        export_path = self.ui.path_txf.text()
        self.character = self.ui.export_character_cbx.currentText()
        comment = self.ui.comment_pte.toPlainText()
        if not export_path:
            if not self.character:
                raise ValueError('export path must be specified')
            else:
                if export_path:
                    self.export_path_folder = export_path
                    if '.groom' not in export_path:
                        self.export_path_folder = export_path + '.groom'
                else:
                    working_folder = artella.config.get('server', 'working_folder')
                    self.export_path_folder = os.path.join(self.proje.get_asses_path(), 'Characters', self.character, working_folder, 'groom', 'groom_package.groom')
        else:
            self.delete_artella_folder(self.export_path_folder)
            os.makedirs(self.export_path_folder)
            if '${PROJECT}' in ptx_folder:
                project_path = str(mc.workspace(fullName=True, q=True))
                ptx_folder = os.path.join(project_path, ptx_folder.replace('${PROJECT}', ''))
            LOGGER.debug('XGEN || All data parsed')
            self.ui.progress_lbl.setText('Exporting Files (PTX)')
            shutil.copytree(ptx_folder, os.path.join(self.export_path_folder, self.collection_name))
            LOGGER.debug('XGEN || PTEX files exported')
            xg.exportPalette(palette=(str(self.collection_name)), fileName=(str('{}/{}.xgen'.format(self.export_path_folder, self.collection_name))))
            self.ui.progress_lbl.setText('Exporting Files (.XGEN)')
            LOGGER.debug('XGEN || Collection file exported')
            mc.select((self.scalps_list), replace=True)
            mc.file(rename=(os.path.join(self.export_path_folder, 'scalps.ma')))
            mc.file(es=True, type='mayaAscii')
            mc.select(cl=True)
            self.ui.progress_lbl.setText('Exporting Scalps (.MA)')
            LOGGER.debug('XGEN || Sculpts Exported')
            artellapipe.ShadersMgr().export_shaders(shader_names=(self.shaders_dict.values()), publish=True, comment=comment)
            self.ui.progress_lbl.setText('Exporting Material (.sshader)')
            LOGGER.debug('XGEN || Material Exported')
            with open(os.path.join(self.export_path_folder, 'shader.json'), 'w') as (fp):
                json.dump(self.shaders_dict, fp)
            self.ui.progress_lbl.setText('Exporting Mapping (.JSON)')
            LOGGER.debug('XGEN || Mapping Exported')
            if comment:
                self._add_file_to_artella(file_path_global=(self.export_path_folder), comment=comment)
                LOGGER.debug('XGEN || Files added to artella')
            else:
                LOGGER.warning('XGEN || Files are not been loaded to Artella. Do it manually')

    def _do_import(self):
        """
        Imports the groom into the scene
        """
        import_folder = self.ui.groom_package_txf.text()
        self.character = self.ui.import_character_cbx.currentText()
        if not import_folder:
            raise ValueError('Import path must be specified')
        mc.loadPlugin('xgenToolkit.mll')
        import_path_folder = import_folder.replace('.zip', '')
        _, groom_asset = os.path.split(import_path_folder)
        xgen_file = [f for f in os.listdir(import_path_folder) if f.endswith('.xgen')][(-1)]
        xgen_file = os.path.join(import_path_folder, xgen_file).replace('\\', '/')
        map_folder = [os.path.join(import_path_folder, d) for d in os.listdir(import_path_folder) if os.path.isdir(os.path.join(import_path_folder, d))][0]
        mc.file((os.path.join(import_folder, 'scalps.ma')), i=True, type='mayaAscii', ignoreVersion=True, mergeNamespacesOnClash=False,
          gl=True,
          namespace=(self.character),
          options='v=0',
          groupReference=False)
        in_data = dict()
        with open(os.path.join(import_path_folder, 'mapping.json'), 'r') as (fp):
            in_data = json.load(fp)
        try:
            xg.importPalette(fileName=(str(xgen_file)), deltas=[], nameSpace=(str(self.character)))
        except Exception:
            LOGGER.warning('Not found maps folder')

        xg.setAttr('xgDataPath', str(map_folder), xg.palettes()[0])
        de = xgg.DescriptionEditor
        de.refresh('Full')

    def _get_root_folder(self):
        """
        Gets the xgen root folder
        :return: String with the xgen folder path
        """
        return xg.getAttr('xgDataPath', str(self.collection_name))

    def delete_artella_folder(self, p):
        self.ui.progress_bar.setValue(0)
        self.ui.progress_lbl.setText('Locking Files')
        i = 0
        for root, dirs, files in os.walk(p):
            for file in files:
                i += 1

        if i == 0:
            return
        j = 0
        self.ui.progress_bar.setMinimum(0)
        self.ui.progress_bar.setMaximum(i - 1)
        for root, dirs, files in os.walk(p):
            for file in files:
                artellapipe.FilesMgr().lock_file(file_path=(os.path.join(root, file)))
                self.ui.progress_bar.setValue(j / float(i) * 100)
                LOGGER.debug('XGEN || {} file locked'.format(file))
                j += 1

        shutil.rmtree(p, onerror=(self._on_rm_error))
        LOGGER.debug('XGEN || {} path deleted'.format(p))

    def _add_file_to_artella(self, file_path_global, comment):
        """
        Method that adds all the files of a given path to the artella system
        :param file_path_global: String with the base path to ad
        :param comment: String with the comment to add
        """
        self.ui.progress_bar.setValue(0)
        self.ui.progress_lbl.setText('Uploading Files')
        i = 0
        for root, dirs, files in os.walk(file_path_global):
            for file in files:
                i += 1

        j = 0
        self.ui.progress_bar.setMinimum(0)
        self.ui.progress_bar.setMaximum(i - 1)
        for root, dirs, files in os.walk(file_path_global):
            for file in files:
                artellapipe.FilesMgr().upload_working_version((os.path.join(root, file)), comment=comment, force=True)
                self.ui.progress_bar.setValue(j / float(i) * 100)
                LOGGER.debug('XGEN || {} file added'.format(file))
                j += 1

    def _get_shaders(self):
        """
        Gets a dictionary with the used materials for each description
        :return: Dictionary with the shader --> description mapping
        """
        import pymel.core as pm
        material_dict = dict()
        for description in xg.descriptions(str(self.collection_name)):
            pm.select(description)
            pm.hyperShade(shaderNetworksSelectMaterialNodes=True)
            for shd in pm.selected(materials=True):
                if [c for c in shd.classification() if 'shader/surface' in c]:
                    material_dict[description] = shd.name()

        return material_dict

    def _get_scalps(self):
        """
        Gets a list with the used scalps in the descriptions
        :return: List with the scalps names
        """
        scalps = list()
        for description in xg.descriptions(str(self.collection_name)):
            scalpt = xg.boundGeometry(str(self.collection_name), str(description))[0]
            if scalpt not in scalps:
                scalps.append(scalpt)

        return scalps

    def _on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)