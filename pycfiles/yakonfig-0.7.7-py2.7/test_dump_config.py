# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yakonfig/tests/test_dump_config.py
# Compiled at: 2015-07-07 22:00:14
import argparse, sys, time, pytest, pexpect, yakonfig

def toy_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--thing')
    modules = [yakonfig]
    args = yakonfig.parse_args(parser, modules)
    config = yakonfig.get_global_config()


@pytest.mark.parametrize(('dump_config', ), [
 ('full', ),
 ('default', ),
 ('effective', )])
def test_cli_dump(request, dump_config):
    cmd = 'python -m yakonfig.tests.test_dump_config --thing foo --dump-config %s' % dump_config
    child = pexpect.spawn(cmd)
    child.logfile = sys.stdout
    time.sleep(2)
    child.expect(pexpect.EOF, timeout=180)
    time.sleep(0.2)
    assert not child.isalive()
    assert child.exitstatus == 0


if __name__ == '__main__':
    toy_main()