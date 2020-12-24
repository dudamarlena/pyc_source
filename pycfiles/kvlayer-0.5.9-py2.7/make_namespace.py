# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/tests/make_namespace.py
# Compiled at: 2015-07-31 13:31:44
import logging, pytest, kvlayer, yakonfig
logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def namespace(request, namespace_string):

    def fin():
        logger.info('tearing down %s...', namespace_string)
        try:
            config = yakonfig.get_global_config('kvlayer')
            config['namespace'] = namespace_string
            client = kvlayer.client(config)
            client.delete_namespace()
            logger.info('finished tearing down %s.', namespace_string)
        except KeyError:
            logger.warn('%s not configured in this process; cannot guess config', namespace_string)
        except Exception as exc:
            logger.error('failed to tear down %s', namespace_string, exc_info=True)

    request.addfinalizer(fin)
    return namespace_string