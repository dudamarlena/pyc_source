# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/tools_test/factory_test.py
# Compiled at: 2019-10-16 15:59:54
# Size of source mod 2**32: 4000 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, subprocess, pytest, paleomix.tools.factory as factory

class ProcError(RuntimeError):
    pass


def check_run(call, *args, **kwargs):
    devnull = os.open(os.devnull, os.O_RDONLY)
    kwargs.setdefault('stdin', devnull)
    kwargs.setdefault('close_fds', True)
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    returncode = kwargs.pop('expected_returncode', 0)
    proc = (subprocess.Popen)(call, *args, **kwargs)
    os.close(devnull)
    stdout, stderr = proc.communicate()
    if proc.returncode != returncode:
        raise ProcError('Command returned %i: %r:\nSTDOUT: %r\nSTDERR: %r' % (
         proc.returncode, call, stdout, stderr))
    return (
     stdout.decode('utf-8', 'replace'), stderr.decode('utf-8', 'replace'))


def test_paleomix_command():
    stdout, stderr = check_run(['paleomix'])
    @py_assert2 = ''
    @py_assert1 = stdout == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/tools_test/factory_test.py', lineno=65)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (stdout, @py_assert2)) % {'py0':@pytest_ar._saferepr(stdout) if 'stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stdout) else 'stdout',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'PALEOMIX - pipelines and tools for NGS data analyses.'
    @py_assert2 = @py_assert0 in stderr
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/tools_test/factory_test.py', lineno=66)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, stderr)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(stderr) if 'stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stderr) else 'stderr'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


FACTORY_COMMANDS = (('bam_pipeline', 'Usage: paleomix bam_pipeline <command> [options] [makefiles]'),
                    ('trim_pipeline', 'Usage: paleomix trim_pipeline <command> [options] [makefiles]'),
                    ('phylo_pipeline', 'Usage: paleomix phylo_pipeline <command> [options] [makefiles]'),
                    ('cleanup', 'usage: paleomix cleanup --temp-prefix prefix --fasta reference.fasta < in.sam'),
                    ('coverage', 'usage: paleomix coverage [options] sorted.bam [out.coverage]'),
                    ('depths', 'usage: paleomix depths [options] sorted.bam [out.depths]'),
                    ('duphist', 'usage: paleomix duphist sorted.bam > out.histogram'),
                    ('rmdup_collapsed', 'usage: paleomix rmdup_collapsed [options] < sorted.bam > out.bam'),
                    ('genotype', 'usage: paleomix genotype [options] sorted.bam out.vcf.bgz'),
                    ('gtf_to_bed', 'usage: paleomix gtf_to_bed [options] in.gtf out_prefix [in.scaffolds]'),
                    ('vcf_filter', 'Usage: paleomix vcf_filter [options] [in1.vcf, ...]'),
                    ('vcf_to_fasta', 'usage: paleomix vcf_to_fasta [options] --genotype in.vcf --intervals in.bed'),
                    ('cat', 'usage: paleomix cat [-h] [--output OUTPUT] file [file ...]'))

@pytest.mark.parametrize('command, expected', FACTORY_COMMANDS)
def test_factory__commands(command, expected):
    cmd = factory.new(command)
    call = cmd.finalized_call
    if command in ('bam_pipeline', 'trim_pipeline'):
        call.append('run')
    stdout, stderr = check_run(call + ['--help'])
    @py_assert0 = stdout.split('\n')[0]
    @py_assert2 = @py_assert0 == expected
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/tools_test/factory_test.py', lineno=111)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = ''
    @py_assert1 = stderr == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/tools_test/factory_test.py', lineno=112)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (stderr, @py_assert2)) % {'py0':@pytest_ar._saferepr(stderr) if 'stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stderr) else 'stderr',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None