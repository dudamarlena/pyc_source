# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/hbase/THBaseService.py
# Compiled at: 2019-09-05 21:58:10
# Size of source mod 2**32: 363799 bytes
from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec
import sys, logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []

class Iface(object):

    def exists(self, table, tget):
        """
        Test for the existence of columns in the table, as specified in the TGet.

        @return true if the specified TGet matches one or more keys, false if not

        Parameters:
         - table: the table to check on
         - tget: the TGet to check for
        """
        pass

    def existsAll(self, table, tgets):
        """
        Test for the existence of columns in the table, as specified by the TGets.

        This will return an array of booleans. Each value will be true if the related Get matches
        one or more keys, false if not.

        Parameters:
         - table: the table to check on
         - tgets: a list of TGets to check for
        """
        pass

    def get(self, table, tget):
        """
        Method for getting data from a row.

        If the row cannot be found an empty Result is returned.
        This can be checked by the empty field of the TResult

        @return the result

        Parameters:
         - table: the table to get from
         - tget: the TGet to fetch
        """
        pass

    def getMultiple(self, table, tgets):
        """
        Method for getting multiple rows.

        If a row cannot be found there will be a null
        value in the result list for that TGet at the
        same position.

        So the Results are in the same order as the TGets.

        Parameters:
         - table: the table to get from
         - tgets: a list of TGets to fetch, the Result list
        will have the Results at corresponding positions
        or null if there was an error
        """
        pass

    def put(self, table, tput):
        """
        Commit a TPut to a table.

        Parameters:
         - table: the table to put data in
         - tput: the TPut to put
        """
        pass

    def checkAndPut(self, table, row, family, qualifier, value, tput):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it adds the TPut.

        @return true if the new put was executed, false otherwise

        Parameters:
         - table: to check in and put to
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - value: the expected value, if not provided the
        check is for the non-existence of the
        column in question
         - tput: the TPut to put if the check succeeds
        """
        pass

    def putMultiple(self, table, tputs):
        """
        Commit a List of Puts to the table.

        Parameters:
         - table: the table to put data in
         - tputs: a list of TPuts to commit
        """
        pass

    def deleteSingle(self, table, tdelete):
        """
        Deletes as specified by the TDelete.

        Note: "delete" is a reserved keyword and cannot be used in Thrift
        thus the inconsistent naming scheme from the other functions.

        Parameters:
         - table: the table to delete from
         - tdelete: the TDelete to delete
        """
        pass

    def deleteMultiple(self, table, tdeletes):
        """
        Bulk commit a List of TDeletes to the table.

        Throws a TIOError if any of the deletes fail.

        Always returns an empty list for backwards compatibility.

        Parameters:
         - table: the table to delete from
         - tdeletes: list of TDeletes to delete
        """
        pass

    def checkAndDelete(self, table, row, family, qualifier, value, tdelete):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it adds the delete.

        @return true if the new delete was executed, false otherwise

        Parameters:
         - table: to check in and delete from
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - value: the expected value, if not provided the
        check is for the non-existence of the
        column in question
         - tdelete: the TDelete to execute if the check succeeds
        """
        pass

    def increment(self, table, tincrement):
        """
        Parameters:
         - table: the table to increment the value on
         - tincrement: the TIncrement to increment
        """
        pass

    def append(self, table, tappend):
        """
        Parameters:
         - table: the table to append the value on
         - tappend: the TAppend to append
        """
        pass

    def openScanner(self, table, tscan):
        """
        Get a Scanner for the provided TScan object.

        @return Scanner Id to be used with other scanner procedures

        Parameters:
         - table: the table to get the Scanner for
         - tscan: the scan object to get a Scanner for
        """
        pass

    def getScannerRows(self, scannerId, numRows):
        """
        Grabs multiple rows from a Scanner.

        @return Between zero and numRows TResults

        Parameters:
         - scannerId: the Id of the Scanner to return rows from. This is an Id returned from the openScanner function.
         - numRows: number of rows to return
        """
        pass

    def closeScanner(self, scannerId):
        """
        Closes the scanner. Should be called to free server side resources timely.
        Typically close once the scanner is not needed anymore, i.e. after looping
        over it to get all the required rows.

        Parameters:
         - scannerId: the Id of the Scanner to close *
        """
        pass

    def mutateRow(self, table, trowMutations):
        """
        mutateRow performs multiple mutations atomically on a single row.

        Parameters:
         - table: table to apply the mutations
         - trowMutations: mutations to apply
        """
        pass

    def getScannerResults(self, table, tscan, numRows):
        """
        Get results for the provided TScan object.
        This helper function opens a scanner, get the results and close the scanner.

        @return between zero and numRows TResults

        Parameters:
         - table: the table to get the Scanner for
         - tscan: the scan object to get a Scanner for
         - numRows: number of rows to return
        """
        pass

    def getRegionLocation(self, table, row, reload):
        """
        Given a table and a row get the location of the region that
        would contain the given row key.

        reload = true means the cache will be cleared and the location
        will be fetched from meta.

        Parameters:
         - table
         - row
         - reload
        """
        pass

    def getAllRegionLocations(self, table):
        """
        Get all of the region locations for a given table.

        Parameters:
         - table
        """
        pass

    def checkAndMutate(self, table, row, family, qualifier, compareOperator, value, rowMutations):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it mutates the row.

        @return true if the row was mutated, false otherwise

        Parameters:
         - table: to check in and delete from
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - compareOperator: comparison to make on the value
         - value: the expected value to be compared against, if not provided the
        check is for the non-existence of the column in question
         - rowMutations: row mutations to execute if the value matches
        """
        pass

    def getTableDescriptor(self, table):
        """
        Get a table descriptor.
        @return the TableDescriptor of the giving tablename

        Parameters:
         - table: the tablename of the table to get tableDescriptor
        """
        pass

    def getTableDescriptors(self, tables):
        """
        Get table descriptors of tables.
        @return the TableDescriptor of the giving tablename

        Parameters:
         - tables: the tablename list of the tables to get tableDescriptor
        """
        pass

    def tableExists(self, tableName):
        """

        @return true if table exists already, false if not

        Parameters:
         - tableName: the tablename of the tables to check
        """
        pass

    def getTableDescriptorsByPattern(self, regex, includeSysTables):
        """
        Get table descriptors of tables that match the given pattern
        @return the tableDescriptors of the matching table

        Parameters:
         - regex: The regular expression to match against
         - includeSysTables: set to false if match only against userspace tables
        """
        pass

    def getTableDescriptorsByNamespace(self, name):
        """
        Get table descriptors of tables in the given namespace
        @return the tableDescriptors in the namespce

        Parameters:
         - name: The namesapce's name
        """
        pass

    def getTableNamesByPattern(self, regex, includeSysTables):
        """
        Get table names of tables that match the given pattern
        @return the table names of the matching table

        Parameters:
         - regex: The regular expression to match against
         - includeSysTables: set to false if match only against userspace tables
        """
        pass

    def getTableNamesByNamespace(self, name):
        """
        Get table names of tables in the given namespace
        @return the table names of the matching table

        Parameters:
         - name: The namesapce's name
        """
        pass

    def createTable(self, desc, splitKeys):
        """
        Creates a new table with an initial set of empty regions defined by the specified split keys.
        The total number of regions created will be the number of split keys plus one. Synchronous
        operation.

        Parameters:
         - desc: table descriptor for table
         - splitKeys: rray of split keys for the initial regions of the table
        """
        pass

    def deleteTable(self, tableName):
        """
        Deletes a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to delete
        """
        pass

    def truncateTable(self, tableName, preserveSplits):
        """
        Truncate a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to truncate
         - preserveSplits: whether to  preserve previous splits
        """
        pass

    def enableTable(self, tableName):
        """
        Enalbe a table

        Parameters:
         - tableName: the tablename to enable
        """
        pass

    def disableTable(self, tableName):
        """
        Disable a table

        Parameters:
         - tableName: the tablename to disable
        """
        pass

    def isTableEnabled(self, tableName):
        """

        @return true if table is enabled, false if not

        Parameters:
         - tableName: the tablename to check
        """
        pass

    def isTableDisabled(self, tableName):
        """

        @return true if table is disabled, false if not

        Parameters:
         - tableName: the tablename to check
        """
        pass

    def isTableAvailable(self, tableName):
        """

        @return true if table is available, false if not

        Parameters:
         - tableName: the tablename to check
        """
        pass

    def isTableAvailableWithSplit(self, tableName, splitKeys):
        """
         * Use this api to check if the table has been created with the specified number of splitkeys
         * which was used while creating the given table. Note : If this api is used after a table's
         * region gets splitted, the api may return false.
         *
         * @return true if table is available, false if not
         *
         * @deprecated Since 2.2.0. Because the same method in Table interface has been deprecated
         * since 2.0.0, we will remove it in 3.0.0 release.
         * Use {@link #isTableAvailable(TTableName tableName)} instead
        *

        Parameters:
         - tableName: the tablename to check
         - splitKeys: keys to check if the table has been created with all split keys
        """
        pass

    def addColumnFamily(self, tableName, column):
        """
        Add a column family to an existing table. Synchronous operation.

        Parameters:
         - tableName: the tablename to add column family to
         - column: column family descriptor of column family to be added
        """
        pass

    def deleteColumnFamily(self, tableName, column):
        """
        Delete a column family from a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to delete column family from
         - column: name of column family to be deleted
        """
        pass

    def modifyColumnFamily(self, tableName, column):
        """
        Modify an existing column family on a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to modify column family
         - column: column family descriptor of column family to be modified
        """
        pass

    def modifyTable(self, desc):
        """
        Modify an existing table

        Parameters:
         - desc: the descriptor of the table to modify
        """
        pass

    def createNamespace(self, namespaceDesc):
        """
        Create a new namespace. Blocks until namespace has been successfully created or an exception is
        thrown

        Parameters:
         - namespaceDesc: descriptor which describes the new namespace
        """
        pass

    def modifyNamespace(self, namespaceDesc):
        """
        Modify an existing namespace.  Blocks until namespace has been successfully modified or an
        exception is thrown

        Parameters:
         - namespaceDesc: descriptor which describes the new namespace
        """
        pass

    def deleteNamespace(self, name):
        """
        Delete an existing namespace. Only empty namespaces (no tables) can be removed.
        Blocks until namespace has been successfully deleted or an
        exception is thrown.

        Parameters:
         - name: namespace name
        """
        pass

    def getNamespaceDescriptor(self, name):
        """
        Get a namespace descriptor by name.
        @retrun the descriptor

        Parameters:
         - name: name of namespace descriptor
        """
        pass

    def listNamespaceDescriptors(self):
        """
        @return all namespaces

        """
        pass

    def listNamespaces(self):
        """
        @return all namespace names

        """
        pass


class Client(Iface):

    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def exists(self, table, tget):
        """
        Test for the existence of columns in the table, as specified in the TGet.

        @return true if the specified TGet matches one or more keys, false if not

        Parameters:
         - table: the table to check on
         - tget: the TGet to check for
        """
        self.send_exists(table, tget)
        return self.recv_exists()

    def send_exists(self, table, tget):
        self._oprot.writeMessageBegin('exists', TMessageType.CALL, self._seqid)
        args = exists_args()
        args.table = table
        args.tget = tget
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_exists(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = exists_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'exists failed: unknown result')

    def existsAll(self, table, tgets):
        """
        Test for the existence of columns in the table, as specified by the TGets.

        This will return an array of booleans. Each value will be true if the related Get matches
        one or more keys, false if not.

        Parameters:
         - table: the table to check on
         - tgets: a list of TGets to check for
        """
        self.send_existsAll(table, tgets)
        return self.recv_existsAll()

    def send_existsAll(self, table, tgets):
        self._oprot.writeMessageBegin('existsAll', TMessageType.CALL, self._seqid)
        args = existsAll_args()
        args.table = table
        args.tgets = tgets
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_existsAll(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = existsAll_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'existsAll failed: unknown result')

    def get(self, table, tget):
        """
        Method for getting data from a row.

        If the row cannot be found an empty Result is returned.
        This can be checked by the empty field of the TResult

        @return the result

        Parameters:
         - table: the table to get from
         - tget: the TGet to fetch
        """
        self.send_get(table, tget)
        return self.recv_get()

    def send_get(self, table, tget):
        self._oprot.writeMessageBegin('get', TMessageType.CALL, self._seqid)
        args = get_args()
        args.table = table
        args.tget = tget
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_get(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = get_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'get failed: unknown result')

    def getMultiple(self, table, tgets):
        """
        Method for getting multiple rows.

        If a row cannot be found there will be a null
        value in the result list for that TGet at the
        same position.

        So the Results are in the same order as the TGets.

        Parameters:
         - table: the table to get from
         - tgets: a list of TGets to fetch, the Result list
        will have the Results at corresponding positions
        or null if there was an error
        """
        self.send_getMultiple(table, tgets)
        return self.recv_getMultiple()

    def send_getMultiple(self, table, tgets):
        self._oprot.writeMessageBegin('getMultiple', TMessageType.CALL, self._seqid)
        args = getMultiple_args()
        args.table = table
        args.tgets = tgets
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getMultiple(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getMultiple_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getMultiple failed: unknown result')

    def put(self, table, tput):
        """
        Commit a TPut to a table.

        Parameters:
         - table: the table to put data in
         - tput: the TPut to put
        """
        self.send_put(table, tput)
        self.recv_put()

    def send_put(self, table, tput):
        self._oprot.writeMessageBegin('put', TMessageType.CALL, self._seqid)
        args = put_args()
        args.table = table
        args.tput = tput
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_put(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = put_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def checkAndPut(self, table, row, family, qualifier, value, tput):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it adds the TPut.

        @return true if the new put was executed, false otherwise

        Parameters:
         - table: to check in and put to
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - value: the expected value, if not provided the
        check is for the non-existence of the
        column in question
         - tput: the TPut to put if the check succeeds
        """
        self.send_checkAndPut(table, row, family, qualifier, value, tput)
        return self.recv_checkAndPut()

    def send_checkAndPut(self, table, row, family, qualifier, value, tput):
        self._oprot.writeMessageBegin('checkAndPut', TMessageType.CALL, self._seqid)
        args = checkAndPut_args()
        args.table = table
        args.row = row
        args.family = family
        args.qualifier = qualifier
        args.value = value
        args.tput = tput
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_checkAndPut(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = checkAndPut_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'checkAndPut failed: unknown result')

    def putMultiple(self, table, tputs):
        """
        Commit a List of Puts to the table.

        Parameters:
         - table: the table to put data in
         - tputs: a list of TPuts to commit
        """
        self.send_putMultiple(table, tputs)
        self.recv_putMultiple()

    def send_putMultiple(self, table, tputs):
        self._oprot.writeMessageBegin('putMultiple', TMessageType.CALL, self._seqid)
        args = putMultiple_args()
        args.table = table
        args.tputs = tputs
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_putMultiple(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = putMultiple_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def deleteSingle(self, table, tdelete):
        """
        Deletes as specified by the TDelete.

        Note: "delete" is a reserved keyword and cannot be used in Thrift
        thus the inconsistent naming scheme from the other functions.

        Parameters:
         - table: the table to delete from
         - tdelete: the TDelete to delete
        """
        self.send_deleteSingle(table, tdelete)
        self.recv_deleteSingle()

    def send_deleteSingle(self, table, tdelete):
        self._oprot.writeMessageBegin('deleteSingle', TMessageType.CALL, self._seqid)
        args = deleteSingle_args()
        args.table = table
        args.tdelete = tdelete
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteSingle(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteSingle_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def deleteMultiple(self, table, tdeletes):
        """
        Bulk commit a List of TDeletes to the table.

        Throws a TIOError if any of the deletes fail.

        Always returns an empty list for backwards compatibility.

        Parameters:
         - table: the table to delete from
         - tdeletes: list of TDeletes to delete
        """
        self.send_deleteMultiple(table, tdeletes)
        return self.recv_deleteMultiple()

    def send_deleteMultiple(self, table, tdeletes):
        self._oprot.writeMessageBegin('deleteMultiple', TMessageType.CALL, self._seqid)
        args = deleteMultiple_args()
        args.table = table
        args.tdeletes = tdeletes
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteMultiple(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteMultiple_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'deleteMultiple failed: unknown result')

    def checkAndDelete(self, table, row, family, qualifier, value, tdelete):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it adds the delete.

        @return true if the new delete was executed, false otherwise

        Parameters:
         - table: to check in and delete from
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - value: the expected value, if not provided the
        check is for the non-existence of the
        column in question
         - tdelete: the TDelete to execute if the check succeeds
        """
        self.send_checkAndDelete(table, row, family, qualifier, value, tdelete)
        return self.recv_checkAndDelete()

    def send_checkAndDelete(self, table, row, family, qualifier, value, tdelete):
        self._oprot.writeMessageBegin('checkAndDelete', TMessageType.CALL, self._seqid)
        args = checkAndDelete_args()
        args.table = table
        args.row = row
        args.family = family
        args.qualifier = qualifier
        args.value = value
        args.tdelete = tdelete
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_checkAndDelete(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = checkAndDelete_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'checkAndDelete failed: unknown result')

    def increment(self, table, tincrement):
        """
        Parameters:
         - table: the table to increment the value on
         - tincrement: the TIncrement to increment
        """
        self.send_increment(table, tincrement)
        return self.recv_increment()

    def send_increment(self, table, tincrement):
        self._oprot.writeMessageBegin('increment', TMessageType.CALL, self._seqid)
        args = increment_args()
        args.table = table
        args.tincrement = tincrement
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_increment(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = increment_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'increment failed: unknown result')

    def append(self, table, tappend):
        """
        Parameters:
         - table: the table to append the value on
         - tappend: the TAppend to append
        """
        self.send_append(table, tappend)
        return self.recv_append()

    def send_append(self, table, tappend):
        self._oprot.writeMessageBegin('append', TMessageType.CALL, self._seqid)
        args = append_args()
        args.table = table
        args.tappend = tappend
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_append(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = append_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'append failed: unknown result')

    def openScanner(self, table, tscan):
        """
        Get a Scanner for the provided TScan object.

        @return Scanner Id to be used with other scanner procedures

        Parameters:
         - table: the table to get the Scanner for
         - tscan: the scan object to get a Scanner for
        """
        self.send_openScanner(table, tscan)
        return self.recv_openScanner()

    def send_openScanner(self, table, tscan):
        self._oprot.writeMessageBegin('openScanner', TMessageType.CALL, self._seqid)
        args = openScanner_args()
        args.table = table
        args.tscan = tscan
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_openScanner(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = openScanner_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'openScanner failed: unknown result')

    def getScannerRows(self, scannerId, numRows):
        """
        Grabs multiple rows from a Scanner.

        @return Between zero and numRows TResults

        Parameters:
         - scannerId: the Id of the Scanner to return rows from. This is an Id returned from the openScanner function.
         - numRows: number of rows to return
        """
        self.send_getScannerRows(scannerId, numRows)
        return self.recv_getScannerRows()

    def send_getScannerRows(self, scannerId, numRows):
        self._oprot.writeMessageBegin('getScannerRows', TMessageType.CALL, self._seqid)
        args = getScannerRows_args()
        args.scannerId = scannerId
        args.numRows = numRows
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getScannerRows(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getScannerRows_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        if result.ia is not None:
            raise result.ia
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getScannerRows failed: unknown result')

    def closeScanner(self, scannerId):
        """
        Closes the scanner. Should be called to free server side resources timely.
        Typically close once the scanner is not needed anymore, i.e. after looping
        over it to get all the required rows.

        Parameters:
         - scannerId: the Id of the Scanner to close *
        """
        self.send_closeScanner(scannerId)
        self.recv_closeScanner()

    def send_closeScanner(self, scannerId):
        self._oprot.writeMessageBegin('closeScanner', TMessageType.CALL, self._seqid)
        args = closeScanner_args()
        args.scannerId = scannerId
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_closeScanner(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = closeScanner_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io
        if result.ia is not None:
            raise result.ia

    def mutateRow(self, table, trowMutations):
        """
        mutateRow performs multiple mutations atomically on a single row.

        Parameters:
         - table: table to apply the mutations
         - trowMutations: mutations to apply
        """
        self.send_mutateRow(table, trowMutations)
        self.recv_mutateRow()

    def send_mutateRow(self, table, trowMutations):
        self._oprot.writeMessageBegin('mutateRow', TMessageType.CALL, self._seqid)
        args = mutateRow_args()
        args.table = table
        args.trowMutations = trowMutations
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_mutateRow(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = mutateRow_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def getScannerResults(self, table, tscan, numRows):
        """
        Get results for the provided TScan object.
        This helper function opens a scanner, get the results and close the scanner.

        @return between zero and numRows TResults

        Parameters:
         - table: the table to get the Scanner for
         - tscan: the scan object to get a Scanner for
         - numRows: number of rows to return
        """
        self.send_getScannerResults(table, tscan, numRows)
        return self.recv_getScannerResults()

    def send_getScannerResults(self, table, tscan, numRows):
        self._oprot.writeMessageBegin('getScannerResults', TMessageType.CALL, self._seqid)
        args = getScannerResults_args()
        args.table = table
        args.tscan = tscan
        args.numRows = numRows
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getScannerResults(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getScannerResults_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getScannerResults failed: unknown result')

    def getRegionLocation(self, table, row, reload):
        """
        Given a table and a row get the location of the region that
        would contain the given row key.

        reload = true means the cache will be cleared and the location
        will be fetched from meta.

        Parameters:
         - table
         - row
         - reload
        """
        self.send_getRegionLocation(table, row, reload)
        return self.recv_getRegionLocation()

    def send_getRegionLocation(self, table, row, reload):
        self._oprot.writeMessageBegin('getRegionLocation', TMessageType.CALL, self._seqid)
        args = getRegionLocation_args()
        args.table = table
        args.row = row
        args.reload = reload
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getRegionLocation(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getRegionLocation_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getRegionLocation failed: unknown result')

    def getAllRegionLocations(self, table):
        """
        Get all of the region locations for a given table.

        Parameters:
         - table
        """
        self.send_getAllRegionLocations(table)
        return self.recv_getAllRegionLocations()

    def send_getAllRegionLocations(self, table):
        self._oprot.writeMessageBegin('getAllRegionLocations', TMessageType.CALL, self._seqid)
        args = getAllRegionLocations_args()
        args.table = table
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getAllRegionLocations(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getAllRegionLocations_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getAllRegionLocations failed: unknown result')

    def checkAndMutate(self, table, row, family, qualifier, compareOperator, value, rowMutations):
        """
        Atomically checks if a row/family/qualifier value matches the expected
        value. If it does, it mutates the row.

        @return true if the row was mutated, false otherwise

        Parameters:
         - table: to check in and delete from
         - row: row to check
         - family: column family to check
         - qualifier: column qualifier to check
         - compareOperator: comparison to make on the value
         - value: the expected value to be compared against, if not provided the
        check is for the non-existence of the column in question
         - rowMutations: row mutations to execute if the value matches
        """
        self.send_checkAndMutate(table, row, family, qualifier, compareOperator, value, rowMutations)
        return self.recv_checkAndMutate()

    def send_checkAndMutate(self, table, row, family, qualifier, compareOperator, value, rowMutations):
        self._oprot.writeMessageBegin('checkAndMutate', TMessageType.CALL, self._seqid)
        args = checkAndMutate_args()
        args.table = table
        args.row = row
        args.family = family
        args.qualifier = qualifier
        args.compareOperator = compareOperator
        args.value = value
        args.rowMutations = rowMutations
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_checkAndMutate(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = checkAndMutate_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'checkAndMutate failed: unknown result')

    def getTableDescriptor(self, table):
        """
        Get a table descriptor.
        @return the TableDescriptor of the giving tablename

        Parameters:
         - table: the tablename of the table to get tableDescriptor
        """
        self.send_getTableDescriptor(table)
        return self.recv_getTableDescriptor()

    def send_getTableDescriptor(self, table):
        self._oprot.writeMessageBegin('getTableDescriptor', TMessageType.CALL, self._seqid)
        args = getTableDescriptor_args()
        args.table = table
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableDescriptor(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableDescriptor_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableDescriptor failed: unknown result')

    def getTableDescriptors(self, tables):
        """
        Get table descriptors of tables.
        @return the TableDescriptor of the giving tablename

        Parameters:
         - tables: the tablename list of the tables to get tableDescriptor
        """
        self.send_getTableDescriptors(tables)
        return self.recv_getTableDescriptors()

    def send_getTableDescriptors(self, tables):
        self._oprot.writeMessageBegin('getTableDescriptors', TMessageType.CALL, self._seqid)
        args = getTableDescriptors_args()
        args.tables = tables
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableDescriptors(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableDescriptors_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableDescriptors failed: unknown result')

    def tableExists(self, tableName):
        """

        @return true if table exists already, false if not

        Parameters:
         - tableName: the tablename of the tables to check
        """
        self.send_tableExists(tableName)
        return self.recv_tableExists()

    def send_tableExists(self, tableName):
        self._oprot.writeMessageBegin('tableExists', TMessageType.CALL, self._seqid)
        args = tableExists_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_tableExists(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = tableExists_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'tableExists failed: unknown result')

    def getTableDescriptorsByPattern(self, regex, includeSysTables):
        """
        Get table descriptors of tables that match the given pattern
        @return the tableDescriptors of the matching table

        Parameters:
         - regex: The regular expression to match against
         - includeSysTables: set to false if match only against userspace tables
        """
        self.send_getTableDescriptorsByPattern(regex, includeSysTables)
        return self.recv_getTableDescriptorsByPattern()

    def send_getTableDescriptorsByPattern(self, regex, includeSysTables):
        self._oprot.writeMessageBegin('getTableDescriptorsByPattern', TMessageType.CALL, self._seqid)
        args = getTableDescriptorsByPattern_args()
        args.regex = regex
        args.includeSysTables = includeSysTables
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableDescriptorsByPattern(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableDescriptorsByPattern_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableDescriptorsByPattern failed: unknown result')

    def getTableDescriptorsByNamespace(self, name):
        """
        Get table descriptors of tables in the given namespace
        @return the tableDescriptors in the namespce

        Parameters:
         - name: The namesapce's name
        """
        self.send_getTableDescriptorsByNamespace(name)
        return self.recv_getTableDescriptorsByNamespace()

    def send_getTableDescriptorsByNamespace(self, name):
        self._oprot.writeMessageBegin('getTableDescriptorsByNamespace', TMessageType.CALL, self._seqid)
        args = getTableDescriptorsByNamespace_args()
        args.name = name
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableDescriptorsByNamespace(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableDescriptorsByNamespace_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableDescriptorsByNamespace failed: unknown result')

    def getTableNamesByPattern(self, regex, includeSysTables):
        """
        Get table names of tables that match the given pattern
        @return the table names of the matching table

        Parameters:
         - regex: The regular expression to match against
         - includeSysTables: set to false if match only against userspace tables
        """
        self.send_getTableNamesByPattern(regex, includeSysTables)
        return self.recv_getTableNamesByPattern()

    def send_getTableNamesByPattern(self, regex, includeSysTables):
        self._oprot.writeMessageBegin('getTableNamesByPattern', TMessageType.CALL, self._seqid)
        args = getTableNamesByPattern_args()
        args.regex = regex
        args.includeSysTables = includeSysTables
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableNamesByPattern(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableNamesByPattern_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableNamesByPattern failed: unknown result')

    def getTableNamesByNamespace(self, name):
        """
        Get table names of tables in the given namespace
        @return the table names of the matching table

        Parameters:
         - name: The namesapce's name
        """
        self.send_getTableNamesByNamespace(name)
        return self.recv_getTableNamesByNamespace()

    def send_getTableNamesByNamespace(self, name):
        self._oprot.writeMessageBegin('getTableNamesByNamespace', TMessageType.CALL, self._seqid)
        args = getTableNamesByNamespace_args()
        args.name = name
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getTableNamesByNamespace(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getTableNamesByNamespace_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getTableNamesByNamespace failed: unknown result')

    def createTable(self, desc, splitKeys):
        """
        Creates a new table with an initial set of empty regions defined by the specified split keys.
        The total number of regions created will be the number of split keys plus one. Synchronous
        operation.

        Parameters:
         - desc: table descriptor for table
         - splitKeys: rray of split keys for the initial regions of the table
        """
        self.send_createTable(desc, splitKeys)
        self.recv_createTable()

    def send_createTable(self, desc, splitKeys):
        self._oprot.writeMessageBegin('createTable', TMessageType.CALL, self._seqid)
        args = createTable_args()
        args.desc = desc
        args.splitKeys = splitKeys
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_createTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = createTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def deleteTable(self, tableName):
        """
        Deletes a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to delete
        """
        self.send_deleteTable(tableName)
        self.recv_deleteTable()

    def send_deleteTable(self, tableName):
        self._oprot.writeMessageBegin('deleteTable', TMessageType.CALL, self._seqid)
        args = deleteTable_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def truncateTable(self, tableName, preserveSplits):
        """
        Truncate a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to truncate
         - preserveSplits: whether to  preserve previous splits
        """
        self.send_truncateTable(tableName, preserveSplits)
        self.recv_truncateTable()

    def send_truncateTable(self, tableName, preserveSplits):
        self._oprot.writeMessageBegin('truncateTable', TMessageType.CALL, self._seqid)
        args = truncateTable_args()
        args.tableName = tableName
        args.preserveSplits = preserveSplits
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_truncateTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = truncateTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def enableTable(self, tableName):
        """
        Enalbe a table

        Parameters:
         - tableName: the tablename to enable
        """
        self.send_enableTable(tableName)
        self.recv_enableTable()

    def send_enableTable(self, tableName):
        self._oprot.writeMessageBegin('enableTable', TMessageType.CALL, self._seqid)
        args = enableTable_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_enableTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = enableTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def disableTable(self, tableName):
        """
        Disable a table

        Parameters:
         - tableName: the tablename to disable
        """
        self.send_disableTable(tableName)
        self.recv_disableTable()

    def send_disableTable(self, tableName):
        self._oprot.writeMessageBegin('disableTable', TMessageType.CALL, self._seqid)
        args = disableTable_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_disableTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = disableTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def isTableEnabled(self, tableName):
        """

        @return true if table is enabled, false if not

        Parameters:
         - tableName: the tablename to check
        """
        self.send_isTableEnabled(tableName)
        return self.recv_isTableEnabled()

    def send_isTableEnabled(self, tableName):
        self._oprot.writeMessageBegin('isTableEnabled', TMessageType.CALL, self._seqid)
        args = isTableEnabled_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_isTableEnabled(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = isTableEnabled_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'isTableEnabled failed: unknown result')

    def isTableDisabled(self, tableName):
        """

        @return true if table is disabled, false if not

        Parameters:
         - tableName: the tablename to check
        """
        self.send_isTableDisabled(tableName)
        return self.recv_isTableDisabled()

    def send_isTableDisabled(self, tableName):
        self._oprot.writeMessageBegin('isTableDisabled', TMessageType.CALL, self._seqid)
        args = isTableDisabled_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_isTableDisabled(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = isTableDisabled_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'isTableDisabled failed: unknown result')

    def isTableAvailable(self, tableName):
        """

        @return true if table is available, false if not

        Parameters:
         - tableName: the tablename to check
        """
        self.send_isTableAvailable(tableName)
        return self.recv_isTableAvailable()

    def send_isTableAvailable(self, tableName):
        self._oprot.writeMessageBegin('isTableAvailable', TMessageType.CALL, self._seqid)
        args = isTableAvailable_args()
        args.tableName = tableName
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_isTableAvailable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = isTableAvailable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'isTableAvailable failed: unknown result')

    def isTableAvailableWithSplit(self, tableName, splitKeys):
        """
         * Use this api to check if the table has been created with the specified number of splitkeys
         * which was used while creating the given table. Note : If this api is used after a table's
         * region gets splitted, the api may return false.
         *
         * @return true if table is available, false if not
         *
         * @deprecated Since 2.2.0. Because the same method in Table interface has been deprecated
         * since 2.0.0, we will remove it in 3.0.0 release.
         * Use {@link #isTableAvailable(TTableName tableName)} instead
        *

        Parameters:
         - tableName: the tablename to check
         - splitKeys: keys to check if the table has been created with all split keys
        """
        self.send_isTableAvailableWithSplit(tableName, splitKeys)
        return self.recv_isTableAvailableWithSplit()

    def send_isTableAvailableWithSplit(self, tableName, splitKeys):
        self._oprot.writeMessageBegin('isTableAvailableWithSplit', TMessageType.CALL, self._seqid)
        args = isTableAvailableWithSplit_args()
        args.tableName = tableName
        args.splitKeys = splitKeys
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_isTableAvailableWithSplit(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = isTableAvailableWithSplit_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'isTableAvailableWithSplit failed: unknown result')

    def addColumnFamily(self, tableName, column):
        """
        Add a column family to an existing table. Synchronous operation.

        Parameters:
         - tableName: the tablename to add column family to
         - column: column family descriptor of column family to be added
        """
        self.send_addColumnFamily(tableName, column)
        self.recv_addColumnFamily()

    def send_addColumnFamily(self, tableName, column):
        self._oprot.writeMessageBegin('addColumnFamily', TMessageType.CALL, self._seqid)
        args = addColumnFamily_args()
        args.tableName = tableName
        args.column = column
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_addColumnFamily(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = addColumnFamily_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def deleteColumnFamily(self, tableName, column):
        """
        Delete a column family from a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to delete column family from
         - column: name of column family to be deleted
        """
        self.send_deleteColumnFamily(tableName, column)
        self.recv_deleteColumnFamily()

    def send_deleteColumnFamily(self, tableName, column):
        self._oprot.writeMessageBegin('deleteColumnFamily', TMessageType.CALL, self._seqid)
        args = deleteColumnFamily_args()
        args.tableName = tableName
        args.column = column
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteColumnFamily(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteColumnFamily_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def modifyColumnFamily(self, tableName, column):
        """
        Modify an existing column family on a table. Synchronous operation.

        Parameters:
         - tableName: the tablename to modify column family
         - column: column family descriptor of column family to be modified
        """
        self.send_modifyColumnFamily(tableName, column)
        self.recv_modifyColumnFamily()

    def send_modifyColumnFamily(self, tableName, column):
        self._oprot.writeMessageBegin('modifyColumnFamily', TMessageType.CALL, self._seqid)
        args = modifyColumnFamily_args()
        args.tableName = tableName
        args.column = column
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_modifyColumnFamily(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = modifyColumnFamily_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def modifyTable(self, desc):
        """
        Modify an existing table

        Parameters:
         - desc: the descriptor of the table to modify
        """
        self.send_modifyTable(desc)
        self.recv_modifyTable()

    def send_modifyTable(self, desc):
        self._oprot.writeMessageBegin('modifyTable', TMessageType.CALL, self._seqid)
        args = modifyTable_args()
        args.desc = desc
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_modifyTable(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = modifyTable_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def createNamespace(self, namespaceDesc):
        """
        Create a new namespace. Blocks until namespace has been successfully created or an exception is
        thrown

        Parameters:
         - namespaceDesc: descriptor which describes the new namespace
        """
        self.send_createNamespace(namespaceDesc)
        self.recv_createNamespace()

    def send_createNamespace(self, namespaceDesc):
        self._oprot.writeMessageBegin('createNamespace', TMessageType.CALL, self._seqid)
        args = createNamespace_args()
        args.namespaceDesc = namespaceDesc
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_createNamespace(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = createNamespace_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def modifyNamespace(self, namespaceDesc):
        """
        Modify an existing namespace.  Blocks until namespace has been successfully modified or an
        exception is thrown

        Parameters:
         - namespaceDesc: descriptor which describes the new namespace
        """
        self.send_modifyNamespace(namespaceDesc)
        self.recv_modifyNamespace()

    def send_modifyNamespace(self, namespaceDesc):
        self._oprot.writeMessageBegin('modifyNamespace', TMessageType.CALL, self._seqid)
        args = modifyNamespace_args()
        args.namespaceDesc = namespaceDesc
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_modifyNamespace(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = modifyNamespace_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def deleteNamespace(self, name):
        """
        Delete an existing namespace. Only empty namespaces (no tables) can be removed.
        Blocks until namespace has been successfully deleted or an
        exception is thrown.

        Parameters:
         - name: namespace name
        """
        self.send_deleteNamespace(name)
        self.recv_deleteNamespace()

    def send_deleteNamespace(self, name):
        self._oprot.writeMessageBegin('deleteNamespace', TMessageType.CALL, self._seqid)
        args = deleteNamespace_args()
        args.name = name
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteNamespace(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteNamespace_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.io is not None:
            raise result.io

    def getNamespaceDescriptor(self, name):
        """
        Get a namespace descriptor by name.
        @retrun the descriptor

        Parameters:
         - name: name of namespace descriptor
        """
        self.send_getNamespaceDescriptor(name)
        return self.recv_getNamespaceDescriptor()

    def send_getNamespaceDescriptor(self, name):
        self._oprot.writeMessageBegin('getNamespaceDescriptor', TMessageType.CALL, self._seqid)
        args = getNamespaceDescriptor_args()
        args.name = name
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getNamespaceDescriptor(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getNamespaceDescriptor_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'getNamespaceDescriptor failed: unknown result')

    def listNamespaceDescriptors(self):
        """
        @return all namespaces

        """
        self.send_listNamespaceDescriptors()
        return self.recv_listNamespaceDescriptors()

    def send_listNamespaceDescriptors(self):
        self._oprot.writeMessageBegin('listNamespaceDescriptors', TMessageType.CALL, self._seqid)
        args = listNamespaceDescriptors_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_listNamespaceDescriptors(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = listNamespaceDescriptors_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'listNamespaceDescriptors failed: unknown result')

    def listNamespaces(self):
        """
        @return all namespace names

        """
        self.send_listNamespaces()
        return self.recv_listNamespaces()

    def send_listNamespaces(self):
        self._oprot.writeMessageBegin('listNamespaces', TMessageType.CALL, self._seqid)
        args = listNamespaces_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_listNamespaces(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = listNamespaces_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.io is not None:
            raise result.io
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'listNamespaces failed: unknown result')


class Processor(Iface, TProcessor):

    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap['exists'] = Processor.process_exists
        self._processMap['existsAll'] = Processor.process_existsAll
        self._processMap['get'] = Processor.process_get
        self._processMap['getMultiple'] = Processor.process_getMultiple
        self._processMap['put'] = Processor.process_put
        self._processMap['checkAndPut'] = Processor.process_checkAndPut
        self._processMap['putMultiple'] = Processor.process_putMultiple
        self._processMap['deleteSingle'] = Processor.process_deleteSingle
        self._processMap['deleteMultiple'] = Processor.process_deleteMultiple
        self._processMap['checkAndDelete'] = Processor.process_checkAndDelete
        self._processMap['increment'] = Processor.process_increment
        self._processMap['append'] = Processor.process_append
        self._processMap['openScanner'] = Processor.process_openScanner
        self._processMap['getScannerRows'] = Processor.process_getScannerRows
        self._processMap['closeScanner'] = Processor.process_closeScanner
        self._processMap['mutateRow'] = Processor.process_mutateRow
        self._processMap['getScannerResults'] = Processor.process_getScannerResults
        self._processMap['getRegionLocation'] = Processor.process_getRegionLocation
        self._processMap['getAllRegionLocations'] = Processor.process_getAllRegionLocations
        self._processMap['checkAndMutate'] = Processor.process_checkAndMutate
        self._processMap['getTableDescriptor'] = Processor.process_getTableDescriptor
        self._processMap['getTableDescriptors'] = Processor.process_getTableDescriptors
        self._processMap['tableExists'] = Processor.process_tableExists
        self._processMap['getTableDescriptorsByPattern'] = Processor.process_getTableDescriptorsByPattern
        self._processMap['getTableDescriptorsByNamespace'] = Processor.process_getTableDescriptorsByNamespace
        self._processMap['getTableNamesByPattern'] = Processor.process_getTableNamesByPattern
        self._processMap['getTableNamesByNamespace'] = Processor.process_getTableNamesByNamespace
        self._processMap['createTable'] = Processor.process_createTable
        self._processMap['deleteTable'] = Processor.process_deleteTable
        self._processMap['truncateTable'] = Processor.process_truncateTable
        self._processMap['enableTable'] = Processor.process_enableTable
        self._processMap['disableTable'] = Processor.process_disableTable
        self._processMap['isTableEnabled'] = Processor.process_isTableEnabled
        self._processMap['isTableDisabled'] = Processor.process_isTableDisabled
        self._processMap['isTableAvailable'] = Processor.process_isTableAvailable
        self._processMap['isTableAvailableWithSplit'] = Processor.process_isTableAvailableWithSplit
        self._processMap['addColumnFamily'] = Processor.process_addColumnFamily
        self._processMap['deleteColumnFamily'] = Processor.process_deleteColumnFamily
        self._processMap['modifyColumnFamily'] = Processor.process_modifyColumnFamily
        self._processMap['modifyTable'] = Processor.process_modifyTable
        self._processMap['createNamespace'] = Processor.process_createNamespace
        self._processMap['modifyNamespace'] = Processor.process_modifyNamespace
        self._processMap['deleteNamespace'] = Processor.process_deleteNamespace
        self._processMap['getNamespaceDescriptor'] = Processor.process_getNamespaceDescriptor
        self._processMap['listNamespaceDescriptors'] = Processor.process_listNamespaceDescriptors
        self._processMap['listNamespaces'] = Processor.process_listNamespaces

    def process(self, iprot, oprot):
        name, type, seqid = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % name)
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_exists(self, seqid, iprot, oprot):
        args = exists_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = exists_result()
        try:
            result.success = self._handler.exists(args.table, args.tget)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('exists', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_existsAll(self, seqid, iprot, oprot):
        args = existsAll_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = existsAll_result()
        try:
            result.success = self._handler.existsAll(args.table, args.tgets)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('existsAll', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_get(self, seqid, iprot, oprot):
        args = get_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = get_result()
        try:
            result.success = self._handler.get(args.table, args.tget)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('get', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getMultiple(self, seqid, iprot, oprot):
        args = getMultiple_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getMultiple_result()
        try:
            result.success = self._handler.getMultiple(args.table, args.tgets)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getMultiple', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_put(self, seqid, iprot, oprot):
        args = put_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = put_result()
        try:
            self._handler.put(args.table, args.tput)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('put', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_checkAndPut(self, seqid, iprot, oprot):
        args = checkAndPut_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = checkAndPut_result()
        try:
            result.success = self._handler.checkAndPut(args.table, args.row, args.family, args.qualifier, args.value, args.tput)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('checkAndPut', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_putMultiple(self, seqid, iprot, oprot):
        args = putMultiple_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = putMultiple_result()
        try:
            self._handler.putMultiple(args.table, args.tputs)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('putMultiple', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteSingle(self, seqid, iprot, oprot):
        args = deleteSingle_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteSingle_result()
        try:
            self._handler.deleteSingle(args.table, args.tdelete)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteSingle', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteMultiple(self, seqid, iprot, oprot):
        args = deleteMultiple_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteMultiple_result()
        try:
            result.success = self._handler.deleteMultiple(args.table, args.tdeletes)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteMultiple', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_checkAndDelete(self, seqid, iprot, oprot):
        args = checkAndDelete_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = checkAndDelete_result()
        try:
            result.success = self._handler.checkAndDelete(args.table, args.row, args.family, args.qualifier, args.value, args.tdelete)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('checkAndDelete', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_increment(self, seqid, iprot, oprot):
        args = increment_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = increment_result()
        try:
            result.success = self._handler.increment(args.table, args.tincrement)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('increment', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_append(self, seqid, iprot, oprot):
        args = append_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = append_result()
        try:
            result.success = self._handler.append(args.table, args.tappend)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('append', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_openScanner(self, seqid, iprot, oprot):
        args = openScanner_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = openScanner_result()
        try:
            result.success = self._handler.openScanner(args.table, args.tscan)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('openScanner', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getScannerRows(self, seqid, iprot, oprot):
        args = getScannerRows_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getScannerRows_result()
        try:
            result.success = self._handler.getScannerRows(args.scannerId, args.numRows)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TIllegalArgument as ia:
            try:
                msg_type = TMessageType.REPLY
                result.ia = ia
            finally:
                ia = None
                del ia

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getScannerRows', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_closeScanner(self, seqid, iprot, oprot):
        args = closeScanner_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = closeScanner_result()
        try:
            self._handler.closeScanner(args.scannerId)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TIllegalArgument as ia:
            try:
                msg_type = TMessageType.REPLY
                result.ia = ia
            finally:
                ia = None
                del ia

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('closeScanner', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_mutateRow(self, seqid, iprot, oprot):
        args = mutateRow_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = mutateRow_result()
        try:
            self._handler.mutateRow(args.table, args.trowMutations)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('mutateRow', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getScannerResults(self, seqid, iprot, oprot):
        args = getScannerResults_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getScannerResults_result()
        try:
            result.success = self._handler.getScannerResults(args.table, args.tscan, args.numRows)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getScannerResults', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getRegionLocation(self, seqid, iprot, oprot):
        args = getRegionLocation_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getRegionLocation_result()
        try:
            result.success = self._handler.getRegionLocation(args.table, args.row, args.reload)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getRegionLocation', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getAllRegionLocations(self, seqid, iprot, oprot):
        args = getAllRegionLocations_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getAllRegionLocations_result()
        try:
            result.success = self._handler.getAllRegionLocations(args.table)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getAllRegionLocations', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_checkAndMutate(self, seqid, iprot, oprot):
        args = checkAndMutate_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = checkAndMutate_result()
        try:
            result.success = self._handler.checkAndMutate(args.table, args.row, args.family, args.qualifier, args.compareOperator, args.value, args.rowMutations)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('checkAndMutate', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableDescriptor(self, seqid, iprot, oprot):
        args = getTableDescriptor_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableDescriptor_result()
        try:
            result.success = self._handler.getTableDescriptor(args.table)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableDescriptor', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableDescriptors(self, seqid, iprot, oprot):
        args = getTableDescriptors_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableDescriptors_result()
        try:
            result.success = self._handler.getTableDescriptors(args.tables)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableDescriptors', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_tableExists(self, seqid, iprot, oprot):
        args = tableExists_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = tableExists_result()
        try:
            result.success = self._handler.tableExists(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('tableExists', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableDescriptorsByPattern(self, seqid, iprot, oprot):
        args = getTableDescriptorsByPattern_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableDescriptorsByPattern_result()
        try:
            result.success = self._handler.getTableDescriptorsByPattern(args.regex, args.includeSysTables)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableDescriptorsByPattern', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableDescriptorsByNamespace(self, seqid, iprot, oprot):
        args = getTableDescriptorsByNamespace_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableDescriptorsByNamespace_result()
        try:
            result.success = self._handler.getTableDescriptorsByNamespace(args.name)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableDescriptorsByNamespace', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableNamesByPattern(self, seqid, iprot, oprot):
        args = getTableNamesByPattern_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableNamesByPattern_result()
        try:
            result.success = self._handler.getTableNamesByPattern(args.regex, args.includeSysTables)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableNamesByPattern', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getTableNamesByNamespace(self, seqid, iprot, oprot):
        args = getTableNamesByNamespace_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTableNamesByNamespace_result()
        try:
            result.success = self._handler.getTableNamesByNamespace(args.name)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getTableNamesByNamespace', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_createTable(self, seqid, iprot, oprot):
        args = createTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = createTable_result()
        try:
            self._handler.createTable(args.desc, args.splitKeys)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('createTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteTable(self, seqid, iprot, oprot):
        args = deleteTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteTable_result()
        try:
            self._handler.deleteTable(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_truncateTable(self, seqid, iprot, oprot):
        args = truncateTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = truncateTable_result()
        try:
            self._handler.truncateTable(args.tableName, args.preserveSplits)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('truncateTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_enableTable(self, seqid, iprot, oprot):
        args = enableTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = enableTable_result()
        try:
            self._handler.enableTable(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('enableTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_disableTable(self, seqid, iprot, oprot):
        args = disableTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = disableTable_result()
        try:
            self._handler.disableTable(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('disableTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_isTableEnabled(self, seqid, iprot, oprot):
        args = isTableEnabled_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = isTableEnabled_result()
        try:
            result.success = self._handler.isTableEnabled(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('isTableEnabled', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_isTableDisabled(self, seqid, iprot, oprot):
        args = isTableDisabled_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = isTableDisabled_result()
        try:
            result.success = self._handler.isTableDisabled(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('isTableDisabled', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_isTableAvailable(self, seqid, iprot, oprot):
        args = isTableAvailable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = isTableAvailable_result()
        try:
            result.success = self._handler.isTableAvailable(args.tableName)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('isTableAvailable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_isTableAvailableWithSplit(self, seqid, iprot, oprot):
        args = isTableAvailableWithSplit_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = isTableAvailableWithSplit_result()
        try:
            result.success = self._handler.isTableAvailableWithSplit(args.tableName, args.splitKeys)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('isTableAvailableWithSplit', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_addColumnFamily(self, seqid, iprot, oprot):
        args = addColumnFamily_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = addColumnFamily_result()
        try:
            self._handler.addColumnFamily(args.tableName, args.column)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('addColumnFamily', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteColumnFamily(self, seqid, iprot, oprot):
        args = deleteColumnFamily_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteColumnFamily_result()
        try:
            self._handler.deleteColumnFamily(args.tableName, args.column)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteColumnFamily', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_modifyColumnFamily(self, seqid, iprot, oprot):
        args = modifyColumnFamily_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = modifyColumnFamily_result()
        try:
            self._handler.modifyColumnFamily(args.tableName, args.column)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('modifyColumnFamily', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_modifyTable(self, seqid, iprot, oprot):
        args = modifyTable_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = modifyTable_result()
        try:
            self._handler.modifyTable(args.desc)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('modifyTable', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_createNamespace(self, seqid, iprot, oprot):
        args = createNamespace_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = createNamespace_result()
        try:
            self._handler.createNamespace(args.namespaceDesc)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('createNamespace', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_modifyNamespace(self, seqid, iprot, oprot):
        args = modifyNamespace_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = modifyNamespace_result()
        try:
            self._handler.modifyNamespace(args.namespaceDesc)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('modifyNamespace', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteNamespace(self, seqid, iprot, oprot):
        args = deleteNamespace_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteNamespace_result()
        try:
            self._handler.deleteNamespace(args.name)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteNamespace', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_getNamespaceDescriptor(self, seqid, iprot, oprot):
        args = getNamespaceDescriptor_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getNamespaceDescriptor_result()
        try:
            result.success = self._handler.getNamespaceDescriptor(args.name)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('getNamespaceDescriptor', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_listNamespaceDescriptors(self, seqid, iprot, oprot):
        args = listNamespaceDescriptors_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = listNamespaceDescriptors_result()
        try:
            result.success = self._handler.listNamespaceDescriptors()
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('listNamespaceDescriptors', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_listNamespaces(self, seqid, iprot, oprot):
        args = listNamespaces_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = listNamespaces_result()
        try:
            result.success = self._handler.listNamespaces()
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TIOError as io:
            try:
                msg_type = TMessageType.REPLY
                result.io = io
            finally:
                io = None
                del io

        except TApplicationException as ex:
            try:
                logging.exception('TApplication exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = ex
            finally:
                ex = None
                del ex

        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('listNamespaces', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


class exists_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to check on\n     - tget: the TGet to check for\n    '

    def __init__(self, table=None, tget=None):
        self.table = table
        self.tget = tget

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tget = TGet()
                    self.tget.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('exists_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tget is not None:
            oprot.writeFieldBegin('tget', TType.STRUCT, 2)
            self.tget.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tget is None:
            raise TProtocolException(message='Required field tget is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(exists_args)
exists_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tget', [TGet, None], None))

class exists_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('exists_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(exists_result)
exists_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class existsAll_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to check on\n     - tgets: a list of TGets to check for\n    '

    def __init__(self, table=None, tgets=None):
        self.table = table
        self.tgets = tgets

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.tgets = []
                    _etype172, _size169 = iprot.readListBegin()
                    for _i173 in range(_size169):
                        _elem174 = TGet()
                        _elem174.read(iprot)
                        self.tgets.append(_elem174)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('existsAll_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tgets is not None:
            oprot.writeFieldBegin('tgets', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.tgets))
            for iter175 in self.tgets:
                iter175.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tgets is None:
            raise TProtocolException(message='Required field tgets is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(existsAll_args)
existsAll_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.LIST, 'tgets', (TType.STRUCT, [TGet, None], False), None))

class existsAll_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype179, _size176 = iprot.readListBegin()
                    for _i180 in range(_size176):
                        _elem181 = iprot.readBool()
                        self.success.append(_elem181)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('existsAll_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.BOOL, len(self.success))
            for iter182 in self.success:
                oprot.writeBool(iter182)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(existsAll_result)
existsAll_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.BOOL, None, False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class get_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to get from\n     - tget: the TGet to fetch\n    '

    def __init__(self, table=None, tget=None):
        self.table = table
        self.tget = tget

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tget = TGet()
                    self.tget.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('get_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tget is not None:
            oprot.writeFieldBegin('tget', TType.STRUCT, 2)
            self.tget.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tget is None:
            raise TProtocolException(message='Required field tget is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(get_args)
get_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tget', [TGet, None], None))

class get_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('get_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(get_result)
get_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [TResult, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getMultiple_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to get from\n     - tgets: a list of TGets to fetch, the Result list\n    will have the Results at corresponding positions\n    or null if there was an error\n    '

    def __init__(self, table=None, tgets=None):
        self.table = table
        self.tgets = tgets

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.tgets = []
                    _etype186, _size183 = iprot.readListBegin()
                    for _i187 in range(_size183):
                        _elem188 = TGet()
                        _elem188.read(iprot)
                        self.tgets.append(_elem188)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getMultiple_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tgets is not None:
            oprot.writeFieldBegin('tgets', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.tgets))
            for iter189 in self.tgets:
                iter189.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tgets is None:
            raise TProtocolException(message='Required field tgets is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getMultiple_args)
getMultiple_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.LIST, 'tgets', (TType.STRUCT, [TGet, None], False), None))

class getMultiple_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype193, _size190 = iprot.readListBegin()
                    for _i194 in range(_size190):
                        _elem195 = TResult()
                        _elem195.read(iprot)
                        self.success.append(_elem195)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getMultiple_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter196 in self.success:
                iter196.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getMultiple_result)
getMultiple_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TResult, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class put_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to put data in\n     - tput: the TPut to put\n    '

    def __init__(self, table=None, tput=None):
        self.table = table
        self.tput = tput

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tput = TPut()
                    self.tput.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('put_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tput is not None:
            oprot.writeFieldBegin('tput', TType.STRUCT, 2)
            self.tput.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tput is None:
            raise TProtocolException(message='Required field tput is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(put_args)
put_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tput', [TPut, None], None))

class put_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('put_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(put_result)
put_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class checkAndPut_args(object):
    __doc__ = '\n    Attributes:\n     - table: to check in and put to\n     - row: row to check\n     - family: column family to check\n     - qualifier: column qualifier to check\n     - value: the expected value, if not provided the\n    check is for the non-existence of the\n    column in question\n     - tput: the TPut to put if the check succeeds\n    '

    def __init__(self, table=None, row=None, family=None, qualifier=None, value=None, tput=None):
        self.table = table
        self.row = row
        self.family = family
        self.qualifier = qualifier
        self.value = value
        self.tput = tput

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.STRING:
                        self.row = iprot.readBinary()
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 3:
                        if ftype == TType.STRING:
                            self.family = iprot.readBinary()
                        else:
                            iprot.skip(ftype)
                    else:
                        if fid == 4:
                            if ftype == TType.STRING:
                                self.qualifier = iprot.readBinary()
                            else:
                                iprot.skip(ftype)
                        else:
                            if fid == 5:
                                if ftype == TType.STRING:
                                    self.value = iprot.readBinary()
                                else:
                                    iprot.skip(ftype)
                            else:
                                if fid == 6:
                                    if ftype == TType.STRUCT:
                                        self.tput = TPut()
                                        self.tput.read(iprot)
                                    else:
                                        iprot.skip(ftype)
                                else:
                                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndPut_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 2)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 3)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 4)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 5)
            oprot.writeBinary(self.value)
            oprot.writeFieldEnd()
        if self.tput is not None:
            oprot.writeFieldBegin('tput', TType.STRUCT, 6)
            self.tput.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')
        if self.tput is None:
            raise TProtocolException(message='Required field tput is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndPut_args)
checkAndPut_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRING, 'row', 'BINARY', None),
 (
  3, TType.STRING, 'family', 'BINARY', None),
 (
  4, TType.STRING, 'qualifier', 'BINARY', None),
 (
  5, TType.STRING, 'value', 'BINARY', None),
 (
  6, TType.STRUCT, 'tput', [TPut, None], None))

class checkAndPut_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndPut_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndPut_result)
checkAndPut_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class putMultiple_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to put data in\n     - tputs: a list of TPuts to commit\n    '

    def __init__(self, table=None, tputs=None):
        self.table = table
        self.tputs = tputs

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.tputs = []
                    _etype200, _size197 = iprot.readListBegin()
                    for _i201 in range(_size197):
                        _elem202 = TPut()
                        _elem202.read(iprot)
                        self.tputs.append(_elem202)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('putMultiple_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tputs is not None:
            oprot.writeFieldBegin('tputs', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.tputs))
            for iter203 in self.tputs:
                iter203.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tputs is None:
            raise TProtocolException(message='Required field tputs is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(putMultiple_args)
putMultiple_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.LIST, 'tputs', (TType.STRUCT, [TPut, None], False), None))

class putMultiple_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('putMultiple_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(putMultiple_result)
putMultiple_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class deleteSingle_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to delete from\n     - tdelete: the TDelete to delete\n    '

    def __init__(self, table=None, tdelete=None):
        self.table = table
        self.tdelete = tdelete

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tdelete = TDelete()
                    self.tdelete.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteSingle_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tdelete is not None:
            oprot.writeFieldBegin('tdelete', TType.STRUCT, 2)
            self.tdelete.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tdelete is None:
            raise TProtocolException(message='Required field tdelete is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteSingle_args)
deleteSingle_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tdelete', [TDelete, None], None))

class deleteSingle_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteSingle_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteSingle_result)
deleteSingle_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class deleteMultiple_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to delete from\n     - tdeletes: list of TDeletes to delete\n    '

    def __init__(self, table=None, tdeletes=None):
        self.table = table
        self.tdeletes = tdeletes

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.tdeletes = []
                    _etype207, _size204 = iprot.readListBegin()
                    for _i208 in range(_size204):
                        _elem209 = TDelete()
                        _elem209.read(iprot)
                        self.tdeletes.append(_elem209)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteMultiple_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tdeletes is not None:
            oprot.writeFieldBegin('tdeletes', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.tdeletes))
            for iter210 in self.tdeletes:
                iter210.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tdeletes is None:
            raise TProtocolException(message='Required field tdeletes is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteMultiple_args)
deleteMultiple_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.LIST, 'tdeletes', (TType.STRUCT, [TDelete, None], False), None))

class deleteMultiple_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype214, _size211 = iprot.readListBegin()
                    for _i215 in range(_size211):
                        _elem216 = TDelete()
                        _elem216.read(iprot)
                        self.success.append(_elem216)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteMultiple_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter217 in self.success:
                iter217.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteMultiple_result)
deleteMultiple_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TDelete, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class checkAndDelete_args(object):
    __doc__ = '\n    Attributes:\n     - table: to check in and delete from\n     - row: row to check\n     - family: column family to check\n     - qualifier: column qualifier to check\n     - value: the expected value, if not provided the\n    check is for the non-existence of the\n    column in question\n     - tdelete: the TDelete to execute if the check succeeds\n    '

    def __init__(self, table=None, row=None, family=None, qualifier=None, value=None, tdelete=None):
        self.table = table
        self.row = row
        self.family = family
        self.qualifier = qualifier
        self.value = value
        self.tdelete = tdelete

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.STRING:
                        self.row = iprot.readBinary()
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 3:
                        if ftype == TType.STRING:
                            self.family = iprot.readBinary()
                        else:
                            iprot.skip(ftype)
                    else:
                        if fid == 4:
                            if ftype == TType.STRING:
                                self.qualifier = iprot.readBinary()
                            else:
                                iprot.skip(ftype)
                        else:
                            if fid == 5:
                                if ftype == TType.STRING:
                                    self.value = iprot.readBinary()
                                else:
                                    iprot.skip(ftype)
                            else:
                                if fid == 6:
                                    if ftype == TType.STRUCT:
                                        self.tdelete = TDelete()
                                        self.tdelete.read(iprot)
                                    else:
                                        iprot.skip(ftype)
                                else:
                                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndDelete_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 2)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 3)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 4)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 5)
            oprot.writeBinary(self.value)
            oprot.writeFieldEnd()
        if self.tdelete is not None:
            oprot.writeFieldBegin('tdelete', TType.STRUCT, 6)
            self.tdelete.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')
        if self.tdelete is None:
            raise TProtocolException(message='Required field tdelete is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndDelete_args)
checkAndDelete_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRING, 'row', 'BINARY', None),
 (
  3, TType.STRING, 'family', 'BINARY', None),
 (
  4, TType.STRING, 'qualifier', 'BINARY', None),
 (
  5, TType.STRING, 'value', 'BINARY', None),
 (
  6, TType.STRUCT, 'tdelete', [TDelete, None], None))

class checkAndDelete_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndDelete_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndDelete_result)
checkAndDelete_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class increment_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to increment the value on\n     - tincrement: the TIncrement to increment\n    '

    def __init__(self, table=None, tincrement=None):
        self.table = table
        self.tincrement = tincrement

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tincrement = TIncrement()
                    self.tincrement.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('increment_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tincrement is not None:
            oprot.writeFieldBegin('tincrement', TType.STRUCT, 2)
            self.tincrement.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tincrement is None:
            raise TProtocolException(message='Required field tincrement is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(increment_args)
increment_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tincrement', [TIncrement, None], None))

class increment_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('increment_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(increment_result)
increment_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [TResult, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class append_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to append the value on\n     - tappend: the TAppend to append\n    '

    def __init__(self, table=None, tappend=None):
        self.table = table
        self.tappend = tappend

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tappend = TAppend()
                    self.tappend.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('append_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tappend is not None:
            oprot.writeFieldBegin('tappend', TType.STRUCT, 2)
            self.tappend.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tappend is None:
            raise TProtocolException(message='Required field tappend is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(append_args)
append_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tappend', [TAppend, None], None))

class append_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('append_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(append_result)
append_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [TResult, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class openScanner_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to get the Scanner for\n     - tscan: the scan object to get a Scanner for\n    '

    def __init__(self, table=None, tscan=None):
        self.table = table
        self.tscan = tscan

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tscan = TScan()
                    self.tscan.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('openScanner_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tscan is not None:
            oprot.writeFieldBegin('tscan', TType.STRUCT, 2)
            self.tscan.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tscan is None:
            raise TProtocolException(message='Required field tscan is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(openScanner_args)
openScanner_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tscan', [TScan, None], None))

class openScanner_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.I32:
                    self.success = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('openScanner_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.I32, 0)
            oprot.writeI32(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(openScanner_result)
openScanner_result.thrift_spec = (
 (
  0, TType.I32, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getScannerRows_args(object):
    __doc__ = '\n    Attributes:\n     - scannerId: the Id of the Scanner to return rows from. This is an Id returned from the openScanner function.\n     - numRows: number of rows to return\n    '

    def __init__(self, scannerId=None, numRows=1):
        self.scannerId = scannerId
        self.numRows = numRows

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.I32:
                    self.scannerId = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.numRows = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getScannerRows_args')
        if self.scannerId is not None:
            oprot.writeFieldBegin('scannerId', TType.I32, 1)
            oprot.writeI32(self.scannerId)
            oprot.writeFieldEnd()
        if self.numRows is not None:
            oprot.writeFieldBegin('numRows', TType.I32, 2)
            oprot.writeI32(self.numRows)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.scannerId is None:
            raise TProtocolException(message='Required field scannerId is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getScannerRows_args)
getScannerRows_args.thrift_spec = (
 None,
 (
  1, TType.I32, 'scannerId', None, None),
 (
  2, TType.I32, 'numRows', None, 1))

class getScannerRows_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n     - ia: if the scannerId is invalid\n    '

    def __init__(self, success=None, io=None, ia=None):
        self.success = success
        self.io = io
        self.ia = ia

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype221, _size218 = iprot.readListBegin()
                    for _i222 in range(_size218):
                        _elem223 = TResult()
                        _elem223.read(iprot)
                        self.success.append(_elem223)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 2:
                        if ftype == TType.STRUCT:
                            self.ia = TIllegalArgument()
                            self.ia.read(iprot)
                        else:
                            iprot.skip(ftype)
                    else:
                        iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getScannerRows_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter224 in self.success:
                iter224.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        if self.ia is not None:
            oprot.writeFieldBegin('ia', TType.STRUCT, 2)
            self.ia.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getScannerRows_result)
getScannerRows_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TResult, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None),
 (
  2, TType.STRUCT, 'ia', [TIllegalArgument, None], None))

class closeScanner_args(object):
    __doc__ = '\n    Attributes:\n     - scannerId: the Id of the Scanner to close *\n    '

    def __init__(self, scannerId=None):
        self.scannerId = scannerId

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.I32:
                    self.scannerId = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('closeScanner_args')
        if self.scannerId is not None:
            oprot.writeFieldBegin('scannerId', TType.I32, 1)
            oprot.writeI32(self.scannerId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.scannerId is None:
            raise TProtocolException(message='Required field scannerId is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(closeScanner_args)
closeScanner_args.thrift_spec = (
 None,
 (
  1, TType.I32, 'scannerId', None, None))

class closeScanner_result(object):
    __doc__ = '\n    Attributes:\n     - io\n     - ia: if the scannerId is invalid\n    '

    def __init__(self, io=None, ia=None):
        self.io = io
        self.ia = ia

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.ia = TIllegalArgument()
                    self.ia.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('closeScanner_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        if self.ia is not None:
            oprot.writeFieldBegin('ia', TType.STRUCT, 2)
            self.ia.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(closeScanner_result)
closeScanner_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None),
 (
  2, TType.STRUCT, 'ia', [TIllegalArgument, None], None))

class mutateRow_args(object):
    __doc__ = '\n    Attributes:\n     - table: table to apply the mutations\n     - trowMutations: mutations to apply\n    '

    def __init__(self, table=None, trowMutations=None):
        self.table = table
        self.trowMutations = trowMutations

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.trowMutations = TRowMutations()
                    self.trowMutations.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('mutateRow_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.trowMutations is not None:
            oprot.writeFieldBegin('trowMutations', TType.STRUCT, 2)
            self.trowMutations.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.trowMutations is None:
            raise TProtocolException(message='Required field trowMutations is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(mutateRow_args)
mutateRow_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'trowMutations', [TRowMutations, None], None))

class mutateRow_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('mutateRow_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(mutateRow_result)
mutateRow_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getScannerResults_args(object):
    __doc__ = '\n    Attributes:\n     - table: the table to get the Scanner for\n     - tscan: the scan object to get a Scanner for\n     - numRows: number of rows to return\n    '

    def __init__(self, table=None, tscan=None, numRows=1):
        self.table = table
        self.tscan = tscan
        self.numRows = numRows

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.tscan = TScan()
                    self.tscan.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.numRows = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getScannerResults_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.tscan is not None:
            oprot.writeFieldBegin('tscan', TType.STRUCT, 2)
            self.tscan.write(oprot)
            oprot.writeFieldEnd()
        if self.numRows is not None:
            oprot.writeFieldBegin('numRows', TType.I32, 3)
            oprot.writeI32(self.numRows)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.tscan is None:
            raise TProtocolException(message='Required field tscan is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getScannerResults_args)
getScannerResults_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRUCT, 'tscan', [TScan, None], None),
 (
  3, TType.I32, 'numRows', None, 1))

class getScannerResults_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype228, _size225 = iprot.readListBegin()
                    for _i229 in range(_size225):
                        _elem230 = TResult()
                        _elem230.read(iprot)
                        self.success.append(_elem230)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getScannerResults_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter231 in self.success:
                iter231.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getScannerResults_result)
getScannerResults_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TResult, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getRegionLocation_args(object):
    __doc__ = '\n    Attributes:\n     - table\n     - row\n     - reload\n    '

    def __init__(self, table=None, row=None, reload=None):
        self.table = table
        self.row = row
        self.reload = reload

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.row = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.BOOL:
                    self.reload = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getRegionLocation_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 2)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.reload is not None:
            oprot.writeFieldBegin('reload', TType.BOOL, 3)
            oprot.writeBool(self.reload)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getRegionLocation_args)
getRegionLocation_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRING, 'row', 'BINARY', None),
 (
  3, TType.BOOL, 'reload', None, None))

class getRegionLocation_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = THRegionLocation()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getRegionLocation_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getRegionLocation_result)
getRegionLocation_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [THRegionLocation, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getAllRegionLocations_args(object):
    __doc__ = '\n    Attributes:\n     - table\n    '

    def __init__(self, table=None):
        self.table = table

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.table = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getAllRegionLocations_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getAllRegionLocations_args)
getAllRegionLocations_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None))

class getAllRegionLocations_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype235, _size232 = iprot.readListBegin()
                    for _i236 in range(_size232):
                        _elem237 = THRegionLocation()
                        _elem237.read(iprot)
                        self.success.append(_elem237)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getAllRegionLocations_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter238 in self.success:
                iter238.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getAllRegionLocations_result)
getAllRegionLocations_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [THRegionLocation, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class checkAndMutate_args(object):
    __doc__ = '\n    Attributes:\n     - table: to check in and delete from\n     - row: row to check\n     - family: column family to check\n     - qualifier: column qualifier to check\n     - compareOperator: comparison to make on the value\n     - value: the expected value to be compared against, if not provided the\n    check is for the non-existence of the column in question\n     - rowMutations: row mutations to execute if the value matches\n    '

    def __init__(self, table=None, row=None, family=None, qualifier=None, compareOperator=None, value=None, rowMutations=None):
        self.table = table
        self.row = row
        self.family = family
        self.qualifier = qualifier
        self.compareOperator = compareOperator
        self.value = value
        self.rowMutations = rowMutations

    def read--- This code section failed: ---

 L.6662         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.6663        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.6664        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.6665        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.6666     68_70  SETUP_LOOP          442  'to 442'

 L.6667        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.6668        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.6669        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.6670        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.6671       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.6672       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               table
              126  JUMP_FORWARD        430  'to 430'
            128_0  COME_FROM           114  '114'

 L.6674       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        430  'to 430'
            142_0  COME_FROM           104  '104'

 L.6675       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   184  'to 184'

 L.6676       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                STRING
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.6677       160  LOAD_FAST                'iprot'
              162  LOAD_METHOD              readBinary
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               row
              170  JUMP_FORWARD        182  'to 182'
            172_0  COME_FROM           158  '158'

 L.6679       172  LOAD_FAST                'iprot'
              174  LOAD_METHOD              skip
              176  LOAD_FAST                'ftype'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          
            182_0  COME_FROM           170  '170'
              182  JUMP_FORWARD        430  'to 430'
            184_0  COME_FROM           148  '148'

 L.6680       184  LOAD_FAST                'fid'
              186  LOAD_CONST               3
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   226  'to 226'

 L.6681       192  LOAD_FAST                'ftype'
              194  LOAD_GLOBAL              TType
              196  LOAD_ATTR                STRING
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L.6682       202  LOAD_FAST                'iprot'
              204  LOAD_METHOD              readBinary
              206  CALL_METHOD_0         0  '0 positional arguments'
              208  LOAD_FAST                'self'
              210  STORE_ATTR               family
              212  JUMP_FORWARD        224  'to 224'
            214_0  COME_FROM           200  '200'

 L.6684       214  LOAD_FAST                'iprot'
              216  LOAD_METHOD              skip
              218  LOAD_FAST                'ftype'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          
            224_0  COME_FROM           212  '212'
              224  JUMP_FORWARD        430  'to 430'
            226_0  COME_FROM           190  '190'

 L.6685       226  LOAD_FAST                'fid'
              228  LOAD_CONST               4
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   272  'to 272'

 L.6686       236  LOAD_FAST                'ftype'
              238  LOAD_GLOBAL              TType
              240  LOAD_ATTR                STRING
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L.6687       248  LOAD_FAST                'iprot'
              250  LOAD_METHOD              readBinary
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  LOAD_FAST                'self'
              256  STORE_ATTR               qualifier
              258  JUMP_FORWARD        270  'to 270'
            260_0  COME_FROM           244  '244'

 L.6689       260  LOAD_FAST                'iprot'
              262  LOAD_METHOD              skip
              264  LOAD_FAST                'ftype'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  POP_TOP          
            270_0  COME_FROM           258  '258'
              270  JUMP_FORWARD        430  'to 430'
            272_0  COME_FROM           232  '232'

 L.6690       272  LOAD_FAST                'fid'
              274  LOAD_CONST               5
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   318  'to 318'

 L.6691       282  LOAD_FAST                'ftype'
              284  LOAD_GLOBAL              TType
              286  LOAD_ATTR                I32
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   306  'to 306'

 L.6692       294  LOAD_FAST                'iprot'
              296  LOAD_METHOD              readI32
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  LOAD_FAST                'self'
              302  STORE_ATTR               compareOperator
              304  JUMP_FORWARD        316  'to 316'
            306_0  COME_FROM           290  '290'

 L.6694       306  LOAD_FAST                'iprot'
              308  LOAD_METHOD              skip
              310  LOAD_FAST                'ftype'
              312  CALL_METHOD_1         1  '1 positional argument'
              314  POP_TOP          
            316_0  COME_FROM           304  '304'
              316  JUMP_FORWARD        430  'to 430'
            318_0  COME_FROM           278  '278'

 L.6695       318  LOAD_FAST                'fid'
              320  LOAD_CONST               6
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   364  'to 364'

 L.6696       328  LOAD_FAST                'ftype'
              330  LOAD_GLOBAL              TType
              332  LOAD_ATTR                STRING
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   352  'to 352'

 L.6697       340  LOAD_FAST                'iprot'
              342  LOAD_METHOD              readBinary
              344  CALL_METHOD_0         0  '0 positional arguments'
              346  LOAD_FAST                'self'
              348  STORE_ATTR               value
              350  JUMP_FORWARD        362  'to 362'
            352_0  COME_FROM           336  '336'

 L.6699       352  LOAD_FAST                'iprot'
              354  LOAD_METHOD              skip
              356  LOAD_FAST                'ftype'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  POP_TOP          
            362_0  COME_FROM           350  '350'
              362  JUMP_FORWARD        430  'to 430'
            364_0  COME_FROM           324  '324'

 L.6700       364  LOAD_FAST                'fid'
              366  LOAD_CONST               7
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   420  'to 420'

 L.6701       374  LOAD_FAST                'ftype'
              376  LOAD_GLOBAL              TType
              378  LOAD_ATTR                STRUCT
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   408  'to 408'

 L.6702       386  LOAD_GLOBAL              TRowMutations
              388  CALL_FUNCTION_0       0  '0 positional arguments'
              390  LOAD_FAST                'self'
              392  STORE_ATTR               rowMutations

 L.6703       394  LOAD_FAST                'self'
              396  LOAD_ATTR                rowMutations
              398  LOAD_METHOD              read
              400  LOAD_FAST                'iprot'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  POP_TOP          
              406  JUMP_FORWARD        418  'to 418'
            408_0  COME_FROM           382  '382'

 L.6705       408  LOAD_FAST                'iprot'
              410  LOAD_METHOD              skip
              412  LOAD_FAST                'ftype'
              414  CALL_METHOD_1         1  '1 positional argument'
            416_0  COME_FROM           126  '126'
              416  POP_TOP          
            418_0  COME_FROM           406  '406'
              418  JUMP_FORWARD        430  'to 430'
            420_0  COME_FROM           370  '370'

 L.6707       420  LOAD_FAST                'iprot'
              422  LOAD_METHOD              skip
              424  LOAD_FAST                'ftype'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  POP_TOP          
            430_0  COME_FROM           418  '418'
            430_1  COME_FROM           362  '362'
            430_2  COME_FROM           316  '316'
            430_3  COME_FROM           270  '270'
            430_4  COME_FROM           224  '224'
            430_5  COME_FROM           182  '182'
            430_6  COME_FROM           138  '138'

 L.6708       430  LOAD_FAST                'iprot'
              432  LOAD_METHOD              readFieldEnd
              434  CALL_METHOD_0         0  '0 positional arguments'
              436  POP_TOP          
              438  JUMP_BACK            72  'to 72'
              440  POP_BLOCK        
            442_0  COME_FROM_LOOP       68  '68'

 L.6709       442  LOAD_FAST                'iprot'
              444  LOAD_METHOD              readStructEnd
              446  CALL_METHOD_0         0  '0 positional arguments'
              448  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 416_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndMutate_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRING, 1)
            oprot.writeBinary(self.table)
            oprot.writeFieldEnd()
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 2)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 3)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 4)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.compareOperator is not None:
            oprot.writeFieldBegin('compareOperator', TType.I32, 5)
            oprot.writeI32(self.compareOperator)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 6)
            oprot.writeBinary(self.value)
            oprot.writeFieldEnd()
        if self.rowMutations is not None:
            oprot.writeFieldBegin('rowMutations', TType.STRUCT, 7)
            self.rowMutations.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')
        if self.compareOperator is None:
            raise TProtocolException(message='Required field compareOperator is unset!')
        if self.rowMutations is None:
            raise TProtocolException(message='Required field rowMutations is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndMutate_args)
checkAndMutate_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'table', 'BINARY', None),
 (
  2, TType.STRING, 'row', 'BINARY', None),
 (
  3, TType.STRING, 'family', 'BINARY', None),
 (
  4, TType.STRING, 'qualifier', 'BINARY', None),
 (
  5, TType.I32, 'compareOperator', None, None),
 (
  6, TType.STRING, 'value', 'BINARY', None),
 (
  7, TType.STRUCT, 'rowMutations', [TRowMutations, None], None))

class checkAndMutate_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('checkAndMutate_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(checkAndMutate_result)
checkAndMutate_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableDescriptor_args(object):
    __doc__ = '\n    Attributes:\n     - table: the tablename of the table to get tableDescriptor\n    '

    def __init__(self, table=None):
        self.table = table

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.table = TTableName()
                    self.table.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptor_args')
        if self.table is not None:
            oprot.writeFieldBegin('table', TType.STRUCT, 1)
            self.table.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table is None:
            raise TProtocolException(message='Required field table is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptor_args)
getTableDescriptor_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'table', [TTableName, None], None))

class getTableDescriptor_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TTableDescriptor()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptor_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptor_result)
getTableDescriptor_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [TTableDescriptor, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableDescriptors_args(object):
    __doc__ = '\n    Attributes:\n     - tables: the tablename list of the tables to get tableDescriptor\n    '

    def __init__(self, tables=None):
        self.tables = tables

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.LIST:
                    self.tables = []
                    _etype242, _size239 = iprot.readListBegin()
                    for _i243 in range(_size239):
                        _elem244 = TTableName()
                        _elem244.read(iprot)
                        self.tables.append(_elem244)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptors_args')
        if self.tables is not None:
            oprot.writeFieldBegin('tables', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.tables))
            for iter245 in self.tables:
                iter245.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tables is None:
            raise TProtocolException(message='Required field tables is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptors_args)
getTableDescriptors_args.thrift_spec = (
 None,
 (
  1, TType.LIST, 'tables', (TType.STRUCT, [TTableName, None], False), None))

class getTableDescriptors_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype249, _size246 = iprot.readListBegin()
                    for _i250 in range(_size246):
                        _elem251 = TTableDescriptor()
                        _elem251.read(iprot)
                        self.success.append(_elem251)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptors_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter252 in self.success:
                iter252.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptors_result)
getTableDescriptors_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TTableDescriptor, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class tableExists_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename of the tables to check\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('tableExists_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(tableExists_args)
tableExists_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class tableExists_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('tableExists_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(tableExists_result)
tableExists_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableDescriptorsByPattern_args(object):
    __doc__ = '\n    Attributes:\n     - regex: The regular expression to match against\n     - includeSysTables: set to false if match only against userspace tables\n    '

    def __init__(self, regex=None, includeSysTables=None):
        self.regex = regex
        self.includeSysTables = includeSysTables

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.regex = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.BOOL:
                    self.includeSysTables = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptorsByPattern_args')
        if self.regex is not None:
            oprot.writeFieldBegin('regex', TType.STRING, 1)
            oprot.writeString(self.regex.encode('utf-8') if sys.version_info[0] == 2 else self.regex)
            oprot.writeFieldEnd()
        if self.includeSysTables is not None:
            oprot.writeFieldBegin('includeSysTables', TType.BOOL, 2)
            oprot.writeBool(self.includeSysTables)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.includeSysTables is None:
            raise TProtocolException(message='Required field includeSysTables is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptorsByPattern_args)
getTableDescriptorsByPattern_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'regex', 'UTF8', None),
 (
  2, TType.BOOL, 'includeSysTables', None, None))

class getTableDescriptorsByPattern_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype256, _size253 = iprot.readListBegin()
                    for _i257 in range(_size253):
                        _elem258 = TTableDescriptor()
                        _elem258.read(iprot)
                        self.success.append(_elem258)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptorsByPattern_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter259 in self.success:
                iter259.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptorsByPattern_result)
getTableDescriptorsByPattern_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TTableDescriptor, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableDescriptorsByNamespace_args(object):
    __doc__ = "\n    Attributes:\n     - name: The namesapce's name\n    "

    def __init__(self, name=None):
        self.name = name

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptorsByNamespace_args')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptorsByNamespace_args)
getTableDescriptorsByNamespace_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'UTF8', None))

class getTableDescriptorsByNamespace_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype263, _size260 = iprot.readListBegin()
                    for _i264 in range(_size260):
                        _elem265 = TTableDescriptor()
                        _elem265.read(iprot)
                        self.success.append(_elem265)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableDescriptorsByNamespace_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter266 in self.success:
                iter266.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableDescriptorsByNamespace_result)
getTableDescriptorsByNamespace_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TTableDescriptor, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableNamesByPattern_args(object):
    __doc__ = '\n    Attributes:\n     - regex: The regular expression to match against\n     - includeSysTables: set to false if match only against userspace tables\n    '

    def __init__(self, regex=None, includeSysTables=None):
        self.regex = regex
        self.includeSysTables = includeSysTables

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.regex = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.BOOL:
                    self.includeSysTables = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableNamesByPattern_args')
        if self.regex is not None:
            oprot.writeFieldBegin('regex', TType.STRING, 1)
            oprot.writeString(self.regex.encode('utf-8') if sys.version_info[0] == 2 else self.regex)
            oprot.writeFieldEnd()
        if self.includeSysTables is not None:
            oprot.writeFieldBegin('includeSysTables', TType.BOOL, 2)
            oprot.writeBool(self.includeSysTables)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.includeSysTables is None:
            raise TProtocolException(message='Required field includeSysTables is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableNamesByPattern_args)
getTableNamesByPattern_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'regex', 'UTF8', None),
 (
  2, TType.BOOL, 'includeSysTables', None, None))

class getTableNamesByPattern_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype270, _size267 = iprot.readListBegin()
                    for _i271 in range(_size267):
                        _elem272 = TTableName()
                        _elem272.read(iprot)
                        self.success.append(_elem272)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableNamesByPattern_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter273 in self.success:
                iter273.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableNamesByPattern_result)
getTableNamesByPattern_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TTableName, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getTableNamesByNamespace_args(object):
    __doc__ = "\n    Attributes:\n     - name: The namesapce's name\n    "

    def __init__(self, name=None):
        self.name = name

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableNamesByNamespace_args')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableNamesByNamespace_args)
getTableNamesByNamespace_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'UTF8', None))

class getTableNamesByNamespace_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype277, _size274 = iprot.readListBegin()
                    for _i278 in range(_size274):
                        _elem279 = TTableName()
                        _elem279.read(iprot)
                        self.success.append(_elem279)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getTableNamesByNamespace_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter280 in self.success:
                iter280.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getTableNamesByNamespace_result)
getTableNamesByNamespace_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TTableName, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class createTable_args(object):
    __doc__ = '\n    Attributes:\n     - desc: table descriptor for table\n     - splitKeys: rray of split keys for the initial regions of the table\n    '

    def __init__(self, desc=None, splitKeys=None):
        self.desc = desc
        self.splitKeys = splitKeys

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.desc = TTableDescriptor()
                    self.desc.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.splitKeys = []
                    _etype284, _size281 = iprot.readListBegin()
                    for _i285 in range(_size281):
                        _elem286 = iprot.readBinary()
                        self.splitKeys.append(_elem286)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('createTable_args')
        if self.desc is not None:
            oprot.writeFieldBegin('desc', TType.STRUCT, 1)
            self.desc.write(oprot)
            oprot.writeFieldEnd()
        if self.splitKeys is not None:
            oprot.writeFieldBegin('splitKeys', TType.LIST, 2)
            oprot.writeListBegin(TType.STRING, len(self.splitKeys))
            for iter287 in self.splitKeys:
                oprot.writeBinary(iter287)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.desc is None:
            raise TProtocolException(message='Required field desc is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(createTable_args)
createTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'desc', [TTableDescriptor, None], None),
 (
  2, TType.LIST, 'splitKeys', (TType.STRING, 'BINARY', False), None))

class createTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('createTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(createTable_result)
createTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class deleteTable_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to delete\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteTable_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteTable_args)
deleteTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class deleteTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteTable_result)
deleteTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class truncateTable_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to truncate\n     - preserveSplits: whether to  preserve previous splits\n    '

    def __init__(self, tableName=None, preserveSplits=None):
        self.tableName = tableName
        self.preserveSplits = preserveSplits

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.BOOL:
                    self.preserveSplits = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('truncateTable_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.preserveSplits is not None:
            oprot.writeFieldBegin('preserveSplits', TType.BOOL, 2)
            oprot.writeBool(self.preserveSplits)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')
        if self.preserveSplits is None:
            raise TProtocolException(message='Required field preserveSplits is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(truncateTable_args)
truncateTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.BOOL, 'preserveSplits', None, None))

class truncateTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('truncateTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(truncateTable_result)
truncateTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class enableTable_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to enable\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('enableTable_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(enableTable_args)
enableTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class enableTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('enableTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(enableTable_result)
enableTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class disableTable_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to disable\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('disableTable_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(disableTable_args)
disableTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class disableTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('disableTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(disableTable_result)
disableTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class isTableEnabled_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to check\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableEnabled_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableEnabled_args)
isTableEnabled_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class isTableEnabled_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableEnabled_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableEnabled_result)
isTableEnabled_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class isTableDisabled_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to check\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableDisabled_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableDisabled_args)
isTableDisabled_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class isTableDisabled_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableDisabled_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableDisabled_result)
isTableDisabled_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class isTableAvailable_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to check\n    '

    def __init__(self, tableName=None):
        self.tableName = tableName

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableAvailable_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableAvailable_args)
isTableAvailable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None))

class isTableAvailable_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableAvailable_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableAvailable_result)
isTableAvailable_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class isTableAvailableWithSplit_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to check\n     - splitKeys: keys to check if the table has been created with all split keys\n    '

    def __init__(self, tableName=None, splitKeys=None):
        self.tableName = tableName
        self.splitKeys = splitKeys

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.splitKeys = []
                    _etype291, _size288 = iprot.readListBegin()
                    for _i292 in range(_size288):
                        _elem293 = iprot.readBinary()
                        self.splitKeys.append(_elem293)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableAvailableWithSplit_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.splitKeys is not None:
            oprot.writeFieldBegin('splitKeys', TType.LIST, 2)
            oprot.writeListBegin(TType.STRING, len(self.splitKeys))
            for iter294 in self.splitKeys:
                oprot.writeBinary(iter294)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableAvailableWithSplit_args)
isTableAvailableWithSplit_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.LIST, 'splitKeys', (TType.STRING, 'BINARY', False), None))

class isTableAvailableWithSplit_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('isTableAvailableWithSplit_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(isTableAvailableWithSplit_result)
isTableAvailableWithSplit_result.thrift_spec = (
 (
  0, TType.BOOL, 'success', None, None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class addColumnFamily_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to add column family to\n     - column: column family descriptor of column family to be added\n    '

    def __init__(self, tableName=None, column=None):
        self.tableName = tableName
        self.column = column

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.column = TColumnFamilyDescriptor()
                    self.column.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('addColumnFamily_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.column is not None:
            oprot.writeFieldBegin('column', TType.STRUCT, 2)
            self.column.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')
        if self.column is None:
            raise TProtocolException(message='Required field column is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(addColumnFamily_args)
addColumnFamily_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.STRUCT, 'column', [TColumnFamilyDescriptor, None], None))

class addColumnFamily_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('addColumnFamily_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(addColumnFamily_result)
addColumnFamily_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class deleteColumnFamily_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to delete column family from\n     - column: name of column family to be deleted\n    '

    def __init__(self, tableName=None, column=None):
        self.tableName = tableName
        self.column = column

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.column = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteColumnFamily_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.column is not None:
            oprot.writeFieldBegin('column', TType.STRING, 2)
            oprot.writeBinary(self.column)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')
        if self.column is None:
            raise TProtocolException(message='Required field column is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteColumnFamily_args)
deleteColumnFamily_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.STRING, 'column', 'BINARY', None))

class deleteColumnFamily_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteColumnFamily_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteColumnFamily_result)
deleteColumnFamily_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class modifyColumnFamily_args(object):
    __doc__ = '\n    Attributes:\n     - tableName: the tablename to modify column family\n     - column: column family descriptor of column family to be modified\n    '

    def __init__(self, tableName=None, column=None):
        self.tableName = tableName
        self.column = column

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.tableName = TTableName()
                    self.tableName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.column = TColumnFamilyDescriptor()
                    self.column.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyColumnFamily_args')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.column is not None:
            oprot.writeFieldBegin('column', TType.STRUCT, 2)
            self.column.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')
        if self.column is None:
            raise TProtocolException(message='Required field column is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyColumnFamily_args)
modifyColumnFamily_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.STRUCT, 'column', [TColumnFamilyDescriptor, None], None))

class modifyColumnFamily_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyColumnFamily_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyColumnFamily_result)
modifyColumnFamily_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class modifyTable_args(object):
    __doc__ = '\n    Attributes:\n     - desc: the descriptor of the table to modify\n    '

    def __init__(self, desc=None):
        self.desc = desc

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.desc = TTableDescriptor()
                    self.desc.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyTable_args')
        if self.desc is not None:
            oprot.writeFieldBegin('desc', TType.STRUCT, 1)
            self.desc.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.desc is None:
            raise TProtocolException(message='Required field desc is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyTable_args)
modifyTable_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'desc', [TTableDescriptor, None], None))

class modifyTable_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyTable_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyTable_result)
modifyTable_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class createNamespace_args(object):
    __doc__ = '\n    Attributes:\n     - namespaceDesc: descriptor which describes the new namespace\n    '

    def __init__(self, namespaceDesc=None):
        self.namespaceDesc = namespaceDesc

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.namespaceDesc = TNamespaceDescriptor()
                    self.namespaceDesc.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('createNamespace_args')
        if self.namespaceDesc is not None:
            oprot.writeFieldBegin('namespaceDesc', TType.STRUCT, 1)
            self.namespaceDesc.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.namespaceDesc is None:
            raise TProtocolException(message='Required field namespaceDesc is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(createNamespace_args)
createNamespace_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'namespaceDesc', [TNamespaceDescriptor, None], None))

class createNamespace_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('createNamespace_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(createNamespace_result)
createNamespace_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class modifyNamespace_args(object):
    __doc__ = '\n    Attributes:\n     - namespaceDesc: descriptor which describes the new namespace\n    '

    def __init__(self, namespaceDesc=None):
        self.namespaceDesc = namespaceDesc

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.namespaceDesc = TNamespaceDescriptor()
                    self.namespaceDesc.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyNamespace_args')
        if self.namespaceDesc is not None:
            oprot.writeFieldBegin('namespaceDesc', TType.STRUCT, 1)
            self.namespaceDesc.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.namespaceDesc is None:
            raise TProtocolException(message='Required field namespaceDesc is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyNamespace_args)
modifyNamespace_args.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'namespaceDesc', [TNamespaceDescriptor, None], None))

class modifyNamespace_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('modifyNamespace_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(modifyNamespace_result)
modifyNamespace_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class deleteNamespace_args(object):
    __doc__ = '\n    Attributes:\n     - name: namespace name\n    '

    def __init__(self, name=None):
        self.name = name

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteNamespace_args')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteNamespace_args)
deleteNamespace_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'UTF8', None))

class deleteNamespace_result(object):
    __doc__ = '\n    Attributes:\n     - io\n    '

    def __init__(self, io=None):
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('deleteNamespace_result')
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(deleteNamespace_result)
deleteNamespace_result.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class getNamespaceDescriptor_args(object):
    __doc__ = '\n    Attributes:\n     - name: name of namespace descriptor\n    '

    def __init__(self, name=None):
        self.name = name

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getNamespaceDescriptor_args')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getNamespaceDescriptor_args)
getNamespaceDescriptor_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'UTF8', None))

class getNamespaceDescriptor_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TNamespaceDescriptor()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.io = TIOError()
                    self.io.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('getNamespaceDescriptor_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(getNamespaceDescriptor_result)
getNamespaceDescriptor_result.thrift_spec = (
 (
  0, TType.STRUCT, 'success', [TNamespaceDescriptor, None], None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class listNamespaceDescriptors_args(object):

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('listNamespaceDescriptors_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(listNamespaceDescriptors_args)
listNamespaceDescriptors_args.thrift_spec = ()

class listNamespaceDescriptors_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype298, _size295 = iprot.readListBegin()
                    for _i299 in range(_size295):
                        _elem300 = TNamespaceDescriptor()
                        _elem300.read(iprot)
                        self.success.append(_elem300)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('listNamespaceDescriptors_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter301 in self.success:
                iter301.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(listNamespaceDescriptors_result)
listNamespaceDescriptors_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRUCT, [TNamespaceDescriptor, None], False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))

class listNamespaces_args(object):

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('listNamespaces_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(listNamespaces_args)
listNamespaces_args.thrift_spec = ()

class listNamespaces_result(object):
    __doc__ = '\n    Attributes:\n     - success\n     - io\n    '

    def __init__(self, success=None, io=None):
        self.success = success
        self.io = io

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    _etype305, _size302 = iprot.readListBegin()
                    for _i306 in range(_size302):
                        _elem307 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.success.append(_elem307)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.io = TIOError()
                        self.io.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('listNamespaces_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRING, len(self.success))
            for iter308 in self.success:
                oprot.writeString(iter308.encode('utf-8') if sys.version_info[0] == 2 else iter308)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.io is not None:
            oprot.writeFieldBegin('io', TType.STRUCT, 1)
            self.io.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(listNamespaces_result)
listNamespaces_result.thrift_spec = (
 (
  0, TType.LIST, 'success', (TType.STRING, 'UTF8', False), None),
 (
  1, TType.STRUCT, 'io', [TIOError, None], None))
fix_spec(all_structs)
del all_structs