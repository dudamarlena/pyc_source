# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/tests/test_tasks.py
# Compiled at: 2018-10-06 11:39:20
# Size of source mod 2**32: 2187 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from .. import models, tasks

@pytest.mark.django_db
def test_create_or_update_if_needed():
    @py_assert2 = models.CachedImage
    @py_assert4 = @py_assert2.objects
    @py_assert6 = @py_assert4.all
    @py_assert8 = @py_assert6()
    @py_assert10 = list(@py_assert8)
    @py_assert13 = []
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.CachedImage\n}.objects\n}.all\n}()\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(models) if 'models' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(models) else 'models',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    created_obj, modified = tasks.create_or_update_if_needed((models.CachedImage),
      [], uri='https://foo.bar/image.jpg',
      defaults={'format': 'JPEG'})
    @py_assert3 = models.CachedImage
    @py_assert5 = isinstance(created_obj, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.CachedImage\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(created_obj) if 'created_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_obj) else 'created_obj',  'py2':@pytest_ar._saferepr(models) if 'models' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(models) else 'models',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert3 = @py_assert5 = None
    @py_assert1 = created_obj.size_in_bytes
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.size_in_bytes\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(created_obj) if 'created_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(created_obj) else 'created_obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    if not modified:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(modified) if 'modified' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modified) else 'modified'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    updated_obj, modified = tasks.create_or_update_if_needed((models.CachedImage),
      [
     created_obj],
      uri='https://foo.bar/image.jpg',
      defaults={'format':'JPEG', 
     'size_in_bytes':1024})
    @py_assert3 = models.CachedImage
    @py_assert5 = isinstance(updated_obj, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.CachedImage\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(updated_obj) if 'updated_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated_obj) else 'updated_obj',  'py2':@pytest_ar._saferepr(models) if 'models' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(models) else 'models',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert3 = @py_assert5 = None
    @py_assert1 = updated_obj.size_in_bytes
    @py_assert4 = 1024
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.size_in_bytes\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(updated_obj) if 'updated_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated_obj) else 'updated_obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    if not modified:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(modified) if 'modified' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modified) else 'modified'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    not_updated_obj, modified = tasks.create_or_update_if_needed((models.CachedImage),
      [
     updated_obj],
      uri='https://foo.bar/image.jpg',
      defaults={'format':'JPEG', 
     'size_in_bytes':1024})
    @py_assert1 = not_updated_obj is updated_obj
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (not_updated_obj, updated_obj)) % {'py0':@pytest_ar._saferepr(not_updated_obj) if 'not_updated_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(not_updated_obj) else 'not_updated_obj',  'py2':@pytest_ar._saferepr(updated_obj) if 'updated_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated_obj) else 'updated_obj'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = not_updated_obj.size_in_bytes
    @py_assert4 = 1024
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.size_in_bytes\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(not_updated_obj) if 'not_updated_obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(not_updated_obj) else 'not_updated_obj',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = not modified
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(modified) if 'modified' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modified) else 'modified'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_is_object_equivalent():
    attachment = models.Attachment(uri='https://foo.bar/image.jpg',
      title='Foo image',
      mime_type='image/jpeg',
      size_in_bytes=1024)
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'uri': 'https://foo.bar/image.jpg'}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'uri':'https://foo.bar/image.jpg', 
     'title':'Foo image'}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'mime_type':'image/jpeg', 
     'size_in_bytes':1024}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'uri': 'https://foo.bar/image.gif'}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'mime_type':'image/jpeg', 
     'size_in_bytes':1025}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = tasks._is_object_equivalent
    @py_assert4 = {'non_existant': None}
    @py_assert6 = @py_assert1(attachment, @py_assert4)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s._is_object_equivalent\n}(%(py3)s, %(py5)s)\n}') % {'py0':@pytest_ar._saferepr(tasks) if 'tasks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tasks) else 'tasks',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(attachment) if 'attachment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attachment) else 'attachment',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None