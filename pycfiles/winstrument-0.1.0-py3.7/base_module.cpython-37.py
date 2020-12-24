# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\base_module.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 3369 bytes
import frida, sys, os, collections
from tabulate import tabulate
import toml
import winstrument.utils as utils
from winstrument.data.module_message import ModuleMessage

class BaseInstrumentation:
    modulename = 'base_module'

    def __init__(self, session, path, db, settings={}):
        self._settings = settings
        self._session = session
        self._db = db
        self._script = None
        self._processpath = path
        self._output = []
        self._messages = []

    def write_message(self, message):
        """
        Writes the specified message dict to the database and stores in it in _messages as a ModuleMessage data object
        Params:
            message - dict of key, value pairs
        No return
         """
        modulemessage = ModuleMessage(self.modulename, self._processpath, message)
        self._db.write_message(modulemessage)
        self._messages.append(modulemessage)

    def get_name(self):
        return self.modulename

    def load_script(self):
        """
        Load the associated JS file for this moudle into the Frida session, then hook any callbacks etc, and start the script
        """
        with open(os.path.join(os.path.dirname(__file__), 'modules', 'js', f"{self.modulename}.js"), 'r') as (scriptfile):
            self._script = self._session.create_script(scriptfile.read())
        self.register_callbacks()
        self._script.load()
        self.on_load()

    def get_output(self):
        """
        Returns a list of ModuleMessage objects
        Each object represents a single message sent by the module
        """
        return self._messages

    def on_load(self):
        """
        Callback called during load_script after the injected JS is running inside the target. Override in subclasses if desired.
        """
        pass

    def on_message(self, message, data):
        """
        Generic handler for frida's 'message' event.
        Simply saves the raw JSON payload recived as a ModuleMessage object.
        """
        if message['type'] == 'error':
            print(f"Error: {message}")
        else:
            self.write_message(message['payload'])

    def register_callbacks(self):
        """
        Callback called in load_script before the JS is injeted in the target.
        Hook frida events like 'message', 'detached' etc here as needed
        """
        self._script.on('message', self.on_message)

    def on_finish(self):
        """
        Callback called after the target has been detached. Perform any desired cleanup operations here.
        """
        pass