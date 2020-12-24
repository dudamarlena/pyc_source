# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pytest_gui_status\status_plugin\plugin.py
# Compiled at: 2016-01-22 23:49:56
import shlex, subprocess, time, sys, redis, os, psutil, datetime
from ..utils import s
from ..utils import REDIS_PORT, command_redis_server, command_status_gui_gen

class Helpers(object):

    @staticmethod
    def on_start(dir_name):
        """
        Init redis on start of pytest.

        dir_name - Name of directory from which pytest started
        """
        command_redis_server_args = shlex.split(command_redis_server)
        print 'Starting up redis'
        redis_popen_obj = subprocess.Popen(command_redis_server_args)
        time.sleep(1)
        if redis_popen_obj.poll() is None:
            print 'Started successfully redis'
        else:
            print 'Redis couldnt start there, trying to check if already running on that port'
            redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
            if redis_db.ping() and s(redis_db.get('PYTEST_STATUS_DB')) == '1':
                print 'Yup, it was already running'
            else:
                print '** Not found existing redis, couldnt connect, check! **'
                print ('debug pinging... {ping_result}').format(ping_result=redis_db.ping())
                print ('debug PYTEST_STATUS_DB ==... {0}').format(s(redis_db.get('PYTEST_STATUS_DB')))
                sys.exit()
        hash_dir_name = hash(dir_name)
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        redis_pipe = redis_db.pipeline()
        redis_pipe.set('PYTEST_STATUS_DB', '1')
        redis_pipe.hset('directories_to_hash', dir_name, hash_dir_name)
        redis_pipe.execute()
        Helpers.on_start_reset(dir_name)
        redis_db.set(('{hash_a}_state').format(hash_a=hash_dir_name), 'start')
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def start_gui(dir_name):
        """
        Init status_gui at start
        """
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        if not hash_dir_name is not None:
            raise AssertionError
            existing_gui_pid = s(redis_db.get(('{hash_a}_gui_pid').format(hash_a=hash_dir_name)))
            if existing_gui_pid:
                existing_gui_pid = int(existing_gui_pid)
            norm_dir_name = existing_gui_pid and psutil.pid_exists(existing_gui_pid) or os.path.normpath(dir_name)
            command_status_gui = command_status_gui_gen.format(norm_dir_name=norm_dir_name)
            gui_popen_obj = subprocess.Popen(command_status_gui)
            gui_pid = gui_popen_obj.pid
            redis_db.set(('{hash_a}_gui_pid').format(hash_a=hash_dir_name), gui_pid)
        return

    @staticmethod
    def on_collectstart(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        redis_db.set(('{hash_a}_state').format(hash_a=hash_dir_name), 'collect')
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def on_collectend(dir_name, list_test_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        if list_test_name:
            redis_db.rpush(('{hash_a}_collect').format(hash_a=hash_dir_name), *list_test_name)
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def on_test_eachstart(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        redis_db.set(('{hash_a}_state').format(hash_a=hash_dir_name), 'runtest')
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def on_test_eachend(dir_name, list_test_result):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        list_testname_pass = [ test_result.nodeid for test_result in list_test_result if test_result.outcome == 'passed'
                             ]
        list_testname_fail = [ test_result.nodeid for test_result in list_test_result if test_result.outcome == 'failed'
                             ]
        list_testname_skip = [ test_result.nodeid for test_result in list_test_result if test_result.outcome == 'skipped'
                             ]
        redis_pipe = redis_db.pipeline()
        if list_testname_pass:
            redis_pipe.lpush(('{hash_a}_pass').format(hash_a=hash_dir_name), *list_testname_pass)
        if list_testname_fail:
            redis_pipe.lpush(('{hash_a}_fail').format(hash_a=hash_dir_name), *list_testname_fail)
        if list_testname_skip:
            redis_pipe.lpush(('{hash_a}_skip').format(hash_a=hash_dir_name), *list_testname_skip)
        redis_pipe.execute()
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def on_end(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        redis_db.set(('{hash_a}_state').format(hash_a=hash_dir_name), 'end')
        Helpers.modify_last_updated(dir_name)
        return

    @staticmethod
    def on_start_reset(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        list_gen_varname = [
         '{hash_a}_state', '{hash_a}_last_updated', '{hash_a}_collect', '{hash_a}_pass', '{hash_a}_fail', '{hash_a}_skip']
        list_cur_varname = [ varname.format(hash_a=hash_dir_name) for varname in list_gen_varname ]
        del list_gen_varname
        redis_db.delete(*list_cur_varname)
        return

    @staticmethod
    def modify_last_updated(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = s(redis_db.hget('directories_to_hash', dir_name))
        assert hash_dir_name is not None
        cur_iso_datetime = datetime.datetime.now().isoformat()
        redis_db.set(('{hash_a}_last_updated').format(hash_a=hash_dir_name), cur_iso_datetime)
        return


class PYTEST_DATA(object):
    data = {}


def pytest_addoption(parser):
    parser.addoption('--show_status_gui', dest='show_status_gui', action='store_true')


def pytest_configure(config):
    pass


def pytest_sessionstart(session):
    config = session.config
    PYTEST_DATA.data['dir_name_start'] = str(session.startdir)
    Helpers.on_start(PYTEST_DATA.data['dir_name_start'])
    if config.getoption('show_status_gui'):
        Helpers.start_gui(PYTEST_DATA.data['dir_name_start'])


def pytest_collectstart(collector):
    Helpers.on_collectstart(PYTEST_DATA.data['dir_name_start'])


def pytest_itemcollected(item):
    Helpers.on_collectend(PYTEST_DATA.data['dir_name_start'], [item.nodeid])


def pytest_runtest_logstart(nodeid, location):
    Helpers.on_test_eachstart(PYTEST_DATA.data['dir_name_start'])


def pytest_runtest_logreport(report):
    if report.when == 'call':
        Helpers.on_test_eachend(PYTEST_DATA.data['dir_name_start'], [report])


def pytest_sessionfinish(session, exitstatus):
    Helpers.on_end(PYTEST_DATA.data['dir_name_start'])