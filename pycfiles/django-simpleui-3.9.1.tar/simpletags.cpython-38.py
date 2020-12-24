# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/panjing/dev/simpleui_demo/simpleui/templatetags/simpletags.py
# Compiled at: 2019-12-24 03:02:47
# Size of source mod 2**32: 12445 bytes
import base64, json, os, platform, sys, time, django, simpleui
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = template.Library()
PY_VER = sys.version[0]
import django.utils.translation as _
if PY_VER != '2':
    from importlib import reload

def unicode_to_str(u):
    if PY_VER != '2':
        return u
    return u.encode()


class LazyEncoder(DjangoJSONEncoder):
    __doc__ = '\n        解决json __proxy__ 问题\n    '

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


@register.simple_tag(takes_context=True)
def context_test(context):
    print(context)


@register.simple_tag(takes_context=True)
def load_dates(context):
    data = {}
    cl = context.get('cl')
    if cl.has_filters:
        for spec in cl.filter_specs:
            if not hasattr(spec, 'field'):
                pass
            else:
                field = spec.field
                field_type = None
                if isinstance(field, models.DateTimeField):
                    field_type = 'datetime'
                else:
                    if isinstance(field, models.DateField):
                        field_type = 'date'
                    else:
                        if isinstance(field, models.TimeField):
                            field_type = 'time'
                if field_type:
                    data[spec.field_path] = field_type

    context['date_field'] = data
    return '<script type="text/javascript">var searchDates={}</script>'.format(json.dumps(data, cls=LazyEncoder))


@register.filter
def has_filter(spec):
    return hasattr(spec, 'parameter_name')


@register.filter
def get_date_type(spec):
    field = spec.field
    field_type = ''
    if isinstance(field, models.DateTimeField):
        field_type = 'datetime'
    else:
        if isinstance(field, models.DateField):
            field_type = 'date'
        else:
            if isinstance(field, models.TimeField):
                field_type = 'time'
    return field_type


@register.filter
def test(obj):
    print(obj)
    return ''


@register.filter
def to_str(obj):
    return str(obj)


@register.filter
def date_to_json(obj):
    return json.dumps((obj.date_params), cls=LazyEncoder)


@register.simple_tag(takes_context=True)
def home_page(context):
    """
    处理首页，通过设置判断打开的是默认页还是自定义的页面
    :return:
    """
    home = __get_config('SIMPLEUI_HOME_PAGE')
    if home:
        context['home'] = home
    title = __get_config('SIMPLEUI_HOME_TITLE')
    if not title:
        title = '首页'
    icon = __get_config('SIMPLEUI_HOME_ICON')
    if not icon:
        icon = 'el-icon-menu'
    context['title'] = title
    context['icon'] = icon
    return ''


def __get_config(name):
    from django.conf import settings
    value = os.environ.get(name, getattr(settings, name, None))
    return value


@register.filter
def get_config(key):
    return __get_config(key)


@register.simple_tag
def get_version():
    return simpleui.get_version()


@register.simple_tag
def get_app_info():
    dict = {'version': simpleui.get_version()}
    return format_table(dict)


def format_table(dict):
    html = '<table class="simpleui-table"><tbody>'
    for key in dict:
        html += '<tr><th>{}</th><td>{}</td></tr>'.format(key, dict.get(key))
    else:
        html += '</tbody></table>'
        return format_html(html)


@register.simple_tag(takes_context=True)
def menus(context, _get_config=None):
    data = []
    if not _get_config:
        _get_config = get_config
    config = _get_config('SIMPLEUI_CONFIG')
    if not config:
        config = {}
    if config.get('dynamic', False) is True:
        config = _import_reload(_get_config('DJANGO_SETTINGS_MODULE')).SIMPLEUI_CONFIG
    app_list = context.get('app_list')
    for app in app_list:
        _models = [{'name':m.get('name'), 
         'icon':get_icon(m.get('object_name'), unicode_to_str(m.get('name'))), 
         'url':m.get('admin_url'), 
         'addUrl':m.get('add_url'), 
         'breadcrumbs':[
          {'name':app.get('name'), 
           'icon':get_icon(app.get('app_label'), app.get('name'))},
          {'name':m.get('name'), 
           'icon':get_icon(m.get('object_name'), unicode_to_str(m.get('name')))}]} for m in app.get('models')] if app.get('models') else []
        module = {'name':app.get('name'), 
         'icon':get_icon(app.get('app_label'), app.get('name')), 
         'models':_models}
        data.append(module)
    else:
        key = 'system_keep'
        if config:
            if 'menus' in config:
                if key in config and config.get(key) != False:
                    temp = config.get('menus')
                    for i in temp:
                        if 'models' in i:
                            for k in i.get('models'):
                                k['breadcrumbs'] = [
                                 {'name':i.get('name'),  'icon':i.get('icon')},
                                 {'name':k.get('name'), 
                                  'icon':k.get('icon')}]

                        else:
                            i['breadcrumbs'] = [{'name':i.get('name'), 
                              'icon':i.get('icon')}]
                        data.append(i)

                else:
                    data = config.get('menus')
        if config.get('menu_display') is not None:
            display_data = list()
            for _app in data:
                if _app['name'] not in config.get('menu_display'):
                    pass
                else:
                    _app['_weight'] = config.get('menu_display').index(_app['name'])
                    display_data.append(_app)
            else:
                display_data.sort(key=(lambda x: x['_weight']))
                data = display_data

        eid = 1000
        for i in data:
            eid += 1
            i['eid'] = eid
            if 'models' in i:
                for k in i.get('models'):
                    eid += 1
                    k['eid'] = eid

            return '<script type="text/javascript">var menus={}</script>'.format(json.dumps(data, cls=LazyEncoder))


def get_icon(obj, name=None):
    temp = get_config_icon(name)
    if temp != '':
        return temp
    _dict = {'auth':'fas fa-shield-alt', 
     'User':'far fa-user', 
     'Group':'fas fa-users-cog'}
    temp = _dict.get(obj)
    if not temp:
        _default = __get_config('SIMPLEUI_DEFAULT_ICON')
        if _default is None or _default:
            return 'far fa-file'
        return ''
    return temp


def get_config_icon(name):
    _config_icon = __get_config('SIMPLEUI_ICON')
    if _config_icon is None:
        return ''
    if name in _config_icon:
        return _config_icon.get(name)
    return ''


@register.simple_tag(takes_context=True)
def load_message(context):
    messages = context.get('messages')
    array = [dict(msg=(msg.message), tag=(msg.tags)) for msg in messages] if messages else []
    return '<script id="out_message" type="text/javascript">var messages={}</script>'.format(json.dumps(array, cls=LazyEncoder))


@register.simple_tag(takes_context=True)
def context_to_json(context):
    json_str = '{}'
    return mark_safe(json_str)


@register.simple_tag()
def get_language():
    from django.conf import settings
    return settings.LANGUAGE_CODE.lower()


@register.filter
def get_language_code(val):
    from django.conf import settings
    return settings.LANGUAGE_CODE.lower()


def get_analysis_config():
    val = __get_config('SIMPLEUI_ANALYSIS')
    if not val:
        if val == False:
            return False
    return True


@register.simple_tag(takes_context=True)
def load_analysis--- This code section failed: ---

 L. 335         0  SETUP_FINALLY       202  'to 202'

 L. 336         2  LOAD_GLOBAL              get_analysis_config
                4  CALL_FUNCTION_0       0  ''
                6  LOAD_CONST               False
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 337        12  POP_BLOCK        
               14  LOAD_STR                 ''
               16  RETURN_VALUE     
             18_0  COME_FROM            10  '10'

 L. 340        18  LOAD_STR                 'simpleui_'
               20  LOAD_GLOBAL              time
               22  LOAD_METHOD              strftime
               24  LOAD_STR                 '%Y%m%d'
               26  LOAD_GLOBAL              time
               28  LOAD_METHOD              localtime
               30  CALL_METHOD_0         0  ''
               32  CALL_METHOD_2         2  ''
               34  BINARY_ADD       
               36  STORE_FAST               'key'

 L. 342        38  LOAD_FAST                'key'
               40  LOAD_FAST                'context'
               42  LOAD_ATTR                request
               44  LOAD_ATTR                session
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    56  'to 56'

 L. 343        50  POP_BLOCK        
               52  LOAD_STR                 ''
               54  RETURN_VALUE     
             56_0  COME_FROM            48  '48'

 L. 345        56  LOAD_STR                 ''
               58  STORE_FAST               'b64'

 L. 347        60  LOAD_GLOBAL              platform
               62  LOAD_METHOD              node
               64  CALL_METHOD_0         0  ''

 L. 348        66  LOAD_GLOBAL              platform
               68  LOAD_METHOD              platform
               70  CALL_METHOD_0         0  ''

 L. 349        72  LOAD_GLOBAL              platform
               74  LOAD_METHOD              python_version
               76  CALL_METHOD_0         0  ''

 L. 350        78  LOAD_GLOBAL              django
               80  LOAD_METHOD              get_version
               82  CALL_METHOD_0         0  ''

 L. 351        84  LOAD_GLOBAL              simpleui
               86  LOAD_METHOD              get_version
               88  CALL_METHOD_0         0  ''

 L. 346        90  LOAD_CONST               ('n', 'o', 'p', 'd', 's')
               92  BUILD_CONST_KEY_MAP_5     5 
               94  STORE_FAST               'j'

 L. 353        96  LOAD_STR                 'theme_name'
               98  LOAD_FAST                'context'
              100  LOAD_ATTR                request
              102  LOAD_ATTR                COOKIES
              104  COMPARE_OP               in
              106  POP_JUMP_IF_FALSE   126  'to 126'

 L. 354       108  LOAD_FAST                'context'
              110  LOAD_ATTR                request
              112  LOAD_ATTR                COOKIES
              114  LOAD_STR                 'theme_name'
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'j'
              120  LOAD_STR                 't'
              122  STORE_SUBSCR     
              124  JUMP_FORWARD        134  'to 134'
            126_0  COME_FROM           106  '106'

 L. 356       126  LOAD_STR                 'Default'
              128  LOAD_FAST                'j'
              130  LOAD_STR                 't'
              132  STORE_SUBSCR     
            134_0  COME_FROM           124  '124'

 L. 358       134  LOAD_GLOBAL              base64
              136  LOAD_METHOD              b64encode
              138  LOAD_GLOBAL              str
              140  LOAD_FAST                'j'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_METHOD              encode
              146  LOAD_STR                 'utf-8'
              148  CALL_METHOD_1         1  ''
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'b64'

 L. 360       154  LOAD_STR                 '//simpleui.88cto.com/analysis'
              156  STORE_FAST               'url'

 L. 361       158  LOAD_FAST                'b64'
              160  LOAD_METHOD              decode
              162  LOAD_STR                 'utf-8'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'b64'

 L. 362       168  LOAD_STR                 '<script async type="text/javascript" src="{}/{}"></script>'
              170  LOAD_METHOD              format
              172  LOAD_FAST                'url'
              174  LOAD_FAST                'b64'
              176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'html'

 L. 363       180  LOAD_CONST               True
              182  LOAD_FAST                'context'
              184  LOAD_ATTR                request
              186  LOAD_ATTR                session
              188  LOAD_FAST                'key'
              190  STORE_SUBSCR     

 L. 365       192  LOAD_GLOBAL              mark_safe
              194  LOAD_FAST                'html'
              196  CALL_FUNCTION_1       1  ''
              198  POP_BLOCK        
              200  RETURN_VALUE     
            202_0  COME_FROM_FINALLY     0  '0'

 L. 366       202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 367       208  POP_EXCEPT       
              210  LOAD_STR                 ''
              212  RETURN_VALUE     
              214  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 14


@register.simple_tag(takes_context=True)
def custom_button(context):
    admin = context.get('cl').model_admin
    data = {}
    actions = admin.get_actions(context.request)
    if actions:
        id = 0
        for name in actions:
            values = {}
            fun = actions.get(name)[0]
            for key, v in fun.__dict__.items():
                if key != '__len__':
                    if key != '__wrapped__':
                        values[key] = v
                    values['eid'] = id
                    id += 1
                    data[name] = values

    return json.dumps(data, cls=LazyEncoder)


from django.db.models.fields.related import ForeignKey

def get_model_fields(model, base=None):
    list = []
    fields = model._meta.fields
    for f in fields:
        label = f.name
        if hasattr(f, 'verbose_name'):
            label = getattr(f, 'verbose_name')
        if isinstance(label, Promise):
            label = str(label)
        if base:
            list.append(('{}__{}'.format(base, f.name), label))
        else:
            list.append((f.name, label))
    else:
        return list


@register.simple_tag(takes_context=True)
def search_placeholder--- This code section failed: ---

 L. 418         0  LOAD_FAST                'context'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'cl'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'cl'

 L. 421        10  LOAD_GLOBAL              get_model_fields
               12  LOAD_FAST                'cl'
               14  LOAD_ATTR                model
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'fields'

 L. 423        20  LOAD_FAST                'cl'
               22  LOAD_ATTR                model
               24  LOAD_ATTR                _meta
               26  LOAD_ATTR                fields
               28  GET_ITER         
             30_0  COME_FROM            42  '42'
               30  FOR_ITER             66  'to 66'
               32  STORE_FAST               'f'

 L. 424        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'f'
               38  LOAD_GLOBAL              ForeignKey
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    30  'to 30'

 L. 425        44  LOAD_FAST                'fields'
               46  LOAD_METHOD              extend
               48  LOAD_GLOBAL              get_model_fields
               50  LOAD_FAST                'f'
               52  LOAD_ATTR                related_model
               54  LOAD_FAST                'f'
               56  LOAD_ATTR                name
               58  CALL_FUNCTION_2       2  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  JUMP_BACK            30  'to 30'

 L. 427        66  BUILD_LIST_0          0 
               68  STORE_FAST               'verboses'

 L. 429        70  LOAD_FAST                'cl'
               72  LOAD_ATTR                search_fields
               74  GET_ITER         
               76  FOR_ITER            122  'to 122'
               78  STORE_FAST               's'

 L. 430        80  LOAD_FAST                'fields'
               82  GET_ITER         
             84_0  COME_FROM            98  '98'
               84  FOR_ITER            120  'to 120'
               86  STORE_FAST               'f'

 L. 431        88  LOAD_FAST                'f'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_FAST                's'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE    84  'to 84'

 L. 432       100  LOAD_FAST                'verboses'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'f'
              106  LOAD_CONST               1
              108  BINARY_SUBSCR    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 433       114  POP_TOP          
              116  CONTINUE             76  'to 76'
              118  JUMP_BACK            84  'to 84'
              120  JUMP_BACK            76  'to 76'

 L. 435       122  LOAD_STR                 ','
              124  LOAD_METHOD              join
              126  LOAD_FAST                'verboses'
              128  CALL_METHOD_1         1  ''
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 116


def _import_reload(_modules):
    _obj = __import__(_modules, fromlist=(_modules.split('.')))
    reload(_obj)
    return _obj


@register.simple_tag
def get_tz_suffix():
    tz = __get_config('USE_TZ')
    if tz:
        return '+08:00'
    return ''


@register.simple_tag
def simple_version():
    return simpleui.get_version()


@register.simple_tag(takes_context=True)
def get_model_url(context):
    opts = context.get('opts')
    key = 'admin:{}_{}_changelist'.format(opts.app_label, opts.model_name)
    return reverse(key)


@register.simple_tag
def has_enable_admindoc():
    from django.conf import settings
    apps = settings.INSTALLED_APPS
    return 'django.contrib.admindocs' in apps


@register.simple_tag(takes_context=True)
def has_admindoc_page(context):
    if hasattr(context, 'template_name'):
        return context.template_name.find('admin_doc') == 0
    return False


@register.simple_tag
def get_boolean_choices():
    return (
     (
      'True', _('Yes')),
     (
      'False', _('No')))