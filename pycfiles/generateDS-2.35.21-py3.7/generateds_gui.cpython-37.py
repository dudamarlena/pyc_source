# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libgenerateDS/gui/generateds_gui.py
# Compiled at: 2020-04-23 13:22:25
# Size of source mod 2**32: 133194 bytes
import sys, os
from optparse import OptionParser
from configparser import ConfigParser
from xml.parsers import expat
import subprocess, re, locale, gettext
if sys.version_info.major == 2:
    import gtk
else:
    import gi
    gi.require_version('Gtk', '3.0')
    import gi.repository as gtk
from libgenerateDS.gui import generateds_gui_session
VERSION = '2.35.21'
Builder = None
ParamNameList = []
CmdTemplate = '%(exec_path)s --no-questions%(force)s%(output_superclass)s%(output_subclass)s%(prefix)s%(namespace_prefix)s%(behavior_filename)s%(properties)s%(old_getters_setters)s%(subclass_suffix)s%(root_element)s%(superclass_module)s%(validator_bodies)s%(user_methods)s%(no_dates)s%(no_versions)s%(no_process_includes)s%(silence)s%(namespace_defs)s%(external_encoding)s%(member_specs)s%(export_spec)s%(one_file_per_xsd)s%(output_directory)s%(module_suffix)s%(preserve_cdata_tags)s%(cleanup_name_list)s %(input_schema)s'
CaptureCmdTemplate = '%(exec_path)s --no-questions%(force)s%(properties)s%(namespace_prefix)s%(output_superclass)s%(output_subclass)s%(prefix)s%(behavior_filename)s%(old_getters_setters)s%(subclass_suffix)s%(root_element)s%(superclass_module)s%(validator_bodies)s%(user_methods)s%(no_dates)s%(no_versions)s%(no_process_includes)s%(silence)s%(namespace_defs)s%(external_encoding)s%(member_specs)s%(export_spec)s%(one_file_per_xsd)s%(output_directory)s%(module_suffix)s%(preserve_cdata_tags)s%(cleanup_name_list)s \\\n    %(input_schema)s'
ErrorMessages = [
 '',
 'Must enter input schema name.',
 'Must enter either output superclass name or output subclass file name.']
Memberspecs_tooltip_text = 'Generate member (type) specifications in each\nclass: a dictionary of instances of class\nMemberSpec_ containing member name, type,\nand array or not.  Allowed values are\n"list" or "dict".  Default: None.\n'

class UIItemSpec(object):

    def __init__(self, name='', ui_type='', access_action=''):
        self.name = name
        self.ui_type = ui_type
        self.access_action = access_action

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_ui_type(self):
        return self.ui_type

    def set_ui_type(self, ui_type):
        self.ui_type = ui_type

    def get_access_action(self):
        return self.access_action

    def set_access_action(self, access_action):
        self.access_action = access_action


class GeneratedsGui(object):

    def __init__(self, options):
        global Builder
        Builder = gtk.Builder()
        Builder.set_translation_domain('generateds_gui')
        self.options = options
        self.filename = None
        self.about_dialog = None
        self.params = generateds_gui_session.sessionType()
        self.ui_obj_dict = {}
        self.session_filename = None
        self.current_folder = None
        ui_spec_filename = options.impl_gui
        try:
            if ui_spec_filename is None:
                Builder.add_from_string(branch_version('Ui_spec, len(Ui_spec)', 'Ui_spec'))
            else:
                Builder.add_from_file(ui_spec_filename)
        except:
            msg = 'Failed to load UI XML file: %s' % ui_spec_filename
            self.error_message(msg)
            sys.exit(1)

        bgo = Builder.get_object
        self.window = bgo('window1')
        self.statusbar = bgo('statusbar1')
        for item in ParamNameList:
            if item.get_ui_type() != 'combobox':
                s1 = '%s_%s' % (item.get_name(), item.get_ui_type())
                setattr(self, s1, bgo(s1))
                self.ui_obj_dict[s1] = bgo(s1)

        member_specs_combobox = branch_version('gtk.combo_box_new_text()', 'gtk.ComboBoxText()')
        member_specs_combobox.set_name('member_specs_combobox')
        member_specs_combobox.set_tooltip_text(Memberspecs_tooltip_text)
        self.ui_obj_dict['member_specs_combobox'] = member_specs_combobox
        member_specs_combobox.append_text('none')
        member_specs_combobox.append_text('list')
        member_specs_combobox.append_text('dict')
        member_specs_combobox_container = bgo('member_specs_combobox_container')
        member_specs_combobox_container.add(member_specs_combobox)
        member_specs_combobox.set_active(0)
        member_specs_combobox.show()
        self.content_dialog = ContentDialog()
        Builder.connect_signals(self)
        Builder.connect_signals(self.content_dialog)
        branch_version('gtk.window_set_default_icon_name(gtk.STOCK_EDIT)', 'gtk.Window.set_default_icon_name(gtk.STOCK_EDIT)')
        self.statusbar_cid = self.statusbar.get_context_id('Tutorial GTK+ Text Editor')
        self.reset_default_status()
        self.params = generateds_gui_session.sessionType()
        session = self.options.session
        if session:
            session = os.path.abspath(session)
            self.session_filename = session
            self.load_session(session)
            msg = 'Session file: %s' % (self.session_filename,)
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, msg)
        else:
            self.trans_gui_2_obj()
            self.saved_params = self.params.copy()

    def on_window_destroy(self, widget, data=None):
        self.trans_gui_2_obj()
        if self.params != self.saved_params:
            message = 'Session data has changed.\n\nSave?'
            if sys.version_info.major == 2:
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE, message)
                dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES, '_Discard', 1, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            else:
                dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT, gtk.MessageType.ERROR, gtk.ButtonsType.NONE, message)
                dialog.add_buttons(gtk.STOCK_YES, gtk.ResponseType.YES, '_Discard', 1, gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL)
            response = dialog.run()
            dialog.destroy()
            if response == branch_version('gtk.RESPONSE_YES', 'gtk.ResponseType.YES'):
                self.save_session_action()
            else:
                if response == 1:
                    pass
                elif response == branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL'):
                    return
        gtk.main_quit()

    def on_window_delete_event(self, widget, event, data=None):
        self.on_window_destroy(widget, data)

    def on_quit_menu_item_activate(self, widget, data=None):
        self.on_window_destroy(widget, data)

    def on_quit_button_clicked(self, widget, data=None):
        self.on_window_destroy(widget, data)

    def on_generate_menuitem_activate(self, menuitem, data=None):
        self.trans_gui_2_obj()
        params_dict = self.trans_params_2_dict()
        result, msg = self.validate_params(params_dict)
        if result:
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, 'Error: %s' % (msg,))
            self.error_message(msg)
        else:
            cmd = self.create_command_line(params_dict, CmdTemplate)
            self.run_command(cmd)
        return True

    on_generate_button_clicked = on_generate_menuitem_activate

    def on_capture_cl_menuitem_activate(self, menuitem, data=None):
        self.trans_gui_2_obj()
        params_dict = self.trans_params_2_dict()
        result, msg = self.validate_params(params_dict)
        if result:
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, 'Error: %s' % (msg,))
            self.error_message(msg)
        else:
            cmd = self.create_command_line(params_dict, CaptureCmdTemplate)
            cmd = cmd.replace(' --', ' \\\n    --')
            cmd = cmd.replace(' -o', ' \\\n    -o')
            cmd = cmd.replace(' -s', ' \\\n    -s')
            cmd = cmd.replace(' -f', ' \\\n    -f')
            cmd = cmd.replace(' -m', ' \\\n    -m')
            self.display_content('Command line', cmd)
        return True

    def trans_gui_2_obj(self):
        for item in ParamNameList:
            ui_name = '%s_%s' % (item.get_name(), item.get_ui_type())
            ui_obj = self.ui_obj_dict[ui_name]
            if ui_obj is not None:
                if item.get_name() == 'member_specs':
                    value = ui_obj.get_active()
                    if value == 1:
                        self.params.set_member_specs('list')
                    elif value == 2:
                        self.params.set_member_specs('dict')
                    else:
                        self.params.set_member_specs('none')
                else:
                    method = getattr(ui_obj, 'get_%s' % item.get_access_action())
                    value = method()
                    setattr(self.params, item.get_name(), value)

    def trans_obj_2_gui(self):
        for item in ParamNameList:
            ui_name = '%s_%s' % (item.get_name(), item.get_ui_type())
            ui_obj = self.ui_obj_dict[ui_name]
            if ui_obj is not None:
                if item.get_name() == 'member_specs':
                    if self.params.get_member_specs() == 'list':
                        ui_obj.set_active(1)
                    elif self.params.get_member_specs() == 'dict':
                        ui_obj.set_active(2)
                    else:
                        ui_obj.set_active(0)
                else:
                    value = getattr(self.params, item.get_name())
                    if value is None:
                        if item.get_ui_type() == 'entry':
                            value = ''
                        else:
                            if item.get_ui_type() == 'checkbutton':
                                value = False
                            else:
                                if item.get_ui_type() == 'combobox':
                                    value = 0
                    method = getattr(ui_obj, 'set_%s' % item.get_access_action())
                    method(value)

    def dump_params(self, msg, params):
        print(msg)
        params.export((sys.stdout), 0, name_='session')

    def trans_params_2_dict(self):
        params = self.params
        params_dict = {}
        pd = params_dict
        pd['input_schema'] = getattr(params, 'input_schema')
        self.transform_1_param(params, pd, 'output_superclass', 'o')
        self.transform_1_param(params, pd, 'output_subclass', 's')
        pd['force'] = ' -f' if params.get_force() else ''
        self.transform_1_param(params, pd, 'prefix', 'p')
        if params.get_empty_namespace_prefix():
            pd['namespace_prefix'] = ' -a ""'
        else:
            self.transform_1_param(params, pd, 'namespace_prefix', 'a')
        self.transform_1_param(params, pd, 'behavior_filename', 'b')
        pd['properties'] = ' -m' if params.get_properties() else ''
        self.transform_1_param(params, pd, 'subclass_suffix', 'subclass-suffix', True)
        self.transform_1_param(params, pd, 'root_element', 'root-element', True)
        self.transform_1_param(params, pd, 'superclass_module', 'super', True)
        pd['old_getters_setters'] = ' --use-old-getter-setter' if params.get_old_getters_setters() else ''
        self.transform_1_param(params, pd, 'user_methods', 'user-methods', True)
        self.transform_1_param(params, pd, 'validator_bodies', 'validator-bodies', True)
        pd['no_dates'] = ' --no-dates' if params.get_no_dates() else ''
        pd['no_versions'] = ' --no-versions' if params.get_no_versions() else ''
        pd['no_process_includes'] = ' --no-process-includes' if params.get_no_process_includes() else ''
        pd['silence'] = ' --silence' if params.get_silence() else ''
        name = 'namespace_defs'
        flag = 'namespacedef'
        value = getattr(params, name)
        params_dict[name] = " --%s='%s'" % (flag, value) if value.strip() else ''
        self.transform_1_param(params, pd, 'external_encoding', 'external-encoding', True)
        if params.get_member_specs() == 'list':
            pd['member_specs'] = ' --member-specs=list'
        else:
            if params.get_member_specs() == 'dict':
                pd['member_specs'] = ' --member-specs=dict'
            else:
                pd['member_specs'] = ''
        self.transform_1_param(params, pd, 'export_spec', 'export', True)
        pd['one_file_per_xsd'] = ' --one-file-per-xsd' if params.get_one_file_per_xsd() else ''
        self.transform_1_param(params, pd, 'output_directory', 'output-directory', True)
        self.transform_1_param(params, pd, 'module_suffix', 'module-suffix', True)
        pd['preserve_cdata_tags'] = ' --preserve-cdata-tags' if params.get_preserve_cdata_tags() else ''
        self.transform_1_param(params, pd, 'cleanup_name_list', 'cleanup-name-list', True)
        return pd

    def transform_1_param(self, params, params_dict, name, flag, longopt=False):
        value = getattr(params, name)
        if longopt:
            params_dict[name] = ' --%s="%s"' % (flag, value) if value.strip() else ''
        else:
            params_dict[name] = ' -%s "%s"' % (flag, value) if value.strip() else ''

    def create_command_line(self, params_dict, template):
        params_dict['exec_path'] = self.options.exec_path
        cmd = template % params_dict
        return cmd

    def validate_params(self, params_dict):
        p = params_dict
        result = 0
        msg = ''
        if not p['input_schema']:
            result = 1
        else:
            if not p['output_superclass']:
                if not p['output_subclass']:
                    result = 2
        if result:
            msg = ErrorMessages[result]
        return (
         result, msg)

    def on_clear_menuitem_activate(self, menuitem, data=None):
        message = 'Clear all entries?\nAre you sure?'
        if sys.version_info.major == 2:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL, message)
        else:
            dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT, gtk.MessageType.WARNING, gtk.ButtonsType.OK_CANCEL, message)
        response = dialog.run()
        dialog.destroy()
        if response == branch_version('gtk.RESPONSE_OK', 'gtk.ResponseType.OK'):
            self.session_filename = None
            self.params = generateds_gui_session.sessionType(input_schema='',
              output_superclass='',
              output_subclass='',
              force=False,
              prefix='',
              namespace_prefix='',
              empty_namespace_prefix=False,
              behavior_filename='',
              properties=False,
              subclass_suffix='',
              root_element='',
              superclass_module='',
              auto_super=False,
              old_getters_setters=False,
              validator_bodies='',
              user_methods='',
              no_dates=False,
              no_versions=False,
              no_process_includes=False,
              silence=False,
              namespace_defs='',
              external_encoding='',
              member_specs='',
              export_spec='',
              one_file_per_xsd=False,
              output_directory='',
              module_suffix='',
              preserve_cdata_tags=False,
              cleanup_name_list='')
            self.trans_obj_2_gui()

    def run_command(self, cmd):
        spobj = subprocess.Popen(cmd,
          shell=True,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          close_fds=False)
        outcontent = spobj.stdout.read()
        errcontent = spobj.stderr.read()
        error = False
        if outcontent.strip():
            self.display_content('Messages', outcontent)
            error = True
        if errcontent.strip():
            self.display_content('Errors', errcontent)
            error = True
        if not error:
            msg = 'Successfully generated.'
            self.error_message(msg, branch_version('gtk.MESSAGE_INFO', 'gtk.MessageType.INFO'))

    def display_content(self, title, content):
        self.content_dialog.show(content)

    def on_open_session_menuitem_activate(self, menuitem, data=None):
        self.trans_gui_2_obj()
        if self.params != self.saved_params:
            message = 'Session data has changed.\n\nSave?'
            if sys.version_info.major == 2:
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE, message)
                dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES, '_Discard', 1, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            else:
                dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT, gtk.MessageType.ERROR, gtk.ButtonsType.NONE, message)
                dialog.add_buttons(gtk.STOCK_YES, gtk.ResponseType.YES, '_Discard', 1, gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL)
            response = dialog.run()
            dialog.destroy()
            if response == branch_version('gtk.RESPONSE_YES', 'gtk.ResponseType.YES'):
                self.save_session_action()
            else:
                if response == 1:
                    pass
                elif response == branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL'):
                    return
        session_filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_OPEN', 'gtk.FileChooserAction.OPEN'), (('Session *.session', '*.session'), ))
        if session_filename:
            self.session_filename = session_filename
            self.load_session(self.session_filename)
            msg = 'Session file: %s' % (self.session_filename,)
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, msg)

    def on_save_session_menuitem_activate(self, menuitem, data=None):
        self.save_session_action()

    def save_session_action(self):
        if not self.session_filename:
            filename = self.choose_filename((branch_version('gtk.FILE_CHOOSER_ACTION_SAVE', 'gtk.FileChooserAction.SAVE')),
              (('Session *.session', '*.session'), ),
              confirm_overwrite=True,
              initfilename=(self.session_filename),
              buttons=(
             gtk.STOCK_CANCEL,
             branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL'),
             gtk.STOCK_SAVE,
             branch_version('gtk.RESPONSE_OK', 'gtk.ResponseType.OK')))
            if filename:
                self.session_filename = filename
        if self.session_filename:
            stem, ext = os.path.splitext(self.session_filename)
            if not ext:
                self.session_filename += '.session'
            self.save_session(self.session_filename)
            msg = 'Session file: %s' % (self.session_filename,)
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, msg)

    def on_save_session_as_menuitem_activate(self, menuitem, data=None):
        filename = self.choose_filename((branch_version('gtk.FILE_CHOOSER_ACTION_SAVE', 'gtk.FileChooserAction.SAVE')),
          (('Session *.session', '*.session'), ),
          confirm_overwrite=True,
          initfilename=(self.session_filename),
          buttons=(
         gtk.STOCK_CANCEL,
         branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL'),
         gtk.STOCK_SAVE,
         branch_version('gtk.RESPONSE_OK', 'gtk.ResponseType.OK')))
        if filename:
            self.session_filename = filename
            stem, ext = os.path.splitext(self.session_filename)
            if not ext:
                self.session_filename += '.session'
            self.save_session(self.session_filename)
            msg = 'Session file: %s' % (self.session_filename,)
            self.statusbar.pop(self.statusbar_cid)
            self.statusbar.push(self.statusbar_cid, msg)

    def save_session(self, filename):
        self.trans_gui_2_obj()
        sessionObj = self.params
        outfile = open(filename, 'w')
        outfile.write('<?xml version="1.0" ?>\n')
        sessionObj.export(outfile,
          0, name_='session', namespacedef_='')
        outfile.close()
        msg = 'Session saved to file:\n%s' % (filename,)
        msgTy = branch_version('gtk.MESSAGE_INFO', 'gtk.MessageType.INFO')
        self.error_message(msg, msgTy)
        self.saved_params = self.params.copy()

    def load_session(self, filename):
        try:
            doc = generateds_gui_session.parsexml_(filename)
            rootNode = doc.getroot()
            rootTag, rootClass = generateds_gui_session.get_root_tag(rootNode)
            if rootClass is None:
                rootClass = generateds_gui_session.sessionType
            sessionObj = rootClass.factory()
            sessionObj.build(rootNode)
            self.params = sessionObj
            self.trans_obj_2_gui()
            self.trans_gui_2_obj()
            self.saved_params = self.params.copy()
        except IOError as exp:
            try:
                msg = str(exp)
                self.error_message(msg)
            finally:
                exp = None
                del exp

        except expat.ExpatError as exp:
            try:
                msg = '%s file: %s' % (str(exp), filename)
                self.error_message(msg)
            finally:
                exp = None
                del exp

    def on_about_menu_item_activate(self, menuitem, data=None):
        if self.about_dialog:
            self.about_dialog.present()
            return
        authors = ['Dave Kuhlman <dkuhlman@rexx.com>']
        about_dialog = gtk.AboutDialog()
        about_dialog.set_transient_for(self.window)
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('generateDS.py Python bindings generator')
        about_dialog.set_version(VERSION)
        about_dialog.set_copyright('Copyright Â© 2009 Dave Kuhlman')
        about_dialog.set_website('http://www.rexx.com/~dkuhlman')
        about_dialog.set_comments('GTK+ and Glade3 GUI front end')
        about_dialog.set_authors(authors)
        about_dialog.set_logo_icon_name(gtk.STOCK_EDIT)

        def close(dialog, response, editor):
            editor.about_dialog = None
            dialog.destroy()

        def delete_event(dialog, event, editor):
            editor.about_dialog = None
            return True

        about_dialog.connect('response', close, self)
        about_dialog.connect('delete-event', delete_event, self)
        self.about_dialog = about_dialog
        about_dialog.show()

    def error_message(self, message, message_type=None):
        if message_type is None:
            message_type = branch_version('gtk.MESSAGE_ERROR', 'gtk.MessageType.ERROR')
        dialog = gtk.MessageDialog(None, branch_version('gtk.DIALOG_MODAL', 'gtk.DialogFlags.MODAL') | branch_version('gtk.DIALOG_DESTROY_WITH_PARENT', 'gtk.DialogFlags.DESTROY_WITH_PARENT'), message_type, branch_version('gtk.BUTTONS_OK', 'gtk.ButtonsType.OK'), message)
        dialog.run()
        dialog.destroy()

    def reset_default_status(self):
        msg = 'Session file: (UNTITLED)'
        self.statusbar.pop(self.statusbar_cid)
        self.statusbar.push(self.statusbar_cid, msg)

    def on_input_schema_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_OPEN', 'gtk.FileChooserAction.OPEN'), (('Schemas *.xsd', '*.xsd'), ))
        if filename:
            self.input_schema_entry.set_text(filename)

    def on_output_superclass_chooser_button_clicked(self, widget, data=None):
        filename = self.choose_filename(patterns=(('Python *.py', '*.py'), ))
        if filename:
            self.output_superclass_entry.set_text(filename)

    def on_output_subclass_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(patterns=(('Python *.py', '*.py'), ))
        if filename:
            self.output_subclass_entry.set_text(filename)

    def on_behavior_filename_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_OPEN', 'gtk.FileChooserAction.OPEN'), (('Python *.py', '*.py'), ))
        if filename:
            self.behavior_filename_entry.set_text(filename)

    def on_validator_bodies_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER', 'gtk.FileChooserAction.SELECT_FOLDER'))
        if filename:
            self.validator_bodies_entry.set_text(filename)

    def on_user_methods_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_OPEN', 'gtk.FileChooserAction.OPEN'), (('Python *.py', '*.py'), ))
        if filename:
            self.user_methods_entry.set_text(filename)

    def on_output_directory_chooser_button_clicked(self, button, data=None):
        filename = self.choose_filename(branch_version('gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER', 'gtk.FileChooserAction.SELECT_FOLDER'))
        if filename:
            self.output_directory_entry.set_text(filename)

    def choose_filename(self, action=None, patterns=(), confirm_overwrite=False, initfilename=None, buttons=None):
        if action is None:
            action = branch_version('gtk.FILE_CHOOSER_ACTION_SAVE', 'gtk.FileChooserAction.SAVE')
        filename = None
        ty_CANCEL = branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL')
        ty_OK = branch_version('gtk.RESPONSE_OK', 'gtk.ResponseType.OK')
        if buttons is None:
            buttons = (gtk.STOCK_CANCEL, ty_CANCEL,
             gtk.STOCK_OPEN, ty_OK)
        dialog = gtk.FileChooserDialog(title=None,
          action=action,
          buttons=buttons)
        if self.current_folder is not None:
            dialog.set_current_folder(self.current_folder)
        if initfilename is not None:
            dialog.set_filename(initfilename)
        if patterns:
            filter = gtk.FileFilter()
            for name, pattern in patterns:
                filter.set_name(name)
                filter.add_pattern(pattern)

            dialog.add_filter(filter)
            filter = gtk.FileFilter()
            filter.set_name('All files *.*')
            filter.add_pattern('*')
            dialog.add_filter(filter)
        dialog.set_do_overwrite_confirmation(confirm_overwrite)
        response = dialog.run()
        if response == branch_version('gtk.RESPONSE_OK', 'gtk.ResponseType.OK'):
            filename = dialog.get_filename()
            self.current_folder = dialog.get_current_folder()
        else:
            if response == branch_version('gtk.RESPONSE_CANCEL', 'gtk.ResponseType.CANCEL'):
                pass
            dialog.destroy()
            return filename

    def on_namespace_prefix_entry_changed(self, widget, data=None):
        checkbutton = self.ui_obj_dict['empty_namespace_prefix_checkbutton']
        checkbutton.set_active(False)
        return True

    def on_empty_namespace_prefix_checkbutton_toggled(self, widget, data=None):
        entry = self.ui_obj_dict['namespace_prefix_entry']
        if widget.get_active():
            entry.set_text('')
        return True

    def on_output_superclass_entry_changed(self, widget, data=None):
        entry = self.ui_obj_dict['superclass_module_entry']
        checkbutton = self.auto_super_checkbutton
        if checkbutton.get_active():
            path = widget.get_text()
            if path:
                stem = os.path.splitext(os.path.split(path)[1])[0]
                if stem:
                    entry.set_text(stem)
        return True

    def on_auto_super_checkbutton_toggled(self, widget, data=None):
        entry = self.ui_obj_dict['superclass_module_entry']
        superclass_entry = self.ui_obj_dict['output_superclass_entry']
        if widget.get_active():
            path = superclass_entry.get_text()
            if path:
                stem = os.path.splitext(os.path.split(path)[1])[0]
                if stem:
                    entry.set_text(stem)
        return True

    def on_ok_button_activate(self, widget, data=None):
        response = self.content_dialog.on_ok_button_activate(self.content_dialog, data)
        return response

    name_pat1 = re.compile('^(.*)_clear_button')

    def on_clear_button_clicked(self, widget, data=None):
        name = widget.get_name() if sys.version_info.major == 2 else gtk.Buildable.get_name(widget)
        mo = GeneratedsGui.name_pat1.search(name)
        if mo is not None:
            stem = mo.group(1)
            name1 = '%s_entry' % (stem,)
            ui_obj = self.ui_obj_dict[name1]
            ui_obj.set_text('')

    def main(self):
        self.window.show()
        gtk.main()


class ContentDialog(gtk.Dialog):

    def __init__(self):
        self.content_dialog = Builder.get_object('content_dialog')
        self.content_textview = Builder.get_object('content_textview')
        self.content_textview.get_buffer().set_text('')

    def show(self, content):
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        self.content_textview.get_buffer().set_text(content)
        self.content_dialog.run()
        self.content_dialog.hide()

    def on_ok_button_activate(self, widget, data=None):
        return False


def branch_version(for_2, for_3):
    """
    The Branch works depends on the version of Python
    """
    if sys.version_info.major == 2:
        return eval(for_2)
    if sys.version_info.major == 3:
        return eval(for_3)
    return eval(for_3)


def capture_options(options):
    config_parser = ConfigParser()
    config_parser.read([
     os.path.expanduser('~/.generateds_gui.ini'),
     './generateds_gui.ini'])
    section = 'general'
    names = ('exec-path', 'exec_path')
    capture_1_option(options, config_parser, section, names)
    names = ('impl-gui', 'impl_gui')
    capture_1_option(options, config_parser, section, names)
    names = ('session', 'session')
    capture_1_option(options, config_parser, section, names)
    if options.exec_path is None:
        options.exec_path = 'generateDS.py'


def capture_1_option(options, config_parser, section, names):
    if getattr(options, names[1]) is None:
        if config_parser.has_option(section, names[0]):
            setattr(options, names[1], config_parser.get(section, names[0]))


def capture_ui_names():
    items = generateds_gui_session.sessionType.member_data_items_
    for item in items:
        ui_item = UIItemSpec(item.get_name())
        if item.get_name() == 'member_specs':
            ui_item.set_ui_type('combobox')
            ui_item.set_access_action('active')
        else:
            if item.get_data_type() == 'xs:string':
                ui_item.set_ui_type('entry')
                ui_item.set_access_action('text')
            else:
                if item.get_data_type() == 'xs:boolean':
                    ui_item.set_ui_type('checkbutton')
                    ui_item.set_access_action('active')
        ParamNameList.append(ui_item)


USAGE_TEXT = '\n    python %prog [options] --session=<some_session_file.session>\nexample:\n    python %prog --session=generator01.session'

def usage(parser):
    parser.print_help()
    sys.exit(1)


def main():
    parser = OptionParser(USAGE_TEXT)
    parser.add_option('--exec-path',
      type='string',
      action='store',
      dest='exec_path',
      help='path to executable generated in command line.  Example: "python /path/to/generateDS.py".  Default: "./generateDS.py".  Use Tools/Generate CL (Ctrl-T) to see it.')
    parser.add_option('--impl-gui',
      type='string',
      action='store',
      dest='impl_gui',
      help='name of glade file that defines the GUI if not embedded.')
    parser.add_option('-s',
      '--session', type='string',
      action='store',
      dest='session',
      help='name of a session file to be loaded.')
    options, args = parser.parse_args()
    capture_options(options)
    capture_ui_names()
    if len(args) > 0:
        usage(parser)
    app_name = 'generateds_gui'
    dir_name = 'locale'
    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain(app_name, dir_name)
    gettext.textdomain(app_name)
    editor = GeneratedsGui(options)
    editor.main()


Ui_spec = '\n<?xml version="1.0" encoding="UTF-8"?>\n<!-- Generated with glade 3.18.3 -->\n<interface>\n  <requires lib="gtk+" version="3.0"/>\n  <object class="GtkAccelGroup" id="accelgroup1"/>\n  <object class="GtkDialog" id="content_dialog">\n    <property name="can_focus">False</property>\n    <property name="border_width">5</property>\n    <property name="title" translatable="yes">Messages and Content</property>\n    <property name="default_width">800</property>\n    <property name="default_height">600</property>\n    <property name="type_hint">normal</property>\n    <child internal-child="vbox">\n      <object class="GtkBox" id="dialog-vbox3">\n        <property name="visible">True</property>\n        <property name="can_focus">False</property>\n        <property name="spacing">2</property>\n        <child internal-child="action_area">\n          <object class="GtkButtonBox" id="dialog-action_area3">\n            <property name="visible">True</property>\n            <property name="can_focus">False</property>\n            <property name="layout_style">end</property>\n            <child>\n              <object class="GtkButton" id="content_dialog_ok_button">\n                <property name="label" translatable="yes">OK</property>\n                <property name="visible">True</property>\n                <property name="can_focus">True</property>\n                <property name="receives_default">True</property>\n                <signal name="activate" handler="on_ok_button_activate" swapped="no"/>\n              </object>\n              <packing>\n                <property name="expand">False</property>\n                <property name="fill">False</property>\n                <property name="position">0</property>\n              </packing>\n            </child>\n          </object>\n          <packing>\n            <property name="expand">False</property>\n            <property name="fill">False</property>\n            <property name="pack_type">end</property>\n            <property name="position">0</property>\n          </packing>\n        </child>\n        <child>\n          <object class="GtkScrolledWindow" id="scrolledwindow1">\n            <property name="visible">True</property>\n            <property name="can_focus">True</property>\n            <property name="min_content_width">250</property>\n            <property name="min_content_height">500</property>\n            <child>\n              <object class="GtkTextView" id="content_textview">\n                <property name="visible">True</property>\n                <property name="can_focus">True</property>\n                <property name="editable">False</property>\n              </object>\n            </child>\n          </object>\n          <packing>\n            <property name="expand">False</property>\n            <property name="fill">True</property>\n            <property name="position">1</property>\n          </packing>\n        </child>\n      </object>\n    </child>\n    <action-widgets>\n      <action-widget response="0">content_dialog_ok_button</action-widget>\n    </action-widgets>\n  </object>\n  <object class="GtkImage" id="image1">\n    <property name="visible">True</property>\n    <property name="can_focus">False</property>\n    <property name="stock">gtk-save</property>\n  </object>\n  <object class="GtkImage" id="image2">\n    <property name="visible">True</property>\n    <property name="can_focus">False</property>\n    <property name="stock">gtk-save-as</property>\n  </object>\n  <object class="GtkImage" id="image3">\n    <property name="visible">True</property>\n    <property name="can_focus">False</property>\n    <property name="stock">gtk-open</property>\n  </object>\n  <object class="GtkImage" id="image4">\n    <property name="visible">True</property>\n    <property name="can_focus">False</property>\n    <property name="stock">gtk-clear</property>\n  </object>\n  <object class="GtkWindow" id="window1">\n    <property name="can_focus">False</property>\n    <accel-groups>\n      <group name="accelgroup1"/>\n    </accel-groups>\n    <signal name="delete-event" handler="on_window_delete_event" swapped="no"/>\n    <child>\n      <object class="GtkVBox" id="vbox1">\n        <property name="visible">True</property>\n        <property name="can_focus">False</property>\n        <child>\n          <object class="GtkMenuBar" id="menubar1">\n            <property name="visible">True</property>\n            <property name="can_focus">False</property>\n            <child>\n              <object class="GtkMenuItem" id="menuitem1">\n                <property name="visible">True</property>\n                <property name="can_focus">False</property>\n                <property name="label" translatable="yes">_File</property>\n                <property name="use_underline">True</property>\n                <child type="submenu">\n                  <object class="GtkMenu" id="menu1">\n                    <property name="visible">True</property>\n                    <property name="can_focus">False</property>\n                    <child>\n                      <object class="GtkImageMenuItem" id="clear_menuitem">\n                        <property name="label">Clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="image">image4</property>\n                        <property name="use_stock">False</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_clear_menuitem_activate" swapped="no"/>\n                        <accelerator key="n" signal="activate" modifiers="GDK_CONTROL_MASK"/>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkImageMenuItem" id="open_session_menuitem">\n                        <property name="label">_Load session</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Load a previous saved session.</property>\n                        <property name="use_underline">True</property>\n                        <property name="image">image3</property>\n                        <property name="use_stock">False</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_open_session_menuitem_activate" swapped="no"/>\n                        <accelerator key="o" signal="activate" modifiers="GDK_CONTROL_MASK"/>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkImageMenuItem" id="save_session_menuitem">\n                        <property name="label">_Save session</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Save the current session.</property>\n                        <property name="use_underline">True</property>\n                        <property name="image">image1</property>\n                        <property name="use_stock">False</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_save_session_menuitem_activate" swapped="no"/>\n                        <accelerator key="s" signal="activate" modifiers="GDK_CONTROL_MASK"/>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkImageMenuItem" id="save_session_as_menuitem">\n                        <property name="label">Save session as ...</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Save the current session in\nfile chosen by the user.</property>\n                        <property name="image">image2</property>\n                        <property name="use_stock">False</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_save_session_as_menuitem_activate" swapped="no"/>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkSeparatorMenuItem" id="menuitem5">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkImageMenuItem" id="imagemenuitem5">\n                        <property name="label">gtk-quit</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Exit from the application.</property>\n                        <property name="use_underline">True</property>\n                        <property name="use_stock">True</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_quit_menu_item_activate" swapped="no"/>\n                      </object>\n                    </child>\n                  </object>\n                </child>\n              </object>\n            </child>\n            <child>\n              <object class="GtkMenuItem" id="menuitem2">\n                <property name="visible">True</property>\n                <property name="can_focus">False</property>\n                <property name="label" translatable="yes">_Tools</property>\n                <property name="use_underline">True</property>\n                <child type="submenu">\n                  <object class="GtkMenu" id="menu2">\n                    <property name="visible">True</property>\n                    <property name="can_focus">False</property>\n                    <child>\n                      <object class="GtkMenuItem" id="capture_cl_menuitem">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Capture the command line that would be used\nto generate the bindings modules.</property>\n                        <property name="label" translatable="yes">_Capture CL</property>\n                        <property name="use_underline">True</property>\n                        <signal name="activate" handler="on_capture_cl_menuitem_activate" swapped="no"/>\n                        <accelerator key="t" signal="activate" modifiers="GDK_CONTROL_MASK"/>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkMenuItem" id="generate_menuitem">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="tooltip_text" translatable="yes">Generate the bindings modules.</property>\n                        <property name="label" translatable="yes">_Generate</property>\n                        <property name="use_underline">True</property>\n                        <signal name="activate" handler="on_generate_menuitem_activate" swapped="no"/>\n                        <accelerator key="g" signal="activate" modifiers="GDK_CONTROL_MASK"/>\n                      </object>\n                    </child>\n                  </object>\n                </child>\n              </object>\n            </child>\n            <child>\n              <object class="GtkMenuItem" id="menuitem4">\n                <property name="visible">True</property>\n                <property name="can_focus">False</property>\n                <property name="label" translatable="yes">_Help</property>\n                <property name="use_underline">True</property>\n                <child type="submenu">\n                  <object class="GtkMenu" id="menu3">\n                    <property name="visible">True</property>\n                    <property name="can_focus">False</property>\n                    <child>\n                      <object class="GtkImageMenuItem" id="imagemenuitem10">\n                        <property name="label">gtk-about</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="use_underline">True</property>\n                        <property name="use_stock">True</property>\n                        <property name="accel_group">accelgroup1</property>\n                        <signal name="activate" handler="on_about_menu_item_activate" swapped="no"/>\n                      </object>\n                    </child>\n                  </object>\n                </child>\n              </object>\n            </child>\n          </object>\n          <packing>\n            <property name="expand">False</property>\n            <property name="fill">True</property>\n            <property name="position">0</property>\n          </packing>\n        </child>\n        <child>\n          <object class="GtkScrolledWindow" id="scrolledwindow2">\n            <property name="visible">True</property>\n            <property name="can_focus">True</property>\n            <property name="shadow_type">in</property>\n            <property name="min_content_width">1000</property>\n            <property name="min_content_height">600</property>\n            <child>\n              <object class="GtkViewport" id="viewport1">\n                <property name="visible">True</property>\n                <property name="can_focus">False</property>\n                <child>\n                  <object class="GtkTable" id="table1">\n                    <property name="visible">True</property>\n                    <property name="can_focus">False</property>\n                    <property name="n_rows">29</property>\n                    <property name="n_columns">4</property>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label1">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Input schema file:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label2">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Output superclass file:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">1</property>\n                        <property name="bottom_attach">2</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label3">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Output subclass file:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">2</property>\n                        <property name="bottom_attach">3</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label4">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Overwrite without asking:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">3</property>\n                        <property name="bottom_attach">4</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="force_checkbutton">\n                        <property name="label" translatable="yes">Force</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Always overwrite output files.\nDo not ask for confirmation.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">3</property>\n                        <property name="bottom_attach">4</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="input_schema_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">The path and name of the\ninput XML schema defining the\nbindings to be generated.</property>\n                        <property name="invisible_char">●</property>\n                        <property name="width_chars">80</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="output_superclass_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">The path and name of the output file\nto be generated and to contain the \nsuperclasses.</property>\n                        <property name="invisible_char">●</property>\n                        <signal name="changed" handler="on_output_superclass_entry_changed" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">1</property>\n                        <property name="bottom_attach">2</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="output_subclass_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">The path and name of the output file\nto be generated and to contain the \nsubclasses.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">2</property>\n                        <property name="bottom_attach">3</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label5">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Prefix (for class names):</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">4</property>\n                        <property name="bottom_attach">5</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="prefix_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Prefix for class names.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">4</property>\n                        <property name="bottom_attach">5</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label6">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Namespace prefix:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">5</property>\n                        <property name="bottom_attach">6</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="namespace_prefix_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="events">GDK_KEY_RELEASE_MASK | GDK_STRUCTURE_MASK</property>\n                        <property name="tooltip_text" translatable="yes">Override default namespace\nprefix in schema file.\nExample: -a "xsd:"\nDefault: "xs:".</property>\n                        <property name="invisible_char">●</property>\n                        <signal name="changed" handler="on_namespace_prefix_entry_changed" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">5</property>\n                        <property name="bottom_attach">6</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label7">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Behavior file name:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">6</property>\n                        <property name="bottom_attach">7</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="behavior_filename_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Input file name for behaviors\nadded to subclasses.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">6</property>\n                        <property name="bottom_attach">7</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label8">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Generate Python properties:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">7</property>\n                        <property name="bottom_attach">8</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="properties_checkbutton">\n                        <property name="label" translatable="yes">Properties</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Generate Python properties for member variables\nso that the value can be retrieved and modified\nwithout calling getter and setter functions.\n</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">7</property>\n                        <property name="bottom_attach">8</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label10">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Subclass suffix:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">9</property>\n                        <property name="bottom_attach">10</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="subclass_suffix_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Append this text to the generated subclass names.\nDefault="Sub".</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">9</property>\n                        <property name="bottom_attach">10</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label11">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Root element:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">10</property>\n                        <property name="bottom_attach">11</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="root_element_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Assume that this value is the name\nof the root element of instance docs.\nDefault is first element defined in schema.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">10</property>\n                        <property name="bottom_attach">11</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="input_schema_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the input schema file.</property>\n                        <signal name="clicked" handler="on_input_schema_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_superclass_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the output superclass bindings file.</property>\n                        <signal name="clicked" handler="on_output_superclass_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">1</property>\n                        <property name="bottom_attach">2</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_subclass_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the output subclass bindings file.</property>\n                        <signal name="clicked" handler="on_output_subclass_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">2</property>\n                        <property name="bottom_attach">3</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="behavior_filename_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the nput file name for\nbehaviors added to subclasses.</property>\n                        <signal name="clicked" handler="on_behavior_filename_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">6</property>\n                        <property name="bottom_attach">7</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label12">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Superclass module:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">11</property>\n                        <property name="bottom_attach">12</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="superclass_module_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Superclass module name in subclass module.\nDefault="???".</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">11</property>\n                        <property name="bottom_attach">12</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label13">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Use old getters and setters:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">12</property>\n                        <property name="bottom_attach">13</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="old_getters_setters_checkbutton">\n                        <property name="label" translatable="yes">Old getters and setters</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Name getters and setters getVar() and setVar(),\ninstead of get_var() and set_var().</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">12</property>\n                        <property name="bottom_attach">13</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label14">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Validator bodies path:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">13</property>\n                        <property name="bottom_attach">14</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label15">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">User methods module:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">14</property>\n                        <property name="bottom_attach">15</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label16">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">No dates:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">15</property>\n                        <property name="bottom_attach">16</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label17">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">No versions:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">16</property>\n                        <property name="bottom_attach">17</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="no_dates_checkbutton">\n                        <property name="label" translatable="yes">No dates in generated output</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Do not include the current date in the generated\nfiles. This is useful if you want to minimize\nthe amount of (no-operation) changes to the\ngenerated python code.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">15</property>\n                        <property name="bottom_attach">16</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="validator_bodies_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Path to a directory containing files that provide\nbodies (implementations) of validator methods.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">13</property>\n                        <property name="bottom_attach">14</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="validator_bodies_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the path to a directory containing files that provide\nbodies (implementations) of validator methods.</property>\n                        <signal name="clicked" handler="on_validator_bodies_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">13</property>\n                        <property name="bottom_attach">14</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="no_versions_checkbutton">\n                        <property name="label" translatable="yes">No version info in generated output</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Do not include the current version in the generated\nfiles. This is useful if you want to minimize\nthe amount of (no-operation) changes to the\ngenerated python code.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">16</property>\n                        <property name="bottom_attach">17</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="user_methods_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the optional module containing user methods.  See\nsection "User Methods" in the documentation.</property>\n                        <signal name="clicked" handler="on_user_methods_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">14</property>\n                        <property name="bottom_attach">15</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="user_methods_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Optional module containing user methods.  See\nsection "User Methods" in the documentation.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">14</property>\n                        <property name="bottom_attach">15</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label18">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">No process includes:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">17</property>\n                        <property name="bottom_attach">18</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label19">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Silence:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">18</property>\n                        <property name="bottom_attach">19</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="no_process_includes_checkbutton">\n                        <property name="label" translatable="yes">Do not process includes in schema</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Do not process included XML Schema files.  By\ndefault, generateDS.py will insert content\nfrom files referenced by &lt;include ... /&gt;\nelements into the XML Schema to be processed.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">17</property>\n                        <property name="bottom_attach">18</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="silence_checkbutton">\n                        <property name="label" translatable="yes">Generate code that does not echo the parsed XML</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Normally, the code generated with generateDS\nechoes the information being parsed. Use\nthis option to turn off that behavior.\n</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">18</property>\n                        <property name="bottom_attach">19</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label20">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Namespace definitions:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">19</property>\n                        <property name="bottom_attach">20</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label21">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">External encoding:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">20</property>\n                        <property name="bottom_attach">21</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label22">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Member specs:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">22</property>\n                        <property name="bottom_attach">23</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="namespace_defs_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Namespace definition to be passed in as the\nvalue for the namespacedef_ parameter of\nthe export() method by the generated\nparse() and parseString() functions.\nDefault=\'\'.  Example:\nxmlns:abc="http://www.abc.com"</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">19</property>\n                        <property name="bottom_attach">20</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="external_encoding_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Encode output written by the generated export\nmethods using this encoding.  Default, if omitted,\nis the value returned by sys.getdefaultencoding().\nExample: utf-8.</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">20</property>\n                        <property name="bottom_attach">21</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkHBox" id="member_specs_combobox_container">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <child>\n                          <placeholder/>\n                        </child>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">22</property>\n                        <property name="bottom_attach">23</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="empty_namespace_prefix_checkbutton">\n                        <property name="label" translatable="yes">Empty</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Assume an empty namespace\nprefix in the XML schema, not\nthe default ("xs:").</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                        <signal name="toggled" handler="on_empty_namespace_prefix_checkbutton_toggled" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">5</property>\n                        <property name="bottom_attach">6</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="auto_super_checkbutton">\n                        <property name="label" translatable="yes">Auto</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Use the superclass file name\nstem as the super-class module\nname.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                        <signal name="toggled" handler="on_auto_super_checkbutton_toggled" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">11</property>\n                        <property name="bottom_attach">12</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="input_schema_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the input schema file entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_superclass_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the output superclass file entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">1</property>\n                        <property name="bottom_attach">2</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_subclass_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the output subclass file entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">2</property>\n                        <property name="bottom_attach">3</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="prefix_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the prefix entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">4</property>\n                        <property name="bottom_attach">5</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="namespace_prefix_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the XML namespace prefix entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">5</property>\n                        <property name="bottom_attach">6</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="behavior_filename_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the behavior file name entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">6</property>\n                        <property name="bottom_attach">7</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="subclass_suffix_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the subclass suffix.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">9</property>\n                        <property name="bottom_attach">10</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="root_element_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the root element entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">10</property>\n                        <property name="bottom_attach">11</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="superclass_module_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the superclass module entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">11</property>\n                        <property name="bottom_attach">12</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="validator_bodies_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the validator bodies path entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">13</property>\n                        <property name="bottom_attach">14</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="user_methods_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the user methods module entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">14</property>\n                        <property name="bottom_attach">15</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="namespace_defs_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the namespace definitions entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">19</property>\n                        <property name="bottom_attach">20</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="external_encoding_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the external encoding entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">20</property>\n                        <property name="bottom_attach">21</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label23">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Get encoded:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">21</property>\n                        <property name="bottom_attach">22</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="get_encoded_checkbutton">\n                        <property name="label" translatable="yes">Getters return encoded values by default</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Getters return encoded value by default if true.\nCan be changed at run-time by either\n(1) changing global variable GetEncodedValue or\n(2) using optional parameter to getter.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">21</property>\n                        <property name="bottom_attach">22</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label24">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Exports:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">23</property>\n                        <property name="bottom_attach">24</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="export_spec_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Specifies export functions to be generated.  Value is a whitespace separated list of any of the following: "write" (write XML to file), "literal" (write out python code), "etree" (build element tree (can serialize to XML)).            Example: "write etree".  Default: "write".</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">23</property>\n                        <property name="bottom_attach">24</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label25">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">One file per XSD:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">24</property>\n                        <property name="bottom_attach">25</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="one_file_per_xsd_checkbutton">\n                        <property name="label" translatable="yes">Create a python module for each XSD processed.</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Create a python module for each XSD processed.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">24</property>\n                        <property name="bottom_attach">25</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label26">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Output directory:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">25</property>\n                        <property name="bottom_attach">26</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="output_directory_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Used in conjunction with --one-file-per-xsd.  The directory where the modules will be created.</property>\n                        <property name="invisible_char">●</property>\n                        <property name="width_chars">80</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">25</property>\n                        <property name="bottom_attach">26</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_directory_chooser_button">\n                        <property name="label" translatable="yes">Choose</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Choose the output directory for one-file-per-xsd.</property>\n                        <signal name="clicked" handler="on_output_directory_chooser_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">2</property>\n                        <property name="right_attach">3</property>\n                        <property name="top_attach">25</property>\n                        <property name="bottom_attach">26</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="output_directory_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the output directory entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">25</property>\n                        <property name="bottom_attach">26</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="export_spec_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the exports entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">23</property>\n                        <property name="bottom_attach">24</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label27">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Module suffix:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">26</property>\n                        <property name="bottom_attach">27</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label28">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Preserve CData tags:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">27</property>\n                        <property name="bottom_attach">28</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkLabel" id="label29">\n                        <property name="visible">True</property>\n                        <property name="can_focus">False</property>\n                        <property name="label" translatable="yes">Cleanup name list:</property>\n                        <property name="xalign">0</property>\n                      </object>\n                      <packing>\n                        <property name="top_attach">28</property>\n                        <property name="bottom_attach">29</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="module_suffix_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">To be used in conjunction with --one-file-per-xsd.  Append XXX to the end of each file created.</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">26</property>\n                        <property name="bottom_attach">27</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkEntry" id="cleanup_name_list_entry">\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="tooltip_text" translatable="yes">Specifies list of 2-tuples used for cleaning names.  First element is a regular expression search pattern and second is a replacement. Example: "[(\'[-:.]\', \'_\'), (\'^__\', \'Special\')]".  Default: "[(\'[-:.]\', \'_\')]".</property>\n                        <property name="invisible_char">●</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">28</property>\n                        <property name="bottom_attach">29</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkCheckButton" id="preserve_cdata_tags_checkbutton">\n                        <property name="label" translatable="yes">Preserve CData tags</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">False</property>\n                        <property name="tooltip_text" translatable="yes">Preserve CDATA tags.  Default: False.</property>\n                        <property name="xalign">0</property>\n                        <property name="draw_indicator">True</property>\n                      </object>\n                      <packing>\n                        <property name="left_attach">1</property>\n                        <property name="right_attach">2</property>\n                        <property name="top_attach">27</property>\n                        <property name="bottom_attach">28</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="module_suffix_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the module suffix entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">26</property>\n                        <property name="bottom_attach">27</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <object class="GtkButton" id="cleanup_name_list_clear_button">\n                        <property name="label">gtk-clear</property>\n                        <property name="visible">True</property>\n                        <property name="can_focus">True</property>\n                        <property name="receives_default">True</property>\n                        <property name="tooltip_text" translatable="yes">Clear the cleanup name list entry.</property>\n                        <property name="use_stock">True</property>\n                        <signal name="clicked" handler="on_clear_button_clicked" swapped="no"/>\n                      </object>\n                      <packing>\n                        <property name="left_attach">3</property>\n                        <property name="right_attach">4</property>\n                        <property name="top_attach">28</property>\n                        <property name="bottom_attach">29</property>\n                      </packing>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                    <child>\n                      <placeholder/>\n                    </child>\n                  </object>\n                </child>\n              </object>\n            </child>\n          </object>\n          <packing>\n            <property name="expand">True</property>\n            <property name="fill">True</property>\n            <property name="position">1</property>\n          </packing>\n        </child>\n        <child>\n          <object class="GtkHBox" id="hbox1">\n            <property name="visible">True</property>\n            <property name="can_focus">False</property>\n            <property name="homogeneous">True</property>\n            <child>\n              <object class="GtkButton" id="generate_button">\n                <property name="label" translatable="yes">Generate</property>\n                <property name="visible">True</property>\n                <property name="can_focus">True</property>\n                <property name="receives_default">True</property>\n                <property name="tooltip_text" translatable="yes">Generate the bindings modules.</property>\n                <signal name="clicked" handler="on_generate_button_clicked" swapped="no"/>\n              </object>\n              <packing>\n                <property name="expand">True</property>\n                <property name="fill">True</property>\n                <property name="position">0</property>\n              </packing>\n            </child>\n            <child>\n              <object class="GtkButton" id="quit_button">\n                <property name="label" translatable="yes">Quit</property>\n                <property name="visible">True</property>\n                <property name="can_focus">True</property>\n                <property name="receives_default">True</property>\n                <property name="tooltip_text" translatable="yes">Exit from the application.</property>\n                <signal name="clicked" handler="on_quit_button_clicked" swapped="no"/>\n              </object>\n              <packing>\n                <property name="expand">True</property>\n                <property name="fill">True</property>\n                <property name="position">1</property>\n              </packing>\n            </child>\n          </object>\n          <packing>\n            <property name="expand">False</property>\n            <property name="fill">False</property>\n            <property name="position">2</property>\n          </packing>\n        </child>\n        <child>\n          <object class="GtkStatusbar" id="statusbar1">\n            <property name="visible">True</property>\n            <property name="can_focus">False</property>\n            <property name="spacing">2</property>\n          </object>\n          <packing>\n            <property name="expand">False</property>\n            <property name="fill">True</property>\n            <property name="position">3</property>\n          </packing>\n        </child>\n        <child>\n          <placeholder/>\n        </child>\n      </object>\n    </child>\n  </object>\n  <object class="GtkImage" id="image5">\n    <property name="visible">True</property>\n    <property name="can_focus">False</property>\n    <property name="stock">gtk-missing-image</property>\n  </object>\n</interface>\n'
if __name__ == '__main__':
    main()