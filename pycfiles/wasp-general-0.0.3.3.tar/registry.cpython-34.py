# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/task/registry.py
# Compiled at: 2017-09-28 10:36:47
# Size of source mod 2**32: 8683 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_subclass, verify_type
from wasp_general.task.base import WTask

class WRegisteredTask(ABCMeta):
    __doc__ = ' Metaclass for task, that is stored in registry.  Derived class must redefine __registry__ property\n\t(and __registry_tag__ depends on registry storage - see\n\t:attr:`.WTaskRegistryStorage.__multiple_tasks_per_tag__`)\n\t'
    __auto_registry__ = True
    __registry_tag__ = None
    __registry__ = None

    def __init__(cls, name, bases, namespace):
        """ Construct new class. Derived class must redefine __registry__ property (and __registry_tag__
                depends on registry storage - see :attr:`.WTaskRegistryStorage.__multiple_tasks_per_tag__`)

                :param name: as name in type(cls, name, bases, namespace)
                :param bases: as bases in type(cls, name, bases, namespace)
                :param namespace: as namespace in type(cls, name, bases, namespace)
                """
        ABCMeta.__init__(cls, name, bases, namespace)
        if cls.__auto_registry__ is not True:
            return
        if cls.__registry__ is None:
            raise ValueError('__registry__ must be defined')
        if issubclass(cls.__registry__, WTaskRegistry) is False:
            raise TypeError("Property '__registry__' of tasks class has invalid type (must beWTaskRegistry or its subclass)")
        if issubclass(cls, WTask) is False:
            raise TypeError('This class must inherit WTask class')
        cls.__registry__.add(cls)


class WTaskRegistryBase(metaclass=ABCMeta):
    __doc__ = ' Prototype for registry storage. Derived class must redefined following methods\n\t'

    @abstractmethod
    def add(self, task):
        """ Add task to storage

                :param task: task to add (WTask class with WRegisteredTask metaclass)
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def remove(self, task):
        """ Remove task from storage

                :param task: task to remove (WTask class with WRegisteredTask metaclass)
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def clear(self):
        """ Remove every task from storage

                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def tasks_by_tag(self, registry_tag):
        """ Get tasks from registry by its tag

                :param registry_tag: any hash-able object
                :return: Return task or list of tasks
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def tasks(self, task_cls=None):
        """ Return tasks that was added to this registry

                :param task_cls: if it is not None, then result will be consist of this subclass only (useful fo
                filtering tasks)

                :return: tuple of WRegisteredTask
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def count(self):
        """ Registered task count

                :return: int
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def tags(self):
        """ Return available registry tags

                :return: tuple of str
                """
        raise NotImplementedError('This method is abstract')


class WTaskRegistryStorage(WTaskRegistryBase):
    __doc__ = ' Simple registry storage implementation\n\t'
    __multiple_tasks_per_tag__ = True

    def __init__(self):
        """ Construct new registry storage
                """
        self._WTaskRegistryStorage__registry = {}

    @verify_subclass(task_cls=WTask)
    @verify_type(task_cls=WRegisteredTask)
    def add(self, task_cls):
        """ Add task to this storage. Depends on :attr:`.WTaskRegistryStorage.__multiple_tasks_per_tag__`
                tasks with the same __registry_tag__ can be treated as error.

                :param task_cls: task to add
                :return: None
                """
        registry_tag = task_cls.__registry_tag__
        if registry_tag not in self._WTaskRegistryStorage__registry.keys():
            self._WTaskRegistryStorage__registry[registry_tag] = [
             task_cls]
        else:
            if self.__multiple_tasks_per_tag__ is True:
                self._WTaskRegistryStorage__registry[registry_tag].append(task_cls)
            else:
                raise RuntimeError('Multiple tasks with same tag appended')

    @verify_subclass(task_cls=WTask)
    @verify_type(task_cls=WRegisteredTask)
    def remove(self, task_cls):
        """ Remove task from the storage. If task class are stored multiple times
                (if :attr:`.WTaskRegistryStorage.__multiple_tasks_per_tag__` is True) - removes all of them.

                :param task_cls: task to remove
                :return: None
                """
        registry_tag = task_cls.__registry_tag__
        if registry_tag in self._WTaskRegistryStorage__registry.keys():
            self._WTaskRegistryStorage__registry[registry_tag] = list(filter(lambda x: x != task_cls, self._WTaskRegistryStorage__registry[registry_tag]))
            if len(self._WTaskRegistryStorage__registry[registry_tag]) == 0:
                self._WTaskRegistryStorage__registry.pop(registry_tag)

    def clear(self):
        """ Removes every task from storage

                :return: None
                """
        self._WTaskRegistryStorage__registry.clear()

    def tasks_by_tag(self, registry_tag):
        """ Get tasks from registry by its tag

                :param registry_tag: any hash-able object
                :return: Return task (if :attr:`.WTaskRegistryStorage.__multiple_tasks_per_tag__` is not True) or               list of tasks
                """
        if registry_tag not in self._WTaskRegistryStorage__registry.keys():
            return
        tasks = self._WTaskRegistryStorage__registry[registry_tag]
        if self.__multiple_tasks_per_tag__ is True:
            return tasks
        return tasks[0]

    @verify_type(task_cls=(WRegisteredTask, None))
    def tasks(self, task_cls=None):
        """ :meth:`.WTaskRegistryBase.tasks` implementation
                """
        result = []
        for tasks in self._WTaskRegistryStorage__registry.values():
            result.extend(tasks)

        if task_cls is not None:
            result = filter(lambda x: issubclass(x, task_cls), result)
        return tuple(result)

    def tags(self):
        """ :meth:`.WTaskRegistryBase.tags` implementation
                """
        return tuple(self._WTaskRegistryStorage__registry.keys())

    def count(self):
        """ Registered task count

                :return: int
                """
        result = 0
        for tasks in self._WTaskRegistryStorage__registry.values():
            result += len(tasks)

        return result


class WTaskRegistry:
    __doc__ = ' Basic task registry. Derived classes must redefine __registry_storage__ property\n\t(see :attr:`.WTaskRegistry.__registry_storage__`)\n\t'
    __registry_storage__ = None
    __skip_none_registry_tag__ = True

    @classmethod
    def registry_storage(cls):
        """ Get registry storage

                :return: WTaskRegistryBase
                """
        if cls.__registry_storage__ is None:
            raise ValueError('__registry_storage__ must be defined')
        if isinstance(cls.__registry_storage__, WTaskRegistryBase) is False:
            raise TypeError("Property '__registry_storage__' is invalid (must derived from WTaskRegistryBase)")
        return cls.__registry_storage__

    @classmethod
    @verify_subclass('paranoid', task_cls=WTask)
    @verify_type('paranoid', task_cls=WRegisteredTask)
    def add(cls, task_cls):
        """ Add task class to storage

                :param task_cls: task to add
                :return: None
                """
        if task_cls.__registry_tag__ is None and cls.__skip_none_registry_tag__ is True:
            return
        cls.registry_storage().add(task_cls)

    @classmethod
    @verify_subclass('paranoid', task_cls=WTask)
    @verify_type('paranoid', task_cls=WRegisteredTask)
    def remove(cls, task_cls):
        """ Remove task class to storage

                :param task_cls: task to remove
                :return: None
                """
        cls.registry_storage().remove(task_cls)

    @classmethod
    def clear(cls):
        """ Remove every task from storage

                :return: None
                """
        cls.registry_storage().clear()