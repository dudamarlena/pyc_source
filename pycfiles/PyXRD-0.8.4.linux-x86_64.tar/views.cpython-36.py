# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/project/views.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2275 bytes
from pkg_resources import resource_filename
from pyxrd.generic.views import DialogView

class ProjectView(DialogView):
    title = 'Edit Project'
    subview_builder = resource_filename(__name__, 'glade/project.glade')
    subview_toplevel = 'nbk_edit_project'
    resizable = False
    widget_format = 'project_%s'
    widget_groups = {'full_mode_only': [
                        'algn_calc_color',
                        'lbl_calccolor',
                        'algn_calc_lw',
                        'calc_lw_lbl']}

    @property
    def specimens_treeview_container(self):
        return self['vbox_specimens']

    @property
    def specimens_treeview(self):
        return self['project_specimens']

    def __init__(self, *args, **kwargs):
        (DialogView.__init__)(self, *args, **kwargs)
        self['popup_menu_item_add_specimen'].set_related_action(self.parent['add_specimen'])
        self['popup_menu_item_edit_specimen'].set_related_action(self.parent['edit_specimen'])
        self['popup_menu_item_import_specimens'].set_related_action(self.parent['import_specimens'])
        self['popup_menu_item_replace_data'].set_related_action(self.parent['replace_specimen_data'])
        self['popup_menu_item_export_data'].set_related_action(self.parent['export_specimen_data'])
        self['popup_menu_item_del_specimen'].set_related_action(self.parent['del_specimen'])

    def present(self, *args, **kwargs):
        (super(ProjectView, self).present)(*args, **kwargs)
        self['nbk_edit_project'].set_current_page(0)

    def show_specimens_context_menu(self, event):
        self['specimen_popup'].popup(None, None, None, None, event.button, event.time)

    def hide_specimens_context_menu(self):
        self['specimen_popup'].hide()

    def set_x_range_sensitive(self, sensitive):
        self['box_manual_xrange'].set_sensitive(sensitive)

    def set_y_range_sensitive(self, sensitive):
        self['box_manual_yrange'].set_sensitive(sensitive)

    def set_selection_state(self, value):
        if value is None:
            self.hide_specimens_context_menu()