# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/twitter/content_plugin.py
# Compiled at: 2012-10-12 07:02:39
import os, pickle, time
from urllib2 import URLError
from coils.core import *

class TwitterContentPlugin(ContentPlugin):
    __entity__ = [
     'Contact', 'Enterprise']
    __pluginName__ = 'org.opengroupware.coils.twitter'
    __cache_dir = None

    def __repr__(cls):
        return 'TwitterContentPlugin'

    def __init__(self, ctx):
        ContentPlugin.__init__(self, ctx)
        if TwitterContentPlugin.__cache_dir is None:
            TwitterContentPlugin.__cache_dir = 'cache/plugin.twitter'
        return

    def get_extra_content(self, entity):
        prop = self._ctx.property_manager.get_property(entity, 'http://whitemice.consulting.com/coils.twitter', 'screenName')
        if prop is None:
            return {}
        else:
            screen_name = str(prop.get_value())
            timeline = self.get_cached_timeline(screen_name)
            if timeline is None:
                self.log.debug(('Retrieving timeline for Twitter user {0}.').format(screen_name))
                try:
                    timeline = self._ctx.run_command('twitter::get-user-timeline', screenname=screen_name)
                except URLError, e:
                    self.log.error('Unable to communicate with Twitter.')
                    self.log.exception(e)
                    timeline = []
                else:
                    self.cache_timeline(screen_name, timeline)
            else:
                self.log.debug(('Using cached timeline for Twitter user {0}').format(screen_name))
            self.log.debug(('Twitter content plugin found {0} elements').format(len(timeline)))
            return {'screenName': screen_name, 'timeLine': timeline}

    def get_cached_timeline(self, screen_name):
        filename = ('{0}/{1}.timeline.cpd').format(TwitterContentPlugin.__cache_dir, screen_name)
        blob = BLOBManager.Open(filename, 'rb', encoding='binary')
        if blob is not None:
            timeline = pickle.load(blob)
            BLOBManager.Close(blob)
            t = time.time()
            if t - timeline.get('timestamp') < 3600:
                return timeline.get('timeline')
            BLOBManager.Delete(filename)
        return

    def cache_timeline(self, screen_name, timeline):
        filename = ('{0}/{1}.timeline.cpd').format(TwitterContentPlugin.__cache_dir, screen_name)
        data = {'timestamp': time.time(), 'timeline': timeline}
        blob = BLOBManager.Create(filename, encoding='binary')
        pickle.dump(data, blob)
        BLOBManager.Close(blob)