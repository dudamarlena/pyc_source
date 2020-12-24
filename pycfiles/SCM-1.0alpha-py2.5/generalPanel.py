# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/generalPanel.py
# Compiled at: 2009-05-29 13:49:10
import wx, os, epscComp.config
from SCMPanel import SCMPanel
from crystalDialog import CrystalDialog
from epscComp.diffractionData import DiffractionData

class GeneralPanel(wx.Panel, SCMPanel):
    """
        Panel to input general parameters of the material
        Data members :
                controller ==> controller from materialNotebook
                treePanel ==> from materialNotebook
    """

    def __init__(self, *args, **kwds):
        SCMPanel.__init__(self, *args, **kwds)
        wx.Panel.__init__(self, *args, **kwds)
        self.controller = self.Parent.Parent.controller
        self.treePanel = self.Parent.Parent.treePanel
        self.file_Material = ''
        self.file_Texture = ''
        self.flagMaterial = 0
        self.flagTexture = 0
        self.flagDiffraction = 0
        self.diffraction = 1
        self.sbox_Volume = wx.StaticBox(self, -1, 'Volume Fraction')
        self.label_Phase1 = wx.StaticText(self, -1, 'Phase1(0.xx):')
        self.label_Phase2 = wx.StaticText(self, -1, 'Phase2(0.xx):')
        self.text_Phase1 = wx.TextCtrl(self, -1, '')
        self.text_Phase2 = wx.TextCtrl(self, -1, '')
        self.sbox_Material = wx.StaticBox(self, -1, 'Material and Deformation File (optional)')
        self.sbox_Texture = wx.StaticBox(self, -1, 'Texture File (optional)')
        self.sbox_Diffraction = wx.StaticBox(self, -1, 'Diffraction Data File (optional)')
        self.sbox_Process = wx.StaticBox(self, -1, 'Process File')
        self.label_NumProcess = wx.StaticText(self, -1, 'Number of Process Files:')
        self.text_NumProcess = wx.TextCtrl(self, -1, '')
        self.Bind(wx.EVT_TEXT, self.OnProcessNum, self.text_NumProcess)
        self.text_Material = wx.TextCtrl(self, -1, '', size=(500, -1))
        self.button_Material = wx.Button(self, 30, 'Browse')
        self.Bind(wx.EVT_BUTTON, self.OnMaterial, self.button_Material)
        self.text_Texture = wx.TextCtrl(self, -1, '', size=(500, -1))
        self.button_Texture = wx.Button(self, 40, 'Browse')
        self.Bind(wx.EVT_BUTTON, self.OnTexture, self.button_Texture)
        self.text_Diffraction = wx.TextCtrl(self, -1, '', size=(500, -1))
        self.button_Diffraction = wx.Button(self, 50, 'Browse')
        self.Bind(wx.EVT_BUTTON, self.OnDiffraction, self.button_Diffraction)
        self.button_OK = wx.Button(self, 10, 'OK')
        self.button_Cancel = wx.Button(self, 20, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.button_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_Cancel)
        self.__do_layout()

    def setProperties(self):
        """ set custom properties to widgets
        """
        self.text_Phase1.SetValue('1.0')
        self.text_Phase2.SetValue('0.0')
        self.text_Phase1.Enable(False)
        self.text_Phase2.Enable(False)
        self.text_NumProcess.SetValue('1')

    def __do_layout(self):
        """ Do layout of all the widgets
        """
        sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_upper = wx.BoxSizer(wx.VERTICAL)
        sizer_btn = wx.BoxSizer(wx.VERTICAL)
        sizer_sbox_Material = wx.StaticBoxSizer(self.sbox_Material, wx.HORIZONTAL)
        sizer_sbox_Texture = wx.StaticBoxSizer(self.sbox_Texture, wx.VERTICAL)
        sizer_sbox_Diffraction = wx.StaticBoxSizer(self.sbox_Diffraction, wx.VERTICAL)
        self.sizer_sbox_Process = wx.StaticBoxSizer(self.sbox_Process, wx.VERTICAL)
        sizer_sbox_Volume = wx.StaticBoxSizer(self.sbox_Volume, wx.VERTICAL)
        self.sizer_upper.Add(sizer_sbox_Volume, 1, wx.EXPAND, 0)
        self.sizer_upper.Add(sizer_sbox_Material, 1, wx.EXPAND, 0)
        self.sizer_upper.Add(sizer_sbox_Texture, 1, wx.EXPAND, 0)
        self.sizer_upper.Add(sizer_sbox_Diffraction, 1, wx.EXPAND, 0)
        self.sizer_upper.Add(self.sizer_sbox_Process, 1, wx.EXPAND, 0)
        grid_sizer_Volume = wx.GridSizer(1, 4, 0, 0)
        grid_sizer_Volume.Add(self.label_Phase1, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        grid_sizer_Volume.Add(self.text_Phase1, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        grid_sizer_Volume.Add(self.label_Phase2, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        grid_sizer_Volume.Add(self.text_Phase2, 0, wx.ALL | wx.ALIGN_LEFT | wx.ADJUST_MINSIZE, 5)
        sizer_sbox_Volume.Add(grid_sizer_Volume, 0, wx.EXPAND, 0)
        grid_sizer_Material = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        grid_sizer_Material.Add(self.text_Material, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        grid_sizer_Material.Add(self.button_Material, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_sbox_Material.Add(grid_sizer_Material, 0, wx.EXPAND, 0)
        grid_sizer_Texture = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        grid_sizer_Texture.Add(self.text_Texture, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        grid_sizer_Texture.Add(self.button_Texture, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_sbox_Texture.Add(grid_sizer_Texture, 0, wx.EXPAND, 0)
        self.grid_sizer_Diffraction = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)
        self.grid_sizer_Diffraction.Add(self.text_Diffraction, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        self.grid_sizer_Diffraction.Add(self.button_Diffraction, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_sbox_Diffraction.Add(self.grid_sizer_Diffraction, 0, wx.EXPAND, 0)
        self.grid_sizer_Process = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        self.grid_sizer_Process.Add(self.label_NumProcess, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ADJUST_MINSIZE, 5)
        self.grid_sizer_Process.Add(self.text_NumProcess, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        self.sizer_sbox_Process.Add(self.grid_sizer_Process, 0, wx.EXPAND, 0)
        grid_sizer_btn = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_btn.Add(self.button_OK, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        grid_sizer_btn.Add(self.button_Cancel, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        sizer_btn.Add(grid_sizer_btn, 0, wx.EXPAND, 0)
        self.sizer_upper.Add(sizer_btn, 1, wx.EXPAND, 0)
        sizer_top.Add(self.sizer_upper, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_top)

    def showVolFrac(self):
        if self.controller.epscData.generalData.saved == True:
            self.text_Phase1.SetValue(self.controller.epscData.generalData.volFracPhase1)
            self.text_Phase2.SetValue(self.controller.epscData.generalData.volFracPhase2)
            self.text_NumProcess.SetValue(self.controller.epscData.generalData.numProcessFiles)
            self.Update()

    def showData(self):
        if self.controller.epscData.phaseNum != 201:
            self.text_Phase1.SetValue(self.controller.epscData.generalData.volFracPhase1)
            self.text_Phase2.SetValue(self.controller.epscData.generalData.volFracPhase2)
        self.text_Material.SetValue(self.controller.epscData.generalData.materialFile[self.kind])
        self.text_Texture.SetValue(self.controller.epscData.generalData.textureFile[self.kind])
        self.text_NumProcess.SetValue(str(self.controller.epscData.generalData.numProcessFiles))
        self.Update()

    def OnMaterial(self, event):
        dlgCrystal = CrystalDialog(self, winSize=(300, 300))
        if dlgCrystal.ShowModal() == wx.ID_OK:
            dlg = wx.FileDialog(self, message='Choose a material information file', defaultDir=os.getcwd(), defaultFile='', wildcard='All files (*.*)|*.*', style=wx.OPEN | wx.CHANGE_DIR)
            if dlg.ShowModal() == wx.ID_OK:
                self.file_Material = dlg.GetPaths()[0]
                self.text_Material.SetValue(dlg.GetPaths()[0])
                self.flagMaterial = 1

    def OnTexture(self, event):
        dlg = wx.FileDialog(self, message='Choose a texture file', defaultDir=os.getcwd(), defaultFile='', wildcard='All files (*.*)|*.*', style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_Texture.SetValue(dlg.GetPaths()[0])
            self.file_Texture = dlg.GetPaths()[0]
            self.flagTexture = 1

    def OnProcessNum(self, event):
        pass

    def OnProcess(self, event):
        pass

    def OnDiffraction(self, event):
        dlg = wx.FileDialog(self, message='Choose a Diffraction file', defaultDir=os.getcwd(), defaultFile='', wildcard='All files (*.*)|*.*', style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_Diffraction.SetValue(dlg.GetPaths()[0])
            self.file_Diffraction = dlg.GetPaths()[0]
            self.flagDiffraction = 1

    def checkInputs(self):
        """ Check whether required input data are entered.
        """
        if self.text_Phase1.IsEmpty() == True:
            msg = 'Volume fractions are required. '
            dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def setEpscDataMaterial(self):
        fid = open(self.controller.epscData.generalData.materialFile[self.kind], 'r')
        findSlip = 0
        while fid:
            line = fid.readline()
            if not line:
                break
            if line.lower().find('material:') >= 0:
                ind1 = line.find(':') + 1
                ind2 = line.find('\n')
                self.controller.epscData.matParam[self.kind].nameMaterial = line[ind1:ind2]
            if line.lower().find('elastic stiffness') >= 0:
                for i in range(6):
                    elastic = fid.readline().split()
                    for j in range(6):
                        self.controller.epscData.matParam[self.kind].elastic[i][j] = elastic[j]

            if line.lower().find('thermal') >= 0:
                thermal = fid.readline().split()
                for i in range(6):
                    self.controller.epscData.matParam[self.kind].thermal[i] = thermal[i]

            if line.lower().find('number of modes') >= 0:
                self.controller.epscData.matParam[self.kind].numSystems = int(fid.readline())
            if line.lower().find('index of modes') >= 0:
                self.controller.epscData.matParam[self.kind].selectedSystems = fid.readline().split()
            if line.find('slip & twinning') < 0 and (line.lower().find('slip') >= 0 or line.lower().find('twin') >= 0):
                findSlip += 1
                if str(findSlip) in self.controller.epscData.matParam[self.kind].selectedSystems:
                    fid.readline()
                    self.controller.epscData.matParam[self.kind].voce[findSlip - 1] = fid.readline().split()

    def setEpscDataTexture(self):
        self.controller.epscData.textureFileNum = 0

    def OnOK(self, event):
        """ Save data when OK button clicked
        """
        if self.checkInputs() == False:
            return
        if float(self.text_Phase1.GetValue()) + float(self.text_Phase2.GetValue()) != 1:
            msg = 'Sum of Volume Fraction should be 1.'
            dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        self.controller.epscData.generalData.volFracPhase1 = self.text_Phase1.GetValue()
        self.controller.epscData.generalData.volFracPhase2 = self.text_Phase2.GetValue()
        self.controller.epscData.generalData.numProcessFiles = self.text_NumProcess.GetValue()
        if self.flagMaterial == 1:
            if os.name == 'nt':
                os.system('copy "' + self.file_Material + '" "' + epscComp.config.dirEpscCore + 'MATERIAL_1.sx"')
            else:
                os.system('cp ' + self.file_Material + ' ' + epscComp.config.dirEpscCore + 'MATERIAL_1.sx')
            self.controller.epscData.generalData.materialFile[self.kind] = self.file_Material
            self.setEpscDataMaterial()
        if self.flagTexture == 1:
            if os.name == 'nt':
                os.system('copy "' + self.file_Texture + '" "' + epscComp.config.dirEpscCore + 'TEXTURE_1.tex"')
            else:
                os.system('cp ' + self.file_Texture + ' ' + epscComp.config.dirEpscCore + 'TEXTURE_1.tex')
            self.controller.epscData.generalData.textureFile[self.kind] = self.file_Texture
            self.setEpscDataTexture()
        if self.flagDiffraction == 1:
            if os.name == 'nt':
                os.system('copy "' + self.file_Diffraction + '" "' + epscComp.config.dirEpscCore + 'DIFFRACTION_1.tex"')
            else:
                os.system('cp ' + self.file_Diffraction + ' ' + epscComp.config.dirEpscCore + 'DIFFRACTION_1.tex')
            self.controller.epscData.generalData.diffractionFile[self.kind] = self.file_Diffraction
        if self.controller.epscData.phaseNum == 201:
            self.updateGeneralFile('epscnp.in')
        else:
            self.update2PhaseGeneralFile('epscnp.in')
        self.treePanel.turnOnNode(self.controller.epscData.phaseNum, 0)
        self.controller.epscData.isAltered = True
        self.controller.epscData.generalData.saved = True
        self.Parent.Parent.addMaterialPanel()
        self.disablePanel()

    def OnCancel(self, event):
        """ Reset values when Cancel button clicked
        """
        if self.controller.epscData.generalData.saved:
            msg = 'You can not revert general panel. '
            dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if self.kind.find('2Phase') >= 0:
            self.text_Phase1.SetValue('')
            self.text_Phase2.SetValue('')
        self.text_Material.SetValue('')
        self.text_Texture.SetValue('')
        self.text_Diffraction.SetValue('')
        self.text_NumProcess.SetValue('1')
        self.controller.epscData.generalData.saved = False
        self.treePanel.turnOffNode(self.controller.epscData.phaseNum, 0)

    def disablePanel(self):
        self.text_Phase1.Enable(False)
        self.text_Phase2.Enable(False)
        self.text_Material.Enable(False)
        self.text_Texture.Enable(False)
        self.text_Diffraction.Enable(False)
        self.text_NumProcess.Enable(False)
        self.button_Diffraction.Enable(False)
        self.button_Material.Enable(False)
        self.button_Texture.Enable(False)

    def dataTemplateFile(self):
        return {'Phase1': 'template_EPSC.in', '2Phase1': 'template_2phase_EPSC.in', '2Phase2': 'template_2phase_EPSC.in'}

    def dataPhaseNum(self):
        return {'2Phase1': '1', '2Phase2': '2'}

    def update2PhaseGeneralFile(self, fileIN):
        """update the material file "epscnp.in"
        """
        fid = open(epscComp.config.dirEpscCore + 'template_2phase_EPSC.in', 'r')
        strAll = ''
        while 1:
            line = fid.readline()
            if not line:
                break
            strAll += line

        strAll = strAll.replace('$VOL_FRAC1', str(self.epscData.generalData.volFracPhase1))
        strAll = strAll.replace('$VOL_FRAC2', str(self.epscData.generalData.volFracPhase2))
        strAll = strAll.replace('$NUM_PROCESSES', str(self.epscData.generalData.numProcessFiles))
        fid.close()
        fid = open(epscComp.config.dirEpscCore + fileIN, 'w')
        fid.write(strAll)
        fid.close()
        print strAll

    def updateGeneralFile(self, fileIN):
        """update the material file "epscnp.in"
        """
        import string
        fid = open(epscComp.config.dirEpscCore + 'template_EPSC.in', 'r')
        flag = 0
        strAll = fid.readline()
        strDiffraction = '*Reads diffracting planes and diffraction directions (1=YES or 0=NO) and file:'
        strProcess = '*Number of thermomechanical processes to be run:'
        while 1:
            line = fid.readline()
            if not line:
                break
            if line.find(strDiffraction) != -1:
                flag = 'diff'
            elif line.find(strProcess) != -1:
                flag = 'process'
            else:
                flag = 0
            if flag == 'diff':
                strAll += line
                strAll += str(self.diffraction) + '            "i_diff_dir"\n'
                fid.readline()
            elif flag == 'process':
                strAll += line
                if self.text_NumProcess.IsEmpty():
                    strAll += fid.readline()
                    strAll += fid.readline()
                    strAll += fid.readline()
                else:
                    strAll += self.text_NumProcess.GetValue() + '            "nproc"\n'
                    fid.readline()
                    strAll += fid.readline()
                    for i in range(int(self.text_NumProcess.GetValue())):
                        strAll += 'PROCESS_' + str(i + 1) + '.pro\n'

                    fid.readline()
            else:
                strAll += line

        fid.close()
        fid = open(epscComp.config.dirEpscCore + fileIN, 'w')
        fid.write(strAll)
        fid.close()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = wx.Frame(None, -1, 'dynamic test', size=(800, 600))
    panel = GeneralPanel(frame)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()