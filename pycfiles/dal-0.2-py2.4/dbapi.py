# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dal/dbapi/dbapi.py
# Compiled at: 2007-06-15 17:41:24
""" Wraps DB-API V2 compliant database drivers.

LICENSE
=======

Copyright (c) 2004, Randall Smith
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Usage Example:
import dal
dbmod = dal.wrapdriver('psycopg')
# (Optional) Set the datetime type you want to use.
# Defaults to Python's datetime module.  Can be 'mx', 'py', or 'native'.
dbmod.dtmod = 'py' # Python datetime module.
# (Optional) Set the paramstyle. Defaults to qmark.
dbmod.paramstyle = qmark
cn = dbmod.connect(host='myhost', database='mydb', user='me', password='mypw')
cs = cn.cursor()
query = "Select * from mytable where dtfield = ?"
params = [dbmod.Date(2004, 7, 1)]
cs.execute(query, params)
result = cs.fetchall()
"""
__revision__ = 0.1
import dbtime, paramstyles

class MWrapper(object):
    """Wraps DBAPI2 driver."""
    __module__ = __name__

    def __init__(self, driver, drivername):
        object.__init__(self)
        self._driver = driver
        self._drivername = drivername
        if '\\' in paramstyles.ESCAPE_CHARS:
            paramstyles.ESCAPE_CHARS.remove('\\')
        try:
            self._config = __import__('config_' + drivername, globals())
            if hasattr(self._config, 'init1'):
                self._config.init1(self)
            if hasattr(self._config, 'escape_chars'):
                paramstyles.ESCAPE_CHARS.extend(self._config.escape_chars)
            if hasattr(self._config, 'quote_chars'):
                paramstyles.QUOTE_CHARS.extend(self._config.quote_chars)
        except ImportError:
            self._config = False

        self.__use_db_row = False
        self.apilevel = '2.0'
        self.threadsafety = 0
        self.paramstyle = 'qmark'
        self.__dtmod = 'py'
        self.DATETIME = self._driver.DATETIME
        self.STRING = self._driver.STRING
        self.BINARY = self._driver.BINARY
        self.NUMBER = self._driver.NUMBER
        self.ROWID = self._driver.ROWID
        self.__setExceptions()
        if hasattr(self._config, 'init2'):
            self._config.init2(self)

    def __getDtMod(self):
        return self.__dtmod

    def __setDtMod(self, dtmodname):
        assert dtmodname in ('py', 'mx', 'native')
        if dtmodname == 'py':
            if not dbtime.have_datetime:
                raise Exception, 'datetime module not available.'
        elif dtmodname == 'mx':
            if not dbtime.have_mxDateTime:
                raise Exception, 'mx.DateTime module not available.'
        self.__dtmod = dtmodname

    dtmod = property(__getDtMod, __setDtMod)

    def __getUseDbRow(self):
        return self.__use_db_row

    def __setUseDbRow(self, use_db_row):
        if use_db_row:
            import db_row
            globals()['db_row'] = db_row
        self.__use_db_row = use_db_row

    use_db_row = property(__getUseDbRow, __setUseDbRow)

    def __setExceptions(self):

        class Warning(StandardError):
            __module__ = __name__

        class Error(StandardError):
            __module__ = __name__

        class InterfaceError(Error):
            __module__ = __name__

        class DatabaseError(Error):
            __module__ = __name__

        class DataError(DatabaseError):
            __module__ = __name__

        class OperationalError(DatabaseError):
            __module__ = __name__

        class IntegrityError(DatabaseError):
            __module__ = __name__

        class InternalError(DatabaseError):
            __module__ = __name__

        class ProgrammingError(DatabaseError):
            __module__ = __name__

        class NotSupportedError(DatabaseError):
            __module__ = __name__

        dbapi_exceptions = [
         'Warning', 'Error', 'InterfaceError', 'DatabaseError', 'DataError', 'OperationalError', 'IntegrityError', 'InternalError', 'ProgrammingError', 'NotSupportedError']
        driver = self._driver
        for exception in dbapi_exceptions:
            setattr(self, exception, locals()[exception])
            sub_exception = getattr(driver, exception)
            dbapi_exception = locals()[exception]
            sub_exception.__bases__ += (dbapi_exception,)

    def Date(self, year, month, day):
        if self.dtmod == 'native':
            result = self._driver.Date(year, month, day)
        else:
            result = dbtime.construct_date(self.dtmod, year, month, day)
        return result

    def Time(self, hour, minute, second):
        if self.dtmod == 'native':
            result = self._driver.Time(hour, minute, second)
        else:
            result = dbtime.construct_time(self.dtmod, hour, minute, second)
        return result

    def Timestamp(self, year, month, day, hour, minute, second):
        if self.dtmod == 'native':
            result = self._driver.Timestamp(year, month, day, hour, minute, second)
        else:
            result = dbtime.construct_timestamp(self.dtmod, year, month, day, hour, minute, second)
        return result

    def DateFromTicks(self, ticks):
        if self.dtmod == 'native':
            result = self._driver.DateFromTicks(ticks)
        else:
            result = dbtime.construct_datefromticks(self.dtmod, ticks)
        return result

    def TimeFromTicks(self, ticks):
        if self.dtmod == 'native':
            result = self._driver.TimeFromTicks(ticks)
        else:
            result = dbtime.construct_timefromticks(self.dtmod, ticks)
        return result

    def TimestampFromTicks(self, ticks):
        if self.dtmod == 'native':
            result = self._driver.TimestampFromTicks(ticks)
        else:
            result = dbtime.construct_timestampfromticks(self.dtmod, ticks)
        return result

    def Binary(self, string):
        return self._driver.Binary(string)

    def connect(self, *args, **kwargs):
        """Return connection object."""
        return Connection(self, *args, **kwargs)


class Connection(object):
    """Wrapper for connection object."""
    __module__ = __name__

    def __init__(self, mwrapper, *args, **kwargs):
        object.__init__(self)
        self._mwrapper = mwrapper
        self._native_cn = mwrapper._driver.connect(*args, **kwargs)

    def close(self):
        return self._native_cn.close()

    def commit(self):
        return self._native_cn.commit()

    def rollback(self):
        return self._native_cn.rollback()

    def cursor(self):
        """Return a wrapped cursor."""
        return Cursor(self, self._native_cn)


class Cursor(object):
    """Wrapper for cursor object."""
    __module__ = __name__

    def __init__(self, wrapper_cn, native_cn):
        object.__init__(self)
        self._wrapper_cn = wrapper_cn
        self._mwrapper = wrapper_cn._mwrapper
        self._driver = self._mwrapper._driver
        self._drivername = self._mwrapper._drivername
        self._native_cs = native_cn.cursor()
        self._native_cs.arraysize = 1
        self._siface = False
        self._datetimeo = True
        self.dtmod = self._mwrapper.dtmod
        self.__use_db_row = self._mwrapper.use_db_row
        self.__paramstyle = self._mwrapper.paramstyle

    def __getDbRow(self):
        """Return value of use_db_row for cursor."""
        return self.__use_db_row

    def __setDbRow(self, use_db_row):
        """Set value of use_db_row for cursor."""
        if use_db_row:
            import db_row
            globals()['db_row'] = db_row
        self.__use_db_row = use_db_row

    use_db_row = property(__getDbRow, __setDbRow)

    def __getParamstyle(self):
        """Return value of paramstyle for cursor."""
        return self.__paramstyle

    def __setParamstyle(self, paramstyle):
        """Set value of paramstyle for cursor."""
        self.__paramstyle = paramstyle

    paramstyle = property(__getParamstyle, __setParamstyle)

    def __getDescription(self):
        return self._native_cs.description

    description = property(__getDescription)

    def __getRowCount(self):
        return self._native_cs.rowcount

    rowcount = property(__getRowCount)

    def __getArraySize(self):
        return self._native_cs.arraysize

    def __setArraySize(self, new_array_size):
        self._native_cs.arraysize = new_array_size

    arraysize = property(__getArraySize, __setArraySize)

    def setinputsizes(self, sizes):
        """Do Nothing"""
        pass

    def setoutputsize(self, size, column=None):
        """Do Nothing"""
        pass

    def execute(self, query, params=None):
        if params == None:
            return self._native_cs.execute(query)
        else:
            (newquery, newparams) = self.__formatQueryParams(query, params)
            return self._native_cs.execute(newquery, newparams)
        return

    def executemany(self, query, params=None):
        if params == None:
            return self._native_cs.executemany(query)
        else:
            newparams = []
            for pset in params:
                (newquery, newpset) = self.__formatQueryParams(query, pset)
                newparams.append(newpset)

            return self._native_cs.executemany(newquery, newparams)
        return

    def fetchone(self):
        """Like DBAPI2."""
        native_cs = self._native_cs
        result = native_cs.fetchone()
        if result != None and self.__doFormatResults():
            new_result = self.__formatResults([result])[0]
        elif result != None:
            new_result = result
        else:
            new_result = None
        return new_result

    def fetchmany(self, size=None):
        """Like DBAPI2."""
        native_cs = self._native_cs
        if size == None:
            size = self._native_cs.arraysize
        results = native_cs.fetchmany(size)
        if results != [] and self.__doFormatResults():
            new_results = self.__formatResults(results)
        elif results != []:
            new_results = results
        else:
            new_results = []
        return new_results

    def close(self):
        return self._native_cs.close()

    def fetchall(self):
        """Like DBAPI2."""
        native_cs = self._native_cs
        results = native_cs.fetchall()
        if results != None and self.__doFormatResults():
            new_results = self.__formatResults(results)
        elif results != None:
            new_results = results
        else:
            new_results = None
        return new_results

    def __doFormatResults(self):
        """Check to see if there is reason to format results."""
        native_dt = self._mwrapper.dtmod == 'native'
        use_db_row = self.use_db_row
        if native_dt and not use_db_row:
            return False
        else:
            return True

    def __formatResults(self, results):
        """Format result set before returning."""
        if type(results) == tuple:
            results = list(results)
        desc = self._native_cs.description
        typelist = [ descitem[1] for descitem in desc ]
        if self.use_db_row:
            metarow = db_row.IMetaRow(desc)
        if hasattr(self._mwrapper._config, 'convertdt'):
            cdtfunc = self._mwrapper._config.convertdt
        else:
            cdtfunc = None
        datepos = []
        if self._datetimeo:
            for i in range(len(typelist)):
                if typelist[i] == self._driver.DATETIME:
                    datepos.append(i)

        for i in xrange(len(results)):
            set = results[i]
            if len(datepos) > 0:
                newrow = list(set)
                for rownum in datepos:
                    dt_type = typelist[rownum]
                    inputdt = newrow[rownum]
                    dtpref = self._mwrapper.dtmod
                    if self._mwrapper.dtmod != 'native':
                        newrow[rownum] = dbtime.native2pref(inputdt, dtpref, dt_type, cdtfunc)

                set = tuple(newrow)
            if self.use_db_row:
                results[i] = metarow(set)
            else:
                results[i] = set

        return results

    def __formatQueryParams(self, query, params):
        params = dbtime.dtsubnative(self._mwrapper.dtmod, self._driver, params)
        pstyle1 = self.paramstyle
        pstyle2 = self._driver.paramstyle
        return paramstyles.convert(pstyle1, pstyle2, query, params)


def connect(*args, **kwargs):
    """Return Connection wrapper object."""
    return Connection(*args, **kwargs)


def wrapdriver(driver_name, driver_alias=None):
    """Wrap native driver."""
    if driver_alias == None:
        driver_alias = driver_name
    try:
        driver = __import__(driver_name)
    except ImportError:
        raise

    mwrapper = MWrapper(driver, driver_alias)
    return mwrapper