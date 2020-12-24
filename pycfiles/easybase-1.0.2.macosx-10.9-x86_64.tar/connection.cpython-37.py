# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/connection.py
# Compiled at: 2019-12-20 08:49:15
# Size of source mod 2**32: 14822 bytes
"""
EasyBase connection module.
"""
import logging
from six import iteritems, binary_type, text_type
from thriftpy2.transport import TSocket
from thriftpy2.transport import TBufferedTransport, TFramedTransport
from thriftpy2.protocol import TBinaryProtocol, TCompactProtocol
from thriftpy2.thrift import TClient
from thriftpy2.rpc import make_client
from HBase_thrift import TTableName, TTimeRange, TColumnFamilyDescriptor, TTableDescriptor
from HBase_thrift import THBaseService as HBase
from .table import Table
from .util import pep8_to_camel_case
logger = logging.getLogger(__name__)
COMPAT_MODES = ('0.90', '0.92', '0.94', '0.96', '0.98', '2.2.0')
THRIFT_TRANSPORTS = dict(buffered=TBufferedTransport,
  framed=TFramedTransport)
THRIFT_PROTOCOLS = dict(binary=TBinaryProtocol,
  compact=TCompactProtocol)
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9090
DEFAULT_TRANSPORT = 'buffered'
DEFAULT_COMPAT = '0.96'
DEFAULT_PROTOCOL = 'binary'
STRING_OR_BINARY = (
 binary_type, text_type)

class Connection(object):
    __doc__ = 'Connection to an HBase Thrift server.\n\n    The `host` and `port` arguments specify the host name and TCP port\n    of the HBase Thrift server to connect to. If omitted or ``None``,\n    a connection to the default port on ``localhost`` is made. If\n    specifed, the `timeout` argument specifies the socket timeout in\n    milliseconds.\n\n    If `autoconnect` is `True` (the default) the connection is made\n    directly, otherwise :py:meth:`Connection.open` must be called\n    explicitly before first use.\n\n    The optional `table_prefix` and `table_prefix_separator` arguments\n    specify a prefix and a separator string to be prepended to all table\n    names, e.g. when :py:meth:`Connection.table` is invoked. For\n    example, if `table_prefix` is ``myproject``, all tables tables will\n    have names like ``myproject_XYZ``.\n\n    The optional `compat` argument sets the compatibility level for\n    this connection. Older HBase versions have slightly different Thrift\n    interfaces, and using the wrong protocol can lead to crashes caused\n    by communication errors, so make sure to use the correct one. This\n    value can be either the string ``0.90``, ``0.92``, ``0.94``, or\n    ``0.96`` (the default).\n\n    The optional `transport` argument specifies the Thrift transport\n    mode to use. Supported values for this argument are ``buffered``\n    (the default) and ``framed``. Make sure to choose the right one,\n    since otherwise you might see non-obvious connection errors or\n    program hangs when making a connection. HBase versions before 0.94\n    always use the buffered transport. Starting with HBase 0.94, the\n    Thrift server optionally uses a framed transport, depending on the\n    argument passed to the ``hbase-daemon.sh start thrift`` command.\n    The default ``-threadpool`` mode uses the buffered transport; the\n    ``-hsha``, ``-nonblocking``, and ``-threadedselector`` modes use the\n    framed transport.\n\n    The optional `protocol` argument specifies the Thrift transport\n    protocol to use. Supported values for this argument are ``binary``\n    (the default) and ``compact``. Make sure to choose the right one,\n    since otherwise you might see non-obvious connection errors or\n    program hangs when making a connection. ``TCompactProtocol`` is\n    a more compact binary format that is  typically more efficient to\n    process as well. ``TBinaryProtocol`` is the default protocol that\n    Happybase uses.\n\n    .. versionadded:: 0.9\n       `protocol` argument\n\n    .. versionadded:: 0.5\n       `timeout` argument\n\n    .. versionadded:: 0.4\n       `table_prefix_separator` argument\n\n    .. versionadded:: 0.4\n       support for framed Thrift transports\n\n    :param str host: The host to connect to\n    :param int port: The port to connect to\n    :param int timeout: The socket timeout in milliseconds (optional)\n    :param bool autoconnect: Whether the connection should be opened directly\n    :param str table_prefix: Prefix used to construct table names (optional)\n    :param str table_prefix_separator: Separator used for `table_prefix`\n    :param str compat: Compatibility mode (optional)\n    :param str transport: Thrift transport mode (optional)\n    '

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=None, autoconnect=True, table_prefix=None, table_prefix_separator='_', compat=DEFAULT_COMPAT, transport=DEFAULT_TRANSPORT, protocol=DEFAULT_PROTOCOL):
        if transport not in THRIFT_TRANSPORTS:
            raise ValueError("'transport' must be one of %s" % ', '.join(THRIFT_TRANSPORTS.keys()))
        else:
            if table_prefix is not None:
                if not isinstance(table_prefix, str):
                    raise TypeError("'table_prefix' must be a string")
            assert isinstance(table_prefix_separator, str), "'table_prefix_separator' must be a string"
        if compat not in COMPAT_MODES:
            raise ValueError("'compat' must be one of %s" % ', '.join(COMPAT_MODES))
        if protocol not in THRIFT_PROTOCOLS:
            raise ValueError("'protocol' must be one of %s" % ', '.join(THRIFT_PROTOCOLS))
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.timeout = timeout
        self.table_prefix = table_prefix
        self.table_prefix_separator = table_prefix_separator
        self.compat = compat
        self._transport_class = THRIFT_TRANSPORTS[transport]
        self._protocol_class = THRIFT_PROTOCOLS[protocol]
        self._refresh_thrift_client()
        self._initialized = True

    def _refresh_thrift_client(self):
        """Refresh the Thrift socket, transport, and client."""
        self.client = make_client(HBase, (self.host), port=(self.port), timeout=(self.timeout))

    def _table_name(self, name):
        """Construct a table name by optionally adding a table name prefix."""
        if self.table_prefix is None:
            return name
        return self.table_prefix + self.table_prefix_separator + name

    def open(self):
        """Open the underlying transport to the HBase instance.

        This method opens the underlying Thrift transport (TCP connection).
        """
        logger.debug('Opening Thrift transport to %s:%d', self.host, self.port)

    def close(self):
        """Close the underyling transport to the HBase instance.

        This method closes the underlying Thrift transport (TCP connection).
        """
        self.client.close()

    def __del__(self):
        try:
            self._initialized
        except AttributeError:
            return
        else:
            self.close()

    def table(self, name, use_prefix=True):
        """Return a table object.

        Returns a :py:class:`easybase.Table` instance for the table
        named `name`. This does not result in a round-trip to the
        server, and the table is not checked for existence.

        The optional `use_prefix` argument specifies whether the table
        prefix (if any) is prepended to the specified `name`. Set this
        to `False` if you want to use a table that resides in another
        ‘prefix namespace’, e.g. a table from a ‘friendly’ application
        co-hosted on the same HBase instance. See the `table_prefix`
        argument to the :py:class:`Connection` constructor for more
        information.

        :param str name: the name of the table
        :param bool use_prefix: whether to use the table prefix (if any)
        :return: Table instance
        :rtype: :py:class:`Table`
        """
        if use_prefix:
            name = self._table_name(name)
        return Table(name, self)

    def tables(self):
        """Return a list of table names available in this HBase instance.

        If a `table_prefix` was set for this :py:class:`Connection`, only
        tables that have the specified prefix will be listed.

        :return: The table names
        :rtype: List of strings
        """
        raise NotImplementedError('not implemented yet')

    def create_table(self, name, families):
        """Create a table.

        :param str name: The table name
        :param dict families: The name and options for each column family

        The `families` argument is a dictionary mapping column family
        names to a dictionary containing the options for this column
        family, e.g.

        ::

            families = {
                'cf1': dict(max_versions=10),
                'cf2': dict(max_versions=1, block_cache_enabled=False),
                'cf3': dict(),  # use defaults
            }
            connection.create_table('mytable', families)

        These options correspond to the ColumnDescriptor structure in
        the Thrift API, but note that the names should be provided in
        Python style, not in camel case notation, e.g. `time_to_live`,
        not `timeToLive`. The following options are supported:

        * ``max_versions`` (`int`)
        * ``compression`` (`str`)
        * ``in_memory`` (`bool`)
        * ``bloom_filter_type`` (`str`)
        * ``bloom_filter_vector_size`` (`int`)
        * ``bloom_filter_nb_hashes`` (`int`)
        * ``block_cache_enabled`` (`bool`)
        * ``time_to_live`` (`int`)
        """
        name = self._table_name(name)
        if not isinstance(families, dict):
            raise TypeError("'families' arg must be a dictionary")
        if not families:
            raise ValueError('Cannot create table %r (no column families specified)' % name)
        family_desc = []
        for cf_name, options in iteritems(families):
            if options is None:
                options = dict()
            kwargs = dict()
            for option_name, value in iteritems(options):
                if isinstance(value, STRING_OR_BINARY):
                    value = value.encode()
                kwargs[pep8_to_camel_case(option_name)] = value

            cf = TColumnFamilyDescriptor(name=cf_name.encode(), **kwargs)
            family_desc.append(cf)

        tbl_name = TTableName(ns=None, qualifier=(name.encode()))
        tdesc = TTableDescriptor(tableName=tbl_name, columns=family_desc)
        self.client.createTable(tdesc, splitKeys=None)

    def delete_table(self, name, disable=False):
        """Delete the specified table.

        .. versionadded:: 0.5
           `disable` argument

        In HBase, a table always needs to be disabled before it can be
        deleted. If the `disable` argument is `True`, this method first
        disables the table if it wasn't already and then deletes it.

        :param str name: The table name
        :param bool disable: Whether to first disable the table if needed
        """
        if disable:
            if self.is_table_enabled(name):
                self.disable_table(name)
        self.client.deleteTable(self.get_tablename(name))

    def enable_table(self, name):
        """Enable the specified table.

        :param str name: The table name
        """
        self.client.enableTable(self.get_tablename(name))

    def disable_table(self, name):
        """Disable the specified table.

        :param str name: The table name
        """
        self.client.disableTable(self.get_tablename(name))

    def is_table_enabled(self, name):
        """Return whether the specified table is enabled.

        :param str name: The table name

        :return: whether the table is enabled
        :rtype: bool
        """
        return self.client.isTableEnabled(self.get_tablename(name))

    def compact_table(self, name, major=False):
        """Compact the specified table.

        :param str name: The table name
        :param bool major: Whether to perform a major compaction.
        """
        raise NotImplementedError('not implement yet')

    def exist_table(self, name):
        """Return whether the sepcified table is exists

        :param str name: The table name
        :return whether the table is exists
        :rtype: bool
        """
        return self.client.tableExists(self.get_tablename(name))

    def get_tablename(self, name):
        """Return the py:class:TTableName class of the spcified table name

        :param str name: The table name
        :return the py:class:TTableName Class
        :rtype: class
        """
        return TTableName(ns=None, qualifier=(self._table_name(name).encode()))