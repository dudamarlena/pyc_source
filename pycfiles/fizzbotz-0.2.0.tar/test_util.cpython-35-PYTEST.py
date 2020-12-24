# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/martensm/fizzbotz/tests/test_util.py
# Compiled at: 2016-02-18 00:02:19
# Size of source mod 2**32: 470 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, codecs, pytest
from os import path
import fizzbotz

@pytest.mark.asyncio
async def test_get_html():
    file_path = path.join(path.dirname(__file__), 'test_files', 'httpbin_html.html')
    with codecs.open(file_path, 'r', 'utf-8') as (test_file):
        expected_html = test_file.read()[:-1]
    @py_assert0 = await fizzbotz.util.get_markup('http://httpbin.org/html')
    @py_assert2 = @py_assert0 == expected_html
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected_html)) % {'py3': @pytest_ar._saferepr(expected_html) if 'expected_html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_html) else 'expected_html', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None