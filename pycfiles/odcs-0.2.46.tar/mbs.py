# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/mbs.py
# Compiled at: 2019-01-03 01:37:10
from functools import wraps
import json, responses
from six.moves.urllib.parse import urlparse, parse_qs
from odcs.server import conf
import gi
gi.require_version('Modulemd', '1.0')
from gi.repository import Modulemd

def make_module(name, stream, version, requires={}, mdversion=1, context=None):
    mmd = Modulemd.Module()
    mmd.set_mdversion(mdversion)
    mmd.set_name(name)
    mmd.set_stream(stream)
    mmd.set_version(version)
    mmd.set_context(context or '00000000')
    mmd.set_summary('foo')
    mmd.set_description('foo')
    licenses = Modulemd.SimpleSet()
    licenses.add('GPL')
    mmd.set_module_licenses(licenses)
    if mdversion == 1:
        mmd.set_requires(requires)
    else:
        deps = Modulemd.Dependencies()
        for req_name, req_stream in requires.items():
            deps.add_requires_single(req_name, req_stream)

        mmd.set_dependencies((deps,))
    return {'name': name, 
       'stream': stream, 
       'version': str(version), 
       'context': context or '00000000', 
       'modulemd': mmd.dumps()}


TEST_MBS_MODULES_MMDv1 = [
 make_module('moduleA', 'f26', 20170809000000, {'moduleB': 'f26'}),
 make_module('moduleA', 'f26', 20170805000000, {'moduleB': 'f26'}),
 make_module('moduleB', 'f26', 20170808000000, {'moduleC': 'f26', 'moduleD': 'f26'}),
 make_module('moduleB', 'f27', 2017081000000, {'moduleC': 'f27'}),
 make_module('moduleC', 'f26', 20170807000000, {'moduleD': 'f26'}),
 make_module('moduleD', 'f26', 20170806000000),
 make_module('testmodule', 'master', 20170515074418),
 make_module('testmodule', 'master', 20170515074419)]
TEST_MBS_MODULES_MMDv2 = [
 make_module('moduleA', 'f26', 20170809000000, {'moduleB': 'f26'}, 2),
 make_module('moduleA', 'f26', 20170805000000, {'moduleB': 'f26'}, 2),
 make_module('moduleB', 'f26', 20170808000000, {'moduleC': 'f26', 'moduleD': 'f26'}, 2),
 make_module('moduleB', 'f27', 2017081000000, {'moduleC': 'f27'}, 2),
 make_module('moduleC', 'f26', 20170807000000, {'moduleD': 'f26'}, 2),
 make_module('moduleD', 'f26', 20170806000000, {}, 2),
 make_module('testmodule', 'master', 20170515074418, {}, 2),
 make_module('testmodule', 'master', 20170515074419, {}, 2),
 make_module('parent', 'master', 1, {}, 2, context='a'),
 make_module('parent', 'master', 1, {}, 2, context='b'),
 make_module('testcontexts', 'master', 1, {'parent': 'master'}, 2, context='a'),
 make_module('testcontexts', 'master', 1, {'parent': 'master'}, 2, context='b')]

def mock_mbs(mdversion=2):
    """
    Decorator that sets up a test environment so that calls to the PDC to look up
    modules are redirected to return results from the TEST_MODULES array above.
    """

    def wrapper(f):

        @wraps(f)
        def wrapped(*args, **kwargs):

            def handle_module_builds(request):
                query = parse_qs(urlparse(request.url).query)
                nsvc = query['nsvc'][0]
                nsvc_parts = nsvc.split(':')
                nsvc_keys = ['name', 'stream', 'version', 'context']
                nsvc_dict = {}
                for key, part in zip(nsvc_keys, nsvc_parts):
                    nsvc_dict[key] = part

                if mdversion == 1:
                    modules = TEST_MBS_MODULES_MMDv1
                else:
                    modules = TEST_MBS_MODULES_MMDv2
                body = {'items': [], 'meta': {'total': 0}}
                for module in modules:
                    skip = False
                    for key in nsvc_keys:
                        if key in nsvc_dict and nsvc_dict[key] != module[key]:
                            skip = True
                            break

                    if skip:
                        continue
                    body['items'].append(module)

                body['meta']['total'] = len(body['items'])
                return (200, {}, json.dumps(body))

            responses.add_callback(responses.GET, conf.mbs_url + '/1/module-builds/', content_type='application/json', callback=handle_module_builds)
            return f(*args, **kwargs)

        return responses.activate(wrapped)

    return wrapper