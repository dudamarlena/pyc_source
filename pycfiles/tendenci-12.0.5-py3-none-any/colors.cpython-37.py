# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/event_logs/colors.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 2185 bytes
import django.core.cache as cache
from django.conf import settings
non_model_event_logs = {'rss':{'feed_base':('630000', '00FF00'), 
  'global_feed':('630500', '00FF00'), 
  'article_feed':('630543', '00FF33'), 
  'news_feed':('630530', '00FFCC'), 
  'pages_feed':('630560', '33FF99'), 
  'jobs_feed':('630525', '00FF99')}, 
 'homepage':{'view': ('100000', '17ABB9')}}

def generate_colors():
    """Create the event id to color dict so we won't
    have to iterate over the apps in the event registry
    for every event id.
    """
    from tendenci.apps.registry.sites import site
    d = {}
    apps = site.get_registered_apps().all_apps
    for app in apps:
        if 'event_logs' in app:
            for model in app['event_logs']:
                for event in app['event_logs'][model]:
                    log_id = app['event_logs'][model][event][0]
                    color = app['event_logs'][model][event][1]
                    d[log_id] = color

    return d


def generate_base_colors():
    """Crete the event id to color dict for event logs that
    are not associated with any model or registry.
    """
    d = {}
    for model in non_model_event_logs:
        for event in non_model_event_logs[model]:
            log_id = non_model_event_logs[model][event][0]
            color = non_model_event_logs[model][event][1]
            d[log_id] = color

    return d


def cache_colors(colors):
    keys = [
     settings.CACHE_PRE_KEY, 'event_log_colors']
    key = '.'.join(keys)
    cache.set(key, colors)


def get_color(event_id):
    """Gets the hex color of an event log based on the event id
    get_color('id')
    """
    keys = [
     settings.CACHE_PRE_KEY, 'event_log_colors']
    key = '.'.join(keys)
    colors = cache.get(key)
    if not colors:
        colors = generate_colors()
        colors.update(generate_base_colors())
        cache_colors(colors)
    if event_id in colors:
        print(event_id)
        return colors[event_id]
    return '17ABB9'
    return ''