# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_differ.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 2328 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from abp.filters.renderer import render_diff
BASE = '[Adblock Plus 2.0]\n! Version: 111\n! diff-url: https://easylist-downloads.adblockplus.org/easylist/diffs/111.txt\n! diff-expires: 1 hours\n! Title: EasyList\n! Expires: 1 days (update frequency)\n! Homepage: https://easylist.to/\n! Licence: https://easylist.to/pages/licence.html\n!\n! Please report any unblocked adverts or problems\n! in the forums (https://forums.lanik.us/)\n! or via e-mail (easylist.subscription@gmail.com).\n!\n!-----------------------General advert blocking filters-----------------------!\n! *** easylist:easylist/easylist_general_block.txt ***\ntest\n&act=ads_\n&ad.vid=$~xmlhttprequest\n&ad_box_\n'
LATEST = '[Adblock Plus 2.0]\n! Version: 123\n! Diff-URL: https://easylist-downloads.adblockplus.org/easylist/diffs/123.txt\n! Diff-Expires: 1 hours\n! Title: EasyList\n! Homepage: https://easylist.to/\n! Licence: https://easylist.to/pages/licence.html\n!\n! Please report any unblocked adverts or problems\n! in the forums (https://forums.lanik.us/)\n! or via e-mail (easylist.subscription@gmail.com).\n!\n!-----------------------General advert blocking filters-----------------------!\n! *** easylist:easylist/easylist_general_block.txt ***\n&act=ads_\n&ad_box_\n&ad_channel=£\n test\n&test_\n'
EXPECTED = '[Adblock Plus Diff]\n! Diff-URL: https://easylist-downloads.adblockplus.org/easylist/diffs/123.txt\n! Expires:\n! Version: 123\n- &ad.vid=$~xmlhttprequest\n+ &ad_channel=£\n+ &test_\n'

def test_differ():
    exp = set(EXPECTED.splitlines())
    gen = set(render_diff(BASE.splitlines(), LATEST.splitlines()))
    @py_assert1 = gen == exp
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_differ.py', lineno=76)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (gen, exp)) % {'py0':@pytest_ar._saferepr(gen) if 'gen' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen) else 'gen',  'py2':@pytest_ar._saferepr(exp) if 'exp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp) else 'exp'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None