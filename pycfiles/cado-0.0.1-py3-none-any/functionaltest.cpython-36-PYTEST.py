# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shawn/Desktop/projects/cadnano2.5/cadnano/tests/functionaltest.py
# Compiled at: 2017-11-11 17:28:32
# Size of source mod 2**32: 4020 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from cntestcase import CNTestApp

@pytest.fixture()
def cnapp():
    app = CNTestApp()
    yield app
    app.tearDown()


def testStapleOutput_simple42legacy(cnapp):
    """p7308 applied to 42-base duplex (json source)"""
    designname = 'simple42legacy.json'
    refname = 'simple42legacy.csv'
    sequences = [('p7308', 0, 0)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_skip(cnapp):
    """Simple design with a single skip"""
    designname = 'skip.json'
    refname = 'skip.csv'
    sequences = [('M13mp18', 0, 14)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_inserts_and_skips(cnapp):
    """Insert and skip stress test"""
    designname = 'loops_and_skips.json'
    refname = 'loops_and_skips.csv'
    sequences = [('M13mp18', 0, 0)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_insert_size_1(cnapp):
    """Test sequence output with a single insert of size 1"""
    designname = 'loop_size_1.json'
    refname = 'loop_size_1.csv'
    sequences = [('M13mp18', 0, 14)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_Science09_prot120_98_v3(cnapp):
    """Staples match reference set for Science09 protractor 120 v3"""
    designname = 'Science09_prot120_98_v3.json'
    refname = 'Science09_prot120_98_v3.csv'
    sequences = [('p7704', 0, 105)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_Nature09_monolith(cnapp):
    """Staples match reference set for Nature09 monolith"""
    designname = 'Nature09_monolith.json'
    refname = 'Nature09_monolith.csv'
    sequences = [('p7560', 4, 73)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def testStapleOutput_Nature09_monolith_legacy(cnapp):
    """Staples match reference set for Nature09 monolith"""
    designname = 'Nature09_monolith_legacy.json'
    refname = 'Nature09_monolith.csv'
    sequences = [('p7560', 4, 73)]
    test_set = cnapp.getTestSequences(designname, sequences)
    ref_set = cnapp.getRefSequences(refname)
    @py_assert1 = test_set == ref_set
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (test_set, ref_set)) % {'py0':@pytest_ar._saferepr(test_set) if 'test_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_set) else 'test_set',  'py2':@pytest_ar._saferepr(ref_set) if 'ref_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ref_set) else 'ref_set'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None