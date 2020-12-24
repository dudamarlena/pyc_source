# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/view.py
# Compiled at: 2016-10-03 09:39:22
import itertools, os, sys, traceback, cgi, logging
logger = logging.getLogger(__name__)
import gtk, gobject, pango, threading
from bauble.i18n import _
from pyparsing import ParseException
from sqlalchemy.orm import object_session
import sqlalchemy.exc as saexc, bauble
from bauble import db
from bauble.error import check, BaubleError
from bauble import paths
from bauble import pluginmgr
from bauble import prefs
from bauble import search
from bauble import utils
from bauble import editor
from bauble import pictures_view
_mainstr_tmpl = '<b>%s</b>'
if sys.platform == 'win32':
    _substr_tmpl = '%s'
else:
    _substr_tmpl = '<small>%s</small>'

class Action(gtk.Action):
    """
    An Action allows a label, tooltip, callback and accelerator to be called
    when specific items are selected in the SearchView
    """

    def __init__(self, name, label, tooltip=None, stock_id=None, callback=None, accelerator=None, multiselect=False, singleselect=True):
        """
        callback: the function to call when the the action is activated
        accelerator: accelerator to call this action
        multiselect: show menu when multiple items are selected
        singleselect: show menu when single items are selected

        The activate signal is not automatically connected to the
        callback method.
        """
        super(Action, self).__init__(name, label, tooltip, stock_id)
        self.callback = callback
        self.multiselect = multiselect
        self.singleselect = singleselect
        self.accelerator = accelerator

    def _set_enabled(self, enable):
        self.set_visible(enable)

    def _get_enabled(self):
        return self.get_visible()

    enabled = property(_get_enabled, _set_enabled)


class InfoExpander(gtk.Expander):
    """
    an abstract class that is really just a generic expander with a vbox
    to extend this you just have to implement the update() method
    """
    expanded_pref = None

    def __init__(self, label, widgets=None):
        """
        :param label: the name of this info expander, this is displayed on the
        expander's expander

        :param widgets: a bauble.utils.BuilderWidgets instance
        """
        super(InfoExpander, self).__init__(label)
        self.vbox = gtk.VBox(False)
        self.vbox.set_border_width(5)
        self.add(self.vbox)
        self.widgets = widgets
        if not self.expanded_pref:
            self.set_expanded(True)
        self.connect('notify::expanded', self.on_expanded)

    def on_expanded(self, expander, *args):
        if self.expanded_pref:
            prefs.prefs[self.expanded_pref] = expander.get_expanded()
            prefs.prefs.save()

    def widget_set_value(self, widget_name, value, markup=False, default=None):
        """
        a shorthand for L{bauble.utils.set_widget_value()}
        """
        utils.set_widget_value(self.widgets[widget_name], value, markup, default)

    def update(self, value):
        """
        This method should be implemented by classes that extend InfoExpander
        """
        raise NotImplementedError('InfoExpander.update(): not implemented')


class PropertiesExpander(InfoExpander):

    def __init__(self):
        super(PropertiesExpander, self).__init__(_('Properties'))
        table = gtk.Table(rows=4, columns=2)
        table.set_col_spacings(15)
        table.set_row_spacings(8)
        id_label = gtk.Label('<b>' + _('ID:') + '</b>')
        id_label.set_use_markup(True)
        id_label.set_alignment(1, 0.5)
        self.id_data = gtk.Label('--')
        self.id_data.set_alignment(0, 0.5)
        table.attach(id_label, 0, 1, 0, 1)
        table.attach(self.id_data, 1, 2, 0, 1)
        type_label = gtk.Label('<b>' + _('Type:') + '</b>')
        type_label.set_use_markup(True)
        type_label.set_alignment(1, 0.5)
        self.type_data = gtk.Label('--')
        self.type_data.set_alignment(0, 0.5)
        table.attach(type_label, 0, 1, 1, 2)
        table.attach(self.type_data, 1, 2, 1, 2)
        created_label = gtk.Label('<b>' + _('Date created:') + '</b>')
        created_label.set_use_markup(True)
        created_label.set_alignment(1, 0.5)
        self.created_data = gtk.Label('--')
        self.created_data.set_alignment(0, 0.5)
        table.attach(created_label, 0, 1, 2, 3)
        table.attach(self.created_data, 1, 2, 2, 3)
        updated_label = gtk.Label('<b>' + _('Last updated:') + '</b>')
        updated_label.set_use_markup(True)
        updated_label.set_alignment(1, 0.5)
        self.updated_data = gtk.Label('--')
        self.updated_data.set_alignment(0, 0.5)
        table.attach(updated_label, 0, 1, 3, 4)
        table.attach(self.updated_data, 1, 2, 3, 4)
        box = gtk.HBox()
        box.pack_start(table, expand=False, fill=False)
        self.vbox.pack_start(box, expand=False, fill=False)

    def update(self, row):
        """"
        Update the widget in the expander.
        """
        self.id_data.set_text(str(row.id))
        self.type_data.set_text(str(type(row).__name__))
        self.created_data.set_text(row._created and row._created.strftime('%Y-%m-%d %H:%m:%S') or '')
        self.updated_data.set_text(row._last_updated and row._last_updated.strftime('%Y-%m-%d %H:%m:%S') or '')


class InfoBoxPage(gtk.ScrolledWindow):
    """
    A :class:`gtk.ScrolledWindow` that contains
    :class:`bauble.view.InfoExpander` objects.
    """

    def __init__(self):
        super(InfoBoxPage, self).__init__()
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.vbox = gtk.VBox()
        self.vbox.set_spacing(10)
        viewport = gtk.Viewport()
        viewport.add(self.vbox)
        self.add(viewport)
        self.expanders = {}
        self.label = None
        return

    def add_expander(self, expander):
        """
        Add an expander to the list of exanders in this infobox

        :param expander: the bauble.view.InfoExpander to add to this infobox
        """
        self.vbox.pack_start(expander, expand=False, fill=True, padding=5)
        self.expanders[expander.get_property('label')] = expander
        expander._sep = gtk.HSeparator()
        self.vbox.pack_start(expander._sep, False, False)

    def get_expander(self, label):
        """
        Returns an expander by the expander's label name

        :param label: the name of the expander to return
        """
        if label in self.expanders:
            return self.expanders[label]
        else:
            return
            return

    def remove_expander(self, label):
        """
        Remove expander from the infobox by the expander's label bel

        :param label: the name of th expander to remove

        Return the expander that was removed from the infobox.
        """
        if label in self.expanders:
            return self.vbox.remove(self.expanders[label])

    def update(self, row):
        """
        Updates the infobox with values from row

        :param row: the mapper instance to use to update this infobox,
          this is passed to each of the infoexpanders in turn
        """
        for expander in self.expanders.values():
            expander.update(row)


class InfoBox(gtk.Notebook):
    """
    Holds list of expanders with an optional tabbed layout.

    The default is to not use tabs. To create the InfoBox with tabs
    use InfoBox(tabbed=True).  When using tabs then you can either add
    expanders directly to the InfoBoxPage or using
    InfoBox.add_expander with the page_num argument.

    Also, it's not recommended to create a subclass of a subclass of
    InfoBox since if they both use bauble.utils.BuilderWidgets then
    the widgets will be parented to the infobox that is created first
    and the expanders of the second infobox will appear empty.
    """

    def __init__(self, tabbed=False):
        super(InfoBox, self).__init__()
        self.row = None
        self.set_property('show-border', False)
        if not tabbed:
            page = InfoBoxPage()
            self.insert_page(page, position=0)
            self.set_property('show-tabs', False)
        self.set_current_page(0)
        self.connect('switch-page', self.on_switch_page)
        return

    def on_switch_page(self, notebook, dummy_page, page_num, *args):
        """
        Called when a page is switched
        """
        if not self.row:
            return
        page = self.get_nth_page(page_num)
        page.update(self.row)

    def add_expander(self, expander, page_num=0):
        """
        Add an expander to a page.

        :param expander: The expander to add.
        :param page_num: The page number in the InfoBox to add the expander.
        """
        page = self.get_nth_page(page_num)
        page.add_expander(expander)

    def update(self, row):
        """
        Update the current page with row.
        """
        self.row = row
        page_num = self.get_current_page()
        self.get_nth_page(page_num).update(row)


class LinksExpander(InfoExpander):

    def __init__(self, notes=None, links=[]):
        """
        :param notes: the name of the notes property on the row
        """
        super(LinksExpander, self).__init__(_('Links'))
        self.dynamic_box = gtk.VBox()
        self.vbox.pack_start(self.dynamic_box)
        self.notes = notes
        self.buttons = []
        from bauble.utils.web import BaubleLinkButton
        for link in links:
            try:
                klass = type(link['name'], (BaubleLinkButton,), link)
                self.buttons.append(klass())
            except Exception as e:
                logger.debug('wrong link definition %s, %s(%s)' % (
                 link, type(e), e))

        for b in self.buttons:
            b.set_alignment(0, -1)
            self.vbox.pack_start(b)

    def update(self, row):
        import pango
        map(self.dynamic_box.remove, self.dynamic_box.get_children())
        for b in self.buttons:
            b.set_string(row)

        if self.notes:
            notes = getattr(row, self.notes)
            for note in notes:
                for label, url in utils.get_urls(note.note):
                    if not label:
                        label = url
                    label = gtk.Label(label)
                    label.set_ellipsize(pango.ELLIPSIZE_END)
                    button = gtk.LinkButton(uri=url)
                    button.add(label)
                    button.set_alignment(0, -1)
                    self.dynamic_box.pack_start(button, expand=False, fill=False)

            self.dynamic_box.show_all()


class AddOneDot(threading.Thread):

    @staticmethod
    def callback(dotno):
        statusbar = bauble.gui.widgets.statusbar
        sbcontext_id = statusbar.get_context_id('searchview.nresults')
        statusbar.pop(sbcontext_id)
        statusbar.push(sbcontext_id, _('counting results') + '.' * dotno)

    def __init__(self, group=None, verbose=None, **kwargs):
        super(AddOneDot, self).__init__(group=group, target=None, name=None, verbose=verbose)
        self.__stopped = threading.Event()
        self.dotno = 0
        return

    def cancel(self):
        self.__stopped.set()

    def run(self):
        while not self.__stopped.wait(1.0):
            self.dotno += 1
            gobject.idle_add(self.callback, self.dotno)


class CountResultsTask(threading.Thread):

    def __init__(self, klass, ids, dots_thread, group=None, verbose=None, **kwargs):
        super(CountResultsTask, self).__init__(group=group, target=None, name=None, verbose=verbose)
        self.klass = klass
        self.ids = ids
        self.dots_thread = dots_thread
        self.__cancel = False
        return

    def cancel(self):
        self.__cancel = True

    def run(self):
        session = db.Session()
        klass = self.klass
        d = {}
        for ndx in self.ids:
            item = session.query(klass).filter(klass.id == ndx).one()
            if self.__cancel:
                break
            for k, v in item.top_level_count().items():
                if isinstance(v, set):
                    d[k] = v.union(d.get(k, set()))
                else:
                    d[k] = v + d.get(k, 0)

        result = []
        for k, v in sorted(d.items()):
            if isinstance(k, tuple):
                k = k[1]
            if isinstance(v, set):
                v = len(v)
            result.append('%s: %d' % (k, v))
            if self.__cancel:
                break

        value = _('top level count: %s') % (', ').join(result)
        if bauble.gui:

            def callback(text):
                statusbar = bauble.gui.widgets.statusbar
                sbcontext_id = statusbar.get_context_id('searchview.nresults')
                statusbar.pop(sbcontext_id)
                statusbar.push(sbcontext_id, text)

            if not self.__cancel:
                self.dots_thread.cancel()
                gobject.idle_add(callback, value)
        else:
            logger.debug('showing text %s', value)
        session.close()


class SearchView(pluginmgr.View):
    """
    The SearchView is the main view for Ghini.  It manages the search
    results returned when search strings are entered into the main
    text entry.
    """

    class ViewMeta(dict):
        """
        This class shouldn't need to be instantiated directly.  Access
        the meta for the SearchView with the
        :class:`bauble.view.SearchView`'s row_meta property.
        """

        class Meta(object):

            def __init__(self):
                self.children = None
                self.infobox = None
                self.markup_func = None
                self.actions = []
                return

            def set(self, children=None, infobox=None, context_menu=None, markup_func=None):
                """
                :param children: where to find the children for this type,
                    can be a callable of the form C{children(row)}

                :param infobox: the infobox for this type

                :param context_menu: a dict describing the context menu used
                when the user right clicks on this type

                :param markup_func: the function to call to markup
                search results of this type, if markup_func is None
                the instances __str__() function is called...the
                strings returned by this function should escape any
                non markup characters
                """
                self.children = children
                self.infobox = infobox
                self.markup_func = markup_func
                self.context_menu = context_menu
                self.actions = []
                if self.context_menu:
                    self.actions = filter(lambda x: isinstance(x, Action), self.context_menu)

            def get_children(self, obj):
                """
                :param obj: get the children from obj according to
                self.children,

                Returns a list or list-like object.
                """
                if self.children is None:
                    return []
                else:
                    if callable(self.children):
                        return self.children(obj)
                    return getattr(obj, self.children)

        def __getitem__(self, item):
            if item not in self:
                self[item] = self.Meta()
            return self.get(item)

    row_meta = ViewMeta()
    bottom_info = ViewMeta()

    def __init__(self):
        """
        the constructor
        """
        logger.debug('SearchView::__init__')
        super(SearchView, self).__init__()
        filename = os.path.join(paths.lib_dir(), 'bauble.glade')
        self.widgets = utils.load_widgets(filename)
        self.view = editor.GenericEditorView(filename, root_widget_name='main_window')
        self.create_gui()
        import pictures_view
        pictures_view.floating_window = pictures_view.PicturesView(parent=self.widgets.search_h2pane)
        self.populate_callback_id = None
        self.context_menu_cache = {}
        self.infobox_cache = {}
        self.infobox = None
        self.session = db.Session()
        self.add_notes_page_to_bottom_notebook()
        self.running_threads = []
        return

    def add_notes_page_to_bottom_notebook(self):
        """add notebook page for notes

        this is a temporary function, will be removed when notes are
        implemented as a plugin. then notes will be added with the
        generic add_page_to_bottom_notebook.

        """
        page = self.view.widgets.notes_scrolledwindow
        self.view.widgets.remove_parent(page)
        label = gtk.Label('Notes')
        self.view.widgets.bottom_notebook.append_page(page, label)
        self.bottom_info[Note] = {'fields_used': [
                         'date', 'user', 'category', 'note'], 
           'tree': page.get_children()[0], 
           'label': label, 
           'name': _('Notes')}

    def add_page_to_bottom_notebook(self, bottom_info):
        """add notebook page for a plugin class
        """
        glade_name = bottom_info['glade_name']
        builder = utils.BuilderLoader.load(glade_name)
        widgets = utils.BuilderWidgets(builder)
        page = getattr(widgets, bottom_info['page_widget'])
        widgets.remove_parent(page)
        label = gtk.Label(bottom_info['name'])
        self.view.widget_append_page('bottom_notebook', page, label)
        bottom_info['tree'] = page.get_children()[0]
        bottom_info['label'] = label

    def update_bottom_notebook(self):
        """
        Update the bottom_notebook from the currently selected row.

        bottom_notebook has one page per type of information. Every page
        is registered by its plugin, which adds an entry to the
        dictionary self.bottom_info.

        the GtkNotebook pages are ScrolledWindow containing a TreeView,
        this should have a model, and the ordered names of the fields to
        be stored in the model is in bottom_info['fields_used'].

        """
        values = self.get_selected_values()
        if len(values) != 1:
            self.view.widget_set_visible('bottom_notebook', False)
            return
        self.view.widget_set_visible('bottom_notebook', True)
        row = values[0]
        for klass, bottom_info in self.bottom_info.items():
            if 'label' not in bottom_info:
                self.add_page_to_bottom_notebook(bottom_info)
            label = bottom_info['label']
            if not hasattr(klass, 'attached_to'):
                logging.warn('class %s does not implement attached_to' % klass)
                continue
            objs = klass.attached_to(row)
            model = bottom_info['tree'].get_model()
            model.clear()
            if len(objs) == 0:
                label.set_use_markup(False)
                label.set_label(bottom_info['name'])
            else:
                label.set_use_markup(True)
                label.set_label('<b>%s</b>' % bottom_info['name'])
                for obj in objs:
                    model.append([ getattr(obj, k) for k in bottom_info['fields_used']
                                 ])

    def update_infobox(self):
        """
        Sets the infobox according to the currently selected row.
        no infobox is shown if nothing is selected
        """

        def set_infobox_from_row(row):
            """implement the logic for update_infobox"""
            logger.debug('set_infobox_from_row: %s --  %s' % (row, repr(row)))
            if row is None:
                if self.infobox is not None and self.infobox.parent == self.pane:
                    self.pane.remove(self.infobox)
                return
            new_infobox = None
            selected_type = type(row)
            if selected_type in self.infobox_cache.keys():
                new_infobox = self.infobox_cache[selected_type]
            elif selected_type in self.row_meta and self.row_meta[selected_type].infobox is not None:
                logger.debug('%s defines infobox class %s' % (
                 selected_type,
                 self.row_meta[selected_type].infobox))
                for ib in self.infobox_cache.values():
                    if isinstance(ib, self.row_meta[selected_type].infobox):
                        logger.debug('found same infobox under different name')
                        new_infobox = ib

                if not new_infobox:
                    logger.debug('not found infobox, we make a new one')
                    new_infobox = self.row_meta[selected_type].infobox()
                self.infobox_cache[selected_type] = new_infobox
            logger.debug('created or retrieved infobox %s %s' % (
             type(new_infobox), new_infobox))
            if self.infobox is not None and type(self.infobox) != type(new_infobox):
                if self.infobox.parent == self.pane:
                    self.pane.remove(self.infobox)
            self.infobox = new_infobox
            if self.infobox is not None:
                self.pane.pack2(self.infobox, resize=False, shrink=True)
                self.pane.show_all()
                self.infobox.update(row)
            return

        logger.debug('update_infobox')
        values = self.get_selected_values()
        if not values:
            set_infobox_from_row(None)
            return
        else:
            if object_session(values[0]) is None:
                logger.debug('cannot populate info box from detached object')
                return
            try:
                set_infobox_from_row(values[0])
            except Exception as e:
                logger.debug('SearchView.update_infobox: %s' % e)
                logger.debug(traceback.format_exc())
                logger.debug(values)
                set_infobox_from_row(None)

            return

    def get_selected_values(self):
        """
        Return the values in all the selected rows.
        """
        model, rows = self.results_view.get_selection().get_selected_rows()
        if model is None:
            return
        else:
            return [ model[row][0] for row in rows ]

    def on_cursor_changed(self, view):
        """
        Update the infobox and switch the accelerators depending on the
        type of the row that the cursor points to.
        """
        self.update_infobox()
        self.update_bottom_notebook()
        pictures_view.floating_window.set_selection(self.get_selected_values())
        for accel, cb in self.installed_accels:
            r = self.accel_group.disconnect_key(accel[0], accel[1])
            if not r:
                logger.warning('callback not removed: %s' % cb)

        self.installed_accels = []
        selected = self.get_selected_values()
        if not selected:
            return
        selected_type = type(selected[0])
        for action in self.row_meta[selected_type].actions:
            enabled = len(selected) > 1 and action.multiselect or len(selected) <= 1 and action.singleselect
            if not enabled:
                continue
            keyval, mod = gtk.accelerator_parse(action.accelerator)
            if (keyval, mod) != (0, 0):

                def cb(func):

                    def _impl(*args):
                        sel = self.get_selected_values()
                        if func(sel):
                            self.update()

                    return _impl

                self.accel_group.connect_group(keyval, mod, gtk.ACCEL_VISIBLE, cb(action.callback))
                self.installed_accels.append(((keyval, mod), action.callback))
            else:
                logger.warning('Could not parse accelerator: %s' % action.accelerator)

    nresults_statusbar_context = 'searchview.nresults'

    def search(self, text):
        """
        search the database using text
        """
        logger.debug('SearchView.search(%s)' % text)
        error_msg = None
        error_details_msg = None
        self.cancel_threads()
        if False:
            self.session.close()
            self.session = db.Session()
        else:
            self.session.rollback()
        bold = '<b>%s</b>'
        results = []
        try:
            results = search.search(text, self.session)
        except ParseException as err:
            error_msg = _('Error in search string at column %s') % err.column
        except (BaubleError, AttributeError, Exception, SyntaxError) as e:
            logger.debug(traceback.format_exc())
            error_msg = _('** Error: %s') % utils.xml_safe(e)
            error_details_msg = utils.xml_safe(traceback.format_exc())

        if error_msg:
            bauble.gui.show_error_box(error_msg, error_details_msg)
            return
        else:
            utils.clear_model(self.results_view)
            self.update_infobox()
            statusbar = bauble.gui.widgets.statusbar
            sbcontext_id = statusbar.get_context_id('searchview.nresults')
            statusbar.pop(sbcontext_id)
            if len(results) == 0:
                model = gtk.ListStore(str)
                msg = bold % cgi.escape(_('Couldn\'t find anything for search: "%s"') % text)
                model.append([msg])
                self.results_view.set_model(model)
            else:
                if len(results) > 5000:
                    msg = _('This query returned %s results.  It may take a long time to get all the data. Are you sure you want to continue?') % len(results)
                    if not utils.yes_no_dialog(msg):
                        return
                statusbar.push(sbcontext_id, _('Retrieving %s search results...') % len(results))
                try:
                    import time
                    start = time.time()
                    if len(results) > 1000:
                        self.populate_results(results)
                    else:
                        task = self._populate_worker(results)
                        while True:
                            try:
                                task.next()
                            except StopIteration:
                                break

                    logger.debug(time.time() - start)
                except StopIteration:
                    return

                statusbar.pop(sbcontext_id)
                statusbar.push(sbcontext_id, _('counting results'))
                if len(set(item.__class__ for item in results)) == 1:
                    dots_thread = self.start_thread(AddOneDot())
                    self.start_thread(CountResultsTask(results[0].__class__, [ i.id for i in results ], dots_thread))
                else:
                    statusbar.push(sbcontext_id, _('size of non homogeneous result: %s') % len(results))
                self.results_view.set_cursor(0)
                gobject.idle_add(lambda : self.results_view.scroll_to_cell(0))
            self.update_bottom_notebook()
            return

    def remove_children(self, model, parent):
        """
        Remove all children of some parent in the model, reverse
        iterate through them so you don't invalidate the iter
        """
        while model.iter_has_child(parent):
            nkids = model.iter_n_children(parent)
            child = model.iter_nth_child(parent, nkids - 1)
            model.remove(child)

    def on_test_expand_row(self, view, treeiter, path, data=None):
        """
        Look up the table type of the selected row and if it has
        any children then add them to the row
        """
        model = view.get_model()
        row = model.get_value(treeiter, 0)
        view.collapse_row(path)
        self.remove_children(model, treeiter)
        try:
            kids = self.row_meta[type(row)].get_children(row)
            if len(kids) == 0:
                return True
        except saexc.InvalidRequestError as e:
            logger.debug(utils.utf8(e))
            model = self.results_view.get_model()
            for found in utils.search_tree_model(model, row):
                model.remove(found)

            return True
        except Exception as e:
            logger.debug(utils.utf8(e))
            logger.debug(traceback.format_exc())
            return True

        self.append_children(model, treeiter, sorted(kids, key=utils.natsort_key))
        return False

    def populate_results(self, results, check_for_kids=False):
        """
        Adds results to the search view in a task.

        :param results: a list or list-like object
        :param check_for_kids: only used for testing
        """
        bauble.task.queue(self._populate_worker(results, check_for_kids))

    def _populate_worker(self, results, check_for_kids=False):
        """
        Generator function for adding the search results to the
        model. This method is usually called by self.populate_results()
        """
        nresults = len(results)
        model = gtk.TreeStore(object)
        model.set_default_sort_func(lambda *args: -1)
        model.set_sort_column_id(-1, gtk.SORT_ASCENDING)
        utils.clear_model(self.results_view)
        groups = []
        results = sorted(results, key=lambda x: type(x))
        for key, group in itertools.groupby(results, key=lambda x: type(x)):
            groups.append(sorted(group, key=utils.natsort_key, reverse=True))

        groups = sorted(groups, key=lambda x: type(x[0]), reverse=True)
        update_every = 200
        steps_so_far = 0
        added = set()
        for obj in itertools.chain(*groups):
            if obj in added:
                continue
            else:
                added.add(obj)
            parent = model.prepend(None, [obj])
            obj_type = type(obj)
            if check_for_kids:
                kids = self.row_meta[obj_type].get_children(obj)
                if len(kids) > 0:
                    model.prepend(parent, ['-'])
            elif self.row_meta[obj_type].children is not None:
                model.prepend(parent, ['-'])
            steps_so_far += 1
            if steps_so_far % update_every == 0:
                percent = float(steps_so_far) / float(nresults)
                if 0 < percent < 1.0:
                    bauble.gui.progressbar.set_fraction(percent)
                yield

        self.results_view.freeze_child_notify()
        self.results_view.set_model(model)
        self.results_view.thaw_child_notify()
        return

    def append_children(self, model, parent, kids):
        """
        append object to a parent iter in the model

        :param model: the model the append to
        :param parent:  the parent gtk.TreeIter
        :param kids: a list of kids to append
        @return: the model with the kids appended
        """
        check(parent is not None, 'append_children(): need a parent')
        for k in kids:
            i = model.append(parent, [k])
            if self.row_meta[type(k)].children is not None:
                model.append(i, ['_dummy'])

        return model

    def cell_data_func(self, col, cell, model, treeiter):
        path = model.get_path(treeiter)
        tree_rect = self.results_view.get_visible_rect()
        cell_rect = self.results_view.get_cell_area(path, col)
        if cell_rect.y > tree_rect.height:
            return
        value = model[treeiter][0]
        if isinstance(value, basestring):
            cell.set_property('markup', value)
        else:
            if not object_session(value):
                if value in self.session:
                    self.session.expire(value)
                else:
                    self.session.merge(value)
            try:
                r = value.search_view_markup_pair()
                try:
                    main, substr = r
                except:
                    main = r
                    substr = '(%s)' % type(value).__name__

                cell.set_property('markup', '%s\n%s' % (
                 _mainstr_tmpl % utils.utf8(main),
                 _substr_tmpl % utils.utf8(substr)))
            except (saexc.InvalidRequestError, TypeError) as e:
                logger.warning('bauble.view.SearchView.cell_data_func(): \n(%s)%s' % (
                 type(e), e))

                def remove():
                    model = self.results_view.get_model()
                    self.results_view.set_model(None)
                    for found in utils.search_tree_model(model, value):
                        model.remove(found)

                    self.results_view.set_model(model)
                    return

                gobject.idle_add(remove)
            except Exception as e:
                logger.error('bauble.view.SearchView.cell_data_func(): \n(%s)%s' % (
                 type(e), e))
                raise

    def get_expanded_rows(self):
        """
        return all the rows in the model that are expanded
        """
        expanded_rows = []
        expand = lambda view, path: expanded_rows.append(gtk.TreeRowReference(view.get_model(), path))
        self.results_view.map_expanded_rows(expand)
        expanded_rows.reverse()
        return expanded_rows

    def expand_to_all_refs(self, references):
        """
        :param references: a list of TreeRowReferences to expand to

        Note: This method calls get_path() on each
        gtk.TreeRowReference in <references> which apparently
        invalidates the reference.
        """
        for ref in references:
            if ref.valid():
                self.results_view.expand_to_path(ref.get_path())

    def on_view_button_release(self, view, event, data=None):
        """right-mouse-button release.

        Popup a context menu on the selected row.
        """
        if event.button != 3:
            return False
        else:
            selected = self.get_selected_values()
            if not selected:
                return
            selected_types = set(map(type, selected))
            if len(selected_types) > 1:
                return False
            selected_type = selected_types.pop()
            if not self.row_meta[selected_type].actions:
                return True
            menu = None
            try:
                menu = self.context_menu_cache[selected_type]
            except KeyError:
                menu = gtk.Menu()
                for action in self.row_meta[selected_type].actions:
                    logger.debug('path: %s' % action.get_accel_path())
                    item = action.create_menu_item()

                    def on_activate(item, cb):
                        result = False
                        try:
                            values = self.get_selected_values()
                            result = cb(values)
                        except Exception as e:
                            msg = utils.xml_safe(str(e))
                            tb = utils.xml_safe(traceback.format_exc())
                            utils.message_details_dialog(msg, tb, gtk.MESSAGE_ERROR)
                            logger.warning(traceback.format_exc())

                        if result:
                            self.update()

                    item.connect('activate', on_activate, action.callback)
                    menu.append(item)

                self.context_menu_cache[selected_type] = menu

            for action in self.row_meta[selected_type].actions:
                action.enabled = len(selected) > 1 and action.multiselect or len(selected) <= 1 and action.singleselect

            menu.popup(None, None, None, event.button, event.time)
            return True

    def update(self):
        """
        Expire all the children in the model, collapse everything,
        reexpand the rows to the previous state where possible and
        update the infobox.
        """
        logger.debug('SearchView::update')
        model, paths = self.results_view.get_selection().get_selected_rows()
        ref = None
        try:
            ref = gtk.TreeRowReference(model, paths[0])
        except:
            pass

        self.session.expire_all()

        def invalidate_cache(model, path, treeiter, data=None):
            obj = model[path][0]
            if hasattr(obj, 'invalidate_str_cache'):
                obj.invalidate_str_cache()

        model.foreach(invalidate_cache)
        expanded_rows = self.get_expanded_rows()
        self.results_view.collapse_all()
        if not ref:
            return
        else:
            path = None
            if ref.valid():
                path = ref.get_path()
            self.expand_to_all_refs(expanded_rows)
            self.results_view.set_cursor(path)
            return

    def on_view_row_activated(self, view, path, column, data=None):
        """
        expand the row on activation
        """
        logger.debug('SearchView::on_view_row_activated %s %s %s %s' % (
         view, path, column, data))
        view.expand_row(path, False)

    def create_gui(self):
        """
        create the interface
        """
        logger.debug('SearchView::create_gui')
        self.results_view = self.widgets.results_treeview
        self.results_view.set_headers_visible(False)
        self.results_view.set_rules_hint(True)
        self.results_view.set_fixed_height_mode(True)
        selection = self.results_view.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        self.results_view.set_rubber_banding(True)
        renderer = gtk.CellRendererText()
        renderer.set_fixed_height_from_font(2)
        renderer.set_property('ellipsize', pango.ELLIPSIZE_END)
        column = gtk.TreeViewColumn('Name', renderer)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_cell_data_func(renderer, self.cell_data_func)
        self.results_view.append_column(column)
        self.results_view.connect('cursor-changed', self.on_cursor_changed)
        self.results_view.connect('test-expand-row', self.on_test_expand_row)
        self.results_view.connect('button-release-event', self.on_view_button_release)

        def on_press(view, event):
            """Ignore the mouse right-click event.

            This makes sure that we don't remove the multiple selection
            when clicking a mouse button.
            """
            if event.button == 3:
                if event.get_state() & gtk.gdk.CONTROL_MASK == 0:
                    path, _, _, _ = view.get_path_at_pos(int(event.x), int(event.y))
                    if not view.get_selection().path_is_selected(path):
                        return False
                return True
            return False

        self.results_view.connect('button-press-event', on_press)
        self.results_view.connect('row-activated', self.on_view_row_activated)
        self.accel_group = gtk.AccelGroup()
        self.installed_accels = []
        self.pane = self.widgets.search_hpane
        self.picpane = self.widgets.search_h2pane
        vbox = self.widgets.search_vbox
        self.widgets.remove_parent(vbox)
        self.pack_start(vbox)

    def on_notes_size_allocation(self, treeview, allocation, column, cell):
        """
        Set the wrap width according to the widgth of the treeview
        """
        otherColumns = (c for c in treeview.get_columns() if c != column)
        newWidth = allocation.width - sum(c.get_width() for c in otherColumns)
        newWidth -= treeview.style_get_property('horizontal-separator') * 2
        if cell.props.wrap_width == newWidth or newWidth <= 0:
            return
        cell.props.wrap_width = newWidth
        store = treeview.get_model()
        treeiter = store.get_iter_first()
        while treeiter and store.iter_is_valid(treeiter):
            store.row_changed(store.get_path(treeiter), treeiter)
            treeiter = store.iter_next(treeiter)
            treeview.set_size_request(0, -1)


class Note():
    """temporary patch before we implement Notes as a plugin
    """

    @classmethod
    def attached_to(cls, obj):
        """return the list of notes connected to obj
        """
        try:
            return obj.notes
        except:
            return []


class AppendThousandRows(threading.Thread):

    def callback(self, rows):
        for row in rows:
            self.view.add_row(row)

    def cancel_callback(self):
        row = ['---'] * 6
        row[4] = '** ' + _('interrupted') + ' **'
        self.view.liststore.append(row)

    def __init__(self, view, group=None, verbose=None, **kwargs):
        super(AppendThousandRows, self).__init__(group=group, target=None, name=None, verbose=verbose)
        self.__stopped = threading.Event()
        self.view = view
        return

    def cancel(self):
        self.__stopped.set()

    def run(self):
        session = db.Session()
        q = session.query(db.History).order_by(db.History.timestamp.desc())
        offset = 0
        step = 200
        count = q.count()
        while offset < count and not self.__stopped.isSet():
            rows = q.offset(offset).limit(step).all()
            gobject.idle_add(self.callback, rows)
            offset += step

        session.close()
        if offset < count:
            gobject.idle_add(self.cancel_callback)


class HistoryView(pluginmgr.View):
    """Show the tables row in the order they were last updated
    """
    TVC_TIMESTAMP = 0
    TVC_OPERATION = 1
    TVC_USER = 2
    TVC_TABLE = 3
    TVC_USER_FRIENDLY = 4
    TVC_DICT = 5

    def __init__(self):
        logger.debug('PrefsView::__init__')
        super(HistoryView, self).__init__(filename=os.path.join(paths.lib_dir(), 'bauble.glade'), root_widget_name='history_window')
        self.view.connect_signals(self)
        self.liststore = self.view.widgets.history_ls
        self.update()

    @staticmethod
    def cmp_items(a, b):
        ka, va = a
        kb, vb = b
        if ka == 'id':
            return -1
        if kb == 'id':
            return 1
        if va == 'None' and vb != 'None':
            return 1
        if vb == 'None' and va != 'None':
            return -1
        if a < b:
            return -1
        if b < a:
            return 1
        return 0

    @staticmethod
    def show_typed_value(v):
        try:
            eval(v)
            return v
        except:
            return '»%s«' % v

    def add_row(self, item):
        d = eval(item.values)
        del d['_created']
        del d['_last_updated']
        friendly = (', ').join('%s: %s' % (k, self.show_typed_value(v)) for k, v in sorted(d.items(), self.cmp_items))
        self.liststore.append([
         ('%s' % item.timestamp)[:19], item.operation, item.user,
         item.table_name, friendly, item.values])

    def on_row_activated(self, tree, path, column):
        row = self.liststore[path]
        dic = eval(row[self.TVC_DICT])
        table = row[self.TVC_TABLE]
        obj_id = int(dic['id'])
        for table_name, equivalent, key in [
         ('genus_note', 'genus', 'genus_id'),
         ('species_note', 'species', 'species_id'),
         ('location_note', 'location', 'location_id'),
         ('accession_note', 'accession', 'accession_id'),
         ('plant_note', 'plant', 'plant_id'),
         ('genus_synonym', 'genus', 'genus_id'),
         ('species_synonym', 'species', 'species_id'),
         ('vernacular_name', 'species', 'species_id'),
         ('default_vernacular_name', 'species', 'species_id'),
         ('plant_change', 'plant', 'plant_id')]:
            if table == table_name:
                table = equivalent
                obj_id = int(dic[key])

        mapper_search = search.get_strategy('MapperSearch')
        if table in mapper_search._domains:
            query = '%s where id=%s' % (table, obj_id)
            bauble.gui.widgets.main_comboentry.child.set_text(query)
            bauble.gui.widgets.go_button.emit('clicked')

    def update(self):
        """
        Add the history items to the view.
        """
        self.liststore.clear()
        self.start_thread(AppendThousandRows(self))


class HistoryCommandHandler(pluginmgr.CommandHandler):
    command = 'history'
    view = None

    def __init__(self):
        super(HistoryCommandHandler, self).__init__()

    def get_view(self):
        if not self.view:
            self.__class__.view = HistoryView()
        return self.view

    def __call__(self, cmd, arg):
        self.view.update()


pluginmgr.register_command(HistoryCommandHandler)

def select_in_search_results(obj):
    """
    :param obj: the object the select
    @returns: a gtk.TreeIter to the selected row

    Search the tree model for obj if it exists then select it if not
    then add it and select it.

    The the obj is not in the model then we add it.
    """
    check(obj is not None, 'select_in_search_results: arg is None')
    view = bauble.gui.get_view()
    if not isinstance(view, SearchView):
        return
    else:
        logger.debug('select_in_search_results %s is in session %s' % (
         obj, obj in view.session))
        model = view.results_view.get_model()
        found = utils.search_tree_model(model, obj)
        row_iter = None
        if len(found) > 0:
            row_iter = found[0]
        else:
            row_iter = model.append(None, [obj])
            model.append(row_iter, ['-'])
        view.results_view.set_cursor(model.get_path(row_iter))
        return row_iter


class DefaultCommandHandler(pluginmgr.CommandHandler):

    def __init__(self):
        super(DefaultCommandHandler, self).__init__()

    command = [
     None]
    view = None

    def get_view(self):
        if self.__class__.view is None:
            self.__class__.view = SearchView()
        return self.__class__.view

    def __call__(self, cmd, arg):
        self.view.search(arg)