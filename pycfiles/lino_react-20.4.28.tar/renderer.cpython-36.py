# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luc/work/react/lino_react/react/renderer.py
# Compiled at: 2020-04-04 10:21:09
# Size of source mod 2**32: 23099 bytes
from __future__ import unicode_literals
from builtins import str
import six
from cgi import escape
from os import path
from django.conf import settings
from django.db import models
from django.utils.text import format_lazy
from django.utils import translation
from lino.core import constants as ext_requests
from lino.core.renderer import add_user_language, JsRenderer, HtmlRenderer
from lino.core.renderer_mixins import JsCacheRenderer
from lino.core.menus import Menu, MenuItem
from lino.core import constants
from lino.core import choicelists
from lino.core.gfks import ContentType
from lino.modlib.extjs.ext_renderer import ExtRenderer
from lino.core.actions import ShowEmptyTable, ShowDetail, ShowInsert, ShowTable, SubmitDetail, SubmitInsert, Action
from lino.core.boundaction import BoundAction
from lino.core.choicelists import ChoiceListMeta
from lino.core.actors import Actor
from lino.core.layouts import LayoutHandle
from lino.core.elems import LayoutElement, ComboFieldElement, SimpleRemoteComboFieldElement
from lino.core import kernel
from etgen.html import E
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, obj2dict
from lino.modlib.users.utils import get_user_profile, with_user_profile
from inspect import isclass
from .icons import REACT_ICON_MAPPING

def find(itter, target, key=None):
    """Returns the index of an element in a callable which can be use a key function"""
    if not key == None:
        if not callable(key):
            raise AssertionError("key shold be a function that takes the itter's item and returns that wanted matched item")
    for i, x in enumerate(itter):
        if key:
            x = key(x)
        if x == target:
            return i
    else:
        return -1


class Renderer(JsRenderer, JsCacheRenderer):
    __doc__ = '.\n        An JS renderer that uses the react Javascript framework.\n    '
    is_interactive = True
    can_auth = True
    lino_web_template = 'react/linoweb.json'
    file_type = '.json'
    hide_dashboard_items = True

    def __init__(self, plugin):
        super(JsRenderer, self).__init__(plugin)
        JsCacheRenderer.__init__(self)
        jsgen.register_converter(self.py2js_converter)

    def write_lino_js(self, f):
        """

        :param f: File object
        :return: 1
        """
        self.serialise_js_code = True
        choicelists_data = {ID:[{'value':py2js(c[0]).strip('"'),  'text':py2js(c[1]).strip('"')} for c in cl.get_choices()] for ID, cl in kernel.CHOICELISTS.items()}
        actions = set()
        for rpt in self.actors_list:
            for ba in rpt.get_actions():
                if ba.action not in actions:
                    actions.add(ba.action)

        f.write(py2js(dict(actions={a.action_name:a for a in actions},
          menu=(settings.SITE.get_site_menu(get_user_profile())),
          choicelists=choicelists_data,
          suggestors=(list(settings.SITE.plugins.memo.parser.suggesters.keys()))),
          compact=(not settings.SITE.is_demo_site)))
        self.serialise_js_code = False
        return 1

    def reload_js(self):
        return 'window.App.dashboard.reload();'

    def get_request_url(self, ar, *args, **kw):
        """Used for turn requests into urls"""
        if ar.actor.__name__ == 'Main':
            return (self.plugin.build_plain_url)(*args, **kw)
        else:
            st = ar.get_status()
            kw.update(st['base_params'])
            add_user_language(kw, ar)
            if ar.offset is not None:
                kw.setdefault(ext_requests.URL_PARAM_START, ar.offset)
            if ar.limit is not None:
                kw.setdefault(ext_requests.URL_PARAM_LIMIT, ar.limit)
            if ar.order_by is not None:
                sc = ar.order_by[0]
                if sc.startswith('-'):
                    sc = sc[1:]
                    kw.setdefault(ext_requests.URL_PARAM_SORTDIR, 'DESC')
                kw.setdefault(ext_requests.URL_PARAM_SORT, sc)
            return (self.plugin.build_plain_url)(
 ar.actor.app_label, ar.actor.__name__, *args, **kw)

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        if len(label) == 1:
            label = '\xa0{}\xa0'.format(label)
        if ba.action.parameters and not ba.action.no_params_window:
            st = self.get_action_status(ar, ba, obj)
            return (self.window_action_button)(
             ar, ba, st, label, **kw)
        else:
            if ba.action.opens_a_window:
                st = ar.get_status()
                if obj is not None:
                    st.update(record_id=(obj.pk))
                return (self.window_action_button)(ar, ba, st, label, **kw)
            return (self.row_action_button)(obj, ar, ba, label, **kw)

    def action_call_on_instance(self, obj, ar, ba, request_kwargs={}, **status):
        """Note that `ba.actor` may differ from `ar.actor` when defined on a
        different actor. Remember e.g. the "Must read eID card" action
        button in eid_info of newcomers.NewClients (20140422).

        :obj:  The database object
        :ar:   The action request
        :ba:  The bound action
        :request_kwargs: keyword arguments to forwarded to the child action request

        Any kwyword other arguments are forwarded to :meth:`ar2js`.

        """
        if ar is None:
            sar = (ba.request)(**request_kwargs)
        else:
            sar = (ar.spawn)(ba, **request_kwargs)
        return (self.ar2js)(sar, obj, **status)

    def get_action_params(self, ar, ba, obj, **kw):
        if ba.action.parameters:
            fv = ba.action.params_layout.params_store.pv2list(ar, ar.action_param_values)
            kw[constants.URL_PARAM_FIELD_VALUES] = fv
        return kw

    def get_action_icon(self, action):
        """
        Uses an internal mapping for icon names to convert existing icons into react-usable.
        :param action:
        :return: str: a icon name for either prime-react or icon8
        """
        icon = action.react_icon_name or action.icon_name
        react_icon = REACT_ICON_MAPPING.get(icon, None)
        if react_icon is None:
            return
        else:
            return 'pi %s' % react_icon

    def ar2js(self, ar, obj, **status):
        """Implements :meth:`lino.core.renderer.HtmlRenderer.ar2js`.

        """
        rp = ar.requesting_panel
        ba = ar.bound_action
        params = {}
        if ba.action.is_window_action():
            status.update(self.get_action_status(ar, ba, obj))
            params.update(status)
        params.update(self.get_action_params(ar, ba, obj))
        params.update(status)
        js_obj = {'rp':rp, 
         'an':ba.action.action_name, 
         'onMain':ar.is_on_main_actor, 
         'actorId':ba.actor.actor_id, 
         'status':params}
        if hasattr(obj, 'pk'):
            js_obj['sr'] = obj.pk
        else:
            if isinstance(obj, list):
                js_obj['sr'] = obj
        return 'window.App.runAction(%s)' % py2js(js_obj)

    def py2js_converter(self, v):
        """
        Additional converting logic for serializing Python values to json.
        """
        if v is settings.SITE.LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        else:
            if isinstance(v, choicelists.Choice):
                return v.value
            elif isinstance(v, models.Model):
                return v.pk
            else:
                if isinstance(v, Exception):
                    return str(v)
                elif isinstance(v, Menu):
                    if v.parent is None:
                        return v.items
                    else:
                        return dict(text=(v.label), menu=dict(items=(v.items)))
                else:
                    if isinstance(v, MenuItem):
                        if v.instance is not None:
                            h = self.instance_handler(None, v.instance, None)
                            assert h is not None
                            js = '%s' % h
                            return self.handler_item(v, h, None)
                        else:
                            if v.bound_action is not None:
                                if v.params:
                                    ar = (v.bound_action.request)(**v.params)
                                    js = self.request_handler(ar)
                                else:
                                    js = self.action_call(None, v.bound_action, {})
                                return self.handler_item(v, js, v.help_text)
                            if v.javascript is not None:
                                js = '%s' % v.javascript
                                return self.handler_item(v, js, v.help_text)
                            if v.href is not None:
                                url = v.href
                            else:
                                return v.label
                                if v.parent.parent is None:
                                    return dict(xtype='button',
                                      text=(v.label),
                                      handler=(js_code("function() { Lino.load_url('%s'); }" % url)))
                                else:
                                    return dict(text=(v.label), href=url)
                            if issubclass(v.__class__, LayoutElement):
                                result = dict(label=(v.get_label()), repr=(repr(v)),
                                  react_name=(v.__class__.__name__))
                                if hasattr(v, 'elements'):
                                    result['items'] = [e for e in v.elements if e.get_view_permission(get_user_profile())]
                                result.update(obj2dict(v, ' fields_index fields_index_hidden editable vertical hpad is_fieldset name width preferred_width                                      hidden value hflex vflex'))
                                if hasattr(v, 'actor'):
                                    result.update(obj2dict(v.actor, 'actor_id'))
                                if hasattr(v, 'get_field_options'):
                                    result.update(field_options=(v.get_field_options()))
                                return result
                        if isinstance(v, LayoutHandle):
                            return dict(main=(v.main), window_size=(v.layout.window_size))
                    else:
                        if isinstance(v, Action):
                            result = dict(an=(v.action_name), label=(v.get_label()),
                              window_action=(v.is_window_action()),
                              http_method=(v.http_method))
                            if v.preprocessor:
                                result['preprocessor'] = v.preprocessor
                            if v.combo_group:
                                result['combo_group'] = v.combo_group
                            if v.select_rows:
                                result['select_rows'] = v.select_rows
                            if v.submit_form_data:
                                result['submit_form_data'] = True
                            if v.button_text:
                                result['button_text'] = v.button_text
                            icon = self.get_action_icon(v)
                            if icon:
                                result['icon'] = icon
                            return result
                        if isinstance(v, BoundAction):
                            result = dict(an=(v.action.action_name), window_layout=(v.get_layout_handel()))
                            if v.action.window_type:
                                tba = []
                                combo_group = None
                                for ba in v.actor.get_toolbar_actions(v.action):
                                    if ba.action.combo_group == combo_group:
                                        if combo_group is not None:
                                            previous = tba.pop()
                                            if not isinstance(previous, list):
                                                previous = [
                                                 previous]
                                            previous.append(ba.action.action_name)
                                            tba.append(previous)
                                    else:
                                        tba.append(ba.action.action_name)
                                        combo_group = ba.action.combo_group

                                result['toolbarActions'] = tba
                            return result
                    if isclass(v):
                        if issubclass(v, Actor):
                            result = dict(id=(v.actor_id), ba=(v._actions_dict),
                              label=(v.get_actor_label()),
                              slave=(bool(v.master)),
                              editable=(v.editable))
                            if hasattr(v.get_handle(), 'get_columns'):
                                result['col'] = v.get_handle().get_columns()
                                index_mod = 0
                                for c in result['col']:
                                    c.fields_index = find((v.get_handle().store.list_fields), (c.field.name), key=(lambda f: f.name)) + index_mod
                                    if isinstance(c, ComboFieldElement) and not isinstance(c, SimpleRemoteComboFieldElement):
                                        c.fields_index_hidden = c.fields_index + 1
                                        index_mod += 1

                            result.update(obj2dict(v.get_handle().store, 'pk_index'))
                            result.update(obj2dict(v, 'preview_limit use_detail_param_panel use_detail_params_value hide_top_toolbar use_detail_params_value react_responsive react_big_search '))
                            chooser_dict = getattr(v.model, '_choosers_dict', {})
                            if chooser_dict:
                                result.update(chooser_dict={fn:[cf.name for cf in c.context_fields] for fn, c in chooser_dict.items()})
                            if settings.SITE.is_installed('contenttypes'):
                                if getattr(v, 'model', None) is not None:
                                    if hasattr(v.model, '_meta'):
                                        result.update(content_type=(ContentType.objects.get_for_model(v.model).pk))
                            for a in 'detail_action insert_action default_action'.split(' '):
                                if hasattr(v, a) and getattr(v, a) is not None:
                                    result.update({a: getattr(v, a).action.action_name})

                            if v.params_layout is not None:
                                result.update(pv_layout=(v.params_layout.get_layout_handle()),
                                  pv_fields=[f.name for f in v.params_layout.params_store.param_fields])
                            return result
                if isinstance(v, js_code):
                    if getattr(self, 'serialise_js_code', False):
                        return str(v.s)
            return v

    def goto_instance(self, ar, obj, detail_action=None, **kw):
        """Ask the client to display a :term:`detail window` on the given
        record. The client might ignore this if Lino does not know a
        detail window.

        This calls :meth:`obj.get_detail_action
        <lino.core.model.Model.get_detail_action>`.

        """
        js = self.instance_handler(ar, obj, detail_action)
        kw.update(eval_js=js)
        (ar.set_response)(**kw)

    def handler_item(self, mi, handler, help_text):
        """"""
        d = dict(text=(mi.label), handler=handler)
        if mi.bound_action:
            if mi.bound_action.action.icon_name:
                d.update(iconCls=('x-tbar-' + mi.bound_action.action.icon_name))
        if settings.SITE.use_quicktips:
            if help_text:
                d.update(toolTip=help_text)
        return d

    def request_handler(self, ar, *args, **kw):
        """ Generates js string for action button calls.
        """
        st = (ar.get_status)(**kw)
        return self.action_call(ar, ar.bound_action, st)

    def instance_handler(self, ar, obj, ba):
        return super(Renderer, self).instance_handler(ar, obj, ba)

    def action_call(self, request, bound_action, status):
        a = bound_action.action
        actorId, an = bound_action.full_name().rsplit('.', 1)
        if request:
            if request.subst_user:
                status[constants.URL_PARAM_SUBST_USER] = request.subst_user
        if isinstance(a, ShowEmptyTable):
            status.update(record_id=(-99998))
        rp = None if request is None else request.requesting_panel
        if not status:
            status = {}
        return 'window.App.runAction(%s)' % py2js(dict(an=an,
          actorId=actorId,
          status=status,
          rp=rp))

    def js2url(self, js):
        if not js:
            return
        else:
            if not isinstance(js, six.string_types):
                js = str(js)
            js = escape(js)
            return 'javascript:' + js

    def show_menu(self, ar, mnu, level=1):
        """
        Render the given menu as an HTML element.
        Used for writing test cases.
        """
        if not isinstance(mnu, Menu):
            if not isinstance(mnu, MenuItem):
                raise AssertionError
            else:
                if mnu.bound_action:
                    sar = (mnu.bound_action.actor.request)(action=mnu.bound_action, 
                     user=ar.user, 
                     subst_user=ar.subst_user, requesting_panel=ar.requesting_panel, 
                     renderer=self, **mnu.params)
                    url = sar.get_request_url()
                else:
                    url = mnu.href
                assert mnu.label is not None
                if url is None:
                    return E.p()
            return E.li(E.a((mnu.label), href=url, tabindex='-1'))
        else:
            items = [self.show_menu(ar, mi, level + 1) for mi in mnu.items]
            if level == 1:
                return (E.ul)(*items, **{'class': 'nav navbar-nav'})
            if mnu.label is None:
                raise Exception('%s has no label' % mnu)
            if level == 2:
                cl = 'dropdown'
                menu_title = (E.a)(
 str(mnu.label), (E.b)(*(' ', ), **{'class': 'caret'}), href='#', data_toggle='dropdown', **{'class': 'dropdown-toggle'})
            else:
                if level == 3:
                    menu_title = E.a((str(mnu.label)), href='#')
                    cl = 'dropdown-submenu'
                else:
                    raise Exception('Menu with more than three levels')
            return (E.li)(
             menu_title, 
             (E.ul)(*items, **{'class': 'dropdown-menu'}), **{'class': cl})

    def add_help_text(self, kw, help_text, title, datasource, fieldname):
        if settings.SITE.use_quicktips:
            if settings.SITE.show_internal_field_names:
                ttt = '(%s.%s) ' % (datasource, fieldname)
            else:
                ttt = ''
            if help_text:
                ttt = format_lazy('{}{}', ttt, help_text)
            if ttt:
                kw.update(quicktip=('(%s,%s)' % (title,
                 ttt)))

    def lino_js_parts_chunked(self, actorId):
        """ Like lino_js_parts, but for actor_level data"""
        user_type = get_user_profile()
        filename = 'Lino_' + actorId + '_'
        file_type = self.lino_web_template.rsplit('.')[(-1)]
        if user_type is not None:
            filename += user_type.value + '_'
        filename += translation.get_language() + '.' + file_type
        return ('cache', file_type, filename)

    def build_js_cache(self, force):
        self.serialise_js_code = True
        for actor in self.actors_list:
            fn = (path.join)(*self.lino_js_parts_chunked(actor.actor_id))

            def write(f):
                f.write(py2js(actor))

            settings.SITE.kernel.make_cache_file(fn, write, force)

        self.serialise_js_code = False
        return super(Renderer, self).build_js_cache(force)