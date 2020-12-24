# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/tasks.py
# Compiled at: 2013-03-06 03:28:33
from cms.models import CMSPlugin
from goscale import utils
from celery.task import task
from celery.execute import send_task

@task(name='goscale.tasks.update_goscale_plugins')
def update_goscale_plugins():
    for plugin in utils.get_plugins():
        print 'Sending GoScale plugin for updating: %s (%s)' % (plugin, plugin.id)
        send_task('goscale.tasks.update_goscale_plugin_posts', [plugin.id])


@task(name='goscale.tasks.update_goscale_plugin_posts')
def update_goscale_plugin_posts(plugin_id):
    instance, count = utils.update_plugin(plugin_id)
    if instance:
        print 'Updated %d posts for %s (%d)' % (count, instance, plugin_id)
    else:
        print "Couldn't update posts for plugin_id: %d" % plugin_id
    return instance