# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/api_get.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import json, re
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, CommandExit, Option, ParseError

class APIGet(Command):
    name = b'api-get'
    author = b'The Review Board Project'
    description = b'Retrieve raw API resource payloads.'
    args = b'<path> [--<query-arg>=<value> ...]'
    option_list = [
     Option(b'--pretty', action=b'store_true', dest=b'pretty_print', config_key=b'API_GET_PRETTY_PRINT', default=False, help=b'Pretty prints the resulting API payload.'),
     Command.server_options]

    def _dumps(self, payload):
        if self.options.pretty_print:
            return json.dumps(payload, sort_keys=True, indent=4)
        else:
            return json.dumps(payload)

    def main(self, path, *args):
        query_args = {}
        query_arg_re = re.compile(b'^--(?P<name>.*)=(?P<value>.*)$')
        for arg in args:
            m = query_arg_re.match(arg)
            if m:
                query_args[m.group(b'name')] = m.group(b'value')
            else:
                raise ParseError(b'Unexpected query argument %s' % arg)

        if self.options.server:
            server_url = self.options.server
        else:
            repository_info, tool = self.initialize_scm_tool()
            server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        try:
            if path.startswith(b'http://') or path.startswith(b'https://'):
                resource = api_client.get_url(path, **query_args)
            else:
                resource = api_client.get_path(path, **query_args)
        except APIError as e:
            if e.rsp:
                print(self._dumps(e.rsp))
                raise CommandExit(1)
            else:
                raise CommandError(b'Could not retrieve the requested resource: %s' % e)

        print(self._dumps(resource.rsp))