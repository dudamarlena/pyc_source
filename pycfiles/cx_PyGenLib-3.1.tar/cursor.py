# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/cursor.py
# Compiled at: 2015-05-19 16:59:20
from ctypes import byref
import ctypes, oci
from pythonic_oci import OCIAttrGet, OCIParamGet, OCIHandleAlloc
from custom_exceptions import InterfaceError, ProgrammingError, DatabaseError, NotSupportedError
from buffer import cxBuffer
from utils import is_sequence, cxString_from_encoded_string, python3_or_better
from variable_factory import VariableFactory
from objectvar import OBJECTVAR
from numbervar import NUMBER
from stringvar import STRING, BINARY, FIXED_CHAR
from datetimevar import DATETIME
if not python3_or_better():
    from stringvar import UNICODE, FIXED_UNICODE
variable_factory = VariableFactory()

class Cursor(object):

    def __init__(self, connection):
        """Create a new cursor object."""
        self.connection = connection
        self.environment = connection.environment
        self.arraysize = 50
        self.fetch_array_size = 50
        self.bindarraysize = 1
        self.statement_type = -1
        self.output_size = -1
        self.output_size_column = -1
        self.is_open = True
        self.handle = oci.POINTER(oci.OCIStmt)()
        self.statement = None
        self.input_sizes = 0
        self.numbersAsStrings = None
        self.inputtypehandler = None
        self.outputtypehandler = None
        self.rowfactory = None
        self.is_owned = False

    def raise_if_not_open(self):
        if not self.is_open:
            raise InterfaceError('not open')
        return self.connection.raise_if_not_connected()

    def free_handle(self, raise_exception):
        """Free the handle which may be reallocated if necessary."""
        if self.handle:
            if self.is_owned:
                status = oci.OCIHandleFree(self.handle, oci.OCI_HTYPE_STMT)
                if raise_exception:
                    self.environment.check_for_error(status, 'Cursor_FreeHandle()')
            elif self.connection.handle:
                try:
                    buffer = cxBuffer.new_from_object(self.statement_tag, self.environment.encoding)
                except:
                    if raise_exception:
                        raise

                status = oci.OCIStmtRelease(self.handle, self.environment.error_handle, buffer.cast_ptr, buffer.size, oci.OCI_DEFAULT)
                if raise_exception:
                    self.environment.check_for_error(status, 'Cursor_FreeHandle()')
            self.handle = oci.POINTER(oci.OCIStmt)()

    def internal_prepare(self, statement, statement_tag):
        """Internal method for preparing a statement for execution."""
        if statement is None:
            if not self.statement:
                raise ProgrammingError('no statement specified and no prior statement prepared')
            if statement is None or statement == self.statement:
                if self.statement_type not in (oci.OCI_STMT_CREATE, oci.OCI_STMT_DROP, oci.OCI_STMT_ALTER):
                    return
                statement = self.statement
            self.statement = statement
            self.statement_tag = statement_tag
            self.free_handle(True)
            self.is_owned = False
            statement_buffer = cxBuffer.new_from_object(statement, self.environment.encoding)
            tag_buffer = cxBuffer.new_from_object(statement_tag, self.environment.encoding)
            status = oci.OCIStmtPrepare2(self.connection.handle, byref(self.handle), self.environment.error_handle, statement_buffer.cast_ptr, statement_buffer.size, tag_buffer.cast_ptr, tag_buffer.size, oci.OCI_NTV_SYNTAX, oci.OCI_DEFAULT)
            try:
                self.environment.check_for_error(status, 'Cursor_InternalPrepare(): prepare')
            except:
                self.handle = oci.POINTER(oci.OCIStmt)()
                raise

            self.bindvars = self.input_sizes or None
        self.row_factory = None
        self.get_statement_type()

    def get_statement_type(self):
        self.statement_type = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, oci.ub2, oci.OCI_ATTR_STMT_TYPE, self.environment, 'Cursor_GetStatementType()')
        self.fetchvars = None

    def perform_define(self):
        num_params = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, ctypes.c_int, oci.OCI_ATTR_PARAM_COUNT, self.environment, 'Cursor_PerformDefine()')
        self.fetchvars = [
         None] * num_params
        self.fetch_array_size = self.arraysize
        for pos in xrange(1, num_params + 1):
            var = variable_factory.define(self, self.fetch_array_size, pos)
            self.fetchvars[pos - 1] = var

    def internal_execute(self, num_iters):
        """Perform the work of executing a cursor and set the rowcount appropriately
           regardless of whether an error takes place."""
        if self.connection.autocommit:
            mode = oci.OCI_COMMIT_ON_SUCCESS
        else:
            mode = oci.OCI_DEFAULT
        argtypes = oci.OCIStmtExecute.argtypes
        status = oci.OCIStmtExecute(self.connection.handle, self.handle, self.environment.error_handle, num_iters, 0, argtypes[5](), argtypes[6](), mode)
        try:
            self.environment.check_for_error(status, 'Cursor_InternalExecute()')
        except Exception as e:
            new_exception = self.set_error_offset(e)
            try:
                self.set_row_count()
            except:
                pass

            raise new_exception

        return self.set_row_count()

    def set_bind_variables(self, parameters, num_elements, array_pos, defer_type_assignment):
        """Create or set bind variables."""
        num_params = 0
        bound_by_pos = is_sequence(parameters)
        if bound_by_pos:
            num_params = len(parameters)
        if self.bindvars:
            orig_bound_by_pos = isinstance(self.bindvars, list)
            if bound_by_pos != orig_bound_by_pos:
                raise ProgrammingError('positional and named binds cannot be intermixed')
            orig_num_params = len(self.bindvars)
        else:
            if bound_by_pos:
                self.bindvars = [
                 None] * num_params
            else:
                self.bindvars = {}
            orig_num_params = 0
        if bound_by_pos:
            for i, value in enumerate(parameters):
                if i < orig_num_params:
                    orig_var = self.bindvars[i]
                else:
                    orig_var = None
                new_var = self.set_bind_variable_helper(num_elements, array_pos, value, orig_var, defer_type_assignment)
                if new_var:
                    if i < len(self.bindvars):
                        self.bindvars[i] = new_var
                    else:
                        self.bindvars.append(new_var)

        else:
            for key, value in parameters.iteritems():
                orig_var = self.bindvars.get(key, None)
                new_var = self.set_bind_variable_helper(num_elements, array_pos, value, orig_var, defer_type_assignment)
                if new_var:
                    self.bindvars[key] = new_var

    def set_bind_variable_helper(self, num_elements, array_pos, value, orig_var, defer_type_assignment):
        """Helper for setting a bind variable."""
        from variable import Variable
        new_var = None
        is_value_var = isinstance(value, Variable)
        del Variable
        if orig_var:
            if is_value_var:
                if orig_var != value:
                    new_var = value
            elif num_elements > orig_var.numElements:
                new_var = variable_factory.new(self, num_elements, orig_var.type, orig_var.size)
                new_var.set_value(array_pos, value)
            else:
                try:
                    orig_var.set_value(array_pos, value)
                except Exception as e:
                    if array_pos > 0:
                        raise
                    if not isinstance(e, (IndexError, TypeError)):
                        raise
                    orig_var = None

        if not orig_var:
            if is_value_var:
                new_var = value
                new_var.bound_pos = 0
                new_var.bound_name = None
            elif not (value is not None or defer_type_assignment):
                new_var = variable_factory.new_by_value(self, value, num_elements)
                new_var.set_value(array_pos, value)
        return new_var

    def execute(self, statement, *args, **kwargs):
        """Execute the statement."""
        execute_args = undefined = object()
        if args:
            execute_args = args[0]
        if execute_args is not undefined and kwargs:
            raise InterfaceError('expecting argument or keyword arguments, not both')
        if kwargs:
            execute_args = kwargs
        if execute_args is not undefined:
            if not isinstance(execute_args, dict):
                raise (is_sequence(execute_args) or TypeError)('expecting a dictionary, sequence or keyword args')
        self.raise_if_not_open()
        self.internal_prepare(statement, None)
        if execute_args is not undefined:
            self.set_bind_variables(execute_args, 1, 0, 0)
        self.perform_bind()
        is_query = self.statement_type == oci.OCI_STMT_SELECT
        if is_query:
            num_iters = 0
        else:
            num_iters = 1
        self.internal_execute(num_iters)
        if is_query and self.fetchvars is None:
            self.perform_define()
        self.output_size = -1
        self.output_size_column = -1
        if is_query:
            return self

    def prepare(self, statement, statement_tag=None):
        """Prepare the statement for execution."""
        self.raise_if_not_open()
        self.internal_prepare(statement, statement_tag)

    def executemany(self, statement, list_of_arguments):
        """Execute the statement many times. The number of times is equivalent to the number of elements in the array 
of dictionaries."""
        self.prepare(statement, None)
        if self.statement_type == oci.OCI_STMT_SELECT:
            raise NotSupportedError('queries not supported: results undefined')
        num_rows = len(list_of_arguments)
        for i, arguments in enumerate(list_of_arguments):
            if not isinstance(arguments, dict):
                raise (is_sequence(arguments) or InterfaceError)('expecting a list of dictionaries or sequences')
            self.set_bind_variables(arguments, num_rows, i, i < num_rows - 1)

        self.perform_bind()
        if num_rows > 0:
            self.internal_execute(num_rows)

    def set_row_count(self):
        """Set the rowcount variable."""
        if self.statement_type == oci.OCI_STMT_SELECT:
            self.rowcount = 0
            self.actual_rows = -1
            self.row_num = 0
        elif self.statement_type in (oci.OCI_STMT_INSERT, oci.OCI_STMT_UPDATE, oci.OCI_STMT_DELETE):
            self.rowcount = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, oci.ub4, oci.OCI_ATTR_ROW_COUNT, self.environment, 'Cursor_SetRowCount()')
        else:
            self.rowcount = -1

    def perform_bind(self):
        """Perform the binds on the cursor."""
        self.input_sizes = 0
        if self.bindvars:
            if isinstance(self.bindvars, dict):
                for key, var in self.bindvars.iteritems():
                    var.bind(self, key, 0)

            else:
                for i, var in enumerate(self.bindvars):
                    if var is not None:
                        var.bind(self, None, i + 1)

    def fixup_bound_cursor(self):
        """Fixup a cursor so that fetching and returning cursor descriptions are successful after binding a cursor to another cursor."""
        if self.handle and self.statement_type < 0:
            self.get_statement_type()
            try:
                self.perform_define()
            except:
                if self.statement_type == oci.OCI_STMT_SELECT:
                    raise

            self.set_row_count()

    def verify_fetch(self):
        self.raise_if_not_open()
        self.fixup_bound_cursor()
        if self.statement_type != oci.OCI_STMT_SELECT:
            raise InterfaceError('not a query')

    def internal_fetch(self, num_rows):
        """Performs the actual fetch from Oracle."""
        if not self.fetchvars:
            raise InterfaceError('query not executed')
        for var in self.fetchvars:
            var.internal_fetch_num += 1
            if var.type.pre_fetch_proc:
                var.type.pre_fetch_proc(var)

        status = oci.OCIStmtFetch(self.handle, self.environment.error_handle, num_rows, oci.OCI_FETCH_NEXT, oci.OCI_DEFAULT)
        if status != oci.OCI_NO_DATA:
            self.environment.check_for_error(status, 'Cursor_InternalFetch(): fetch')
        row_count = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, oci.ub4, oci.OCI_ATTR_ROW_COUNT, self.environment, 'Cursor_InternalFetch(): row count')
        self.actual_rows = row_count - self.rowcount
        self.row_num = 0

    def create_row(self):
        """Create an object for the row. The object created is a tuple unless a row
           factory function has been defined in which case it is the result of the
           row factory function called with the argument tuple that would otherwise be
           returned."""
        result_as_list = [
         None] * len(self.fetchvars)
        for pos, var in enumerate(self.fetchvars):
            item = var.getvalue(self.row_num)
            result_as_list[pos] = item

        self.row_num += 1
        self.rowcount += 1
        result_as_tuple = tuple(result_as_list)
        if self.rowfactory is not None:
            return self.rowfactory(result_as_tuple)
        return result_as_tuple

    def more_rows(self):
        """Returns a boolean indicating if more rows can be retrieved from the cursor."""
        if self.row_num >= self.actual_rows:
            if self.actual_rows < 0 or self.actual_rows == self.fetch_array_size:
                self.internal_fetch(self.fetch_array_size)
            if self.row_num >= self.actual_rows:
                return False
        return True

    def fetchmany(self, rowLimit=None):
        if rowLimit is None:
            rowLimit = self.arraysize
        self.verify_fetch()
        return self.multi_fetch(rowLimit)

    def fetchone(self):
        """Fetch a single row from the cursor."""
        self.verify_fetch()
        more_rows_to_fetch = self.more_rows()
        if more_rows_to_fetch:
            return self.create_row()

    def fetchall(self):
        """Fetch all remaining rows from the cursor."""
        self.verify_fetch()
        return self.multi_fetch(0)

    def multi_fetch(self, row_limit):
        """Return a list consisting of the remaining rows up to the given row limit (if specified)."""
        results = []
        row_num = 0
        while row_limit == 0 or row_num < row_limit:
            more_rows_available = self.more_rows()
            if more_rows_available:
                row = self.create_row()
                results.append(row)
            else:
                break
            row_num += 1

        return results

    def set_error_offset(self, exception):
        """Set the error offset on the error object, if applicable."""
        if isinstance(exception, DatabaseError):
            error = exception.args[0]
            try:
                error.offset = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, oci.ub4, oci.OCI_ATTR_PARSE_ERROR_OFFSET, self.environment, "Cursor_SetErrorOffset: can't get get oci attr")
            except DatabaseError:
                pass

        return exception

    def call_build_statement(self, name, return_value, list_of_arguments, keyword_arguments):
        """Determine the statement and the bind variables to bind to the statement that is created for calling a stored procedure or function."""
        if list_of_arguments:
            bindvars = list(list_of_arguments)
        else:
            bindvars = []
        if return_value:
            bindvars.insert(0, return_value)
        format_args = [
         name]
        arg_num = 1
        statement_template = 'begin '
        if return_value:
            statement_template += ':1 := '
            arg_num += 1
        statement_template += '%s ('
        if list_of_arguments:
            for i, argument in enumerate(list_of_arguments):
                if i > 0:
                    statement_template += ','
                statement_template += ':%d' % arg_num
                arg_num += 1
                if isinstance(argument, bool):
                    statement_template += ' = 1'

        if keyword_arguments:
            pos = 0
            for key, value in keyword_arguments.iteritems():
                bindvars.append(value)
                format_args.append(key)
                if arg_num > 1 and return_value and arg_num > 2 and return_value:
                    statement_template += ','
                statement_template += '%%s => :%d' % arg_num
                arg_num += 1
                if isinstance(value, bool):
                    statement_template += ' = 1'

        statement_template += '); end;'
        statement = statement_template % tuple(format_args)
        return (
         statement, bindvars)

    def call(self, return_value, name, list_of_arguments, keyword_arguments):
        """Call a stored procedure or function."""
        if list_of_arguments:
            if not is_sequence(list_of_arguments):
                raise TypeError('arguments must be a sequence')
        self.raise_if_not_open()
        statement, bindvars = self.call_build_statement(name, return_value, list_of_arguments, keyword_arguments)
        self.execute(statement, bindvars)

    def callproc(self, name, parameters=None, keywordParameters=None):
        """Call a stored procedure and return the (possibly modified) arguments."""
        self.call(None, name, parameters, keywordParameters)
        results = [ var.getvalue(0) ]
        return results

    def callfunc(self, name, return_type, parameters=None, keywordParameters=None):
        """Call a stored function and return the return value of the function."""
        var = variable_factory.new_by_type(self, return_type, 1)
        self.call(var, name, parameters, keywordParameters)
        results = var.getvalue(0)
        return results

    def close(self):
        self.raise_if_not_open()
        self.free_handle(True)
        self.is_open = False

    def get_bind_names(self, num_elements):
        """Return a list of bind variable names. At this point the cursor must have already been prepared."""
        if not self.statement:
            raise ProgrammingError('statement must be prepared first')
        num_elements = num_elements + (ctypes.sizeof(ctypes.c_void_p) - num_elements % ctypes.sizeof(ctypes.c_void_p))
        bind_names = (ctypes.c_char_p * num_elements)()
        bind_name_lengths = (oci.ub1 * num_elements)()
        indicator_names = (ctypes.c_char_p * num_elements)()
        indicator_name_lengths = (oci.ub1 * num_elements)()
        duplicate = (oci.ub1 * num_elements)()
        bind_handles = (oci.POINTER(oci.OCIBind) * num_elements)()
        cast_bind_names = ctypes.cast(bind_names, oci.POINTER(oci.POINTER(oci.ub1)))
        cast_indicator_names = ctypes.cast(indicator_names, oci.POINTER(oci.POINTER(oci.ub1)))
        c_found_elements = oci.sb4()
        status = oci.OCIStmtGetBindInfo(self.handle, self.environment.error_handle, num_elements, 1, byref(c_found_elements), cast_bind_names, bind_name_lengths, cast_indicator_names, indicator_name_lengths, duplicate, bind_handles)
        found_elements = c_found_elements.value
        try:
            self.environment.check_for_error(status, 'Cursor_GetBindNames()')
        except:
            if status != oci.OCI_NO_DATA:
                raise

        if found_elements < 0:
            names = None
            return (
             abs(found_elements), names)
        names = []
        for i in xrange(found_elements):
            if not duplicate[i]:
                temp = cxString_from_encoded_string(bind_names[i], self.connection.environment.encoding)
                names.append(temp)

        return (num_elements, names)

    def bindnames(self):
        """Return a list of bind variable names."""
        self.raise_if_not_open()
        found_elements, names = self.get_bind_names(8)
        if found_elements < 0:
            return
        found_elements, names = self.get_bind_names(found_elements)
        if names or found_elements < 0:
            return
        return names

    def __iter__(self):
        """Return a reference to the cursor which supports the iterator protocol."""
        self.verify_fetch()
        return self

    def next(self):
        """Return a reference to the cursor which supports the iterator protocol."""
        self.verify_fetch()
        more_rows_available = self.more_rows()
        if more_rows_available:
            return self.create_row()
        raise StopIteration()

    def __del__(self):
        self.free_handle(False)

    def var(self, type, size=0, arraysize=None, inconverter=None, outconverter=None, typename=None):
        """Create a bind variable and return it."""
        if arraysize is None:
            arraysize = self.bindarraysize
        array_size = arraysize
        var_type = variable_factory.type_by_python_type(self, type)
        if var_type.is_variable_length and size == 0:
            size = var_type.size
        if type is OBJECTVAR:
            raise (typename or TypeError)('expecting type name for object variables')
        var = variable_factory.new(self, array_size, var_type, size)
        var.inconverter = inconverter
        var.outconverter = outconverter
        if type is OBJECTVAR:
            var.object_type = ObjectType.new_by_name(self.connection, typeName)
        return var

    def setinputsizes(self, *args, **kwargs):
        """Set the sizes of the bind variables."""
        if args and kwargs:
            raise InterfaceError('expecting arguments or keyword arguments, not both')
        self.raise_if_not_open()
        if kwargs:
            self.bindvars = {}
        else:
            self.bindvars = [
             None] * len(args)
        self.input_sizes = 1
        if kwargs:
            for key, value in kwargs.iteritems():
                var = variable_factory.new_by_type(self, value, self.bindarraysize)
                self.bindvars[key] = var

        else:
            for i, value in enumerate(args):
                if value is None:
                    var = None
                else:
                    var = variable_factory.new_by_type(self, value, self.bindarraysize)
                self.bindvars[i] = var

        return self.bindvars

    def arrayvar(self, type, value, size=0):
        """Create an array bind variable and return it."""
        var_type = variable_factory.type_by_python_type(self, type)
        if var_type.is_variable_length and size == 0:
            size = var_type.size
        if isinstance(value, list):
            num_elements = len(value)
        elif isinstance(value, int):
            num_elements = value
        else:
            raise TypeError('expecting integer or list of values')
        var = variable_factory.new(self, num_elements, var_type, size)
        var.make_array()
        if isinstance(value, list):
            var.set_array_value(value)
        return var

    def get_item_description_helper(self, pos, param):
        """Helper for Cursor_ItemDescription() used so that it is not necessary to
constantly free the descriptor when an error takes place."""
        var_type = variable_factory.type_by_oracle_descriptor(param, self.environment)
        internal_size = OCIAttrGet(param, oci.OCI_HTYPE_DESCRIBE, oci.ub2, oci.OCI_ATTR_DATA_SIZE, self.environment, 'Cursor_ItemDescription(): internal size')
        char_size = OCIAttrGet(param, oci.OCI_HTYPE_DESCRIBE, oci.ub2, oci.OCI_ATTR_CHAR_SIZE, self.environment, 'Cursor_ItemDescription(): character size')
        c_name = ctypes.c_char_p()
        c_name_length = oci.ub4()
        status = oci.OCIAttrGet(param, oci.OCI_HTYPE_DESCRIBE, byref(c_name), byref(c_name_length), oci.OCI_ATTR_NAME, self.environment.error_handle)
        self.environment.check_for_error(status, 'Cursor_ItemDescription(): name')
        name = c_name.value[:c_name_length.value]
        python_type = var_type.python_type
        precision, scale = python_type.lookup_precision_and_scale(self.environment, param)
        null_ok = OCIAttrGet(param, oci.OCI_HTYPE_DESCRIBE, oci.ub1, oci.OCI_ATTR_IS_NULL, self.environment, 'Cursor_ItemDescription(): nullable')
        display_size = python_type.get_display_size(precision, scale, char_size, internal_size)
        result = (
         cxString_from_encoded_string(name, self.connection.environment.encoding), python_type, display_size, internal_size, precision, scale, null_ok)
        return result

    def get_item_description(self, pos):
        """Return a tuple describing the item at the given position."""
        param = OCIParamGet(self.handle, oci.OCI_HTYPE_STMT, self.environment, pos, 'Cursor_ItemDescription(): parameter')
        description_element = self.get_item_description_helper(pos, param)
        oci.OCIDescriptorFree(param, oci.OCI_DTYPE_PARAM)
        return description_element

    @property
    def description(self):
        """Return a list of 7-tuples consisting of the description of the define variables."""
        self.raise_if_not_open()
        self.fixup_bound_cursor()
        if self.statement_type != oci.OCI_STMT_SELECT:
            return
        num_items = OCIAttrGet(self.handle, oci.OCI_HTYPE_STMT, ctypes.c_int, oci.OCI_ATTR_PARAM_COUNT, self.environment, 'Cursor_GetDescription()')
        results = [
         None] * num_items
        for index in xrange(num_items):
            description_element = self.get_item_description(index + 1)
            results[index] = description_element

        return results

    def setoutputsize(self, size, column=-1):
        """Set the size of all of the long columns or just one of them."""
        self.output_size = size
        self.output_size_column = column

    def allocate_handle(self):
        self.is_owned = True
        OCIHandleAlloc(self.environment, self.handle, oci.OCI_HTYPE_STMT, 'Cursor_New()')