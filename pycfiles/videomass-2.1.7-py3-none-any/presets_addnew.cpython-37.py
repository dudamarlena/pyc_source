# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/presets_addnew.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 12738 bytes
import wx, os, webbrowser, json
get = wx.GetApp()
DIR_CONF = get.DIRconf
OS = get.OS
PASS_1 = _('1-PASS, Do not start with `ffmpeg -i filename`; do not end with `output-filename`')
PASS_2 = _('2-PASS (optional), Do not start with `ffmpeg -i filename`; do not end with `output-filename`')
FORMAT = _('Supported Formats list (optional). Do not include the `.`')

class MemPresets(wx.Dialog):
    __doc__ = '\n    Show dialog to store and edit profiles of a selected preset.\n    '

    def __init__(self, parent, arg, filename, array, title):
        """
        arg: evaluate if this dialog is used for add new profile or
             edit a existing profiles from three message strings:
        arg = 'newprofile'  from preset manager
        arg = 'edit' from preset manager
        arg = 'addprofile' from video and audio conversions

        """
        self.path_prst = os.path.join(DIR_CONF, 'presets', '%s.prst' % filename)
        self.arg = arg
        self.array = array
        wx.Dialog.__init__(self, parent, (-1), title, style=(wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER))
        size_base = wx.BoxSizer(wx.VERTICAL)
        size_namedescr = wx.BoxSizer(wx.HORIZONTAL)
        size_base.Add(size_namedescr, 0, wx.ALL | wx.EXPAND, 0)
        box_name = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Profile Name')), wx.VERTICAL)
        size_namedescr.Add(box_name, 1, wx.ALL | wx.EXPAND, 15)
        self.txt_name = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER))
        box_name.Add(self.txt_name, 0, wx.ALL | wx.EXPAND, 15)
        box_descr = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Description')), wx.VERTICAL)
        size_namedescr.Add(box_descr, 1, wx.ALL | wx.EXPAND, 15)
        self.txt_descript = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER))
        box_descr.Add(self.txt_descript, 0, wx.ALL | wx.EXPAND, 15)
        box_pass1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, PASS_1), wx.VERTICAL)
        size_base.Add(box_pass1, 1, wx.ALL | wx.EXPAND, 15)
        self.pass_1_cmd = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER | wx.TE_MULTILINE))
        box_pass1.Add(self.pass_1_cmd, 1, wx.ALL | wx.EXPAND, 15)
        box_pass2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, PASS_2), wx.VERTICAL)
        size_base.Add(box_pass2, 1, wx.ALL | wx.EXPAND, 15)
        self.pass_2_cmd = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER | wx.TE_MULTILINE))
        box_pass2.Add(self.pass_2_cmd, 1, wx.ALL | wx.EXPAND, 15)
        size_formats = wx.BoxSizer(wx.HORIZONTAL)
        size_base.Add(size_formats, 0, wx.ALL | wx.EXPAND, 0)
        box_supp = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, FORMAT), wx.VERTICAL)
        size_formats.Add(box_supp, 1, wx.ALL | wx.EXPAND, 15)
        self.txt_supp = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER))
        box_supp.Add(self.txt_supp, 0, wx.ALL | wx.EXPAND, 15)
        box_format = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Output Format. Do not include the `.`')), wx.VERTICAL)
        size_formats.Add(box_format, 1, wx.ALL | wx.EXPAND, 15)
        self.txt_ext = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER))
        box_format.Add(self.txt_ext, 0, wx.ALL | wx.EXPAND, 15)
        grdhelp = wx.GridSizer(1, 1, 0, 0)
        btn_help = wx.Button(self, wx.ID_HELP, '')
        grdhelp.Add(btn_help, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn = wx.GridSizer(1, 2, 0, 0)
        grdBtn.Add(grdhelp)
        grdexit = wx.BoxSizer(wx.HORIZONTAL)
        btn_canc = wx.Button(self, wx.ID_CANCEL, '')
        grdexit.Add(btn_canc, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_save = wx.Button(self, wx.ID_OK, _('Save..'))
        grdexit.Add(btn_save, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdexit, flag=(wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT), border=0)
        size_base.Add(grdBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizerAndFit(size_base)
        self.Layout()
        if OS == 'Darwin':
            self.pass_1_cmd.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.pass_2_cmd.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        else:
            self.pass_1_cmd.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.pass_2_cmd.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.txt_name.SetToolTip(_('Assign a short name to the profile'))
        self.txt_descript.SetToolTip(_('Assign a long description to the profile'))
        self.pass_1_cmd.SetToolTip(_('Reserved arguments for the first pass'))
        self.pass_2_cmd.SetToolTip(_('Reserved arguments for the second pass'))
        self.txt_supp.SetToolTip(_('You can specify one or more comma-separated format names to include in the profile'))
        self.txt_ext.SetToolTip(_('Type the output format extension here. Leave blank to copy codec and format'))
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_canc)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_apply, btn_save)
        if arg == 'edit':
            self.array[5] = '' if array[5] == 'copy' else array[5]
            self.change()
        else:
            if arg == 'addprofile':
                self.pass_1_cmd.AppendText(self.array[0])
                self.pass_2_cmd.AppendText(self.array[1])
                self.txt_ext.AppendText(self.array[2])

    def change(self):
        """
        In edit mode only, paste the array items on text boxes

        """
        self.txt_name.AppendText(self.array[0])
        self.txt_descript.AppendText(self.array[1])
        self.pass_1_cmd.AppendText(self.array[2])
        self.pass_2_cmd.AppendText(self.array[3])
        self.txt_supp.AppendText(self.array[4])
        self.txt_ext.AppendText(self.array[5])

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/PresetsManager_Panel/Presets_management.html'
        webbrowser.open(page)

    def on_close(self, event):
        event.Skip()

    def on_apply(self, event):
        name = self.txt_name.GetValue()
        decript = self.txt_descript.GetValue()
        pass_1 = self.pass_1_cmd.GetValue()
        pass_2 = self.pass_2_cmd.GetValue()
        file_support = self.txt_supp.GetValue().strip()
        extens = self.txt_ext.GetValue().strip()
        extens = 'copy' if not extens else extens
        if [txt for txt in [name, decript, pass_1] if txt == '']:
            wx.MessageBox(_('Incomplete profile assignments'), 'Videomass ', wx.ICON_INFORMATION, self)
            return
        if len(file_support.split()) > 1:
            supp = ''.join(file_support.split())
            if [i for i in supp.split() if ',' not in i]:
                wx.MessageBox(_('Formats must be comma-separated'), 'Videomass ', wx.ICON_INFORMATION, self)
                return
        with open((self.path_prst), 'r', encoding='utf-8') as (infile):
            stored_data = json.load(infile)
        if self.arg == 'newprofile' or self.arg == 'addprofile':
            for x in stored_data:
                if x['Name'] == name:
                    wx.MessageBox(_('Profile already stored with same name'), 'Videomass ', wx.ICON_INFORMATION, self)
                    return

            data = [
             {'Name':'%s' % name, 
              'Description':'%s' % decript, 
              'First_pass':'%s' % pass_1, 
              'Second_pass':'%s' % pass_2, 
              'Supported_list':'%s' % file_support, 
              'Output_extension':'%s' % extens}]
            new_data = stored_data + data
            new_data.sort(key=(lambda s: s['Name']))
        else:
            if self.arg == 'edit':
                new_data = stored_data
                for item in new_data:
                    if item['Name'] == self.array[0]:
                        item['Name'] = '%s' % name
                        item['Description'] = '%s' % decript
                        item['First_pass'] = '%s' % pass_1
                        item['Second_pass'] = '%s' % pass_2
                        item['Supported_list'] = '%s' % file_support
                        item['Output_extension'] = '%s' % extens

            new_data.sort(key=(lambda s: s['Name']))
            with open((self.path_prst), 'w', encoding='utf-8') as (outfile):
                json.dump(new_data, outfile, ensure_ascii=False, indent=4)
        if self.arg in ('newprofile', 'addprofile'):
            wx.MessageBox(_('Successful storing!'))
            (self.txt_name.SetValue(''), self.txt_descript.SetValue(''))
            (self.pass_1_cmd.SetValue(''), self.txt_ext.SetValue(''))
            self.txt_supp.SetValue('')
        else:
            if self.arg == 'edit':
                wx.MessageBox(_('Successful changes!'))
            event.Skip()