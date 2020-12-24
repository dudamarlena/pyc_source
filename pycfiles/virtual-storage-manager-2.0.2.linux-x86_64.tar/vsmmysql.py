# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/diamond/handlers/vsmmysql.py
# Compiled at: 2016-06-13 14:11:03
"""
Insert the collected values into a mysql table
"""
from Handler import Handler
import MySQLdb

class VSMMySQLHandler(Handler):
    """
    Implements the abstract Handler class, sending data to a mysql table
    """
    conn = None

    def __init__(self, config=None):
        """
        Create a new instance of the VSMMySQLHandler class
        """
        Handler.__init__(self, config)
        self.hostname = self.config['hostname']
        self.port = int(self.config['port'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.table = self.config['table']
        self.col_time = self.config['col_time']
        self.col_metric = self.config['col_metric']
        self.col_value = self.config['col_value']
        self.col_hostname = self.config['col_hostname']
        self.col_instance = self.config['col_instance']
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(VSMMySQLHandler, self).get_default_config_help()
        config.update({})
        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(VSMMySQLHandler, self).get_default_config()
        config.update({})
        return config

    def __del__(self):
        """
        Destroy instance of the VSMMySQLHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric
        """
        self._send(str(metric))

    def _send(self, data):
        """
        Insert the data
        """
        data = data.strip().split(' ')
        data_name = data[0].split('.')
        if data_name[2] == 'cpu' and data_name[4] == 'idle' and data_name[3] != 'total':
            try:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO %s (%s, %s, %s, %s, %s) VALUES(%%s, %%s, %%s ,%%s, %%s)' % (
                 self.table, self.col_metric, self.col_hostname, self.col_instance,
                 self.col_time, self.col_value), (
                 ('_').join(data_name[2:4]), data_name[1], data_name[4], data[2], data[1]))
                cursor.close()
                self.conn.commit()
            except BaseException as e:
                self.log.error('VSMMySQLHandler: Failed sending data. %s.', e)
                self._connect()

        elif data_name[2] == 'CephCollector':
            metric_name = ('_').join(data_name[6:])
            if metric_name in ('osd_op_r', 'osd_op_w', 'osd_op_rw', 'osd_op_in_bytes',
                               'osd_op_out_bytes', 'osd_op_rw_latency_avgcount',
                               'osd_op_r_latency_avgcount', 'osd_op_w_latency_avgcount',
                               'osd_op_rw_latency_sum', 'osd_op_r_latency_sum', 'osd_op_w_latency_sum'):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute('INSERT INTO %s (%s, %s, %s, %s, %s) VALUES(%%s, %%s, %%s ,%%s, %%s)' % (
                     self.table, self.col_metric, self.col_hostname, self.col_instance,
                     self.col_time, self.col_value), (
                     ('_').join(data_name[6:]), data_name[1], ('_').join(data_name[4:6]), data[2], data[1]))
                    cursor.close()
                    self.conn.commit()
                except BaseException as e:
                    self.log.error('VSMMySQLHandler: Failed sending data. %s.', e)
                    self._connect()

    def _connect(self):
        """
        Connect to the MySQL server
        """
        self._close()
        self.conn = MySQLdb.Connect(host=self.hostname, port=self.port, user=self.username, passwd=self.password, db=self.database)

    def _close(self):
        """
        Close the connection
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()