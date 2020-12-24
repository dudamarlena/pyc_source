# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/GNota/main.py
# Compiled at: 2007-08-30 04:11:39
import os, datetime, gobject, gtk, pango, sys, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.curdir))
from SimpleGladeApp import SimpleGladeApp, bindtextdomain
app_name = 'GNota'
app_version = '0.0.1'
glade_dir = 'data'
locale_dir = ''
bindtextdomain(app_name, locale_dir)
import gettext
gettext.install('gNota', unicode=True)
from model import *
from controller import GNotaController
gnota_controller = GNotaController()
dbpath = create_and_connect_to_default_database()
gnota_controller._do_open_gradebook(dbpath)

class ViewActivities(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='view_activities', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        self.cls = None
        return

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__

    def set_class(self, cls):
        self.cls = cls

    def get_class(self):
        return self.cls

    def sort_func_overall_score(self, treemodel, iter1, iter2, user_data=None):
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        cls = self.get_class()
        s1 = gnota_controller.get_student_overall_score_on_class(s1, cls)
        s2 = gnota_controller.get_student_overall_score_on_class(s2, cls)
        return s2.value - s1.value

    def sort_func_last_name(self, treemodel, iter1, iter2, user_data=None):
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        if s1.last_name > s2.last_name:
            return 1
        elif s1.last_name < s2.last_name:
            return -1
        else:
            return 0

    def sort_activity_score(self, treemodel, iter1, iter2, user_data):
        activity = user_data
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        score1 = gnota_controller.get_student_grade_in_activity(s1, activity)
        score2 = gnota_controller.get_student_grade_in_activity(s2, activity)
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            return 0

    def sort_approved(self, treemodel, iter1, iter2, user_data=None):
        student1 = treemodel.get_value(iter1, 0)
        student2 = treemodel.get_value(iter2, 0)
        average = gnota_controller.get_student_overall_score_on_class(student1, self.get_class())
        approved1 = gnota_controller.is_passing_score(average, self.get_class())
        average = gnota_controller.get_student_overall_score_on_class(student2, self.get_class())
        approved2 = gnota_controller.is_passing_score(average, self.get_class())
        if approved1 == True and approved2 == False:
            return -1
        elif approved1 == False and approved2 == True:
            return 1
        else:
            return 0

    def score_text_changed(self, cellrenderertext, path, new_text, user_data):
        if new_text:
            (model, activity) = user_data
            student = self.grades_treeview.props.model.get_value(model.get_iter(path), 0)
            gnota_controller.add_activity_to_student(activity, student)
            gnota_controller.set_student_grade_in_activity(student, activity, new_text)

    def name_cell_data_func(self, column, cell, model, iter):
        cell.props.text = model.get_value(iter, 0).name

    def activity_cell_data_func(self, column, cell, model, iter, activity):
        student = model.get_value(iter, 0)
        if activity in student.activities:
            grade = gnota_controller.get_student_grade_in_activity(student, activity)
            cell.props.text = str(grade.score)
        else:
            cell.props.text = ''

    def final_score_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        average = gnota_controller.get_student_overall_score_on_class(student, self.get_class())
        cell.props.text = str(average)

    def approved_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        average = gnota_controller.get_student_overall_score_on_class(student, self.get_class())
        passing = gnota_controller.is_passing_score(average, self.get_class())
        cell.props.active = passing
        cell.set_property('cell-background-set', True)
        if not passing:
            cell.props.cell_background = 'red3'
        else:
            cell.props.cell_background = 'medium sea green'

    def populate_grades_treeview(self, cls):
        for column in self.grades_treeview.get_columns():
            self.grades_treeview.remove_column(column)

        n_columns = len(cls.activities) + 3
        ls = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.set_cell_data_func(cell, self.name_cell_data_func)
        column.set_sort_column_id(0)
        ls.set_sort_func(0, self.sort_func_last_name)
        self.grades_treeview.append_column(column)
        for i in range(1, n_columns - 2):
            activity = cls.activities[(i - 1)]
            cell = gtk.CellRendererText()
            cell.props.xalign = 0.5
            cell.props.editable = True
            cell.connect('edited', self.score_text_changed, (ls, activity))
            column = gtk.TreeViewColumn(activity.name, cell)
            column.set_cell_data_func(cell, self.activity_cell_data_func, activity)
            column.set_sort_column_id(i)
            ls.set_sort_func(i, self.sort_activity_score, activity)
            self.grades_treeview.append_column(column)

        cell = gtk.CellRendererText()
        cell.props.xalign = 0.5
        column = gtk.TreeViewColumn(_('Overall score'), cell)
        column.set_cell_data_func(cell, self.final_score_cell_data_func)
        column.set_sort_column_id(n_columns - 2)
        ls.set_sort_func(n_columns - 2, self.sort_func_overall_score)
        self.grades_treeview.append_column(column)
        cell = gtk.CellRendererToggle()
        column = gtk.TreeViewColumn(_('Approved'), cell)
        column.set_cell_data_func(cell, self.approved_cell_data_func)
        column.set_sort_column_id(n_columns - 1)
        ls.set_sort_func(n_columns - 1, self.sort_approved)
        self.grades_treeview.append_column(column)
        for student in gnota_controller.get_students_in_class_orderby(cls):
            ls.append((student,))

        self.grades_treeview.props.model = ls

    def on_view_activities_show(self, widget, *args):
        print 'on_view_activities_show called with self.%s' % widget.get_name()
        self.populate_grades_treeview(self.cls)

    def on_print_button_clicked(self, widget, *args):
        print 'on_print_button_clicked called with self.%s' % widget.get_name()
        raise NotImplementedError

    def on_close_button_clicked(self, widget, *args):
        print 'on_close_button_clicked called with self.%s' % widget.get_name()
        self.view_activities.destroy()


class NewCategory(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='new_category', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        try:
            self.cat
        except AttributeError:
            self.cat = None

        if self.cat is not None:
            self.load_category()
        return

    def load_category(self):
        cat = self.cat
        self.name_entry.props.text = cat.name

    def create_category(self):
        self.new_category.run()
        self.new_category.destroy()
        return self.cat

    def on_cancel_button_clicked(self, widget, *args):
        print 'on_cancel_button_clicked called with self.%s' % widget.get_name()
        self.cat = None
        self.new_category.response(0)
        return

    def on_ok_button_clicked(self, widget, *args):
        print 'on_ok_button_clicked called with self.%s' % widget.get_name()
        name = self.name_entry.props.text
        cat = self.cat
        if cat is None:
            self.cat = gnota_controller.add_category(name)
        else:
            gnota_controller.set_category_name(cat, name)
        self.new_category.response(0)
        return


class MainWindow(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='main_window', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        gnota_controller.add_classes_observer(self)
        gnota_controller.set_view(self)
        self.init_grades_treeview()
        self.init_classes_combobox()
        self.populate_main_window()

    def edit_activity(self, activity):
        ma = self.open_manage_activity_window(activity=activity, cls=activity.activity_class, simple_mode=True, edit_mode=True)
        while ma.manage_activities.props.visible:
            gtk.main_iteration()

    def edit_class(self, cls):
        mc = self.open_manage_classes_window(cls=cls, simple_mode=True)
        while mc.manage_classes.props.visible:
            gtk.main_iteration()

    def close_gradebook(self):
        self.clear_classes_combobox()
        self.clear_grades_treeview()

    def show_save_as(self):
        fcd = gtk.FileChooserDialog(title=_('Select filename and folder to save your GNota gradebook to'), parent=self.main_window, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, 1))
        fcd.props.do_overwrite_confirmation = True
        response = fcd.run()
        if response == 1:
            filename = fcd.get_filename()
        fcd.destroy()
        if response == 1:
            return filename
        else:
            return
        return

    def show_open(self):
        fcd = gtk.FileChooserDialog(title=_('Select the gradebook to open...'), parent=self.main_window, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, 1))
        response = fcd.run()
        if response == 1:
            filename = fcd.get_filename()
        fcd.destroy()
        if response == 1:
            return filename
        else:
            return
        return

    def show_about_dialog(self):
        ad = gtk.AboutDialog()
        ad.props.name = 'GNota'
        ad.props.version = '0.1'
        ad.props.license = 'GPLv3'
        ad.props.copyright = 'Leandro Lameiro'
        ad.props.authors = ['Leandro Lameiro']
        ad.props.website_label = _('GNota webpage')
        ad.props.website = 'https://launchpad.net/gnota'
        ad.props.comments = _('A teachers gradebook')
        ad.run()
        ad.destroy()

    def quit_application(self):
        gtk.main_quit()

    def show_close_confirmation_dialog(self):
        md = gtk.MessageDialog(self.main_window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, _('Your open gradebook has unsaved modifications. Do you want to save it before closing?'))
        md.add_action_widget(gtk.Button(stock=gtk.STOCK_NO), gtk.RESPONSE_NO)
        md.add_action_widget(gtk.Button(stock=gtk.STOCK_CANCEL), gtk.RESPONSE_CANCEL)
        md.add_action_widget(gtk.Button(stock=gtk.STOCK_YES), gtk.RESPONSE_YES)
        md.action_area.show_all()
        resp = md.run()
        md.destroy()
        if resp == gtk.RESPONSE_NO:
            return False
        elif resp == gtk.RESPONSE_CANCEL:
            return
        else:
            return True
        return

    def change_title(self, path):
        self.main_window.props.title = _('GNota - %s') % path

    def populate_main_window(self):
        backup_needed = gnota_controller.add_run_to_current_config()
        if backup_needed:
            bd = BackupDialog()
            bd.backup_dialog.run()
            bd.backup_dialog.destroy()
        self.populate_classes_combobox()
        if len(gnota_controller.classes) > 0:
            self.select_first_class()

    def notify_classes_model_changed(self):
        try:
            selected_class = self.get_selected_class()
        except NoSelectedClassException:
            selected_class = None

        self.populate_classes_combobox()
        try:
            if selected_class is not None:
                self.select_class(selected_class)
        except NoSuchClassException:
            self.select_first_class()

        return

    def open_manage_students_window(self):
        ms = ManageStudents()
        ms.manage_students.show_all()

    def open_manage_classes_window(self, cls=None, simple_mode=False):
        mc = ManageClasses(cls=cls, simple_mode=simple_mode)
        mc.manage_classes.show_all()
        return mc

    def open_manage_categories_window(self):
        mc = ManageCategories()
        mc.manage_categories.show_all()

    def open_manage_activity_window(self, activity, cls, simple_mode, edit_mode):
        ma = ManageActivities(activity=activity, cls=cls, simple_mode=simple_mode, edit_mode=edit_mode)
        ma.manage_activities.show_all()
        return ma

    def sort_func_overall_score(self, treemodel, iter1, iter2, user_data=None):
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        cls = self.get_class()
        s1 = gnota_controller.get_student_overall_score_on_class(s1, cls)
        s2 = gnota_controller.get_student_overall_score_on_class(s2, cls)
        return s2.value - s1.value

    def sort_func_last_name(self, treemodel, iter1, iter2, user_data=None):
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        if s1.last_name > s2.last_name:
            return 1
        elif s1.last_name < s2.last_name:
            return -1
        else:
            return 0

    def sort_missed_classes(self, treemodel, iter1, iter2, user_data):
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        cls = self.get_class()
        score1 = gnota_controller.get_student_overall_score_on_class(s1, cls)
        score2 = gnota_controller.get_student_overall_score_on_class(s2, cls)
        return score2.missed_classes - score1.missed_classes

    def sort_activity_score(self, treemodel, iter1, iter2, user_data):
        activity = user_data
        s1 = treemodel.get_value(iter1, 0)
        s2 = treemodel.get_value(iter2, 0)
        score1 = gnota_controller.get_student_grade_in_activity(s1, activity)
        score2 = gnota_controller.get_student_grade_in_activity(s2, activity)
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            return 0

    def sort_approved(self, treemodel, iter1, iter2, user_data=None):
        student1 = treemodel.get_value(iter1, 0)
        student2 = treemodel.get_value(iter2, 0)
        cls = self.get_class()
        approved1 = gnota_controller.student_approved_in_class(student1, cls)
        approved2 = gnota_controller.student_approved_in_class(student2, cls)
        if approved1 == True and approved2 == False:
            return -1
        elif approved1 == False and approved2 == True:
            return 1
        else:
            return 0

    def move_cursor(self, widget, *args):
        (path, column) = self.grades_treeview.get_cursor()
        gobject.timeout_add(100, lambda t, p, c: t.set_cursor(p, c, True), self.grades_treeview, path, column)

    def get_cellrenderer_model(self, ss):
        model = gtk.ListStore(object, str)
        for ssv in gnota_controller.get_scores_of_discrete_scoresystem(ss):
            model.append((ssv, ssv.symbol))

        return model

    def init_grades_treeview(self):
        self.grades_treeview.props.model = gtk.ListStore(object)

    def populate_grades_treeview(self, cls):
        for column in self.grades_treeview.get_columns():
            self.grades_treeview.remove_column(column)

        self.grades_treeview.connect_after('move-cursor', self.move_cursor)
        n_columns = len(cls.activities) + 4
        self.clear_grades_treeview()
        ls = self.grades_treeview.props.model
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.props.resizable = True
        column.props.expand = True
        column.set_cell_data_func(cell, self.name_cell_data_func)
        column.set_sort_column_id(0)
        ls.set_sort_func(0, self.sort_func_last_name)
        self.grades_treeview.append_column(column)
        for i in range(1, n_columns - 3):
            activity = cls.activities[(i - 1)]
            ss = get_subclassed_scoresystem(activity.scoresystem)
            if isinstance(ss, DiscreteValuesScoreSystem):
                cell = gtk.CellRendererCombo()
                cell.props.model = self.get_cellrenderer_model(ss)
                cell.props.text_column = 1
            else:
                cell = gtk.CellRendererText()
            cell.props.editable = True
            cell.connect('edited', self.score_text_changed, (ls, activity))
            cell.props.xalign = 0.5
            column = gtk.TreeViewColumn(activity.name, cell)
            column.props.resizable = True
            column.props.expand = True
            column.set_cell_data_func(cell, self.activity_cell_data_func, activity)
            column.set_sort_column_id(i)
            ls.set_sort_func(i, self.sort_activity_score, activity)
            self.grades_treeview.append_column(column)

        cell = gtk.CellRendererText()
        cell.props.xalign = 0.5
        column = gtk.TreeViewColumn(_('Overall score'), cell)
        column.props.resizable = True
        column.props.expand = True
        column.set_cell_data_func(cell, self.final_score_cell_data_func)
        column.set_sort_column_id(n_columns - 3)
        ls.set_sort_func(n_columns - 3, self.sort_func_overall_score)
        self.grades_treeview.append_column(column)
        cell = gtk.CellRendererText()
        cell.props.xalign = 0.5
        cell.props.editable = True
        cell.connect('edited', self.missed_classes_text_changed, ls)
        column = gtk.TreeViewColumn(_('Missed classes'), cell)
        column.props.resizable = True
        column.props.expand = True
        column.set_cell_data_func(cell, self.missed_classes_cell_data_func)
        column.set_sort_column_id(n_columns - 2)
        ls.set_sort_func(n_columns - 2, self.sort_missed_classes)
        self.grades_treeview.append_column(column)
        cell = gtk.CellRendererToggle()
        cell.cell_background_set = True
        column = gtk.TreeViewColumn(_('Approved'), cell)
        column.set_cell_data_func(cell, self.approved_cell_data_func)
        column.set_sort_column_id(n_columns - 1)
        ls.set_sort_func(n_columns - 1, self.sort_approved)
        self.grades_treeview.append_column(column)
        for student in gnota_controller.get_students_in_class_orderby(cls):
            ls.append((student,))

    def score_text_changed(self, cellrenderertext, path, new_text, user_data):
        if new_text:
            (model, activity) = user_data
            student = self.grades_treeview.props.model.get_value(model.get_iter(path), 0)
            gnota_controller.add_activity_to_student(activity, student)
            gnota_controller.set_student_grade_in_activity(student, activity, new_text)

    def missed_classes_text_changed(self, cellrenderertext, path, new_text, user_data):
        if new_text:
            model = user_data
            student = self.grades_treeview.props.model.get_value(model.get_iter(path), 0)
            gnota_controller.set_student_missed_classes_in_class(student, self.get_class(), int(new_text))

    def name_cell_data_func(self, column, cell, model, iter):
        cell.props.text = model.get_value(iter, 0).name

    def activity_cell_data_func(self, column, cell, model, iter, activity):
        student = model.get_value(iter, 0)
        if activity in student.activities:
            grade = gnota_controller.get_student_grade_in_activity(student, activity)
            cell.props.text = str(grade.score)
        else:
            cell.props.text = ''

    def final_score_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        average = gnota_controller.get_student_overall_score_on_class(student, self.get_class())
        cell.props.text = str(average)

    def missed_classes_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        average = gnota_controller.get_student_missed_classes_in_class(student, self.get_class())
        cell.props.text = str(average)

    def approved_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        passing = gnota_controller.student_approved_in_class(student, self.get_class())
        cell.props.active = passing
        if not passing:
            cell.props.cell_background = 'red3'
        else:
            cell.props.cell_background = 'medium sea green'

    def class_cell_data_func(self, celllayout, cell, model, iter, user_data=None):
        cls = model.get_value(iter, 0)
        if cls is not None:
            cell.props.text = cls.name
        return

    def init_classes_combobox(self):
        cb = self.classes_combobox
        cb.props.model = model = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.set_cell_data_func(cell, self.class_cell_data_func)

    def populate_classes_combobox(self):
        self.clear_classes_combobox()
        model = self.classes_combobox.props.model
        for cls in gnota_controller.classes:
            model.append((cls,))

    def clear_grades_treeview(self):
        self.grades_treeview.props.model.clear()

    def clear_classes_combobox(self):
        model = self.classes_combobox.props.model
        model.clear()

    def select_first_class(self):
        self.classes_combobox.props.active = 0
        self.populate_grades_treeview_with_selected_class()

    def select_class(self, cls):
        model = self.classes_combobox.props.model
        for treemodelrow in model:
            if treemodelrow[0] == cls:
                self.classes_combobox.set_active_iter(treemodelrow.iter)
                break
        else:
            raise NoSuchClassException('Could not find class in the combobox model.')

        self.populate_grades_treeview_with_selected_class()

    def populate_grades_treeview_with_selected_class(self):
        self.populate_grades_treeview(self.get_selected_class())

    def get_class(self):
        return self.get_selected_class()

    def get_selected_class(self):
        try:
            return self.classes_combobox.props.model.get_value(self.classes_combobox.get_active_iter(), 0)
        except TypeError:
            raise NoSelectedClassException('You must select a class')

    def on_main_window_destroy(self, widget, *args):
        print 'on_main_window_destroy called with self.%s' % widget.get_name()
        self.gtk_main_quit()

    def on_new_imagemenuitem_activate(self, widget, *args):
        print 'on_new_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.new_gradebook()

    def on_open_imagemenuitem_activate(self, widget, *args):
        print 'on_open_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.open_gradebook()

    def on_save_imagemenuitem_activate(self, widget, *args):
        print 'on_save_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.save_gradebook()

    def on_saveas_imagemenuitem_activate(self, widget, *args):
        print 'on_saveas_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.save_gradebook_as()

    def on_close_menuitem_activate(self, widget, *args):
        print 'on_close_menuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.close_gradebook()

    def on_csv_import_menuitem_activate(self, widget, *args):
        print 'on_csv_import_menuitem_activate called with self.%s' % widget.get_name()
        fcd = gtk.FileChooserDialog(title=_('Select the CSV to import'), parent=self.main_window, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, 1))
        response = fcd.run()
        if response == 1:
            filename = fcd.get_filename()
            gnota_controller.import_csv(filename)
        fcd.destroy()

    def on_csv_export_menuitem_activate(self, widget, *args):
        print 'on_csv_export_menuitem_activate called with self.%s' % widget.get_name()
        fcd = gtk.FileChooserDialog(title=_('Select the folder and filename to export your gradebook to'), parent=self.main_window, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, 1))
        response = fcd.run()
        if response == 1:
            filename = fcd.get_filename()
        fcd.destroy()
        if response == 1:
            gnota_controller.export_csv(filename)

    def on_quit_imagemenuitem_activate(self, widget, *args):
        print 'on_quit_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.quit_application()

    def on_grading_menuitem_activate(self, widget, *args):
        print 'on_grading_menuitem_activate called with self.%s' % widget.get_name()
        preferences = Preferences()
        preferences.preferences.show_all()

    def on_manage_students_menuitem_activate(self, widget, *args):
        print 'on_manage_students_menuitem_activate called with self.%s' % widget.get_name()
        self.open_manage_students_window()

    def on_manage_classes_menuitem_activate(self, widget, *args):
        print 'on_manage_classes_menuitem_activate called with self.%s' % widget.get_name()
        self.open_manage_classes_window()

    def on_about_imagemenuitem_activate(self, widget, *args):
        print 'on_about_imagemenuitem_activate called with self.%s' % widget.get_name()
        gnota_controller.open_about_dialog()

    def on_open_toolbutton_clicked(self, widget, *args):
        print 'on_open_toolbutton_clicked called with self.%s' % widget.get_name()
        gnota_controller.open_gradebook()

    def on_save_toolbutton_clicked(self, widget, *args):
        print 'on_save_toolbutton_clicked called with self.%s' % widget.get_name()
        gnota_controller.save_gradebook()

    def on_add_activity_toolbutton_clicked(self, widget, *args):
        print 'on_add_activity_toolbutton_clicked called with self.%s' % widget.get_name()
        ma = ManageActivities(cls=self.get_selected_class(), simple_mode=True)
        ma.manage_activities.show_all()

    def on_edit_classes_toolbutton_clicked(self, widget, *args):
        print 'on_edit_classes_toolbutton_clicked called with self.%s' % widget.get_name()
        self.open_manage_classes_window()

    def on_edit_student_toolbutton_clicked(self, widget, *args):
        print 'on_edit_student_toolbutton_clicked called with self.%s' % widget.get_name()
        self.open_manage_students_window()

    def on_classes_combobox_changed(self, widget, *args):
        print 'on_classes_combobox_changed called with self.%s' % widget.get_name()
        self.populate_grades_treeview_with_selected_class()


class ManageStudents(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='manage_students', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        gnota_controller.add_observer(self)
        self.last_search = ('', '', '', '')

    def notify_model_changed(self):
        self.repeat_last_search()

    def repeat_last_search(self):
        self.search(*self.last_search)

    def search(self, first_name, last_name, code, year):
        self.matches_treeview.props.model = model = gtk.ListStore(str, str, str, int)
        for column in self.matches_treeview.get_columns():
            self.matches_treeview.remove_column(column)

        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Last Name'), gtk.CellRendererText(), text=0))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('First Name'), gtk.CellRendererText(), text=1))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('ID'), gtk.CellRendererText(), text=2))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Year'), gtk.CellRendererText(), text=3))
        self.search_results = []
        for student in gnota_controller.get_students_like(first_name=first_name, last_name=last_name, code=code, year=year):
            model.append((student.last_name, student.first_name, student.code, student.year))
            self.search_results.append(student)

        self.last_search = (first_name, last_name, code, year)

    def search_from_ui(self):
        first_name = self.first_name_entry.props.text
        last_name = self.last_name_entry.props.text
        code = self.student_id_entry.props.text
        try:
            year = int(self.year_entry.props.text)
        except ValueError:
            if self.year_entry.props.text == '':
                year = ''
            else:
                raise

        self.search(first_name, last_name, code, year)

    def get_selected(self):
        return self.search_results[self.matches_treeview.get_selection().get_selected_rows()[1][0][0]]

    def fill_ui_with_student_info(self):
        s = self.get_selected()
        self.first_name_entry.props.text = s.first_name
        self.last_name_entry.props.text = s.last_name
        self.student_id_entry.props.text = s.code
        self.notes_textview.props.buffer.props.text = s.notes
        self.year_entry.props.text = str(s.year)
        self.phone_entry.props.text = s.phone
        self.file_button.set_filename(s.photograph or '')

    def show_student_classes(self):
        msc = ManageStudentClasses(student=self.get_selected())
        msc.manage_student_classes.show_all()

    def clear_fields(self):
        self.first_name_entry.props.text = ''
        self.last_name_entry.props.text = ''
        self.student_id_entry.props.text = ''
        self.notes_textview.props.buffer.props.text = ''
        self.year_entry.props.text = ''
        self.phone_entry.props.text = ''
        self.file_button.set_filename('')

    def remove_from_observables(self):
        gnota_controller.remove_observer(self)

    def close_window(self):
        self.manage_students.destroy()

    def on_manage_students_destroy(self, widget, *args):
        print 'on_manage_students_destroy called with self.%s' % widget.get_name()
        self.remove_from_observables()

    def on_manage_students_show(self, widget, *args):
        print 'on_manage_students_show called with self.%s' % widget.get_name()
        self.search_from_ui()
        self.view_classes_button.get_children()[0].get_children()[0].get_children()[1].props.label = _('View classes')

    def on_matches_treeview_cursor_changed(self, widget, *args):
        print 'on_matches_treeview_cursor_changed called with self.%s' % widget.get_name()
        self.fill_ui_with_student_info()

    def on_view_classes_button_clicked(self, widget, *args):
        print 'on_view_classes_button_clicked called with self.%s' % widget.get_name()
        self.show_student_classes()

    def on_remove_student_button_clicked(self, widget, *args):
        print 'on_remove_student_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.remove_student(self.get_selected())
        self.clear_fields()

    def on_file_button_selection_changed(self, widget, *args):
        print 'on_file_button_selection_changed called with self.%s' % widget.get_name()
        self.photograph_image.props.file = self.file_button.get_filename()

    def on_save_button_clicked(self, widget, *args):
        print 'on_save_button_clicked called with self.%s' % widget.get_name()
        first_name = self.first_name_entry.props.text
        last_name = self.last_name_entry.props.text
        student_id = self.student_id_entry.props.text
        photograph = self.file_button.get_filename() or ''
        notes = self.notes_textview.props.buffer.props.text
        year = int(self.year_entry.props.text)
        phone = self.phone_entry.props.text
        gnota_controller.modify_student(self.get_selected(), first_name=first_name, last_name=last_name, code=student_id, photograph=photograph, notes=notes, year=year, phone=phone)

    def on_add_student_button_clicked(self, widget, *args):
        print 'on_add_student_button_clicked called with self.%s' % widget.get_name()
        first_name = self.first_name_entry.props.text
        last_name = self.last_name_entry.props.text
        student_id = self.student_id_entry.props.text
        photograph = self.file_button.get_filename()
        notes = self.notes_textview.props.buffer.props.text
        try:
            year = int(self.year_entry.props.text)
        except ValueError:
            year = 0

        phone = self.phone_entry.props.text
        gnota_controller.add_student(first_name=first_name, last_name=last_name, code=student_id, photograph=photograph, notes=notes, year=year, phone=phone)
        self.clear_fields()

    def on_search_button_clicked(self, widget, *args):
        print 'on_search_button_clicked called with self.%s' % widget.get_name()
        self.search_from_ui()

    def on_close_button_clicked(self, widget, *args):
        print 'on_close_button_clicked called with self.%s' % widget.get_name()
        self.close_window()


class ManageClasses(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='manage_classes', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        gnota_controller.add_observer(self)
        gnota_controller.add_criteria_observer(self)
        self.last_search = ('', '', '', '')
        self.init_combos()
        try:
            self.simple_mode
            self.cls
        except AttributeError:
            self.simple_mode = False
            self.cls = None

        if not self.simple_mode:
            self.show_widgets_for_complete_mode()
        if self.cls:
            self.show_class(self.cls)
        return

    def show_widgets_for_complete_mode(self):
        self.left_vbox.props.visible = True
        self.save_button.props.visible = True
        self.find_button.props.visible = True
        self.add_button.props.visible = True

    def notify_model_changed(self):
        self.repeat_last_search()

    def notify_criteria_model_changed(self):
        self.populate_criteria_combobox()

    def repeat_last_search(self):
        self.search(*self.last_search)

    def search(self, name, course_id, description, website):
        self.matches_treeview.props.model = model = gtk.ListStore(str, str, str)
        for column in self.matches_treeview.get_columns():
            self.matches_treeview.remove_column(column)

        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Name'), gtk.CellRendererText(), text=0))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Course ID'), gtk.CellRendererText(), text=1))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Website'), gtk.CellRendererText(), text=2))
        self.search_results = []
        for cls in gnota_controller.get_classes_like(name=name, course_id=course_id, description=description, website=website):
            model.append((cls.name, cls.course_id, cls.website))
            self.search_results.append(cls)

        self.last_search = (name, course_id, description, website)

    def get_selected_class(self):
        try:
            return self.search_results[self.matches_treeview.get_selection().get_selected_rows()[1][0][0]]
        except IndexError:
            raise NoSelectedClassException

    def get_class(self):
        if self.cls is not None:
            return self.cls
        return self.get_selected_class()

    def get_selected_scoresystem(self):
        return self.combo_scoresystems[self.scoresystems_combobox.props.active]

    def get_selected_criterion(self):
        return self.combo_criteria[self.criterion_combobox.props.active]

    def search_from_ui(self):
        self.search(name=self.name_entry.props.text, course_id=self.course_id_entry.props.text, description=self.description_text_view.props.buffer.props.text, website=self.website_entry.props.text)

    def show_class(self, cls):
        self.name_entry.props.text = cls.name
        self.course_id_entry.props.text = cls.course_id
        self.description_text_view.props.buffer.props.text = cls.description
        self.website_entry.props.text = cls.website
        if cls.criterion is not None:
            criterion = gnota_controller.get_subclassed_criterion(cls.criterion)
            self.select_criterion(criterion)
        if cls.scoresystem is not None:
            ss = gnota_controller.get_subclassed_scoresystem(cls.scoresystem)
            self.scoresystems_combobox.props.active = self.combo_scoresystems.index(ss)
        return

    def save_class_data(self, cls):
        gnota_controller.modify_class(cls, name=self.name_entry.props.text, course_id=self.course_id_entry.props.text, description=self.description_text_view.props.buffer.props.text, website=self.website_entry.props.text, criterion=self.combo_criteria[self.criterion_combobox.props.active], scoresystem=self.combo_scoresystems[self.scoresystems_combobox.props.active])
        if self.simple_mode:
            self.close_window()

    def show_details(self, cls):
        va = ViewActivities()
        va.set_class(cls)
        va.view_activities.show_all()

    def init_combos(self):
        self.init_criterion_combo()
        self.init_scoresystem_combo()

    def init_criterion_combo(self):
        cb = self.criterion_combobox
        cb.props.model = model = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)
        self.combo_criteria = []

    def init_scoresystem_combo(self):
        cb = self.scoresystems_combobox
        cb.props.model = model = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)
        self.combo_scoresystems = []

    def populate_criteria_combobox(self):
        model = self.criterion_combobox.props.model
        model.clear()
        self.combo_criteria = []
        for crit in gnota_controller.criteria:
            model.append([crit.name])
            self.combo_criteria.append(crit)

        model.append(['Separator goes here'])
        model.append(['New criterion...'])

    def populate_scoresystems_combobox(self):
        model = self.scoresystems_combobox.props.model
        model.clear()
        self.combo_scoresystems = []
        for ss in gnota_controller.scoresystems:
            model.append([ss.name])
            self.combo_scoresystems.append(ss)

        model.append(['Separator goes here'])
        model.append(['New scoresystem...'])

    def create_new_criterion(self):
        try:
            cls = self.get_selected_class()
        except NoSelectedClassException:
            cls = None

        ce = CriterionEditorDialog(cls=cls, scoresystem=self.get_selected_scoresystem())
        return ce.create_new_criterion()

    def create_new_scoresystem(self):
        sed = ScoresystemEditorDialog()
        return sed.create_scoresystem()

    def select_criterion(self, crit):
        self.criterion_combobox.props.active = self.combo_criteria.index(crit)

    def select_scoresystem(self, ss):
        self.scoresystems_combobox.props.active = self.combo_scoresystems.index(ss)

    def clear_fields(self):
        self.name_entry.props.text = ''
        self.course_id_entry.props.text = ''
        self.description_text_view.props.buffer.props.text = ''
        self.website_entry.props.text = ''
        self.criterion_combobox.props.active = -1
        self.scoresystems_combobox.props.active = -1

    def close_window(self):
        self.remove_from_observables()
        self.manage_classes.destroy()

    def remove_from_observables(self):
        gnota_controller.remove_observer(self)
        gnota_controller.remove_criteria_observer(self)

    def on_manage_classes_show(self, widget, *args):
        print 'on_manage_classes_show called with self.%s' % widget.get_name()
        self.search_from_ui()
        self.populate_criteria_combobox()
        self.populate_scoresystems_combobox()
        self.details_button.get_children()[0].get_children()[0].get_children()[1].props.label = _('_Details')

    def on_manage_classes_delete_event(self, widget, *args):
        print 'on_manage_classes_delete_event called with self.%s' % widget.get_name()
        self.remove_from_observables()

    def on_matches_treeview_row_activated(self, widget, *args):
        print 'on_matches_treeview_row_activated called with self.%s' % widget.get_name()
        self.show_details(self.get_selected_class())

    def on_matches_treeview_cursor_changed(self, widget, *args):
        print 'on_matches_treeview_cursor_changed called with self.%s' % widget.get_name()
        self.show_class(self.get_selected_class())

    def on_remove_button_clicked(self, widget, *args):
        print 'on_remove_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.remove_class(self.get_selected_class())
        self.clear_fields()

    def on_details_button_clicked(self, widget, *args):
        print 'on_details_button_clicked called with self.%s' % widget.get_name()
        self.show_details(self.get_selected_class())

    def on_edit_activities_button_clicked(self, widget, *args):
        print 'on_edit_activities_button_clicked called with self.%s' % widget.get_name()
        ma = ManageActivities(cls=self.get_selected_class())
        ma.manage_activities.show_all()

    def on_manage_enrollments_button_clicked(self, widget, *args):
        print 'on_manage_enrollments_button_clicked called with self.%s' % widget.get_name()
        me = ManageEnrollments(cls=self.get_selected_class())
        me.manage_enrollments.show_all()

    def on_scoresystems_combobox_changed(self, widget, *args):
        print 'on_scoresystems_combobox_changed called with self.%s' % widget.get_name()
        active = self.scoresystems_combobox.get_active()
        model = self.scoresystems_combobox.props.model
        if active == len(model) - 1:
            ss = self.create_new_scoresystem()
            if ss is not None:
                self.populate_scoresystems_combobox()
                self.select_scoresystem(ss)
        return

    def on_criterion_combobox_changed(self, widget, *args):
        print 'on_criterion_combobox_changed called with self.%s' % widget.get_name()
        active = self.criterion_combobox.get_active()
        model = self.criterion_combobox.props.model
        if active == len(model) - 1:
            criterion = self.create_new_criterion()
            if criterion is not None:
                self.populate_criteria_combobox()
                self.select_criterion(criterion)
        return

    def on_save_button_clicked(self, widget, *args):
        print 'on_save_button_clicked called with self.%s' % widget.get_name()
        self.save_class_data(self.get_class())

    def on_add_button_clicked(self, widget, *args):
        print 'on_add_button_clicked called with self.%s' % widget.get_name()
        name = self.name_entry.props.text
        course_id = self.course_id_entry.props.text
        description = self.description_text_view.props.buffer.props.text
        website = self.website_entry.props.text
        scoresystem = self.get_selected_scoresystem()
        criterion = self.get_selected_criterion()
        gnota_controller.add_class(name=name, course_id=course_id, description=description, website=website, scoresystem=scoresystem, criterion=criterion)
        self.clear_fields()

    def on_find_button_clicked(self, widget, *args):
        print 'on_find_button_clicked called with self.%s' % widget.get_name()
        self.search_from_ui()

    def on_close_button_clicked(self, widget, *args):
        print 'on_close_button_clicked called with self.%s' % widget.get_name()
        self.close_window()


class ManageActivities(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='manage_activities', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        try:
            self.simple_mode
            self.activity
            self.edit_mode
        except AttributeError:
            self.simple_mode = False
            self.activity = None
            self.edit_mode = None

        self.init_scoresystems_combobox()
        gnota_controller.add_observer(self)
        self.last_search = ('', )
        if not self.simple_mode:
            self.show_widgets_for_complete_mode()
            self.search_from_ui()
        if self.activity:
            self.show_selected_activity(self.activity)
        self.populate_comboboxes()
        return

    def show_widgets_for_complete_mode(self):
        self.left_vbox.props.visible = True
        self.save_button.props.visible = True
        self.add_button.props.visible = True
        self.search_button.props.visible = True

    def notify_model_changed(self):
        self.repeat_last_search()

    def repeat_last_search(self):
        self.search(*self.last_search)

    def search(self, name):
        self.matches_treeview.props.model = model = gtk.ListStore(str, str, str)
        for column in self.matches_treeview.get_columns():
            self.matches_treeview.remove_column(column)

        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Activity name'), gtk.CellRendererText(), text=0))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Type'), gtk.CellRendererText(), text=1))
        self.matches_treeview.append_column(gtk.TreeViewColumn(_('Date'), gtk.CellRendererText(), text=2))
        self.search_results = []
        for ac in gnota_controller.get_activities_like_in_class(self.cls, name=name):
            if ac.category is not None:
                cat = ac.category.name
            else:
                cat = ''
            model.append((ac.name, cat, ac.date))
            self.search_results.append(ac)

        self.last_search = (name,)
        return

    def search_from_ui(self):
        self.search(name=self.name_entry.props.text)

    def get_selected_activity(self):
        return self.search_results[self.matches_treeview.get_selection().get_selected_rows()[1][0][0]]

    def get_activity(self):
        if self.activity is not None:
            return self.activity
        return self.get_selected_activity()

    def populate_categories_combobox(self):
        cb = self.categories_combobox
        cb.props.model = model = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)
        self.combo_categories = []
        for cat in gnota_controller.activity_categories:
            model.append([cat.name])
            self.combo_categories.append(cat)

        model.append(('Separator goes here', ))
        model.append((_('New category...'),))

    def init_scoresystems_combobox(self):
        cb = self.scoresystems_combobox
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)

    def populate_scoresystems_combobox(self):
        cb = self.scoresystems_combobox
        cb.props.model = model = gtk.ListStore(str)
        model.clear()
        self.combo_scoresystems = []
        for ss in gnota_controller.scoresystems:
            model.append([ss.name])
            self.combo_scoresystems.append(get_subclassed_scoresystem(ss))

        model.append(('Separator goes here', ))
        model.append((_('N points...'),))
        model.append((_('New scoresystem...'),))

    def populate_comboboxes(self):
        self.populate_categories_combobox()
        self.populate_scoresystems_combobox()

    def save_activity_data(self, ac):
        gnota_controller.modify_activity(ac, name=self.name_entry.props.text, category=self.combo_categories[self.categories_combobox.props.active], description=self.description_text_view.props.buffer.props.text, date=datetime.date(self.calendar.props.year, self.calendar.props.month, self.calendar.props.day), scoresystem=self.get_selected_scoresystem())

    def clear_fields(self):
        self.name_entry.props.text = ''
        self.description_text_view.props.buffer.props.text = ''
        self.categories_combobox.props.active = -1
        self.scoresystems_combobox.props.active = -1

    def remove_from_observables(self):
        gnota_controller.remove_observer(self)

    def close(self):
        self.manage_activities.destroy()

    def create_new_N_points_scoresystem(self):
        npd = NPointsDialog()
        npss = npd.create_new_N_points_scoresystem()
        return npss

    def create_scoresystem(self):
        sed = ScoresystemEditorDialog()
        return sed.create_scoresystem()

    def create_category(self):
        ced = NewCategory()
        return ced.create_category()

    def select_scoresystem(self, ss):
        self.scoresystems_combobox.props.active = self.combo_scoresystems.index(ss)

    def select_category(self, cat):
        self.categories_combobox.props.active = self.combo_categories.index(cat)

    def show_selected_activity(self, ac):
        self.name_entry.props.text = ac.name
        self.calendar.props.day = ac.date.day
        self.calendar.props.month = ac.date.month
        self.calendar.props.year = ac.date.year
        self.description_text_view.props.buffer.props.text = ac.description
        if ac.category is not None:
            self.categories_combobox.props.active = self.combo_categories.index(ac.category)
        if ac.scoresystem is not None:
            self.select_scoresystem(gnota_controller.get_subclassed_scoresystem(ac.scoresystem))
        return

    def get_selected_scoresystem(self):
        return self.combo_scoresystems[self.scoresystems_combobox.props.active]

    def on_manage_activities_destroy(self, widget, *args):
        print 'on_manage_activities_destroy called with self.%s' % widget.get_name()
        self.remove_from_observables()

    def on_manage_activities_show(self, widget, *args):
        print 'on_manage_activities_show called with self.%s' % widget.get_name()

    def on_matches_treeview_cursor_changed(self, widget, *args):
        print 'on_matches_treeview_cursor_changed called with self.%s' % widget.get_name()
        ac = self.get_selected_activity()
        self.show_selected_activity(ac)

    def on_remove_button_clicked(self, widget, *args):
        print 'on_remove_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.remove_activity(self.get_selected_activity())
        self.clear_fields()

    def on_scoresystems_combobox_changed(self, widget, *args):
        print 'on_scoresystems_combobox_changed called with self.%s' % widget.get_name()
        active = self.scoresystems_combobox.get_active()
        model = self.scoresystems_combobox.props.model
        if active == len(model) - 2:
            ss = self.create_new_N_points_scoresystem()
            if ss is not None:
                self.populate_scoresystems_combobox()
                self.select_scoresystem(ss)
        elif active == len(model) - 1:
            ss = self.create_scoresystem()
            if ss is not None:
                self.populate_scoresystems_combobox()
                self.select_scoresystem(ss)
        return

    def on_categories_combobox_changed(self, widget, *args):
        print 'on_categories_combobox_changed called with self.%s' % widget.get_name()
        active = self.scoresystems_combobox.get_active()
        model = self.scoresystems_combobox.props.model
        if active == len(model) - 1:
            cat = self.create_category()
            if ss is not None:
                self.populate_categories_combobox()
                self.select_category(cat)
        return

    def on_save_button_clicked(self, widget, *args):
        print 'on_save_button_clicked called with self.%s' % widget.get_name()
        self.save_activity_data(self.get_activity())
        if self.simple_mode:
            self.close()

    def on_add_button_clicked(self, widget, *args):
        print 'on_add_button_clicked called with self.%s' % widget.get_name()
        name = self.name_entry.props.text
        date = datetime.date(self.calendar.props.year, self.calendar.props.month, self.calendar.props.day)
        description = self.description_text_view.props.buffer.props.text
        category = self.combo_categories[self.categories_combobox.props.active]
        ss = self.get_selected_scoresystem()
        ac = gnota_controller.add_activity(name=name, date=date, description=description, category=category, scoresystem=ss, activity_class=self.cls)
        if self.simple_mode:
            self.close()
        else:
            self.clear_fields()

    def on_search_button_clicked(self, widget, *args):
        print 'on_search_button_clicked called with self.%s' % widget.get_name()
        self.search_from_ui()

    def on_close_button_clicked(self, widget, *args):
        print 'on_close_button_clicked called with self.%s' % widget.get_name()
        self.close()


class ManageStudentClasses(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='manage_student_classes', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        self.set_student(kwargs['student'])

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        gnota_controller.add_observer(self)
        self.init_treeviews()
        self.search_from_ui()
        self.populate_student_classes()

    def set_student(self, student):
        self.student = student
        self.update_student_label(student.name)

    def update_student_label(self, name):
        self.student_label.props.label = self.student_label.props.label % name

    def reload(self):
        self.repeat_last_search()
        self.populate_student_classes()

    def notify_model_changed(self):
        self.reload()

    def init_treeviews(self):
        self.matches_treeview.props.model = gtk.ListStore(object)
        for column in self.matches_treeview.get_columns():
            self.matches_treeview.remove_column(column)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.set_cell_data_func(cell, self.name_cell_data_func)
        self.matches_treeview.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Course ID'), cell)
        column.set_cell_data_func(cell, self.course_id_cell_data_func)
        self.matches_treeview.append_column(column)
        self.classes_treeview.props.model = gtk.ListStore(object)
        for column in self.classes_treeview.get_columns():
            self.classes_treeview.remove_column(column)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.set_cell_data_func(cell, self.name_cell_data_func)
        self.classes_treeview.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Course ID'), cell)
        column.set_cell_data_func(cell, self.course_id_cell_data_func)
        self.classes_treeview.append_column(column)

    def repeat_last_search(self):
        self.search(*self.last_search)

    def search_from_ui(self):
        name = self.name_entry.props.text
        course_id = self.course_id_entry.props.text
        description = self.description_textview.props.buffer.props.text
        website = self.website_entry.props.text
        self.search(name, course_id, description, website)

    def name_cell_data_func(self, column, cell, model, iter):
        cls = model.get_value(iter, 0)
        cell.props.text = cls.name

    def course_id_cell_data_func(self, column, cell, model, iter):
        cls = model.get_value(iter, 0)
        cell.props.text = cls.course_id

    def populate_student_classes(self):
        model = self.classes_treeview.props.model
        model.clear()
        for cls in self.student.classes:
            model.append((cls,))

    def search(self, name, course_id, description, website):
        model = self.matches_treeview.props.model
        model.clear()
        for cls in gnota_controller.get_classes_like(name=name, course_id=course_id, description=description, website=website):
            model.append((cls,))

        self.last_search = (name, course_id, description, website)

    def get_selected_match(self):
        (model, iter) = self.matches_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def get_selected_class(self):
        (model, iter) = self.classes_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def on_manage_student_classes_destroy(self, widget, *args):
        print 'on_manage_student_classes_destroy called with self.%s' % widget.get_name()
        gnota_controller.remove_observer(self)

    def on_remove_button_clicked(self, widget, *args):
        print 'on_remove_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.remove_class_from_student(self.get_selected_class(), self.student)

    def on_add_button_clicked(self, widget, *args):
        print 'on_add_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.add_class_to_student(self.get_selected_match(), self.student)

    def on_search_button_clicked(self, widget, *args):
        print 'on_search_button_clicked called with self.%s' % widget.get_name()
        self.search_from_ui()


class ManageEnrollments(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='manage_enrollments', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        self.cls = kwargs['cls']

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        gnota_controller.add_observer(self)
        self.init_treeviews()
        self.search_from_ui()
        self.populate_enrollments()

    def reload(self):
        self.repeat_last_search()
        self.populate_enrollments()

    def notify_model_changed(self):
        self.reload()

    def init_treeviews(self):
        self.matches_treeview.props.model = gtk.ListStore(object)
        for column in self.matches_treeview.get_columns():
            self.matches_treeview.remove_column(column)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.set_cell_data_func(cell, self.name_cell_data_func)
        self.matches_treeview.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Student ID'), cell)
        column.set_cell_data_func(cell, self.course_id_cell_data_func)
        self.matches_treeview.append_column(column)
        self.enrollments_treeview.props.model = gtk.ListStore(object)
        for column in self.enrollments_treeview.get_columns():
            self.enrollments_treeview.remove_column(column)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Name'), cell)
        column.set_cell_data_func(cell, self.name_cell_data_func)
        self.enrollments_treeview.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Student ID'), cell)
        column.set_cell_data_func(cell, self.course_id_cell_data_func)
        self.enrollments_treeview.append_column(column)

    def repeat_last_search(self):
        self.search(*self.last_search)

    def search_from_ui(self):
        last_name = self.last_name_entry.props.text
        first_name = self.first_name_entry.props.text
        student_id = self.student_id_entry.props.text
        year = self.year_entry.props.text
        self.search(last_name=last_name, first_name=first_name, code=student_id, year=year)

    def name_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        cell.props.text = student.name

    def course_id_cell_data_func(self, column, cell, model, iter):
        student = model.get_value(iter, 0)
        cell.props.text = student.code

    def populate_enrollments(self):
        model = self.enrollments_treeview.props.model
        model.clear()
        for student in self.cls.students:
            model.append((student,))

    def search(self, last_name, first_name, code, year):
        model = self.matches_treeview.props.model
        model.clear()
        for student in gnota_controller.get_students_like(last_name=last_name, first_name=first_name, code=code, year=year):
            model.append((student,))

        self.last_search = (last_name, first_name, code, year)

    def get_selected_match(self):
        (model, iter) = self.matches_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def get_selected_student(self):
        (model, iter) = self.enrollments_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def on_manage_enrollments_destroy(self, widget, *args):
        print 'on_manage_enrollments_destroy called with self.%s' % widget.get_name()
        gnota_controller.remove_observer(self)

    def on_remove_button_clicked(self, widget, *args):
        print 'on_remove_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.remove_class_from_student(self.cls, self.get_selected_student())

    def on_add_button_clicked(self, widget, *args):
        print 'on_add_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.add_class_to_student(self.cls, self.get_selected_match())

    def on_search_button_clicked(self, widget, *args):
        print 'on_search_button_clicked called with self.%s' % widget.get_name()
        self.search_from_ui()


class CriterionEditorDialog(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='criterion_editor_dialog', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)
        self.cls = kwargs.get('cls')
        self.scoresystem = kwargs.get('scoresystem')
        self.criterion = kwargs.get('criterion')

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        try:
            self.criterion
        except AttributeError:
            self.criterion = None

        self.init_scoresystems()
        self.init_classes()
        self.init_treeview()
        if self.criterion is None:
            self.populate_scoresytems_combobox()
            self.populate_classes_combobox()
            if self.scoresystem is not None:
                self.select_scoresystem(self.scoresystem)
            if self.cls is not None:
                self.select_class(self.cls)
        else:
            self.load_criterion()
        return

    def select_scoresystem(self, ss):
        model = self.scoresystems_combobox.props.model
        ss = gnota_controller.get_subclassed_scoresystem(ss)
        for treemodelrow in model:
            if treemodelrow[0] == ss:
                self.scoresystems_combobox.set_active_iter(treemodelrow.iter)
                break
        else:
            raise NoSuchScoreSystemException('Could not find scoresystem in the combobox model.')

    def select_class(self, cls):
        model = self.classes_combobox.props.model
        for treemodelrow in model:
            if treemodelrow[0] == cls:
                self.classes_combobox.set_active_iter(treemodelrow.iter)
                break
        else:
            raise NoSuchClassException('Could not find class in the combobox model.')

    def load_criterion(self):
        criterion = self.criterion
        ss = gnota_controller.get_subclassed_scoresystem(criterion.passing_score[0].scoresystem)
        classes = criterion.classes
        self.populate_scoresytems_combobox()
        self.populate_classes_combobox()
        self.select_scoresystem(ss)
        if len(classes) == 1:
            self.select_class(classes[0])
            if isinstance(criterion, (WeightedAverage,)):
                self.populate_treeview()
        self.name_entry.props.text = criterion.name
        self.min_passing_score_entry.props.text = criterion.passing_score[0].symbol
        if isinstance(criterion, (SimpleAverage, SimpleAverageOfBestN)):
            self.simple_average_radiobutton.props.active = True
        elif isinstance(criterion, (WeightedAverage,)):
            self.weighted_average_radiobutton.props.active = True

    def populate_scoresytems_combobox(self):
        cb = self.scoresystems_combobox
        cb.props.model = model = gtk.ListStore(object)
        for ss in gnota_controller.scoresystems:
            model.append((ss,))

    def populate_classes_combobox(self):
        cb = self.classes_combobox
        cb.props.model = model = gtk.ListStore(object)
        for c in gnota_controller.classes:
            model.append((c,))

    def weights_treeview_name_cell_data_func(self, celllayout, cell, model, iter, user_data=None):
        thing = model.get_value(iter, 0)
        if thing is not None:
            if isinstance(thing, CategoryWeight):
                cell.props.text = thing.category.name
            elif isinstance(thing, Activity):
                cell.props.text = thing.name
            else:
                raise GNotaTypeException('Unexpected object of type = %s' % thing.__class__.__name__)
        return

    def name_cell_data_func(self, celllayout, cell, model, iter, user_data=None):
        thing = model.get_value(iter, 0)
        if thing is not None:
            cell.props.text = thing.name
        return

    def init_scoresystems(self):
        cb = self.scoresystems_combobox
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.set_cell_data_func(cell, self.name_cell_data_func)

    def init_classes(self):
        cb = self.classes_combobox
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.set_cell_data_func(cell, self.name_cell_data_func)

    def get_selected_class(self):
        return self.classes_combobox.props.model.get_value(self.classes_combobox.get_active_iter(), 0)

    def get_selected_scoresystem(self):
        return self.scoresystems_combobox.props.model.get_value(self.scoresystems_combobox.get_active_iter(), 0)

    def get_selected_class_categories_dict(self):
        d = {}
        for activity in self.get_selected_class().activities:
            try:
                d[activity.category].append(activity)
            except KeyError:
                d[activity.category] = [
                 activity]

        return d

    def create_new_criterion(self):
        self.criterion_editor_dialog.run()
        self.criterion_editor_dialog.destroy()
        return self.criterion

    def weight_cell_data_func(self, column, cell, model, iter):
        thing = model.get_value(iter, 0)
        if isinstance(thing, CategoryWeight):
            weight = gnota_controller.get_category_weight(thing)
        else:
            weight = gnota_controller.get_activity_weight(thing)
        cell.props.text = str(weight)

    def weight_text_changed(self, cellrenderertext, path, new_text, user_data=None):
        if new_text:
            model = self.weights_treeview.props.model
            iter = model.get_iter(path)
            thing = model.get_value(iter, 0)
            weight = float(new_text)
            if isinstance(thing, CategoryWeight):
                gnota_controller.set_category_weight(thing, weight)
            else:
                gnota_controller.set_activity_weight(thing, weight)

    def init_treeview(self):
        tv = self.weights_treeview
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Category/Activity'), cell)
        column.set_cell_data_func(cell, self.weights_treeview_name_cell_data_func)
        tv.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Weight'), cell)
        cell.props.editable = True
        cell.connect('edited', self.weight_text_changed)
        column.set_cell_data_func(cell, self.weight_cell_data_func)
        tv.append_column(column)
        self.weights_treeview.props.model = gtk.TreeStore(object)

    def populate_treeview(self):
        model = self.weights_treeview.props.model
        model.clear()
        d = self.get_selected_class_categories_dict()
        for (cat, list_activities) in d.items():
            if self.criterion is None:
                cw = gnota_controller.add_category_weight(cat, 1.0)
            else:
                try:
                    cw = gnota_controller.get_category_weight_object_in_criterion(self.criterion, cat)
                except CategoryWithNoWeightException:
                    cw = gnota_controller.add_category_weight(cat, 0.0)

            ti = model.insert(None, 0, (cw,))
            for activity in list_activities:
                if self.criterion is None:
                    gnota_controller.set_activity_weight(activity, 1.0)
                elif gnota_controller.get_activity_weight(activity) is None:
                    gnota_controller.set_activity_weight(activity, 0.0)
                model.insert(ti, 0, (activity,))

        return

    def get_category_weights_in_treeview(self):
        result = []
        for treemodelrow in self.weights_treeview.props.model:
            if isinstance(treemodelrow[0], CategoryWeight):
                result.append(treemodelrow[0])

        return result

    def on_weighted_average_radiobutton_toggled(self, widget, *args):
        print 'on_weighted_average_radiobutton_toggled called with self.%s' % widget.get_name()
        self.weights_treeview.props.sensitive = self.weighted_average_radiobutton.props.active
        if self.weighted_average_radiobutton.props.active is True:
            self.populate_treeview()

    def on_classes_combobox_changed(self, widget, *args):
        print 'on_classes_combobox_changed called with self.%s' % widget.get_name()
        self.populate_treeview()

    def on_cancel_button_clicked(self, widget, *args):
        print 'on_cancel_button_clicked called with self.%s' % widget.get_name()
        self.criterion_editor_dialog.response(0)

    def on_ok_button_clicked(self, widget, *args):
        print 'on_ok_button_clicked called with self.%s' % widget.get_name()
        name = self.name_entry.props.text
        min_passing_score = self.min_passing_score_entry.props.text
        best_N = self.usebestn_checkbutton.props.active
        scoresystem = self.get_selected_scoresystem()
        maximum_missed_classes = int(self.max_missed_classes_entry.props.text)
        if not self.weighted_average_radiobutton.props.active:
            if best_N:
                N = int(self.N_entry.props.text)
                self.criterion = gnota_controller.create_simple_average_of_best_N_criterion(name, min_passing_score, scoresystem, N)
            else:
                self.criterion = gnota_controller.create_simple_average_criterion(name, min_passing_score, scoresystem)
        else:
            if best_N:
                N = int(self.N_entry.props.text)
                raise NotImplementedError
            else:
                self.criterion = gnota_controller.create_weighted_average_criterion()
            for cw in self.get_category_weights_in_treeview():
                gnota_controller.add_category_weight_to_criterion(self.criterion, cw)

            gnota_controller.set_criterion_name(self.criterion, name)
            gnota_controller.set_min_passing_score_as_text(self.criterion, min_passing_score, scoresystem)
            gnota_controller.set_weighted_average_class(self.criterion, self.get_selected_class())
        gnota_controller.set_maximum_missed_classes(self.criterion, maximum_missed_classes)
        self.criterion_editor_dialog.response(0)


class Preferences(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='preferences', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        self.init_scoresystems_tab()
        self.init_categories_tab()
        self.init_criteria_tab()
        self.populate_scoresystems()
        self.populate_categories()
        self.populate_criteria()
        gnota_controller.add_categories_observer(self)
        gnota_controller.add_scoresystems_observer(self)
        gnota_controller.add_criteria_observer(self)

    def scoresystem_name_cell_data_func(self, column, cell, model, iter, user_data=None):
        cell.props.text = model.get_value(iter, 0).name

    def category_name_cell_data_func(self, column, cell, model, iter, user_data=None):
        cell.props.text = model.get_value(iter, 0).name

    def criterion_name_cell_data_func(self, column, cell, model, iter, user_data=None):
        cell.props.text = model.get_value(iter, 0).name

    def notify_scoresystems_model_changed(self):
        self.populate_scoresystems()

    def notify_categories_model_changed(self):
        self.populate_categories()

    def notify_criteria_model_changed(self):
        self.populate_criteria()

    def init_scoresystems_tab(self):
        tv = self.scoresystems_treeview
        tv.props.model = model = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Scoresystem name'), cell)
        column.set_cell_data_func(cell, self.scoresystem_name_cell_data_func)
        tv.append_column(column)

    def init_categories_tab(self):
        tv = self.categories_treeview
        tv.props.model = model = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Activity Category'), cell)
        column.set_cell_data_func(cell, self.category_name_cell_data_func)
        tv.append_column(column)

    def init_criteria_tab(self):
        tv = self.criteria_treeview
        tv.props.model = model = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Criterion'), cell)
        column.set_cell_data_func(cell, self.criterion_name_cell_data_func)
        tv.append_column(column)

    def populate_scoresystems(self):
        model = self.scoresystems_treeview.props.model
        model.clear()
        for ss in gnota_controller.scoresystems:
            model.append((ss,))

    def populate_categories(self):
        model = self.categories_treeview.props.model
        model.clear()
        for cat in gnota_controller.activity_categories:
            model.append((cat,))

    def populate_criteria(self):
        model = self.criteria_treeview.props.model
        model.clear()
        for crit in gnota_controller.criteria:
            model.append((crit,))

    def get_selected_scoresystem(self):
        (model, iter) = self.scoresystems_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def get_selected_category(self):
        (model, iter) = self.categories_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def get_selected_criterion(self):
        (model, iter) = self.criteria_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def delete_selected_category(self):
        gnota_controller.remove_category(self.get_selected_category())

    def delete_selected_scoresystem(self):
        gnota_controller.remove_scoresystem(self.get_selected_scoresystem())

    def delete_selected_criterion(self):
        gnota_controller.remove_criterion(self.get_selected_criterion())

    def on_preferences_destroy(self, widget, *args):
        print 'on_preferences_destroy called with self.%s' % widget.get_name()
        gnota_controller.remove_scoresystems_observer(self)
        gnota_controller.remove_categories_observer(self)
        gnota_controller.remove_criteria_observer(self)

    def on_new_scoresystem_button_clicked(self, widget, *args):
        print 'on_new_scoresystem_button_clicked called with self.%s' % widget.get_name()
        sed = ScoresystemEditorDialog()
        ss = sed.create_scoresystem()

    def on_delete_scoresystem_button_clicked(self, widget, *args):
        print 'on_delete_scoresystem_button_clicked called with self.%s' % widget.get_name()
        self.delete_selected_scoresystem()

    def on_edit_scoresystem_button_clicked(self, widget, *args):
        print 'on_edit_scoresystem_button_clicked called with self.%s' % widget.get_name()
        ssed = ScoresystemEditorDialog(scoresystem=self.get_selected_scoresystem())
        ssed.create_scoresystem()

    def on_new_category_button_clicked(self, widget, *args):
        print 'on_new_category_button_clicked called with self.%s' % widget.get_name()
        nc = NewCategory()
        nc.new_category.run()
        nc.new_category.destroy()

    def on_delete_category_button_clicked(self, widget, *args):
        print 'on_delete_category_button_clicked called with self.%s' % widget.get_name()
        self.delete_selected_category()

    def on_edit_category_button_clicked(self, widget, *args):
        print 'on_edit_category_button_clicked called with self.%s' % widget.get_name()
        nc = NewCategory(cat=self.get_selected_category())
        nc.new_category.run()

    def on_new_criterion_button_clicked(self, widget, *args):
        print 'on_new_criterion_button_clicked called with self.%s' % widget.get_name()
        ced = CriterionEditorDialog(cls=None, scoresystem=None)
        ced.create_new_criterion()
        return

    def on_delete_criteria_button_clicked(self, widget, *args):
        print 'on_delete_criteria_button_clicked called with self.%s' % widget.get_name()
        self.delete_selected_criterion()

    def on_edit_criterion_button_clicked(self, widget, *args):
        print 'on_edit_criterion_button_clicked called with self.%s' % widget.get_name()
        ce = CriterionEditorDialog(criterion=self.get_selected_criterion())
        ce.create_new_criterion()

    def on_close_button_clicked(self, widget, *args):
        print 'on_close_button_clicked called with self.%s' % widget.get_name()
        self.preferences.destroy()


class ScoresystemEditorDialog(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='scoresystem_editor_dialog', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__
        try:
            self.scoresystem
        except AttributeError:
            self.scoresystem = None

        self.init_treeview()
        if self.scoresystem is None:
            self.select_discrete_values_radiobutton()
        else:
            self.load_scoresystem()
        return

    def load_scoresystem(self):
        ss = gnota_controller.get_subclassed_scoresystem(self.scoresystem)
        self.name_entry.props.text = ss.name
        self.description_textview.props.buffer.props.text = ss.description
        if isinstance(ss, DiscreteValuesScoreSystem):
            self.select_discrete_values_radiobutton()
            self.populate_treeview()
        else:
            self.select_ranged_values_radiobutton()
            self.min_symbol_entry.props.text = ss.min.symbol
            self.min_value_entry.props.text = str(ss.min.value)
            self.max_symbol_entry.props.text = ss.max.symbol
            self.max_value_entry.props.text = str(ss.max.value)

    def populate_treeview(self):
        for ssv in self.scoresystem.scores:
            self.add_ssv_to_model(ssv)

    def symbol_cell_data_func(self, column, cell, model, iter):
        ssv = model.get_value(iter, 0)
        if ssv is not None:
            cell.props.text = model.get_value(iter, 0).symbol
        return

    def value_cell_data_func(self, column, cell, model, iter):
        ssv = model.get_value(iter, 0)
        if ssv is not None:
            cell.props.text = ssv.value
        return

    def init_treeview(self):
        tv = self.ssvs_treeview
        tv.props.model = model = gtk.ListStore(object)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Symbol'), cell)
        column.set_cell_data_func(cell, self.symbol_cell_data_func)
        tv.append_column(column)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_('Value'), cell)
        column.set_cell_data_func(cell, self.value_cell_data_func)
        tv.append_column(column)

    def add_ssv_to_model(self, ssv):
        model = self.ssvs_treeview.props.model
        model.append((ssv,))

    def get_selected_ssv(self):
        (model, iter) = self.ssvs_treeview.get_selection().get_selected()
        return model.get_value(iter, 0)

    def remove_selected_ssv_from_model(self):
        (model, iter) = self.ssvs_treeview.get_selection().get_selected()
        model.remove(iter)

    def create_scoresystem(self):
        self.scoresystem_editor_dialog.run()
        self.scoresystem_editor_dialog.destroy()
        return self.scoresystem

    def select_discrete_values_radiobutton(self):
        self.discrete_values_radiobutton.props.active = True
        self.on_discrete_values_radiobutton_toggled(self.discrete_values_radiobutton, None)
        return

    def select_ranged_values_radiobutton(self):
        self.ranged_values_radiobutton.props.active = True
        self.on_discrete_values_radiobutton_toggled(self.discrete_values_radiobutton, None)
        return

    def on_discrete_values_radiobutton_toggled(self, widget, *args):
        print 'on_discrete_values_radiobutton_toggled called with self.%s' % widget.get_name()
        if self.discrete_values_radiobutton.props.active:
            self.ranged_table.set_sensitive(False)
            self.discrete_hbox.set_sensitive(True)
        else:
            self.ranged_table.set_sensitive(True)
            self.discrete_hbox.set_sensitive(False)

    def on_remove_button_clicked(self, widget, *args):
        print 'on_remove_button_clicked called with self.%s' % widget.get_name()
        self.remove_selected_ssv_from_model()
        gnota_controller.remove_scoresymbolvalue(self.get_selected_ssv())

    def on_add_ssv_button_clicked(self, widget, *args):
        print 'on_add_ssv_button_clicked called with self.%s' % widget.get_name()
        symbol = self.symbol_entry.props.text
        value = self.value_entry.props.text
        ssv = gnota_controller.create_scoresymbolvalue(symbol, value)
        self.add_ssv_to_model(ssv)

    def on_cancel_button_clicked(self, widget, *args):
        print 'on_cancel_button_clicked called with self.%s' % widget.get_name()

    def on_ok_button_clicked(self, widget, *args):
        print 'on_ok_button_clicked called with self.%s' % widget.get_name()
        name = self.name_entry.props.text
        desc = self.description_textview.props.buffer.props.text
        if self.discrete_values_radiobutton.props.active:
            scores = [ ssv[0] for ssv in self.ssvs_treeview.props.model ]
            scores.sort(key=lambda x: x.value, reverse=True)
            if self.scoresystem is None:
                ss = gnota_controller.create_discrete_scoresystem(name, desc, scores)
            else:
                raise NotImplementedError
        else:
            min_symbol = self.min_symbol_entry.props.text
            max_symbol = self.max_symbol_entry.props.text
            min_value = self.min_value_entry.props.text
            max_value = self.max_value_entry.props.text
            min_ssv = gnota_controller.create_scoresymbolvalue(min_symbol, min_value)
            max_ssv = gnota_controller.create_scoresymbolvalue(max_symbol, max_value)
            if self.scoresystem is None:
                ss = gnota_controller.create_ranged_scoresystem(name, desc, min_ssv, max_ssv)
            else:
                raise NotImplementedError
        self.scoresystem = ss
        return


class NPointsDialog(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='n_points_dialog', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__

    def create_new_N_points_scoresystem(self):
        self.n = None
        self.n_points_scoresystem = None
        self.n_points_dialog.run()
        self.n_points_dialog.destroy()
        if self.n is not None:
            min_ssv = gnota_controller.create_scoresymbolvalue('0', 0.0)
            max_ssv = gnota_controller.create_scoresymbolvalue(str(self.n), float(self.n))
            self.n_points_scoresystem = gnota_controller.create_ranged_scoresystem('%d points scoresystem' % self.n, 'A ranged scoresystem from 0 to %d' % self.n, min_ssv, max_ssv)
        return self.n_points_scoresystem

    def on_cancel_button_clicked(self, widget, *args):
        print 'on_cancel_button_clicked called with self.%s' % widget.get_name()
        self.n = None
        return

    def on_ok_button_clicked(self, widget, *args):
        print 'on_ok_button_clicked called with self.%s' % widget.get_name()
        self.n = int(self.n_entry.props.text)


class BackupDialog(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='backup_dialog', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__

    def set_dont_ask(self):
        gc = gnota_controller.get_gnota_config()
        if self.dontask_checkbutton.props.active:
            gnota_controller.set_dont_ask(True)

    def on_no_button_clicked(self, widget, *args):
        print 'on_no_button_clicked called with self.%s' % widget.get_name()
        self.set_dont_ask()
        self.backup_dialog.response(0)

    def on_yes_button_clicked(self, widget, *args):
        print 'on_yes_button_clicked called with self.%s' % widget.get_name()
        self.set_dont_ask()
        bfcd = BackupFilechooserdialog()
        bfcd.backup_filechooserdialog.run()
        bfcd.backup_filechooserdialog.destroy()
        self.backup_dialog.response(0)


class BackupFilechooserdialog(SimpleGladeApp):

    def __init__(self, path='ui.glade3', root='backup_filechooserdialog', domain=app_name, **kwargs):
        path = os.path.join(glade_dir, path)
        SimpleGladeApp.__init__(self, path, root, domain, **kwargs)

    def new(self):
        print 'A new %s has been created' % self.__class__.__name__

    def on_cancel_button_clicked(self, widget, *args):
        print 'on_cancel_button_clicked called with self.%s' % widget.get_name()
        self.backup_filechooserdialog.response(0)

    def on_ok_button_clicked(self, widget, *args):
        print 'on_ok_button_clicked called with self.%s' % widget.get_name()
        gnota_controller.reset_runs_in_current_config()
        dir = os.path.join(self.backup_filechooserdialog.get_filename(), 'gnota-backup.sqlite')
        dbpath = gnota_controller.get_current_dbpath()
        shutil.copy(dbpath, dir)
        self.backup_filechooserdialog.response(0)


def main():
    main_window = MainWindow()
    main_window.run()


if __name__ == '__main__':
    main()