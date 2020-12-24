# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/loader/base.py
# Compiled at: 2010-05-11 09:17:59
from alexandria.dsl.core import MenuSystem, prompt, end
from alexandria.dsl.validators import pick_one

class Loader(object):

    def do_question(self, *args, **kwargs):
        return prompt(validator=pick_one, *args, **kwargs)

    def do_end(self, *args, **kwargs):
        return end(*args)

    def error(self, command):
        raise RuntimeError, 'No dispatcher available for command %s' % command

    def dispatch(self, command, *args, **kwargs):
        mname = 'do_' + command
        if hasattr(self, mname):
            method = getattr(self, mname)
            return method(*args, **kwargs)
        self.error(command)

    def load_from_dict(self, dictionary):
        r"""
        Depends on the order of keys, works for YAML but is flakely nontheless
        
        >>> loader = Loader()
        >>> item = loader.load_from_dict({
        ...     'question': 'What is your favorite color?',
        ...     'options': ['red','white','blue']
        ... })
        >>> item.next() # manually advance
        >>> item.send((None, {})) # fake feed of menu and session store
        ('What is your favorite color?\n1: red\n2: white\n3: blue', False)
        >>> 
        
        """
        menu_type = dictionary.keys()[0]
        menu_option_keys = dictionary.keys()[1:]
        return self.dispatch(menu_type, dictionary[menu_type], **dict([ (key, dictionary[key]) for key in menu_option_keys ]))


class YAMLLoader(Loader):

    def load_from_file(self, fp):
        """Load a menu from the given file"""
        return self.load_from_string(('').join(fp.readlines()))

    def load_from_string(self, string):
        r'''
        Load a menu from a YAML description
        
        >>> loader = YAMLLoader()
        >>> menu = loader.load_from_string("""
        ... - question: What is your favorite color?
        ...   options:
        ...     - red
        ...     - white
        ...     - blue
        ... """)
        >>> index, item = menu.next()
        >>> index # the index of the next menu
        1
        >>> item.next() # manually advance
        >>> item.send((None, {})) # fake feed of menu and session store
        ('What is your favorite color?\n1: red\n2: white\n3: blue', False)
        >>> 
        
        '''
        import yaml
        menu = MenuSystem()
        for item in yaml.safe_load(string):
            menu.append(self.load_from_dict(item))

        return menu