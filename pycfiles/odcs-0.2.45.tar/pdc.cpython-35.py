# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/pdc.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 4040 bytes
from functools import wraps
import json, modulemd, responses
from six.moves.urllib.parse import urlparse, parse_qs
from odcs.server import conf

def make_module(name, stream, version, requires={}):
    mmd = modulemd.ModuleMetadata()
    mmd.name = name
    mmd.stream = stream
    mmd.version = version
    mmd.requires.update(requires)
    return {'variant_id': name, 
     'variant_version': stream, 
     'variant_release': str(version), 
     'variant_uid': name + '-' + stream + '-' + str(version), 
     'modulemd': mmd.dumps()}


TEST_PDC_MODULES = [
 make_module('moduleA', 'f26', 20170809000000, {'moduleB': 'f26'}),
 make_module('moduleA', 'f26', 20170805000000, {'moduleB': 'f26'}),
 make_module('moduleB', 'f26', 20170808000000, {'moduleC': 'f26', 'moduleD': 'f26'}),
 make_module('moduleB', 'f27', 2017081000000, {'moduleC': 'f27'}),
 make_module('moduleC', 'f26', 20170807000000, {'moduleD': 'f26'}),
 make_module('moduleD', 'f26', 20170806000000),
 make_module('testmodule', 'master', 20170515074418),
 make_module('testmodule', 'master', 20170515074419)]

def mock_pdc(f):
    """
    Decorator that sets up a test environment so that calls to the PDC to look up
    modules are redirected to return results from the TEST_MODULES array above.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):

        def handle_unreleasedvariants(request):
            query = parse_qs(urlparse(request.url).query)
            variant_id = query['variant_id']
            variant_version = query['variant_version']
            variant_release = query.get('variant_release', None)
            body = []
            for module in TEST_PDC_MODULES:
                if module['variant_id'] not in variant_id:
                    pass
                else:
                    if module['variant_version'] not in variant_version:
                        pass
                    else:
                        if variant_release is not None and module['variant_release'] not in variant_release:
                            pass
                        else:
                            fields = query.get('fields', None)
                            if fields is not None:
                                return_module = {}
                                for field in fields:
                                    return_module[field] = module[field]

                            else:
                                return_module = module
                            body.append(return_module)

            return (
             200, {}, json.dumps(body))

        responses.add_callback(responses.GET, conf.pdc_url + '/unreleasedvariants/', content_type='application/json', callback=handle_unreleasedvariants)
        return f(*args, **kwargs)

    return responses.activate(wrapped)