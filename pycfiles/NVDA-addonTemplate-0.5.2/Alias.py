# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Node\Alias.py
# Compiled at: 2016-07-07 03:21:36
"""scons.Node.Alias

Alias nodes.

This creates a hash of global Aliases (dummy targets).

"""
__revision__ = 'src/engine/SCons/Node/Alias.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import collections, SCons.Errors, SCons.Node, SCons.Util

class AliasNameSpace(collections.UserDict):

    def Alias(self, name, **kw):
        if isinstance(name, SCons.Node.Alias.Alias):
            return name
        try:
            a = self[name]
        except KeyError:
            a = SCons.Node.Alias.Alias(name, **kw)
            self[name] = a

        return a

    def lookup(self, name, **kw):
        try:
            return self[name]
        except KeyError:
            return

        return


class AliasNodeInfo(SCons.Node.NodeInfoBase):
    __slots__ = ('csig', )
    current_version_id = 2
    field_list = ['csig']

    def str_to_node(self, s):
        return default_ans.Alias(s)

    def __getstate__(self):
        """
        Return all fields that shall be pickled. Walk the slots in the class
        hierarchy and add those to the state dictionary. If a '__dict__' slot is
        available, copy all entries to the dictionary. Also include the version
        id, which is fixed for all instances of a class.
        """
        state = getattr(self, '__dict__', {}).copy()
        for obj in type(self).mro():
            for name in getattr(obj, '__slots__', ()):
                if hasattr(self, name):
                    state[name] = getattr(self, name)

        state['_version_id'] = self.current_version_id
        try:
            del state['__weakref__']
        except KeyError:
            pass

        return state

    def __setstate__(self, state):
        """
        Restore the attributes from a pickled state.
        """
        del state['_version_id']
        for key, value in state.items():
            if key not in ('__weakref__', ):
                setattr(self, key, value)


class AliasBuildInfo(SCons.Node.BuildInfoBase):
    __slots__ = ()
    current_version_id = 2


class Alias(SCons.Node.Node):
    NodeInfo = AliasNodeInfo
    BuildInfo = AliasBuildInfo

    def __init__(self, name):
        SCons.Node.Node.__init__(self)
        self.name = name
        self.changed_since_last_build = 1
        self.store_info = 0

    def str_for_display(self):
        return '"' + self.__str__() + '"'

    def __str__(self):
        return self.name

    def make_ready(self):
        self.get_csig()

    really_build = SCons.Node.Node.build
    is_up_to_date = SCons.Node.Node.children_are_up_to_date

    def is_under(self, dir):
        return 1

    def get_contents(self):
        """The contents of an alias is the concatenation
        of the content signatures of all its sources."""
        childsigs = [ n.get_csig() for n in self.children() ]
        return ('').join(childsigs)

    def sconsign(self):
        """An Alias is not recorded in .sconsign files"""
        pass

    def build(self):
        """A "builder" for aliases."""
        pass

    def convert(self):
        try:
            del self.builder
        except AttributeError:
            pass

        self.reset_executor()
        self.build = self.really_build

    def get_csig(self):
        """
        Generate a node's content signature, the digested signature
        of its content.

        node - the node
        cache - alternate node to use for the signature cache
        returns - the content signature
        """
        try:
            return self.ninfo.csig
        except AttributeError:
            pass

        contents = self.get_contents()
        csig = SCons.Util.MD5signature(contents)
        self.get_ninfo().csig = csig
        return csig


default_ans = AliasNameSpace()
SCons.Node.arg2nodes_lookups.append(default_ans.lookup)