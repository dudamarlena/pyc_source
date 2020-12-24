# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebwiki/test/test_manage.py
# Compiled at: 2014-02-24 07:12:15
"""
Test twanager commands.
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, tiddlywebwiki, tiddlywebwiki.instance as instance_module
from shutil import rmtree
from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag
from tiddlywebplugins.imaker import spawn
instance_dir = 'test_instance'

def setup_module(module):
    tiddlywebwiki.init(config)
    try:
        rmtree(instance_dir)
    except:
        pass


class TestInstance(object):

    def setup_method(self, module):
        try:
            rmtree(instance_dir)
        except:
            pass

        self.env = {'tiddlyweb.config': config}

    def test_create_tiddlywebwiki_instance(self):
        spawn(instance_dir, config, instance_module)
        contents = _get_file_contents('%s/tiddlywebconfig.py' % instance_dir)
        @py_assert0 = "'system_plugins': ['tiddlywebwiki']"
        @py_assert2 = @py_assert0 in contents
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, contents)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = "'twanager_plugins': ['tiddlywebwiki']"
        @py_assert2 = @py_assert0 in contents
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, contents)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return

    def test_create_bag_policies(self):
        spawn(instance_dir, config, instance_module)
        os.chdir(instance_dir)
        store = Store(config['server_store'][0], config['server_store'][1], environ=self.env)
        bag = Bag('system')
        system_policy = store.get(bag).policy
        bag = Bag('common')
        common_policy = store.get(bag).policy
        @py_assert1 = system_policy.read
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.read\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = system_policy.write
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.write\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = system_policy.create
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.create\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = system_policy.manage
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.manage\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = system_policy.accept
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.accept\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = system_policy.delete
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.delete\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(system_policy) if 'system_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(system_policy) else 'system_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.read
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.read\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.write
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.write\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.create
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.create\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.manage
        @py_assert4 = ['R:ADMIN']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.manage\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.accept
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.accept\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = common_policy.delete
        @py_assert4 = []
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.delete\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(common_policy) if 'common_policy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_policy) else 'common_policy', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        os.chdir('..')
        return


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents