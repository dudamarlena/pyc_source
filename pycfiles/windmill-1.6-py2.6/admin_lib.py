# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/bin/admin_lib.py
# Compiled at: 2011-02-09 04:10:54
import windmill, logging
from time import sleep
import os, sys
from datetime import datetime
from threading import Thread
import shutil, socket
from windmill.dep import functest
functest.configure()

def process_options(argv_list):
    """Process all the command line options"""
    import admin_options
    admin_options.process_module(admin_options)
    argv_list.pop(0)
    action = None
    for arg in argv_list:
        if arg.startswith('http://') or arg.startswith('https://'):
            windmill.settings['TEST_URL'] = arg
            functest.registry['url'] = arg
        elif arg.startswith('-'):
            options = arg.replace('-', '')
            for option in options:
                admin_options.flags_dict[option]()

        else:
            value = None
            if arg.find('=') is not -1:
                (name, value) = arg.split('=')
            else:
                name = arg
            if name in admin_options.options_dict:
                processor = admin_options.options_dict[name]
                if value is None:
                    processor()
                else:
                    processor(value)
            elif name in action_mapping:
                action = action_mapping[name]
            else:
                print name, 'is not a windmill argument. Sticking in functest registry.'
                if value is None:
                    value = True
                functest.registry[name] = value

    if action is None:
        return action_mapping['runserver']
    else:
        return action
        return


def setup_servers(console_level=logging.INFO):
    """Setup the server and return httpd and loggers"""
    windmill.is_active = True
    windmill.ide_is_awake = False
    if len(logging.getLogger().handlers) > 0:
        console_handler = logging.getLogger().handlers[0]
        console_handler.setLevel(console_level)
    httpd = windmill.server.wsgi.make_windmill_server()
    return httpd


def run_threaded(console_level=logging.INFO):
    """Run the server threaded."""
    httpd = setup_servers(console_level)
    httpd_thread = Thread(target=httpd.start)
    getattr(httpd_thread, 'setDaemon', lambda x: x)(True)
    httpd_thread.start()
    while not httpd.ready:
        sleep(0.25)

    return (httpd, httpd_thread)


def configure_global_settings(logging_on=True):
    """Configure that global settings for the current run"""
    if logging_on:
        logging.getLogger().setLevel(0)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
    if os.environ.has_key('WINDMILL_CONFIG_FILE'):
        local_settings = os.environ['WINDMILL_CONFIG_FILE']
    else:
        local_settings = None
    windmill.settings = windmill.conf.configure_settings(localSettings=local_settings)
    if 'controllers' not in windmill.settings:
        windmill.settings['controllers'] = []
    port = windmill.settings['SERVER_HTTP_PORT']
    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', port))
            s.close()
            port += 1
        except socket.error:
            break

    windmill.settings['SERVER_HTTP_PORT'] = port
    return windmill.settings


on_ide_awake = []

def setup():
    """Setup server and shell objects"""
    global shell_objects_dict
    shell_objects_dict = {}
    windmill.settings['shell_objects'] = shell_objects_dict
    assert not windmill.settings.get('setup_has_run', False)
    (httpd, httpd_thread) = run_threaded(windmill.settings['CONSOLE_LOG_LEVEL'])
    shell_objects_dict['httpd'] = httpd
    shell_objects_dict['httpd_thread'] = httpd_thread
    from windmill.bin import shell_objects
    if windmill.settings['CONTINUE_ON_FAILURE'] is not False:
        shell_objects.jsonrpc_client.add_json_command('{"method": "commands.setOptions", "params": {"stopOnFailure" : false}}')
    if windmill.settings['EXTENSIONS_DIR'] is not None:
        shell_objects.load_extensions_dir(windmill.settings['EXTENSIONS_DIR'])
    if windmill.settings['RUN_TEST'] is not None:
        shell_objects.run_test(windmill.settings['RUN_TEST'])
    if windmill.settings['LOAD_TEST'] is not None:
        shell_objects.load_test(windmill.settings['LOAD_TEST'])
    if windmill.settings['JAVASCRIPT_TEST_DIR']:
        shell_objects.run_js_tests(windmill.settings['JAVASCRIPT_TEST_DIR'], windmill.settings['JAVASCRIPT_TEST_FILTER'], windmill.settings['JAVASCRIPT_TEST_PHASE'])
    browser = [ setting for setting in windmill.settings.keys() if setting.startswith('START_') if windmill.settings[setting] is True
              ]
    import shell_objects
    if len(browser) is 1:
        shell_objects_dict['browser'] = getattr(shell_objects, browser[0].lower())()
    for attribute in dir(shell_objects):
        shell_objects_dict[attribute] = getattr(shell_objects, attribute)

    shell_objects_dict['setup_has_run'] = True
    return shell_objects_dict


def teardown(shell_objects):
    """Teardown the server, threads, and open browsers."""
    if windmill.is_active:
        windmill.is_active = False
        shell_objects.get('clear_queue', lambda : None)()
        for controller in windmill.settings['controllers']:
            controller.stop()
            del controller

        if windmill.settings['START_FIREFOX'] and windmill.settings['MOZILLA_CREATE_NEW_PROFILE']:
            try:
                shutil.rmtree(windmill.settings['MOZILLA_PROFILE'])
            except WindowsError:
                pass

        for directory in windmill.teardown_directories:
            if os.path.isdir(directory):
                shutil.rmtree(directory)

        shell_objects['httpd'].stop()


def runserver_action(shell_objects):
    """Run the server in the foreground with the options given to the command line"""
    try:
        if 'runserver' in sys.argv or len(windmill.settings['controllers']) is 0:
            print 'Server running...'
        if windmill.settings['EXIT_ON_DONE'] and not windmill.settings['JAVASCRIPT_TEST_DIR']:
            while windmill.block_exit or len(shell_objects['httpd'].controller_queue.queue) is not 0 or len(shell_objects['httpd'].test_resolution_suite.unresolved) is not 0:
                sleep(0.25)

        elif windmill.settings['RUN_TEST']:
            windmill.runserver_running = True
            while windmill.runserver_running:
                sleep(0.25)

        else:
            windmill.runserver_running = True
            while windmill.runserver_running:
                sleep(0.25)

            teardown(shell_objects)
        if windmill.test_has_failed:
            sys.exit(1)
    except KeyboardInterrupt:
        teardown(shell_objects)
        sys.exit(1)


def shell_action(shell_objects):
    """Start the windmill shell environment"""
    windmill.in_shell = True
    try:
        assert not windmill.settings['USECODE']
        from IPython.Shell import IPShellEmbed
        ipshell = IPShellEmbed()
        ipshell(local_ns=shell_objects)
    except:
        import code
        code.interact(local=shell_objects)

    teardown(shell_objects)


def start_windmill():
    """Start windmill and return shell_objects"""
    configure_global_settings()
    shell_objects = setup()
    return shell_objects


def command_line_startup():
    """Command line startup"""
    windmill.stdout, windmill.stdin = sys.stdout, sys.stdin
    configure_global_settings()
    action = process_options(sys.argv)
    shell_objects = setup()
    action(shell_objects)


action_mapping = {'shell': shell_action, 
   'runserver': runserver_action, 
   'run_service': runserver_action}