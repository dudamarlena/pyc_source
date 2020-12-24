# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/call.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...compat import text_type
from ... import pilot

class Call(SubCommand):
    """Call moya code in project context"""
    help = b'call moya code in project context'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'elementref', metavar=b'ELEMENTREF', help=b'element to call')
        parser.add_argument(dest=b'params', metavar=b'PARAMETER', nargs=b'*', help=b'parameter(s) for call, e.g. moya call app#macro 3.14 foo=bar')
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
        return parser

    def run(self):
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True)
        archive = application.archive
        context = application.get_context()
        application.populate_context(context)
        pilot.context = context

        def make_param(v):
            if v == b'True':
                return True
            else:
                if v == b'False':
                    return False
                if v == b'None':
                    return None
                if v.isdigit():
                    return int(v)
                try:
                    return float(v)
                except ValueError:
                    pass

                return v

        positional_args = []
        keyword_args = {}
        for param in args.params:
            if b'=' in param:
                k, v = param.split(b'=', 1)
                k = k.strip()
                v = v.strip()
                keyword_args[k] = make_param(v)
            else:
                positional_args.append(make_param(param))

        ret = archive.call(args.elementref, context, None, *positional_args, **keyword_args)
        application.finalize(context)
        if ret is not None:
            self.console(text_type(ret)).nl()
        return