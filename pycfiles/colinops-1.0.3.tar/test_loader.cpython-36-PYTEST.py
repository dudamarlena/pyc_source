# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/tests/unit/test_loader.py
# Compiled at: 2018-08-17 09:32:41
# Size of source mod 2**32: 3046 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, shutil, colin.checks
from colin.core.loader import CheckLoader

def test_upstream_checks_can_be_loaded():
    """ check whether all upstream checks can be loaded """
    colin_checks_path = colin.checks.__file__
    colin_checks_dir = os.path.dirname(colin_checks_path)
    l = CheckLoader([colin_checks_dir])
    @py_assert1 = l.check_classes
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s.check_classes\n}' % {'py0':@pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert0 = l.mapping['bzcomponent_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['architecture_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['bzcomponent_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['install_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['name_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['release_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['uninstall_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['version_label_capital_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['architecture_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['authoritative_source-url_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['build-date_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['com.redhat.build-host_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['com.redhat.component_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['description_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['description_or_io.k8s.description_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['distribution-scope_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['help_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['io.k8s.description_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['io.k8s.display-name_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['maintainer_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['name_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['release_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['summary_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['url_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['run_or_usage_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['vcs-ref_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['vcs-type_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['vcs-url_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['vendor_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['version_label']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['cmd_or_entrypoint']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['help_file_or_readme']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['no_root']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['shell_runnable']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['from_tag_not_latest']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['maintainer_deprecated']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None


def test_loading_custom_check(tmpdir):
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    a_check_dir = os.path.join(tests_dir, 'data', 'a_check')
    shutil.copytree(a_check_dir, str(tmpdir.join('a_check')))
    l = CheckLoader([str(tmpdir)])
    @py_assert2 = l.check_classes
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 3
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.check_classes\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(l) if 'l' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(l) else 'l',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = l.mapping['a-peter-file-check']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None
    @py_assert0 = l.mapping['this-is-a-funky-check']
    if not @py_assert0:
        @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert0 = None