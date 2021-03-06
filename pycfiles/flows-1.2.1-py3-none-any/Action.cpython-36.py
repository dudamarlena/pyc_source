# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\mastromatteo\Progetti\flows\build\lib\flows\Actions\Action.py
# Compiled at: 2017-03-23 07:19:01
# Size of source mod 2**32: 8099 bytes
"""
Action.py
Action superclasses
-------------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
import gc, glob, importlib, importlib.util, os, site, sys, time, threading
from threading import Thread
from flows import Global

class ActionInput:
    __doc__ = '\n    Standard input for every action in flows\n    '
    sender = ''
    receiver = ''
    message = ''
    file_system_event = None

    def __init__(self, event, message, sender, receiver='*'):
        super().__init__()
        self.message = message
        self.file_system_event = event
        self.sender = sender
        self.receiver = receiver


class Action(Thread):
    __doc__ = '\n    Generic abstract class that should be subclassed to create\n    custom action classes.\n    '
    type = ''
    name = ''
    _instance_lock = threading.Lock()
    configuration = None
    context = None
    socket = None
    is_running = True
    monitored_input = None
    my_action_input = None
    python_files = []

    def __init__(self, name, configuration, managed_input):
        super().__init__()
        self.daemon = True
        self.monitored_input = managed_input
        self.configuration = configuration
        self.name = name
        self.on_init()
        self.start()

    def on_init(self):
        """
        Initialization of the action, code to be executed before start
        """
        pass

    def on_cycle(self):
        """
        Main cycle of the action, code to be executed before the start of each cycle
        """
        pass

    def on_input_received(self, action_input=None):
        """
        Fire the current action
        """
        pass

    def on_stop(self):
        """
        Code to be executed before end
        """
        pass

    def send_output(self, output):
        """
        Send an output to the socket
        """
        Global.MESSAGE_DISPATCHER.send_message(output)

    def send_message(self, output):
        """
        Send a message to the socket
        """
        file_system_event = None
        if self.my_action_input:
            file_system_event = self.my_action_input.file_system_event or None
        output_action = ActionInput(file_system_event, output, self.name, '*')
        Global.MESSAGE_DISPATCHER.send_message(output_action)

    def stop(self):
        """ Stop the current action """
        Global.LOGGER.debug(f"action {self.name} stopped")
        self.is_running = False
        self.on_stop()

    def run(self):
        """
        Start the action
        """
        Global.LOGGER.debug(f"action {self.name} is running")
        for tmp_monitored_input in self.monitored_input:
            sender = '*' + tmp_monitored_input + '*'
            Global.LOGGER.debug(f"action {self.name} is monitoring {sender}")

        while self.is_running:
            try:
                time.sleep(Global.CONFIG_MANAGER.sleep_interval)
                self.on_cycle()
            except Exception as exc:
                Global.LOGGER.error(f"error while running the action {self.name}: {str(exc)}")

    @classmethod
    def load_module(cls, module_name, module_filename):
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_filename)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
        except Exception as ex:
            Global.LOGGER.warn((f"{ex}"))
            Global.LOGGER.warn(f"an error occured while importing {module_name}, so the module will be skipped.")

    @classmethod
    def search_actions(cls):
        if len(Action.python_files) > 0:
            return Action.python_files
        else:
            Global.LOGGER.debug('searching for installed actions... it can takes a while')
            site_packages = site.getsitepackages()
            Global.LOGGER.debug(f"current path: {os.getcwd()}")
            Global.LOGGER.debug('looking inside the current directory')
            tmp_python_files_in_current_directory = glob.glob(f"{os.getcwd()}/*Action.py", recursive=False)
            Global.LOGGER.debug(f"found {len(tmp_python_files_in_current_directory)} actions in current directory")
            basenames = list(map(os.path.basename, tmp_python_files_in_current_directory))
            tmp_python_files_dict = dict(zip(basenames, tmp_python_files_in_current_directory))
            Global.LOGGER.debug('looking inside any ./Actions subdirectory')
            tmp_python_files_in_current_action_subdirectory = glob.glob(f"{os.getcwd()}/**/Actions/*Action.py", recursive=True)
            Global.LOGGER.debug(f"found {len(tmp_python_files_in_current_action_subdirectory)} actions in a ./Actions subdirectory")
            for action_file in tmp_python_files_in_current_action_subdirectory:
                action_filename = os.path.basename(action_file)
                if action_filename not in tmp_python_files_dict:
                    tmp_python_files_dict[action_filename] = action_file

            Global.LOGGER.debug('looking inside the Python environment')
            for my_site in site_packages:
                tmp_python_files_in_site_directory = glob.glob(f"{my_site}/**/Actions/*Action.py", recursive=True)
                Global.LOGGER.debug(f"found {len(tmp_python_files_in_site_directory)} actions in {my_site}")
                for action_file in tmp_python_files_in_site_directory:
                    action_filename = os.path.basename(action_file)
                    if action_filename not in tmp_python_files_dict:
                        tmp_python_files_dict[action_filename] = action_file

            action_files = tmp_python_files_dict.values()
            if len(action_files) > 0:
                Global.LOGGER.debug(f"{len(action_files)} actions found")
                if Global.CONFIG_MANAGER.tracing_mode:
                    actions_found = '\n'.join(action_files)
                    Global.LOGGER.debug(f"actions found: \n{actions_found}")
            else:
                Global.LOGGER.debug(f"no actions found on {my_site}")
            Action.python_files = action_files
            return action_files

    @classmethod
    def create_action_for_code(cls, action_code, name, configuration, managed_input):
        """
        Factory method to create an instance of an Action from an input code
        """
        Global.LOGGER.debug(f"creating action {name} for code {action_code}")
        Global.LOGGER.debug(f"configuration length: {len(configuration)}")
        Global.LOGGER.debug(f"input: {managed_input}")
        my_actions_file = Action.search_actions()
        for filename in my_actions_file:
            module_name = os.path.basename(os.path.normpath(filename))[:-3]
            context = {}
            Action.load_module(module_name, filename)
            for subclass in Action.__subclasses__():
                if subclass.type == action_code:
                    action_class = subclass
                    action = action_class(name, configuration, managed_input)
                    return action

            subclass = None
            gc.collect()