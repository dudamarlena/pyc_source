# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/admin/projects/irco/irco/test/test_authors.py
# Compiled at: 2014-05-04 11:49:52
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from collections import namedtuple
from irco.authors import Author, NamePart, levenshtein
AuthorTestSet = namedtuple('AuthorTestSet', [
 'corresponding', 'expected', 'candidates'])
corresponding_authors = [
 (
  'Ei-Shazly, M', 0, ('EI-Shazly, M.', 'Eissa, B.')),
 (
  'Pan, WH', 0,
  ('Weihua, Pan', 'Liao, Wanqing', 'Khayhan, Kantarawee', 'Hagen, Ferry', 'Boekhout, Teun',
 'Khayhan, Kantarawee', 'Hagen, Ferry', 'Boekhout, Teun', 'Khayhan, Kantarawee',
 'Wahyuningsih, Retno', 'Sjam, Ridhawati', 'Wahyuningsih, Retno', 'Chakrabarti, Arunaloke',
 'Chowdhary, Anuradha', 'Ikeda, Reiko', 'Taj-Aldeen, Saad J.', 'Khan, Ziauddin',
 'Imran, Darma', 'Imran, Darma', 'Sriburee, Pojana', 'Chaicumpar, Kunyaluk', 'Ingviya, Natnicha',
 'Mouton, Johan W.', 'Curfs-Breuker, Ilse', 'Meis, Jacques F.', 'Klaassen, Corne H. W.',
 'Mouton, Johan W.', 'Meis, Jacques F.')),
 (
  'Abu-Shady, ASI', 2,
  ('Al-Mudhaf, Humood F.', 'Al-Hayan, Mohammad N.', 'Abu-Shady, Abdel-Sattar I.', 'Selim, Mustafa I.')),
 (
  'Al-Tahan, ARM', 0,
  ('Al-Tahan, Abdel-Rahman M.', 'Al-Jumah, Mohammed A.', 'Bohlega, Saeed M.', 'Al-Shammari, Suhail N.',
 'Al-Sharoqi, Isa A.', 'Dahdaleh, Maurice P.', 'Hosny, Hassan M.', 'Yamout, Bassem I.')),
 (
  'Elassar, AZA', 0,
  ('Elassar, Abdel-Zaher A.', 'Al-Fulaij, Othman A.', 'El-Sayed, Ahmed E. M.', 'Elassar, Abdel-Zaher A.')),
 (
  'Muller, HP', 0,
  ('Mueller, Hans-Peter', 'Barrieshi-Nusair, Kefah M.')),
 (
  'Chen, HH', 0,
  ('Chen, Hsiao-Hwa', 'Xiao, Yang', 'Chen, Hui', 'Du, Xiaojiang', 'Guizani, Mohsen')),
 (
  'Mosaad, MES', 0,
  ('Mosaad, M. El-Sayed', 'Al-Hajeri, M.', 'Al-Ajmi, R.', 'Koliub, Abo. M.')),
 (
  'Heo, MS', 4,
  ('Harikrishnan, Ramasamy', 'Moon, Young-Gun', 'Kim, Man-Chul', 'Kim, Ju-Sang', 'Heo, Moon-Soo',
 'Jin, Chang-Nam', 'Balasundaram, Chellam', 'Azad, I. S.')),
 (
  'Khedr, MEM', 0,
  ('Khedr, M. -E. M.', 'Chamkha, A. J.', 'Bayomi, M.'))]

@pytest.fixture(params=corresponding_authors)
def corresponding_author(request):
    corresponding, expected, candidates = request.param
    candidates = [ Author(c) for c in candidates ]
    expected = candidates[expected]
    return AuthorTestSet(Author(corresponding), expected, candidates)


def test_authors(corresponding_author):
    corresponding, expected, candidates = corresponding_author
    match = corresponding.find_best_match(candidates)
    if not match:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = match == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (match, expected)) % {'py0': @pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_namepart_isabbrof():
    @py_assert1 = 'WH'
    @py_assert3 = NamePart(@py_assert1)
    @py_assert5 = @py_assert3.isabbrof
    @py_assert8 = 'Weihua'
    @py_assert10 = NamePart(@py_assert8)
    @py_assert12 = @py_assert5(@py_assert10)
    if not @py_assert12:
        @py_format14 = 'assert %(py13)s\n{%(py13)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.isabbrof\n}(%(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n})\n}' % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(NamePart) if 'NamePart' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NamePart) else 'NamePart', 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py7': @pytest_ar._saferepr(NamePart) if 'NamePart' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NamePart) else 'NamePart'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None
    return


def test_chunks():
    a1 = Author('Ei-Shazly, M').chunks
    a2 = Author('EI-Shazly, M.').chunks
    @py_assert1 = a1 == a2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (a1, a2)) % {'py0': @pytest_ar._saferepr(a1) if 'a1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a1) else 'a1', 'py2': @pytest_ar._saferepr(a2) if 'a2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a2) else 'a2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    n1 = NamePart('H.H.')
    n2 = NamePart('Hsiao-Hwa')
    n3 = NamePart('Hui')
    @py_assert1 = n1 == n2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (n1, n2)) % {'py0': @pytest_ar._saferepr(n1) if 'n1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n1) else 'n1', 'py2': @pytest_ar._saferepr(n2) if 'n2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n2) else 'n2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = n1 != n3
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (n1, n3)) % {'py0': @pytest_ar._saferepr(n1) if 'n1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n1) else 'n1', 'py2': @pytest_ar._saferepr(n3) if 'n3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n3) else 'n3'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = n2 != n3
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert1,), ('%(py0)s != %(py2)s', ), (n2, n3)) % {'py0': @pytest_ar._saferepr(n2) if 'n2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n2) else 'n2', 'py2': @pytest_ar._saferepr(n3) if 'n3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(n3) else 'n3'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def _test_match_score():
    corr, expected, cand = corresponding_authors[8]
    corr = Author(corr)
    print
    print corr, corr.chunks
    print
    import difflib
    scored_can = []
    for a in cand:
        p1 = (' ').join([ c.name for c in sorted(corr.chunks) ])
        p2 = (' ').join([ c.name for c in sorted(Author(a).chunks) ])
        l = levenshtein(p1, p2)
        l = float(l ** 2) / len(a) / len(corr.name)
        c = corr.match_score(Author(a))
        scored_can.append((
         Author(a),
         c,
         l,
         c - 10 * l,
         corr.distance(Author(a))))

    for a, c, l, c2, d in scored_can:
        print a.chunks, c, l, c2, d

    print
    print 'Score:', max(scored_can, key=lambda c: c[1])
    print 'Leven:', min(scored_can, key=lambda c: c[2])
    print 'Mixed:', max(scored_can, key=lambda c: c[3])
    print 'Implemented:', min(scored_can, key=lambda c: c[4])
    print 'Diff:', difflib.get_close_matches(corr.name, cand, 1)