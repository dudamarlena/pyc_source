# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/busmon/busmon/widgets.py
# Compiled at: 2012-10-08 11:22:10
import tg, time, memcache
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import moksha.wsgi.widgets.api.live, tw2.core as twc, tw2.d3
from tw2.jquery import jquery_js
global_width = 485

class BusmonWidget(moksha.wsgi.widgets.api.live.LiveWidget):
    resources = [
     twc.JSLink(link='javascript/busmon.js', resources=[jquery_js])]
    backend = tg.config.get('moksha.livesocket.backend', 'websocket')


class TopicsBarChart(tw2.d3.BarChart, BusmonWidget):
    id = 'topics-bar-chart'
    topic = '*'
    onmessage = "busmon.filter(function() {\n        if (! json['topic']) { return; }\n        topic = json['topic'].split('.').slice(3, 5).join('.')\n        tw2.d3.util.bump_value('${id}', topic, 1);\n    }, json)"
    data = OrderedDict()
    padding = [
     30, 10, 10, global_width / 2]
    width = global_width
    height = 225
    interval = 2000

    def prepare(self):
        super(TopicsBarChart, self).prepare()
        self.add_call(twc.js_function('tw2.d3.bar.schedule_halflife')(self.attrs['id'], 60000, 1000, 0.001))


class MessagesTimeSeries(tw2.d3.TimeSeriesChart, BusmonWidget):
    topic = '*'
    onmessage = "busmon.filter(function() {\n        tw2.store['${id}'].value++;\n    }, json)"
    width = global_width
    height = 150

    def prepare(self):
        self.n = int(tg.config.get('busmon.memcached.n'))
        self.duration = int(tg.config.get('busmon.memcached.duration'))
        head = int(time.time() * 1000 / self.duration) % self.n
        indices = range(self.n)
        indices = indices[head:] + indices[:head]
        keys = [ 'busmon_count_%i' % i for i in indices ]
        servers = tg.config.get('busmon.memcached.servers').split(',')
        mc = memcache.Client(servers)
        self.data = map(lambda key: mc.get(key) or 0, keys)
        super(MessagesTimeSeries, self).prepare()


class ColorizedMessagesWidget(BusmonWidget):
    id = 'colorized-messages'
    template = 'mako:busmon.templates.colorized_messages'
    resources = BusmonWidget.resources + [
     twc.CSSLink(link='css/monokai.css'),
     twc.JSLink(link='javascript/markup.js')]
    css_class = 'hll'
    topic = '*'
    onmessage = '\n    busmon.filter(function() {\n        var container = $(\'#${id}\');\n        if ( container.children().size() > 4 ) {\n            container.children().first().slideUp(100, function () {\n                $(this).remove();\n                container.append("<pre>"+markup(json)+"</pre>");\n            });\n        } else {\n            container.append("<pre>"+markup(json)+"</pre>");\n        }\n    }, json)'