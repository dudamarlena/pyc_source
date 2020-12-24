# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/utils/jinja.py
# Compiled at: 2017-11-06 21:55:06
# Size of source mod 2**32: 1532 bytes
import traceback, datetime, json
from ramjet.settings import logger

def debug_wrapper(func):

    def wrapper(*args, **kw):
        logger.debug('debug_wrapper for args {}, kw {}'.format(args, kw))
        try:
            yield from func(*args, **kw)
        except Exception:
            self = args[0]
            err_msg = {'uri':self.request.uri, 
             'version':self.request.version, 
             'headers':self.request.headers, 
             'cookies':self.request.cookies}
            logger.error('{}\n-----\n{}'.format(json.dumps(err_msg, indent=4, sort_keys=True), traceback.format_exc()))
            raise

        if False:
            yield None

    return wrapper


class TemplateRendering:
    __doc__ = '\n    A simple class to hold methods for rendering templates.\n\n    Copied from\n        http://bibhas.in/blog/using-jinja2-as-the-template-engine-for-tornado-web-framework/\n    '
    _jinja_env = None
    _assets_env = None

    def render_template(self, template_name, **kw):
        if not self._jinja_env:
            self._jinja_env.filters.update({'utc2cst':lambda dt: dt + datetime.timedelta(hours=8), 
             'jstime2py':lambda ts: datetime.datetime.fromtimestamp(ts / 1000), 
             'time_format':lambda dt: datetime.datetime.strftime(dt, '%Y/%m/%d %H:%M:%S')})
        template = self._jinja_env.get_template(template_name)
        content = template.render(kw)
        return content