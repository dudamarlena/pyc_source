# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/pg_python/_db_object.py
# Compiled at: 2019-10-12 05:47:14
import logging, psycopg2, socket

class Db(object):
    params = None
    connection = None
    logger = None

    def __init__(self, params):
        self.send_keep_alive_probes = params.pop('send_keep_alive_probes', False)
        self.socket_idle_time = params.pop('socket_idle_time', 120)
        self.params = params
        self._make_connection()

    def _make_connection(self):
        logging.debug(self.params)
        try:
            self.connection = psycopg2.connect(**self.params)
            if self.send_keep_alive_probes:
                self.socket_configuration()
        except psycopg2.DatabaseError as e:
            logging.error('Could not connect to the server: %s' % e)
        except psycopg2.Error as e:
            logging.error('Error %s' % e)
        except Exception as e:
            logging.error('Error %s' % e)

    def get_connection(self):
        return self.connection

    def socket_configuration(self):
        try:
            pg_socket = socket.fromfd(self.connection.fileno(), socket.AF_INET, socket.SOCK_STREAM)
            pg_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            pg_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.socket_idle_time)
            pg_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
            pg_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        except Exception as e:
            logging.error('Failed To Configure Socket')
            logging.error(e)

    def get_cursor(self):
        try:
            cursor = self.connection.cursor()
            return cursor
        except Exception as err:
            logging.warning('Connection seems to have expired, remaking it')
            try:
                self._make_connection()
                cursor = self.connection.cursor()
                return cursor
            except Exception as e:
                logging.error('Connection could not be made: %s' % e)
                return

        return

    def close_cursor(self, cursor):
        logging.debug('Closing cursor...')
        cursor.close()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        logging.info('Closing connection...')
        self.connection.close()