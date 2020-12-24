# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thibault/github/trainline-python/tests/test_trainline.py
# Compiled at: 2019-11-24 09:58:03
# Size of source mod 2**32: 12042 bytes
"""Tests for `trainline` package."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, trainline
from trainline import Trainline, Trip, Passenger, Segment, ComfortClass, Folder
from datetime import date, timedelta
TOULOUSE_STATION_ID = '5311'
BORDEAUX_STATION_ID = '828'
_DEFAULT_COMFORT_CLASS_DICT = {'id':'ae9ba138a7c211e88f35afa2c1b6c287', 
 'name':'pao.default', 
 'description':'Un siège standard.', 
 'title':'Normal', 
 'options':{},  'segment_id':'ae8b939ca7c211e8967edcf1e2aa0fd7', 
 'condition_id':'ae9b9fbca7c211e893c6790139ba5461'}
_DEFAULT_SEGMENT_DICT = {'id':'ae8b939ca7c211e8967edcf1e2aa0fd7', 
 'departure_date':'2018-10-15T08:49:00+02:00', 
 'departure_station_id':TOULOUSE_STATION_ID, 
 'arrival_date':'2018-10-15T10:58:00+02:00', 
 'arrival_station_id':BORDEAUX_STATION_ID, 
 'transportation_mean':'train', 
 'carrier':'sncf', 
 'train_number':'8202', 
 'travel_class':'first', 
 'trip_id':'f721ce4ca2cb11e88152d3a9f56d4f85', 
 'comfort_class_ids':[
  'ae9ba138a7c211e88f35afa2c1b6c287'], 
 'comfort_classes':[
  ComfortClass(mydict=_DEFAULT_COMFORT_CLASS_DICT)]}
_DEFAULT_TRIP_DICT = {'id':'f721ce4ca2cb11e88152d3a9f56d4f85', 
 'departure_date':'2018-10-15T08:49:00+02:00', 
 'departure_station_id':TOULOUSE_STATION_ID, 
 'arrival_date':'2018-10-15T10:58:00+02:00', 
 'arrival_station_id':BORDEAUX_STATION_ID, 
 'price':66.0, 
 'currency':'EUR', 
 'segment_ids':[
  'f721c960a2cb11e89a42408805033f41'], 
 'segments':[
  Segment(mydict=_DEFAULT_SEGMENT_DICT)]}
_DEFAULT_FOLDER_DICT = {'id':'f721d0a4a2cb11e880abfc0416222638', 
 'departure_date':'2018-10-15T08:49:00+02:00', 
 'departure_station_id':TOULOUSE_STATION_ID, 
 'arrival_date':'2018-10-15T10:58:00+02:00', 
 'arrival_station_id':BORDEAUX_STATION_ID, 
 'price':66.0, 
 'currency':'EUR', 
 'trip_ids':[
  'f721ce4ca2cb11e88152d3a9f56d4f85'], 
 'trips':[
  Trip(mydict=_DEFAULT_TRIP_DICT)]}
tommorow_obj = date.today() + timedelta(days=1)
_TOMORROW = tommorow_obj.strftime('%d/%m/%Y')

def test_class_Trainline():
    t = Trainline()
    @py_assert2 = None
    @py_assert1 = t is not @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=75)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (t, @py_assert2)) % {'py0':@pytest_ar._saferepr(t) if 't' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(t) else 't',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_class_ComfortClass():
    cc = ComfortClass(mydict=_DEFAULT_COMFORT_CLASS_DICT)
    @py_assert1 = cc.id
    @py_assert4 = 'ae9ba138a7c211e88f35afa2c1b6c287'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=80)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    print()
    print(cc)


def test_class_Segment():
    seg = Segment(mydict=_DEFAULT_SEGMENT_DICT)
    @py_assert1 = seg.id
    @py_assert4 = 'ae8b939ca7c211e8967edcf1e2aa0fd7'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=87)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(seg) if 'seg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(seg) else 'seg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    print()
    print(seg)


def test_class_Folder():
    folder = Folder(mydict=_DEFAULT_FOLDER_DICT)
    @py_assert1 = folder.id
    @py_assert4 = 'f721d0a4a2cb11e880abfc0416222638'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=94)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(folder) if 'folder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(folder) else 'folder',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    print()
    print(folder)


def test_class_Trip():
    trip = Trip(mydict=_DEFAULT_TRIP_DICT)
    @py_assert1 = trip.id
    @py_assert4 = 'f721ce4ca2cb11e88152d3a9f56d4f85'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=101)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(trip) if 'trip' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(trip) else 'trip',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    print()
    print(trip)


def test_class_Trip_errors():
    with pytest.raises(TypeError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict['departure_station_id'] = 1234
        Trip(mydict=modified_trip_dict)
    with pytest.raises(TypeError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict['price'] = 'not_a_float'
        Trip(mydict=modified_trip_dict)
    with pytest.raises(TypeError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict['departure_date'] = 'not_a_date'
        Trip(mydict=modified_trip_dict)
    with pytest.raises(TypeError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict['id'] = 12345
        Trip(mydict=modified_trip_dict)
    with pytest.raises(TypeError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict.pop('id')
        Trip(mydict=modified_trip_dict)
    with pytest.raises(ValueError):
        modified_trip_dict = _DEFAULT_TRIP_DICT.copy()
        modified_trip_dict['price'] = -1.5
        Trip(mydict=modified_trip_dict)


def test_class_Passenger():
    p1 = Passenger(birthdate='01/01/1980')
    print()
    print(p1)
    @py_assert1 = p1.birthdate
    @py_assert4 = '01/01/1980'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=142)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.birthdate\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = p1.cards
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=143)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.cards\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    age_p1 = date.today().year - 2018 + 38
    @py_assert1 = p1.age
    @py_assert3 = @py_assert1 == age_p1
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=145)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.age\n} == %(py4)s', ), (@py_assert1, age_p1)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(age_p1) if 'age_p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(age_p1) else 'age_p1'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    id_p1 = p1.id
    @py_assert2 = len(id_p1)
    @py_assert5 = 36
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=147)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(id_p1) if 'id_p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id_p1) else 'id_p1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = p1.get_dict
    @py_assert3 = @py_assert1()
    @py_assert6 = {'id':id_p1, 
     'age':age_p1,  'cards':[],  'label':id_p1}
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=148)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get_dict\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(p1) if 'p1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p1) else 'p1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    p2 = Passenger(birthdate='01/01/2006',
      cards=[
     trainline.AVANTAGE_JEUNE, trainline.AVANTAGE_WEEK_END])
    print(p2)
    @py_assert1 = p2.birthdate
    @py_assert4 = '01/01/2006'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=160)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.birthdate\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = p2.cards
    @py_assert4 = [
     trainline.AVANTAGE_JEUNE, trainline.AVANTAGE_WEEK_END]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=161)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.cards\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    age_p2 = date.today().year - 2018 + 12
    @py_assert1 = p2.age
    @py_assert3 = @py_assert1 == age_p2
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=163)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.age\n} == %(py4)s', ), (@py_assert1, age_p2)) % {'py0':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(age_p2) if 'age_p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(age_p2) else 'age_p2'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    id_p2 = p2.id
    @py_assert2 = len(id_p2)
    @py_assert5 = 36
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=165)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(id_p2) if 'id_p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id_p2) else 'id_p2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = p2.get_dict
    @py_assert3 = @py_assert1()
    @py_assert6 = {'id':id_p2, 
     'age':age_p2,  'cards':[{'reference': trainline.AVANTAGE_JEUNE}, {'reference': trainline.AVANTAGE_WEEK_END}],  'label':id_p2}
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=166)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.get_dict\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(p2) if 'p2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p2) else 'p2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_class_Passenger_errors():
    with pytest.raises(KeyError):
        Passenger(birthdate='01/03/2012', cards=['Unknown'])
    with pytest.raises(TypeError):
        Passenger(birthdate='not_a_date')
    with pytest.raises(TypeError):
        Passenger()


def test_get_station_id():
    station_id = trainline.get_station_id(station_name='Toulouse Matabiau')
    @py_assert1 = station_id == TOULOUSE_STATION_ID
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=188)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (station_id, TOULOUSE_STATION_ID)) % {'py0':@pytest_ar._saferepr(station_id) if 'station_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(station_id) else 'station_id',  'py2':@pytest_ar._saferepr(TOULOUSE_STATION_ID) if 'TOULOUSE_STATION_ID' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TOULOUSE_STATION_ID) else 'TOULOUSE_STATION_ID'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    station_id = trainline.get_station_id(station_name='Bordeaux St-Jean')
    @py_assert1 = station_id == BORDEAUX_STATION_ID
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=191)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (station_id, BORDEAUX_STATION_ID)) % {'py0':@pytest_ar._saferepr(station_id) if 'station_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(station_id) else 'station_id',  'py2':@pytest_ar._saferepr(BORDEAUX_STATION_ID) if 'BORDEAUX_STATION_ID' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BORDEAUX_STATION_ID) else 'BORDEAUX_STATION_ID'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_get_station_id_errors():
    with pytest.raises(KeyError):
        trainline.get_station_id(station_name='Unknown station')


def test_internal_search():
    t = Trainline()
    print('Test internal search')
    ret = t.search(departure_station_id=TOULOUSE_STATION_ID,
      arrival_station_id=BORDEAUX_STATION_ID,
      departure_date='2018-10-15T10:48:00+00:00',
      passenger_list=[
     Passenger(birthdate='01/01/1980').get_dict()])
    @py_assert1 = ret.status_code
    @py_assert4 = 200
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=207)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ret) if 'ret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ret) else 'ret',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_basic_search():
    from_date = '{} 18:00'.format(_TOMORROW)
    to_date = '{} 23:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Bordeaux St-Jean'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=225)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)


def test_search_only_bus():
    from_date = '{} 09:00'.format(_TOMORROW)
    to_date = '{} 11:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Bordeaux St-Jean'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date,
      transportation_mean='coach')
    print()
    print('Search BUS trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=246)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)
    for folder in results:
        for trip in folder.trips:
            for segment in trip.segments:
                @py_assert1 = segment.transportation_mean
                @py_assert4 = 'coach'
                @py_assert3 = @py_assert1 == @py_assert4
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestAssertRewriteWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=253)
                if not @py_assert3:
                    @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.transportation_mean\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(segment) if 'segment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(segment) else 'segment',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                    @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format8))
                @py_assert1 = @py_assert3 = @py_assert4 = None


def test_basic_search_with_bicyle():
    from_date = '{} 08:00'.format(_TOMORROW)
    to_date = '{} 12:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Narbonne'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date,
      bicycle_with_or_without_reservation=True)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=272)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)


def test_basic_search_with_bicyle_without_reservation():
    from_date = '{} 08:00'.format(_TOMORROW)
    to_date = '{} 12:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Carcassonne'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date,
      bicycle_without_reservation_only=True)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=293)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)


def test_basic_search_with_bicyle_with_reservation():
    from_date = '{} 20:00'.format(_TOMORROW)
    to_date = '{} 21:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Bordeaux'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date,
      bicycle_with_reservation_only=True)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=315)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)
    csv_header = results.csv().split('\n')[0]
    @py_assert2 = 'departure_date;arrival_date;duration;number_of_segments;price;currency;transportation_mean;bicycle_reservation'
    @py_assert1 = csv_header == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=320)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (csv_header, @py_assert2)) % {'py0':@pytest_ar._saferepr(csv_header) if 'csv_header' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(csv_header) else 'csv_header',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    first_result = results.csv().split('\n')[1]
    @py_assert2 = first_result.split(';')[0]
    @py_assert1 = _TOMORROW in @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=325)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (_TOMORROW, @py_assert2)) % {'py0':@pytest_ar._saferepr(_TOMORROW) if '_TOMORROW' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_TOMORROW) else '_TOMORROW',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    last_result = results.csv().split('\n')[(-2)]
    @py_assert2 = last_result.split(';')[0]
    @py_assert1 = _TOMORROW in @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=328)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (_TOMORROW, @py_assert2)) % {'py0':@pytest_ar._saferepr(_TOMORROW) if '_TOMORROW' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_TOMORROW) else '_TOMORROW',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def display_trips(folder_list):
    print(folder_list.csv())


def test_with_benerail():
    from_date = '{} 08:00'.format(_TOMORROW)
    to_date = '{} 10:00'.format(_TOMORROW)
    departure_station = 'Paris'
    arrival_station = 'Antwerpen-Centraal'
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=353)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)


def test_basic_search_with_card():
    from_date = '{} 10:00'.format(_TOMORROW)
    to_date = '{} 12:00'.format(_TOMORROW)
    departure_station = 'Toulouse Matabiau'
    arrival_station = 'Bordeaux St-Jean'
    p1 = Passenger(birthdate='01/01/1980', cards=[trainline.AVANTAGE_FAMILLE])
    results = trainline.search(departure_station=departure_station,
      arrival_station=arrival_station,
      from_date=from_date,
      to_date=to_date)
    print()
    print('Search trips for {} to {}, between {} and {}'.format(departure_station, arrival_station, from_date, to_date))
    print('{} results'.format(len(results)))
    @py_assert2 = len(results)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/thibault/github/trainline-python/tests/test_trainline.py', lineno=375)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    display_trips(results)