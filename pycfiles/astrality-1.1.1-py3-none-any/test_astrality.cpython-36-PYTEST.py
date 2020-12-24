# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_astrality.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 3794 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, os, psutil, signal, subprocess, time, pytest
from astrality.astrality import main, kill_old_astrality_processes
from astrality import utils
from astrality.tests.utils import Retry
from astrality.xdg import XDG

@pytest.mark.slow
def test_termination_of_main_process():
    astrality_process = subprocess.Popen([
     './bin/astrality'],
      stdout=(subprocess.PIPE),
      preexec_fn=(os.setsid))
    time.sleep(2)
    os.killpg(os.getpgid(astrality_process.pid), signal.SIGTERM)
    astrality_process.wait()
    @py_assert1 = astrality_process.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(astrality_process) if 'astrality_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(astrality_process) else 'astrality_process',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.slow
def test_interrupt_of_main_process():
    astrality_process = subprocess.Popen([
     './bin/astrality'],
      stdout=(subprocess.PIPE),
      preexec_fn=(os.setsid))
    time.sleep(2)
    os.killpg(os.getpgid(astrality_process.pid), signal.SIGINT)
    astrality_process.wait()
    @py_assert1 = astrality_process.returncode
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(astrality_process) if 'astrality_process' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(astrality_process) else 'astrality_process',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_enabling_specific_module_from_command_line(caplog, monkeypatch, test_config_directory):
    """Modules parameter to main should enable specific module(s)."""
    monkeypatch.setitem(os.environ, 'ASTRALITY_CONFIG_HOME', str(test_config_directory))
    main(modules=['../test_modules/two_modules::bangladesh'], test=True)
    @py_assert0 = (
     'astrality.utils', logging.INFO, 'Greetings from Dhaka!')
    @py_assert4 = caplog.record_tuples
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.record_tuples\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(caplog) if 'caplog' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(caplog) else 'caplog',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


class TestKillOldAstralityProcesses:
    __doc__ = 'Tests for astrality.astrality.kill_old_astrality_processes.'

    def test_killing_old_running_process(self):
        """The same running process should be killed."""
        perpetual_process = psutil.Popen([
         'python',
         '-c',
         '"from time import sleep; sleep(9999999999999)"'])
        pidfile = XDG().data('astrality.pid')
        utils.dump_yaml(data=perpetual_process.as_dict(attrs=[
         'pid', 'create_time', 'username']),
          path=pidfile)
        kill_old_astrality_processes()
        @py_assert1 = Retry()
        @py_assert3 = lambda : not perpetual_process.is_running()
        @py_assert5 = @py_assert1(@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None

    def test_not_killing_new_procces_with_same_pid(self):
        """The process should not be killed when it is not the original saved"""
        perpetual_process = psutil.Popen([
         'python',
         '-c',
         '"from time import sleep; sleep(9999999999999)"'])
        process_data = perpetual_process.as_dict(attrs=[
         'pid', 'create_time', 'username'])
        process_data['create_time'] += 1
        utils.dump_yaml(data=process_data,
          path=(XDG().data('astrality.pid')))
        kill_old_astrality_processes()
        @py_assert1 = Retry()
        @py_assert3 = lambda : perpetual_process.is_running()
        @py_assert5 = @py_assert1(@py_assert3)
        if not @py_assert5:
            @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s()\n}(%(py4)s)\n}') % {'py0':@pytest_ar._saferepr(Retry) if 'Retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Retry) else 'Retry',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        perpetual_process.kill()

    def test_trying_to_kill_process_no_longer_running(self):
        """No longer running processes should be handled gracefully."""
        finished_process = psutil.Popen(['echo', 'Done!'])
        process_data = finished_process.as_dict(attrs=[
         'pid', 'create_time', 'username'])
        finished_process.wait()
        utils.dump_yaml(data=process_data,
          path=(XDG().data('astrality.pid')))
        kill_old_astrality_processes()

    def test_killing_processes_when_no_previous_command_has_been_run(self):
        """The first ever invocation of the function should be handled."""
        pidfile = XDG().data('astrality.pid')
        pidfile.unlink()
        kill_old_astrality_processes()
        @py_assert1 = utils.load_yaml
        @py_assert4 = @py_assert1(path=pidfile)
        @py_assert8 = psutil.Process
        @py_assert10 = @py_assert8()
        @py_assert12 = @py_assert10.as_dict
        @py_assert14 = [
         'pid', 'create_time', 'username']
        @py_assert16 = @py_assert12(attrs=@py_assert14)
        @py_assert6 = @py_assert4 == @py_assert16
        if not @py_assert6:
            @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.load_yaml\n}(path=%(py3)s)\n} == %(py17)s\n{%(py17)s = %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s.Process\n}()\n}.as_dict\n}(attrs=%(py15)s)\n}', ), (@py_assert4, @py_assert16)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pidfile) if 'pidfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pidfile) else 'pidfile',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(psutil) if 'psutil' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(psutil) else 'psutil',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16)}
            @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
            raise AssertionError(@pytest_ar._format_explanation(@py_format20))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None