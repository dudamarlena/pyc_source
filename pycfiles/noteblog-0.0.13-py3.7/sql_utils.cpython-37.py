# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/sql_utils.py
# Compiled at: 2019-05-05 05:44:49
# Size of source mod 2**32: 17419 bytes
"""
@author = super_fazai
@File    : sql_utils.py
@Time    : 2016/7/14 14:36
@connect : superonesfazai@gmail.com
"""
import sqlite3
from gc import collect
from time import sleep
from pymysql import connect, IntegrityError
from redis import ConnectionPool, StrictRedis
from .common_utils import _print
__all__ = [
 'BaseSqlServer',
 'BaseRedisCli',
 'BaseSqlite3Cli',
 'pretty_table']

class BaseSqlServer(object):
    __doc__ = '\n    sql_utils for sql_server\n    '

    def __init__(self, host, user, passwd, db, port):
        super(BaseSqlServer, self).__init__()
        self.is_connect_success = True
        self.dead_lock_retry_num = 3
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self._init_conn()

    def _init_conn(self):
        try:
            self.conn = connect(host=(self.host),
              user=(self.user),
              password=(self.passwd),
              database=(self.db),
              port=(self.port),
              charset='utf8')
        except Exception:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def _select_table(self, sql_str, params=None, lock_timeout=20000, logger=None):
        """
        搜索
        :param sql_str:
        :param params:
        :param lock_timeout:
        :return:
        """
        result = None
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])), logger=logger, log_level=2)
                return result
            finally:
                e = None
                del e

        try:
            try:
                cs.execute('set tran isolation level read uncommitted;')
                cs.execute('set lock_timeout {0};'.format(lock_timeout))
                if params is not None:
                    if not isinstance(params, tuple):
                        params = tuple(params)
                    cs.execute(sql_str, params)
                else:
                    cs.execute(sql_str)
                result = cs.fetchall()
            except Exception as e:
                try:
                    _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
                finally:
                    e = None
                    del e

        finally:
            return

        try:
            cs.close()
        except Exception:
            pass

        return result

    def _insert_into_table(self, sql_str, params: tuple):
        """
        插入表数据
        :param sql_str:
        :param params:
        :return:
        """
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])))
                return _
            finally:
                e = None
                del e

        try:
            try:
                cs.execute('set deadlock_priority low;')
                cs.execute(sql_str.encode('utf-8'), params)
                self.conn.commit()
                print('[+] add to db!')
                _ = True
            except IntegrityError:
                print('重复插入...')
                _ = True
            except Exception as e:
                try:
                    print('---------| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
                    print('---------| 错误如下: ', e)
                    print('---------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
                finally:
                    e = None
                    del e

        finally:
            return

        try:
            cs.close()
        except Exception:
            pass

        return _

    def _insert_into_table_2(self, sql_str, params: tuple, logger, set_deadlock_priority_low=True):
        """
        :param sql_str:
        :param params:
        :param logger:
        :param set_deadlock_priority_low: 是否设置死锁等级低
        :return:
        """
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])), logger=logger, log_level=2)
                return _
            finally:
                e = None
                del e

        try:
            try:
                if set_deadlock_priority_low:
                    cs.execute('set deadlock_priority low;')
                cs.execute(sql_str.encode('utf-8'), params)
                self.conn.commit()
                logger.info('[+] add to db!')
                _ = True
            except IntegrityError:
                logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])
                _ = True
            except Exception:
                logger.error(('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: %s' % params[0]), exc_info=True)

        finally:
            return

        try:
            cs.close()
        except Exception:
            pass

        return _

    async def _insert_into_table_3(self, sql_str, params: tuple, logger, error_msg_dict=None):
        """
        异步
            error_msg_dict参数:
                eg: {
                    # 重复插入
                    'repeat_error': {
                        'field_name': '重复插入要记录的字段名',
                        'field_value': '重复记录该字段的值',
                    },
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :return:
        """
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])), logger=logger, log_level=2)
                return _
            finally:
                e = None
                del e

        try:
            try:
                cs.execute('set deadlock_priority low;')
                cs.execute(sql_str.encode('utf-8'), params)
                self.conn.commit()
                logger.info('[+] add to db!')
                _ = True
            except IntegrityError:
                if not error_msg_dict:
                    logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])
                    _ = True
                else:
                    if isinstance(error_msg_dict, dict):
                        msg = '重复插入{0}[{1}], 此处跳过!'.format(error_msg_dict.get('repeat_error', {}).get('field_name', ''), error_msg_dict.get('repeat_error', {}).get('field_value', ''))
                        logger.info(msg)
                        _ = True
                    else:
                        raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')
            except Exception:
                if not error_msg_dict:
                    logger.error(('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[0])), exc_info=True)
                else:
                    if isinstance(error_msg_dict, dict):
                        msg = '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                        for item in error_msg_dict.get('other_error', []):
                            msg += '出错{0}: {1} '.format(item.get('field_name', ''), item.get('field_value', ''))

                        logger.error(msg, exc_info=True)
                    else:
                        raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')

        finally:
            return

        try:
            cs.close()
        except Exception:
            pass

        return _

    def _update_table(self, sql_str, params: tuple):
        """
        更新表数据
        :param sql_str:
        :param params:
        :return: bool
        """
        ERROR_NUMBER = 0
        RETRY_NUM = self.dead_lock_retry_num
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg='遇到错误:', exception=e)
                return _
            finally:
                e = None
                del e

        while RETRY_NUM > 0:
            try:
                try:
                    cs.execute('set deadlock_priority low;')
                    cs.execute(sql_str, params)
                    self.conn.commit()
                    print('[+] add to db!')
                    _ = True
                    RETRY_NUM = 0
                except Exception as e:
                    try:
                        try:
                            ERROR_NUMBER = e.number
                        except:
                            pass

                        if ERROR_NUMBER == 1025:
                            print('遇到死锁!!进入等待...')
                            sleep(1)
                            RETRY_NUM -= 1
                        else:
                            print('---------| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
                            print('--------------------| 错误如下: ', e)
                            RETRY_NUM = 0
                    finally:
                        e = None
                        del e

            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    def _update_table_2(self, sql_str, params: tuple, logger):
        ERROR_NUMBER = 0
        RETRY_NUM = self.dead_lock_retry_num
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])), logger=logger, log_level=2)
                return _
            finally:
                e = None
                del e

        while RETRY_NUM > 0:
            try:
                try:
                    cs.execute('set deadlock_priority low;')
                    cs.execute(sql_str, params)
                    self.conn.commit()
                    logger.info('[+] add to db!')
                    _ = True
                    RETRY_NUM = 0
                except Exception as e:
                    try:
                        try:
                            ERROR_NUMBER = e.number
                        except:
                            pass

                        if ERROR_NUMBER == 1025:
                            logger.error('遇到死锁!!进入等待...')
                            sleep(1)
                            RETRY_NUM -= 1
                        else:
                            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % params[(-1)])
                            logger.exception(e)
                            RETRY_NUM = 0
                    finally:
                        e = None
                        del e

            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    async def _update_table_3(self, sql_str, params: tuple, logger, error_msg_dict=None):
        """
        异步更新数据
            error_msg_dict参数:
                eg: {
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :return:
        """
        ERROR_NUMBER = 0
        RETRY_NUM = self.dead_lock_retry_num
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg=(str(e.args[0])), logger=logger, log_level=2)
                return _
            finally:
                e = None
                del e

        while RETRY_NUM > 0:
            try:
                try:
                    cs.execute('set deadlock_priority low;')
                    cs.execute(sql_str, params)
                    self.conn.commit()
                    logger.info('[+] add to db!')
                    _ = True
                    RETRY_NUM = 0
                except Exception as e:
                    try:
                        try:
                            ERROR_NUMBER = e.number
                        except:
                            pass

                        if ERROR_NUMBER == 1025:
                            sleep(1)
                            RETRY_NUM -= 1
                            logger.error('遇到死锁!!进入等待...')
                        else:
                            RETRY_NUM = 0
                            if not error_msg_dict:
                                logger.error(('---------' + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[(-1)])), exc_info=True)
                            else:
                                if isinstance(error_msg_dict, dict):
                                    msg = '---------| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                                    for item in error_msg_dict.get('other_error', []):
                                        msg += '出错{0}: {1} '.format(item.get('field_name', ''), item.get('field_value', ''))

                                    logger.error(msg, exc_info=True)
                                else:
                                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')
                    finally:
                        e = None
                        del e

            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    def _delete_table(self, sql_str, params=None, lock_timeout=20000):
        _ = False
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            try:
                _print(msg='遇到错误:', exception=e)
                return _
            finally:
                e = None
                del e

        try:
            try:
                cs.execute('set lock_timeout {0};'.format(lock_timeout))
                if params is not None:
                    if not isinstance(params, tuple):
                        params = tuple(params)
                    cs.execute(sql_str, params)
                else:
                    cs.execute(sql_str)
                self.conn.commit()
                _ = True
            except Exception as e:
                try:
                    print('删除时报错: ', e)
                finally:
                    e = None
                    del e

        finally:
            return

        try:
            cs.close()
        except Exception:
            pass

        return _

    def _get_one_select_cursor(self, sql_str, params=None, lock_timeout=20000):
        """
        获得一个select执行结果的cursor(用于美化打印table)
        :return: 查询失败 None | 成功的cursor
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
        except AttributeError as e:
            try:
                print(e.args[0])
                return cursor
            finally:
                e = None
                del e

        try:
            cursor.execute('set lock_timeout {0};'.format(lock_timeout))
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cursor.execute(sql_str, params)
            else:
                cursor.execute(sql_str)
        except Exception as e:
            try:
                print(e)
                cursor = None
                return cursor
            finally:
                e = None
                del e

        return cursor

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass

        collect()


def pretty_table(cursor):
    """
    美化打印table返回的数据(只支持select)
    :param cursor: cursor数据库的游标
    :return: None
    """
    from prettytable import from_db_cursor
    tb = from_db_cursor(cursor=cursor)
    tb.align = 'l'
    print(tb)


class BaseRedisCli:
    __doc__ = 'redis客户端'

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.pool = ConnectionPool(host=host,
          port=port,
          db=db)
        self.redis_cli = StrictRedis(connection_pool=(self.pool))

    def set(self, name, value):
        """写/改"""
        return self.redis_cli.set(name=name, value=value)

    def get(self, name):
        """读"""
        return self.redis_cli.get(name=name)

    def delete(self, name):
        """删"""
        return self.redis_cli.delete(name)

    def __del__(self):
        try:
            del self.pool
            del self.redis_cli
        except:
            pass

        collect()


class BaseSqlite3Cli(object):
    __doc__ = "\n    sqlite3 obj\n        always use:\n            1. 查看db中所有表: select name from sqlite_master where type='table' order by name;\n    "

    def __init__(self, db_path):
        self.conn = sqlite3.connect(database=db_path)

    def _execute(self, sql_str, params: (dict, tuple)=None) -> sqlite3.Cursor:
        """
        执行(结果可根据相应db操作查看结果)(切记游标每次用完close())
        :param sql_str:
        :param params:
        :return:
        """
        cursor = self.conn.cursor()
        try:
            if params is None:
                cursor.execute(sql_str)
            else:
                cursor.execute(sql_str, params)
            self.conn.commit()
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        return cursor

    def __del__(self):
        try:
            del self.conn
        except:
            pass

        collect()