# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/loaders/module_loader.py
# Compiled at: 2019-03-22 05:32:22
# Size of source mod 2**32: 3575 bytes
import pkgutil, importlib, inspect, logging

class ModuleLoader(object):
    __doc__ = '\n    Loads modules via reflection and automatically instantiates classes.\n    '

    @staticmethod
    def load_modules(dir_path: str, package: str, ignore_classes: list, class_suffix: str, *args) -> list:
        """
        Creates a list of objects from all classes found in a package.
        :param dir_path: current path (i.e.: path of the calling file).
        :param package: path to package starting from dir_path,
        :param ignore_classes: Ignores classes named in this list. (list contains strings)
        :param class_suffix: Selects only classes that end with this suffix.
        :param args: Arguments for the class' constructor.
        """
        objects = list()
        logging.info('[ModuleLoader]: Initializing parsers at ' + dir_path + '/' + package)
        modules = pkgutil.iter_modules(path=[dir_path + '/' + package])
        if not modules:
            logging.warning('[ModuleLoader]: No modules found at' + dir_path)
            return objects
        for loader, mod_name, ispkg in modules:
            module_path = package.replace('/', '.')
            mod = importlib.import_module('rosmap.' + module_path + '.' + mod_name)
            for selected_classname in ModuleLoader.get_classnames_from_module(mod, class_suffix, ignore_classes):
                try:
                    objects.append(ModuleLoader.instantiate_class(mod, mod_name, module_path, selected_classname, *args))
                except ValueError as error:
                    logging.warning('[ModuleLoader]: ' + str(error))

        return objects

    @staticmethod
    def get_classnames_from_module(module: str, class_suffix: str, ignore_classes: list) -> iter:
        """
        Yield returns all applicable class-names in a module...
        :param module: The module to search classes in.
        :param class_suffix: Selects only classes that end with this suffix.
        :param ignore_classes: Ignores classes named in this list. (list contains strings)
        :return: iterable of strings containing selected class-names.
        """
        for classname in dir(module):
            if classname[-len(class_suffix):] == class_suffix and classname not in ignore_classes:
                yield classname

    @staticmethod
    def instantiate_class(module: str, module_name: str, module_path: str, class_name: str, *args) -> object:
        """
        Instantiates a class based on parameters.
        :param module: The module the class is located in.
        :param module_name: The name of the module the class is located in.
        :param module_path: The path to the module.
        :param class_name: The name of the class to be instantiated.
        :param args: Arguments for the class' constructor.
        :return: instance of the selected class in the selected module.
        """
        my_class = getattr(module, class_name)
        logging.info('[ModuleLoader]: Instantiating ' + class_name + ' from ' + module_path + '.' + module_name)
        if inspect.isclass(my_class):
            return my_class(*args)
        raise ValueError(class_name + ' is not a class, skipping.')