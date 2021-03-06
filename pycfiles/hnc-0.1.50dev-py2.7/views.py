# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hnc\apps\static_content\views.py
# Compiled at: 2013-10-21 08:25:51
import polib
from pyramid.path import AssetResolver
from hnc.apiclient import Mapping, TextField, ListField, DictField
from hnc.apiclient.cached import CachedLoader
from hnc.forms.formfields import BaseForm, MultipleFormField, IMPORTANT, StringField, TextareaField, GRID_BS3, HtmlAttrs, REQUIRED
from hnc.forms.handlers import FormHandler
from hnc.forms.layout import BS3_NCOL
from hnc.forms.messages import GenericSuccessMessage

class KeyValueModel(Mapping):
    key = TextField()
    value = TextField()


class ContentModel(Mapping):
    Static = ListField(DictField(KeyValueModel))


class StaticContentLoader(object):

    def __init__(self, request, cache, debug):
        self.content = cache.get(request)
        self.debug = debug
        self.cache = cache
        super(StaticContentLoader, self).__init__()

    def refresh(self, request):
        self.cache.refresh(request)

    def __call__(self, key, **kwargs):
        return self.content.get(key, key) or ''

    def pluralize(self, singular, plural, num):
        if num == 1:
            return singular.format(num=num)
        return plural.format(num=num)


def add_content(dictionary_factory, instance_name):
    """
        dictionary_factory: receives request as parameter, returns a dictionary of all static content, the result gets cached, so this is the interface to some persistent storage
    """
    cache = CachedLoader(dictionary_factory, ('STATIC_CONTENT:{}').format(instance_name))

    def add_content_impl(event):
        request = event.request
        request._ = StaticContentLoader(request, cache, request.globals.is_debug)
        request.pluralize = request._.pluralize

    return add_content_impl


CONTENT_FIELDS = [
 MultipleFormField('values', fields=[
  BS3_NCOL(StringField('key', 'Key', REQUIRED), TextareaField('value', 'Full HTML', attrs=HtmlAttrs(important=True, rows=8)))], add_more_link_label='Add More Fields')]

def ContentCreationViewFactory(SetStaticContentProc, fwd_url):

    class ContentCreateForm(BaseForm):
        label = 'Create Content'
        width_class = 'col-lg-12'
        grid = GRID_BS3
        fields = CONTENT_FIELDS

        @classmethod
        def cancel_url(cls, request):
            return request.rld_url()

        @classmethod
        def on_success(cls, request, values):
            data = request.context.contentsMap
            data.update({v['key']:v['value'] for v in values['values']})
            contents = SetStaticContentProc(request, {'Static': [ {'key': k, 'value': v} for k, v in data.items() ]})
            request._.refresh(request)
            request.session.flash(GenericSuccessMessage('Content created successfully!'), 'generic_messages')
            return {'success': True, 'redirect': fwd_url(request)}

    class ContentCreateHandler(FormHandler):

        def __call__(self):
            return super(ContentCreateHandler, self).__call__()

        form = ContentCreateForm

        def pre_fill_values(self, request, result):
            if 'key' in request.GET:
                result['values'][self.form.id]['values'] = [ {'key': k} for k in request.GET.getall('key') ]
            return super(ContentCreateHandler, self).pre_fill_values(request, result)

    return ContentCreateHandler


def ContentEditViewFactory(SetStaticContentProc, fwd_url):

    class ContentEditForm(BaseForm):
        label = 'Edit Content'
        grid = GRID_BS3
        fields = [TextareaField('value', 'Full HTML', attrs=HtmlAttrs(important=True, rows=8), if_empty='')]

        @classmethod
        def cancel_url(cls, request):
            return request.fwd_url(request.context.__parent__)

        @classmethod
        def on_success(cls, request, values):
            data = request.context.contentsMap
            data[request.context.content.key] = values['value']
            contents = SetStaticContentProc(request, {'Static': [ {'key': k, 'value': v} for k, v in data.items() ]})
            request._.refresh(request)
            request.session.flash(GenericSuccessMessage('Content updated successfully!'), 'generic_messages')
            return {'success': True, 'redirect': fwd_url(request)}

    class ContentEditHandler(FormHandler):
        form = ContentEditForm

        def pre_fill_values(self, request, result):
            result['values'][self.form.id] = request.context.content.unwrap(sparse=True)
            return super(ContentEditHandler, self).pre_fill_values(request, result)

    return ContentEditHandler


def delete_view_factory(SetStaticContentProc, fwd_url):

    def delete_view_inner(context, request):
        data = request.context.contentsMap
        data.pop(request.context.content.key, None)
        contents = SetStaticContentProc(request, {'Static': [ {'key': k, 'value': v} for k, v in data.items() ]})
        request._.refresh(request)
        request.session.flash(GenericSuccessMessage('Content updated successfully!'), 'generic_messages')
        request.fwd_raw(fwd_url(request))
        return

    return delete_view_inner


def generic(ctxt, req):
    return {}


class ViewSpec(object):

    def __init__(self, label, view, **kwargs):
        self.label = label
        self.view = view
        self.kwargs = kwargs
        super(ViewSpec, self).__init__()

    @property
    def args(self):
        return [self.view]


def set_up_content_mgmt_app(config, potfile_asset_spec, dictionary_factory):
    """
        provide static content backend for hnc projects, text-keys are provided by babel message extractors into the domain.pot file, this is usually located in the root/locale folder

        config: is pyramid configuration instance
        potfile_asset_spec: describing path to potfile message catalog
        render_ctxt_info: is a function with request as sole parameter, when returns truthy value, additional HTML comments are rendered before the output text, normally only admins are interested in this
    """

    def add_renderer_variables(event):
        if event['renderer_name'] != 'json':
            request = event['request']
            event.update({'_': request._})
        return event

    a = AssetResolver()
    asset_path = a.resolve(potfile_asset_spec)
    if not asset_path.exists():
        raise ValueError(('POTFILE does not exist in specified location: {}').format(potfile_asset_spec))
    config.add_subscriber(add_content(dictionary_factory, potfile_asset_spec), 'pyramid.events.ContextFound')
    config.add_subscriber(add_renderer_variables, 'pyramid.events.BeforeRender')
    return lambda : polib.pofile(asset_path.abspath())