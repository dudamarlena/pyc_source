# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/PycharmProjects/Yeti/yeti/hook_server.py
# Compiled at: 2015-10-06 10:01:46
# Size of source mod 2**32: 3023 bytes
import logging

class Hook(object):
    __doc__ = "\n    This stores a reference to a method, and can be used to remove the hook's reference from the source :class:`HookServer`.\n    Hook objects are generally only created by a :class:`HookServer`.\n    "

    def __init__(self, hook_server, hook_name, func):
        """
        :param hook_server: The instance of :class:`.HookServer` that uses this hook.
        :param hook_name: The name of the method to create a hook for.
        :param func: The function to use with the hook.
        """
        self.func = func
        self.hook_server = hook_server
        self.hook_name = hook_name

    def call(self, *args, **kwargs):
        """
        Calls the hook function with the given parameters
        """
        self.func(*args, **kwargs)

    def unset(self):
        """
        Removes the trigger from hook_server
        """
        self.hook_server.remove_hook(self)


class HookServer(object):
    __doc__ = '\n    This provides a convenient hook registration mechanism.\n    '

    def __init__(self):
        self.logger = logging.getLogger('yeti.' + self.__class__.__name__)
        self._hooks = dict()

    def add_hook(self, hook_name, callback):
        """
        Adds a hooks to be run when method hook_name is called.

        :param hook_name: The name of the method to create a hook for.
        :param callback: The method to use for the hook.

        :returns: The new instance of :class:`.Hook`
        """
        hook = Hook(self, hook_name, callback)
        if hook_name not in self._hooks:
            self._hooks[hook_name] = list()
        self._hooks[hook_name].append(hook)
        return hook

    def call_hook(self, hook_name, *args, supress_exceptions=True, **kwargs):
        """
        Calls all hooks that have been added to this :class:`.HookServer` for the method hook_name with all extra
        provided parameters.

        :param hook_name: The name of the method with hooks to be called.
        :param supress_exceptions: Whether or not to suppress raised exceptions. Defaults to true.

        :returns: True if at least one hook was successfully called.
        """
        retval = False
        if hook_name in self._hooks:
            for hook in self._hooks[hook_name]:
                try:
                    hook.call(*args, **kwargs)
                    retval = True
                except Exception as e:
                    if supress_exceptions:
                        self.logger.exception("Exception on hook '{}' call: {}".format(hook_name, e))
                    else:
                        raise e

        return retval

    def remove_hook(self, hook):
        """
        Removes hook from the instance of :class:`.HookServer`

        :param hook: The :class:`.Hook` object to remove.

        :returns: Weather or not removal was successful.
        """
        if hook in self._hooks[hook.hook_name]:
            self._hooks[hook.hook_name].remove(hook)
            return True
        return False