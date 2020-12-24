# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_q4m/__init__.py
# Compiled at: 2011-05-05 04:57:39
import python_q4m
__author__ = 'Tatsuhiko Kubo (cubicdaiya@gmail.com)'
__version__ = '0.0.6'
__license__ = 'GPL2'
__doc__ = "\nThis module is simple Q4M operation wrapper developed by pixiv Inc. for asynchronous upload system\n\nSimple example of usage is followings\n\n   >>> from python_q4m.q4m import *\n   >>> class QueueTable(Q4M):\n   >>>     def __init__(self, con):\n   >>>         super(self.__class__, self).__init__(con)\n   >>>         self.table   = 'queue_table'\n   >>>         self.columns = ['id',\n   >>>                         'msg',\n   >>>                        ]\n   >>> try:\n   >>>    con = MySQLdb.connect(host='localhost',\n   >>>                          db=dbname,\n   >>>                          user=username,\n   >>>                          passwd=password,\n   >>>                         )\n   >>>    q = QueueTable(con)\n   >>>    q.enqueue([1, 'msg'])\n   >>>    while q.wait() == 0:\n   >>>        time.sleep(1);\n   >>>     res = q.dequeue()\n   >>>     print res['id']\n   >>>     print res['msg']\n   >>>     q.end()\n   >>>     con.close()\n   >>> except MySQLdb.Error, e:\n   >>>     print 'Error %d: %s' % (e.args[0], e.args[1])\n   >>>     q.abort()\n   >>>     con.close()\n\nAnd it is necessary to create following table for above example.\n\nCREATE TABLE `queue_table` (`id` int(11) NOT NULL, `msg` text NOT NULL) ENGINE=QUEUE;\n\n"