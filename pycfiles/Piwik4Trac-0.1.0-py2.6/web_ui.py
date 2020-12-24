# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tracext/piwik/web_ui.py
# Compiled at: 2012-05-02 14:27:07
from genshi.filters.transform import Transformer
from trac.config import Option
from trac.core import Component, implements
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import Chrome

class PiwikStreamFilter(Component):
    config = env = log = None
    implements(ITemplateStreamFilter)

    def filter_stream(self, req, method, filename, stream, data):
        if req.path_info.startswith('/admin'):
            return stream
        options = self.get_options()
        if not options.get('tracking_site'):
            self.log.debug('Plugin not configured, returning stream')
            return stream
        if not options.get('tracking_server'):
            self.log.debug('Plugin not configured, returning stream')
            return stream
        template = Chrome(self.env).load_template('piwik_analytics.html')
        data = template.generate(admin='TRAC_ADMIN' in req.perm, opt=options, base_url='http:\\/\\/%s' % req.environ.get('HTTP_HOST'))
        return stream | Transformer('body').append(data)

    def get_options(self):
        options = {}
        for option in [ option for option in Option.registry.values() if option.section == 'piwik'
                      ]:
            if option.name in ('admin_logging', 'authenticated_logging', 'outbound_link_tracking'):
                value = self.config.getbool('piwik', option.name, option.default)
                option.value = value
            elif option.name == 'extensions':
                value = self.config.get('piwik', option.name, option.default)
                option.value = ('|').join(val.strip() for val in value.split(','))
            else:
                value = self.config.get('piwik', option.name, option.default)
                option.value = value
            options[option.name] = option.value

        return options