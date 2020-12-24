# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/lib/base.py
# Compiled at: 2008-05-18 11:13:57
"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.

AUTHOR: Emanuel Gardaya Calso

"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons import templating
import subicpos.lib.helpers as h, subicpos.model as model
from child import ChildList

def render(*args, **kw):
    return templating.render(*args, **kw)


class PropertyList(object):

    def __init__(self, parent, field, table):
        self.parent = parent
        self.entries = getattr(parent, field)
        self.table = table
        for entry in list(self.entries):
            self.entries.remove(entry)

    def save(self, c_id):
        entry = model.get(self.table, c_id)
        if entry not in self.entries:
            self.entries.append(entry)


class BaseController(WSGIController):

    def __before__(self, action, **kw):
        env = {}
        for (k, v) in request.environ.items():
            env[k] = v

        env['SCRIPT_NAME'] = ''
        import routes
        config = routes.request_config()
        config.environ = env

    def _dbg(self, function=None, msg=None):
        _ = '%s.%s' % (__name__, self.__class__.__name__)
        if function is not None:
            _ += '.' + str(function)
        if msg is not None:
            _ += ': ' + str(msg)
        return _

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        return WSGIController.__call__(self, environ, start_response)


class TableController(BaseController):
    table = None


class ListController(TableController):
    parent = dict()
    children = dict()
    properties = ()
    list_functions = ('delete', 'add')
    entry_functions = ('delete', 'edit', 'details')
    columns_shown = set([])
    columns_hidden = set([
     'id'])
    column_descriptions = dict()

    def __init__(self):
        c.title = self.__class__.__name__.replace('Controller', '')
        c.table = self.table
        c.columns = c.table.c.keys()
        c.parent = self.parent
        c.children = self.children
        c.properties = self.properties
        c.db_sess = model.Session
        c.page = 1
        c.max_entries = 20
        c.list_functions = self.list_functions
        c.entry_functions = self.entry_functions
        c.columns_shown = self.columns_shown
        c.columns_hidden = self.columns_hidden
        c.column_descriptions = self.column_descriptions
        self._init_custom()

    def _init_custom(self):
        pass

    def _add(self):
        c.id = None
        c.entry = self.table()
        return

    def _details(self, id):
        c.id = id
        c.entry = model.Session.query(c.table).get(id)

    def _delete(self, id):
        entry = model.Session.query(c.table).get(id)
        model.Session.delete(entry)
        model.Session.flush()
        model.Session.commit()
        self._dbg('_delete', '%s Successfully deleted' % entry)

    def _list(self):
        c.entries = self.query

    def _list_params(self):
        if 'page' in request.params.keys():
            c.page = int(request.params['page'])

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())

    def _multi(self):
        self._dbg('_multi', request.params.dict_of_lists())
        ids = self._multi_get_ids()
        function = request.params['function']
        if function == g.function_delete:
            self._multi_delete(ids)

    def _multi_delete(self, ids):
        map(self._delete, ids)

    def _multi_get_ids(self):
        try:
            ids = request.params.dict_of_lists()['select']
        except KeyError:
            args = []
            for (k, v) in request.params.iteritems():
                args.append('%s=%s' % (k, v))

            redirect_to(str('list?%s' % ('&').join(args)))

        return ids

    def _save(self, id=None, params=request.params):
        all_args = self._save_custom(params)
        entry_args = {}
        child_args = {}
        for k in all_args.keys():
            if k in self.table.c.keys():
                entry_args[k] = all_args[k]
            else:
                child_args[k] = all_args.dict_of_lists()[k]

        entry = self._save_entry(id, entry_args)
        self._dbg('_save', '%s Successfully saved' % entry)
        self._save_children(entry, **child_args)
        self._save_properties(entry, **child_args)
        model.Session.save_or_update(entry)
        model.Session.commit()
        return entry

    def _save_children(self, entry, **kw):
        for (field, children) in self.children.iteritems():
            child_list = ChildList(entry, field, children)
            child_list.multi_save(**kw)

        return entry

    def _save_custom(self, params):
        return params

    def _save_entry(self, id, entry_args):
        if id is not None:
            entry = model.get(self.table, id)
            for (k, v) in entry_args.iteritems():
                setattr(entry, k, v)

        else:
            entry = self.table(**entry_args)
        return entry

    def _save_properties(self, entry, **kw):
        for (field, col, tbl) in self.properties:
            prop = PropertyList(entry, field, tbl)
            try:
                c_ids = request.params.dict_of_lists()[field]
            except KeyError:
                continue

            self._dbg('add_properties', (field, c_ids))
            map(prop.save, c_ids)

    def add(self):
        self._dbg('add')
        self._add()
        return self.render_edit()

    def blank_out(self):
        return ''

    def details(self, id):
        self._dbg('details', request.params)
        self._details(request.params['id'])
        return self.render_details()

    def delete(self):
        self._dbg('delete', request.params)
        self._delete(request.params['id'])
        redirect_to('index')

    def edit(self, id):
        self._dbg('edit', request.params)
        self._details(request.params['id'])
        return self.render_edit()

    def list(self):
        self._dbg('list', request.params)
        self._list_params()
        self._list_query()
        self._list()
        return self.render_list()

    index = list

    def multi(self):
        self._dbg('delete')
        self._multi()
        return self.list()

    def save(self):
        self._dbg('save')
        try:
            id = request.params['id']
        except KeyError:
            id = None

        entry = self._save(id, request.params)
        self._dbg('save', entry.id)
        redirect_to('list')
        return 'Saved'

    def _edit_child(self):
        c.cnt = request.params['cnt']
        c.child = request.params['child']
        c.columns = self.children[c.child]['columns']
        c.child_details = self.children[c.child]
        c.table = self.children[c.child]['table']

    def add_child(self):
        self._edit_child()
        return self.render_add_child()

    def add_children(self, parent, **kw):
        for child in self.children.keys():
            try:
                self._dbg('add_children', 'Save Child:\n%s' % request.params.dict_of_lists()[child])
            except KeyError:
                break

    def add_properties(self, parent, **kw):
        for (field, col, db_tbl) in self.properties:
            prop = Property(parent, field, db_tbl)
            try:
                c_ids = request.params.dict_of_lists()[field]
            except KeyError:
                break

            self._dbg('add_properties', (field, c_ids))
            map(prop.add, c_ids)

        model.Session.save_or_update(parent)
        model.Session.commit()

    def edit_child(self):
        self._edit_child()
        c.entry = model.get(c.table, request.params['c_id'])
        c.p_id = request.params['p_id']
        return self.render_edit_child()

    def rem_child(self, id):
        child = request.params['child']
        p_id = request.params['p_id']
        table = self.children[child]['table']
        parent = model.get(self.table, p_id)
        entry = model.get(table, id)
        children = getattr(parent, child)
        children.remove(entry)
        model.Session.update(parent)
        model.Session.commit()
        return ''

    def render_add_child(self):
        return render('/add_child.mako')

    def render_details(self):
        return render('/details.mako')

    def render_edit(self):
        return render('/edit.mako')

    def render_edit_child(self):
        return render('/edit_child.mako')

    def render_list(self):
        return render('/list.mako')

    def show_children(self, id):
        c.id = id
        try:
            c.parent = model.get(self.table, id)
        except TypeError:
            c.parent = self.table()

        c.child = request.params['child']
        c.children = getattr(c.parent, c.child)
        c.child_details = self.children[c.child]
        return render('/show_children.mako')


class AJAXController(TableController):

    def __init__(self):
        self._init_custom()

    def _init_custom(self):
        pass


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_'
          ]