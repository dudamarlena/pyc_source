# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/backend/test_nodes.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 1531 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from patientMatcher.utils.add import add_node

def test_add_client(database, test_client):
    """Test adding a client with auth token to the database"""
    is_client = True
    nclients = database['clients'].find().count()
    @py_assert2 = 0
    @py_assert1 = nclients == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (nclients, @py_assert2)) % {'py0':@pytest_ar._saferepr(nclients) if 'nclients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nclients) else 'nclients',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    inserted_id, collection = add_node(mongo_db=database, obj=test_client, is_client=is_client)
    @py_assert2 = test_client['_id']
    @py_assert1 = inserted_id == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (inserted_id, @py_assert2)) % {'py0':@pytest_ar._saferepr(inserted_id) if 'inserted_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_id) else 'inserted_id',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'clients'
    @py_assert1 = collection == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (collection, @py_assert2)) % {'py0':@pytest_ar._saferepr(collection) if 'collection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(collection) else 'collection',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    nclients = database['clients'].find().count()
    @py_assert2 = 1
    @py_assert1 = nclients == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (nclients, @py_assert2)) % {'py0':@pytest_ar._saferepr(nclients) if 'nclients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nclients) else 'nclients',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    inserted_id, collection = add_node(mongo_db=database, obj=test_client, is_client=True)
    @py_assert2 = None
    @py_assert1 = inserted_id == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (inserted_id, @py_assert2)) % {'py0':@pytest_ar._saferepr(inserted_id) if 'inserted_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_id) else 'inserted_id',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_add_server(database, test_node):
    """Test adding a server with auth token to the database"""
    is_client = False
    nservers = database['nodes'].find().count()
    @py_assert2 = 0
    @py_assert1 = nservers == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (nservers, @py_assert2)) % {'py0':@pytest_ar._saferepr(nservers) if 'nservers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nservers) else 'nservers',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    inserted_id, collection = add_node(mongo_db=database, obj=test_node, is_client=is_client)
    @py_assert2 = test_node['_id']
    @py_assert1 = inserted_id == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (inserted_id, @py_assert2)) % {'py0':@pytest_ar._saferepr(inserted_id) if 'inserted_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_id) else 'inserted_id',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'nodes'
    @py_assert1 = collection == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (collection, @py_assert2)) % {'py0':@pytest_ar._saferepr(collection) if 'collection' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(collection) else 'collection',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    nservers = database['nodes'].find().count()
    @py_assert2 = 1
    @py_assert1 = nservers == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (nservers, @py_assert2)) % {'py0':@pytest_ar._saferepr(nservers) if 'nservers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nservers) else 'nservers',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    inserted_id, collection = add_node(mongo_db=database, obj=test_node, is_client=is_client)
    @py_assert2 = None
    @py_assert1 = inserted_id == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (inserted_id, @py_assert2)) % {'py0':@pytest_ar._saferepr(inserted_id) if 'inserted_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_id) else 'inserted_id',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None