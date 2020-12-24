# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\iress\ado.py
# Compiled at: 2012-04-24 01:55:05
"""
Pythonic interface to the ADO stored procedures exposed
by the Iress Portfolio System (IPS).

"""
import win32com.client, pywintypes

def convert_com_dates_to_mx(records):
    import mx.DateTime
    for d in records:
        for k in d:
            if isinstance(d[k], pywintypes.TimeType):
                d[k] = mx.DateTime.DateTimeFromCOMDate(d[k])

    return records


def _extract_recordset(recordset):
    """
    Converts a ADODB.RecordSet object into a list
    of Python dictionaries.

    """
    records = []
    count = recordset.Fields.Count
    keys = [ recordset.Fields(i).Name for i in range(count) ]
    while not recordset.EOF:
        records.append(dict(zip(keys, [ recordset.Fields(i).Value for i in range(count) ])))
        recordset.MoveNext()

    return records


class IressADOClient(object):
    """
    Pythonic wrapper around the IRESS OleDB API.

    """

    def __init__(self):
        self.c = None
        return

    def connect--- This code section failed: ---

 L.  48         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'c'
                6  LOAD_CONST               None
                9  COMPARE_OP            8  is
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Already connected.'
               21  RAISE_VARARGS_2       2  None

 L.  49        24  LOAD_GLOBAL           3  'win32com'
               27  LOAD_ATTR             4  'client'
               30  LOAD_ATTR             5  'Dispatch'
               33  LOAD_CONST               'ADODB.Connection'
               36  CALL_FUNCTION_1       1  None
               39  LOAD_FAST             0  'self'
               42  STORE_ATTR            0  'c'

 L.  50        45  LOAD_CONST               'IRESSOleDBProvider.IOleDBP.1'
               48  LOAD_FAST             0  'self'
               51  LOAD_ATTR             0  'c'
               54  STORE_ATTR            6  'Provider'

 L.  51        57  LOAD_FAST             0  'self'
               60  LOAD_ATTR             0  'c'
               63  LOAD_ATTR             7  'Open'
               66  CALL_FUNCTION_0       0  None
               69  POP_TOP          
               70  LOAD_CONST               None
               73  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 70

    def get_procedures(self):
        """
        Returns a list of the available stored procedures.

        """
        rs = self.c.OpenSchema(16, ['IPS'])
        return [ record['PROCEDURE_NAME'] for record in _extract_recordset(rs) ]

    def get_procedure_params(self, procedure):
        """
        Gets the list of parameters for a given stored procedure.

        """
        cmd = self._create_command(procedure)
        cmd.Parameters.Refresh()
        parameters = [ cmd.Parameters(i).Name for i in range(cmd.Parameters.Count) ]
        parameters.sort()
        return parameters

    def _create_command(self, procedure):
        """
        Create an ADODB.Command object prepared to call
        a stored procedure.

        """
        cmd = win32com.client.Dispatch('ADODB.Command')
        cmd.CommandType = 4
        cmd.CommandText = procedure
        cmd.ActiveConnection = self.c
        return cmd

    def execute_procedure(self, procedure, parameters=None):
        """
        Executes a stored procedure pasing in the given
        parameters.

        """
        parameters = parameters or {}
        cmd = self._create_command(procedure)
        for k, v in parameters.iteritems():
            cmd.Parameters(procedure.lower() + '_' + k.lower()).Value = v

        rs, count = cmd.Execute()
        return _extract_recordset(rs)