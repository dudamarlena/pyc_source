# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/util.py
# Compiled at: 2017-06-09 03:03:53
import re, colander, inspect
from kotti.resources import get_root
from kotti.views.slots import objectevent_listeners
from kotti.views.slots import slot_events
from kotti_controlpanel.config import SETTINGS, CONTROL_PANEL_LINKS
from kotti_controlpanel.resources import ControlPanel
from kotti_controlpanel.resources import ModuleSettings
from kotti_controlpanel.resources import SettingObj

def slugify(text, delim='-'):
    """Generates an slightly worse ASCII-only slug."""
    return re.sub('[^a-zA-Z\\d:]', text.lower(), '-')


def get_setting(name, default=None, modname=None):
    """ Return the setting for a given module.

    :param name:        Setting Name
    :param default:     Default value to be return if the setting not found.
    :param modname:     Name of module it is found in. By default, the function
                        will use the calling module, i.e. the module that is calling this function.
    :returns:           Value store in the setting
    """
    if modname is None:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]
    if not name.startswith(modname):
        name = ('{0}-{1}').format(modname, name)
    settings = get_settings()
    if name in settings:
        return settings[name]
    else:
        return default


def set_setting(name, val, modname=None):
    if modname is None and '-' not in name:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]
    if modname and not name.startswith(modname):
        name = ('{0}-{1}').format(modname, name)
    settings = get_settings()
    if type(val) == set:
        val = list(val)
    settings[name] = val
    return


def get_settings():
    root = get_root()
    if 'kotti_controlpanel' not in root.annotations:
        root.annotations['kotti_controlpanel'] = {}
    return root.annotations['kotti_controlpanel']


def get_links(controlpanel_id):
    cpi = slugify(controlpanel_id)
    return CONTROL_PANEL_LINKS.get(cpi, [])


def add_links(controlpanel_id, *links):
    cpi = slugify(controlpanel_id)
    clinks = CONTROL_PANEL_LINKS.get(cpi, [])
    for link in links:
        clinks.append(link)

    CONTROL_PANEL_LINKS[cpi] = clinks


def add_settings(mod_settings, links=None):
    """Get a dictionary and translate this into an object structure.
    """
    settings = get_settings()
    module_settings = ModuleSettings(**mod_settings)
    if module_settings.module is None:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]
        module_settings.module = modname
    if module_settings.settings:
        for setting in module_settings.settings:
            setting_obj = SettingObj(**setting)
            if setting_obj.name is None:
                raise ValueError('A setting has to have a name.')
            if setting_obj.title is None:
                raise ValueError('A setting has to have a title.')
            setting_obj.module = module_settings.module
            default = None
            if 'default' in setting:
                default = setting['default']
            if setting_obj.field_name not in settings:
                settings[setting_obj.field_name] = default
            module_settings.settings_objs.append(setting_obj)

    if module_settings.schema_factory:
        schema = module_settings.schema_factory()
        for child in schema.children:
            field_name = child.name
            if not field_name.startswith(module_settings.module):
                field_name = '%s-%s' % (module_settings.module, child.name)
            if field_name not in settings:
                value = None
                if child.default is not colander.null:
                    value = child.default
                settings[field_name] = value

    mod_slug = slugify(module_settings.name)
    if type(links) == list:
        add_links(mod_slug, *links)
    module_settings.slug_id = mod_slug
    SETTINGS[mod_slug] = module_settings
    return


def remove_from_slots(widget, slot=None):
    """Check all slots if a widget is already set and remove it
       from the listener.
    """
    for slot_event in slot_events:
        if slot is not None:
            if slot != slot_event.name:
                continue
        try:
            listener = objectevent_listeners[(slot_event, None)]
        except TypeError:
            listener = None

        if listener is not None:
            for func in listener:
                for closure in func.func_closure:
                    if closure.cell_contents == widget:
                        listener.remove(func)
                        break

    return


def show_in_context(setting, context):
    """Check if the the item should be shown in the given context."""
    show = False
    if setting == 'everywhere':
        show = True
    elif setting == 'only on root':
        show = context == get_root()
    elif setting == 'not on root':
        show = context != get_root()
    return show