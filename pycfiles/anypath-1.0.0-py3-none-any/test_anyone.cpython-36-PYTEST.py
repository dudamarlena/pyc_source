# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/herereadthis/Desktop/anyone/tests/test_anyone.py
# Compiled at: 2017-07-09 00:33:28
# Size of source mod 2**32: 1175 bytes
__doc__ = 'Unit tests for anyone.'
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from anyone import anyone

@pytest.fixture
def response():
    """Test fixture."""
    import requests
    return requests.get('https://github.com/herereadthis/anyone.git')


def test_author():
    """Test getting author."""
    poem = anyone.Poem()
    @py_assert1 = poem.author
    @py_assert5 = poem.get_author
    @py_assert7 = @py_assert5()
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.author\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_author\n}()\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_publication():
    """Test getting publication."""
    poem = anyone.Poem()
    @py_assert1 = poem.publication
    @py_assert5 = poem.get_publication
    @py_assert7 = @py_assert5()
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.publication\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_publication\n}()\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_title():
    """Test getting title."""
    poem = anyone.Poem()
    @py_assert1 = poem.title
    @py_assert5 = poem.get_title
    @py_assert7 = @py_assert5()
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_title\n}()\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_verse():
    """Test getting specific verse."""
    poem = anyone.Poem()
    @py_assert1 = poem.get_verse
    @py_assert3 = @py_assert1()
    @py_assert6 = poem.verses[0]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get_verse\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = poem.get_verse
    @py_assert3 = 1
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = poem.verses[0]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_verse\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = poem.get_verse
    @py_assert3 = 4
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = poem.verses[3]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_verse\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = poem.publication
    @py_assert5 = poem.get_publication
    @py_assert7 = @py_assert5()
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.publication\n} == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_publication\n}()\n}', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_line():
    """Test getting specific line."""
    poem = anyone.Poem()
    @py_assert1 = poem.get_line
    @py_assert3 = @py_assert1()
    @py_assert6 = poem.verses[0][0]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get_line\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = poem.get_line
    @py_assert3 = 3
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = poem.verses[0][2]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_line\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = poem.get_line
    @py_assert3 = 5
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ''
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_line\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = poem.get_line
    @py_assert3 = 22
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = poem.verses[4][1]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_line\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = poem.get_line
    @py_assert3 = 1000
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = ''
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_line\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(poem) if 'poem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(poem) else 'poem',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None