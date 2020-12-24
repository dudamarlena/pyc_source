# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/bin/shell_objects.py
# Compiled at: 2011-01-13 02:54:30
import windmill
from windmill.dep import uuid
import os, logging, re
from time import sleep
from threading import Thread
from windmill.dep import functest
logger = logging.getLogger(__name__)
jsonrpc_client = windmill.tools.make_jsonrpc_client()
xmlrpc_client = windmill.tools.make_xmlrpc_client()
from StringIO import StringIO
test_stream_object = StringIO()

def clear_queue():
    """Clear the Service's current queue of tests/actions."""
    try:
        xmlrpc_client.clear_queue()
    except Exception, e:
        logger.debug(type(e).__name__ + ':' + e.message)


windmill.settings['controllers'] = []

def start_firefox():
    """Start the Firefox web browser configured for windmill"""
    controller = windmill.browser.get_firefox_controller()
    controller.start()
    logger.info(str(controller.command))
    windmill.settings['controllers'].append(controller)
    return controller


def start_ie():
    """Start the Internet Explorer web browser configured for windmill"""
    controller = windmill.browser.get_ie_controller()
    controller.start()
    windmill.settings['controllers'].append(controller)
    return controller


def start_safari():
    """Start the Safari web browser configured for windmill"""
    controller = windmill.browser.get_safari_controller()
    controller.start()
    windmill.settings['controllers'].append(controller)
    return controller


def start_chrome():
    """Start the Chrome web browser configured for windmill"""
    controller = windmill.browser.get_chrome_controller()
    controller.start()
    windmill.settings['controllers'].append(controller)
    return controller


def load_json_test_file(filename):
    """Run the json test files passed to this function"""
    test_strings = re.compile('\\{.*\\}').findall(open(filename, 'r').read())
    jsonrpc_client.start_suite(filename.split(os.path.sep)[(-1)])
    jsonrpc_client.run_json_tests(test_strings)
    jsonrpc_client.stop_suite()
    logger.info('Added tests from %s' % filename)


def show_queue():
    """Return the current queue of tests and commands in windmill"""
    return windmill.settings['shell_objects']['httpd'].controller_queue.queue


def do_test(filename, load=False, threaded=True):
    """Run or load the test file or directory passed to this function"""
    windmill.block_exit = True
    if ',' in filename:
        for f in filename.split(','):
            do_test(f, load)

        return
    else:

        def json_test(filename):
            if os.path.isfile(filename) and not os.path.isfile(os.path.join(os.path.dirname(filename), '__init__.py')):
                return (None, load_json_test_file(filename))
            else:
                return (
                 os.path.dirname(os.path.abspath(filename)), [ f for f in filename.split('/') if f != '' ][(-1)].split('.')[0])
                return

        def python_test(filename):
            return (
             os.path.abspath(filename), '')

        def directory_test(filename):
            return (os.path.abspath(filename), '')

        (module_name, filter_string) = {'py': python_test, 
           'json': json_test}.get(filename.split('.')[(-1)], directory_test)(filename)

        def run_functest():
            if load:
                functest.registry['browser_debugging'] = 'True'
                xmlrpc_client.add_command({'method': 'commands.setOptions', 
                   'params': {'runTests': False, 'priority': 'normal'}})
            functest.global_settings.test_filter = filter_string
            from windmill.authoring import WindmillFunctestRunner, post_collector
            functest.collector.Collector.post_collection_functions.append(post_collector)
            functest.run_framework(test_args=[module_name], test_runner=WindmillFunctestRunner())
            if load:
                xmlrpc_client.add_command({'method': 'commands.setOptions', 
                   'params': {'runTests': True, 'priority': 'normal'}})
            windmill.block_exit = False

        if module_name is not None and threaded:
            run_thread = Thread(target=run_functest)
            getattr(run_thread, 'setDaemon', lambda x: x)(True)
            from windmill.bin import admin_lib
            admin_lib.on_ide_awake.append(run_thread.start)
            return run_thread
        if module_name:
            x = []
            from windmill.bin import admin_lib
            admin_lib.on_ide_awake.append(lambda : x.append(True))
            while len(x) is 0:
                sleep(1)

            run_functest()
        return


run_test = lambda filename: do_test(filename, load=False, threaded=True)
run_test.__name__ = 'run_test'
run_test.__doc__ = 'Run the test file or directory passed to this function'
load_test = lambda filename: do_test(filename, load=True, threaded=True)
load_test.__name__ = 'load_test'
load_test.__doc__ = 'Load the test file or directory passed to this function'

def run_js_tests(js_dir, test_filter=None, phase=None):
    import windmill
    from windmill.dep import wsgi_fileserver
    from windmill.server import wsgi
    windmill.js_framework_active = True
    js_dir = os.path.abspath(os.path.expanduser(js_dir))
    WSGIFileServerApplication = wsgi_fileserver.WSGIFileServerApplication
    application = WSGIFileServerApplication(root_path=os.path.abspath(js_dir), mount_point='/windmill-jstest/')
    wsgi.add_namespace('windmill-jstest', application)
    base_url = '/windmill-jstest'
    js_files = []

    def parse_files(x, directory, files):
        if not os.path.split(directory)[(-1)].startswith('.'):
            additional_dir = directory.replace(js_dir, '')
            js_files.extend([ additional_dir + '/' + f for f in files if f.endswith('.js') ])

    os.path.walk(js_dir, parse_files, 'x')
    kwargs = {}
    kwargs['files'] = [ base_url + f for f in js_files ]
    kwargs['uuid'] = str(uuid.uuid1())
    if test_filter:
        kwargs['filter'] = test_filter
    if phase:
        kwargs['phase'] = phase
    xmlrpc_client.add_command({'method': 'commands.setOptions', 
       'params': {'scriptAppendOnly': windmill.settings['SCRIPT_APPEND_ONLY']}})
    xmlrpc_client.add_command({'method': 'commands.jsTests', 'params': kwargs})


def load_extensions_dir(dirname):
    """Mount the directory and send all javascript file links to the IDE in order to execute those test urls under the jsUnit framework"""
    from windmill.dep import wsgi_fileserver
    WSGIFileServerApplication = wsgi_fileserver.WSGIFileServerApplication
    application = WSGIFileServerApplication(root_path=os.path.abspath(dirname), mount_point='/windmill-extentions/')
    from windmill.server import wsgi
    wsgi.add_namespace('windmill-extentions', application)
    base_url = windmill.settings['TEST_URL'] + '/windmill-extentions'
    js_files = []

    def parse_files(x, directory, files):
        if not os.path.split(directory)[(-1)].startswith('.'):
            additional_dir = directory.replace(dirname, '')
            js_files.extend([ additional_dir + '/' + f for f in files if f.endswith('.js') ])

    os.path.walk(dirname, parse_files, 'x')
    xmlrpc_client.add_command({'method': 'commands.loadExtensions', 
       'params': {'extensions': [ base_url + f for f in js_files ]}})