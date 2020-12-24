# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\bfile.py
# Compiled at: 2019-11-20 12:25:22
# Size of source mod 2**32: 31804 bytes
"""
bfile -- binary file handling
====================================

An object of this class supports one file, which can be opened for input or output.  Current implementation assumes file contains big-endian data.

Example use of :class:`bfile.bfile` opens a file, then reads a 2 byte unsigned field, then a 4 byte unsigned field::

    foo = bfile.bfile()
    foo.open(foofile, "rb")
    
    barnone     = foo.uget(2)
    barsome     = foo.uget(4)

    foo.close()
    
Example use of :class:`bfile.brecord` (note highest level is :attr:`foostruct` dictionary)::
    
    import bfile
    
    # need to create the lower level dictionaries first, else python will complain

    # make a convenience copy of the bfile.brecord sign indicators
    (U, TS, S, F) = (bfile.U, bfile.TS, bfile.S, bfile.F)

    # dictionary which describes file structure has scalars such as 'BARNONE', and subrecords such as 
    # 'satcontactrecs'.  Note use of tuples (e.g., "(0, 2, U)", with parens) for scalars, and lists 
    # (e.g., "[9,'NUM_SAT_CONTACTS', satcontactcomm, None]" with square brackets) for subrecords.  Use of list is 
    # required for subrecords because the data within is changed by bfile.brecord itself, and tuples are immutable
    
    # note range field is optional, and it must be a single entry 
    # to verify a min,max range, use the tuple value (min,max) -- **tuples (in parens) are assumed to be min,max!!**
    # to verify within a discrete set of values, use a list, e.g., [1,2,5] or range(6)
    
    foo                     = dict(#   ndx   len sign    range
        BARNONE             = (0,   1,  U,      (0,15)),
        SAT_PN              = (1,   1,  U,      (0,15)),
        ANT_REF_NUM         = (2,   1,  U,      (0,3)),
        T_START_TIME        = (3,   4,  TS),    # note no range specified here
        T_STOP_TIME         = (4,   4,  TS),
        CONTACT_ENRGY       = (5,   4,  U,      (0,480000)),
        NUM_SAT_PWR         = (6,   1,  U,      (1,20)),
                         #    ndx   count           structure       handler(added later)
        satpwrsegs          = [7,   'NUM_SAT_PWR',  satpwrsegcomm,  None],
        NUM_RHPOL_PWR       = (8,   1,  U),
        rhpolpwrsegrecs     = [9,   'NUM_RHPOL_PWR', polpwrsegcomm, None],
        NUM_LHPOL_PWR       = (10,  1,  U),
        lhpolpwrsegrecs     = [11,  'NUM_LHPOL_PWR', polpwrsegcomm, None],
        NUM_BEAMS_F         = (12,  1,  U),
        fwdbeamrecs         = [13,  'NUM_BEAMS_F',  fwdbeamreccomm, None],
        NUM_BEAMS_R         = (14,  1,  U),
        rvsbeamrecs         = [15,  'NUM_BEAMS_R',  rvsbeamreccomm, None],
        )

    raistruct = dict(      #  ndx  len sign     range
        GATEWAY_ID          = (0,   2,  U,      (1,100)),
        START_TIME          = (1,   4,  TS),
        STOP_TIME           = (2,   4,  TS),
        NUM_ALERTING        = (3,   1,  U,      [0,1,2,4]),
        ACCESS_CHAN         = (4,   2,  U),
        REV_ANCHOR_FREQ     = (5,   2,  U,      (4,496)),
        BACH_PWR_OFFSET     = (6,   2,  U,      range(100,900,25)),
        NUM_PAGING          = (7,   1,  U,      [2,4,8]),
        NUM_SAT_CONTACTS    = (8,   2,  U,      (1,512)),
                         #    ndx   count           structure       handler(added later)
        satcontactrecs      = [9,   'NUM_SAT_CONTACTS', foo, None],
        )
    
    # create the handler object
    raih = bfile.brecord(raistruct)

"""
import re, struct, sys

class invalidRangeCheck(Exception):
    pass


def rangecheck(start, fieldname, value, *range, **kwargs):
    """
    range check data
    
    :param start: number of bytes into the file at the start of the field
    :param fieldname: name of the field
    :param value: value of the field
    :param range: verify value is within this range
    
        * If two values supplied, range[0] is min, range[1] is max
        * If tuple supplied, (min,max) is assumed
        * If list supplied, valid values are in the list
        
    :param rangeerr=sys.stdout: file to send output to
    """
    maxwidth = 30
    rangeerr = kwargs.get('rangeerr', sys.stdout)
    origrange = range
    if len(range) == 1:
        if isinstance(range[0], tuple):
            range = range[0]
    else:
        if isinstance(range[0], list) or isinstance(range[0], set):
            if value not in range[0]:
                iset = range[0]
                pset = format(iset)[0:maxwidth]
                if iset != pset:
                    pset += '...'
                print(('{0:06x}:\tRange Error: {1}={2} ({3})'.format(start, fieldname, value, pset)), file=rangeerr)
        else:
            if isinstance(range[0], int) or isinstance(range[0], float):
                if value < range[0] or value > range[1]:
                    print(('{0:06x}:\tRange Error: {1}={2} ({3}..{4})'.format(start, fieldname, value, range[0], range[1])), file=rangeerr)
            else:
                raise invalidRangeCheck('start={0}, fieldname={1}, range={2}'.format(start, fieldname, origrange))


class Struct:

    def __init__(self, format):
        self.format = format

    def pack(self, *v):
        return (struct.pack)(self.format, *v)

    def unpack(self, string):
        return struct.unpack(self.format, string)


tf = '%Y-%m-%d-%H:%M:%S'

class unexpectedEOF(Exception):
    pass


class parameterError(Exception):
    pass


class bfile:
    __doc__ = "\n    Create an object of this class to work with an associated with a binary file\n    \n    :param byteorder: indicate byte order character, per struct fmt param '>' is big-endian (default), '<' is little-endian, see http://docs.python.org/release/2.6.6/library/struct.html#byte-order-size-and-alignment\n    "

    def __init__(self, byteorder='>'):
        self._bfile__currloc = 0
        allowedbyteorder = [
         '>', '<', '@', '=', '!']
        if byteorder not in allowedbyteorder:
            raise parameterError('byteorder must be one of {0}'.format(allowedbyteorder))
        self.sint8 = Struct(byteorder + 'b')
        self.uint8 = Struct(byteorder + 'B')
        self.sint16 = Struct(byteorder + 'h')
        self.uint16 = Struct(byteorder + 'H')
        self.sint32 = Struct(byteorder + 'l')
        self.uint32 = Struct(byteorder + 'L')
        self.sint64 = Struct(byteorder + 'q')
        self.uint64 = Struct(byteorder + 'Q')
        self.float32 = Struct(byteorder + 'f')
        self.float64 = Struct(byteorder + 'd')
        self.ustruct = {1:self.uint8, 
         2:self.uint16,  4:self.uint32,  8:self.uint64}
        self.sstruct = {1:self.sint8,  2:self.sint16,  4:self.sint32,  8:self.sint64}
        self.fstruct = {4:self.float32,  8:self.float64}

    def open(self, filename, mode):
        """
        open file object

        :param filename: name of file to open
        :param mode: mode to open file - must include 'b' to support binary read / write
        """
        self.file = open(filename, mode)
        self._bfile__currloc = 0

    def close(self):
        """
        close the file object
        """
        self.file.close()

    def uget(self, numbytes):
        """
        get unsigned bytes

        
        :param numbytes: number of bytes to read from the file
        :rtype: str with bytes from file
        """
        self._bfile__currloc += numbytes
        data = self.file.read(numbytes)
        if len(data) < numbytes:
            raise unexpectedEOF
        rtnval, = self.ustruct[numbytes].unpack(data)
        return rtnval

    def sget(self, numbytes):
        """
        get signed bytes

        
        :param numbytes: number of bytes to read from the file
        :rtype: str with bytes from file
        """
        self._bfile__currloc += numbytes
        data = self.file.read(numbytes)
        if len(data) < numbytes:
            raise unexpectedEOF
        rtnval, = self.sstruct[numbytes].unpack(data)
        return rtnval

    def fget(self, numbytes):
        """
        get floating point bytes

        
        :param numbytes: number of bytes to read from the file
        :rtype: str with bytes from file
        """
        self._bfile__currloc += numbytes
        data = self.file.read(numbytes)
        if len(data) < numbytes:
            raise unexpectedEOF
        rtnval, = self.fstruct[numbytes].unpack(data)
        return rtnval

    def uput(self, numbytes, buffer):
        """
        put unsigned bytes

        :param numbytes: number of bytes to write to the file
        :param buffer: str with bytes to be written to file
        """
        self._bfile__currloc += numbytes
        self.file.write(self.ustruct[numbytes].pack(buffer))

    def sput(self, numbytes, buffer):
        """
        put signed bytes

        :param numbytes: number of bytes to write to the file
        :param buffer: str with bytes to be written to file
        """
        self._bfile__currloc += numbytes
        self.file.write(self.sstruct[numbytes].pack(buffer))

    def fput(self, numbytes, buffer):
        """
        put floating point bytes

        :param numbytes: number of bytes to write to the file
        :param buffer: str with bytes to be written to file
        """
        self._bfile__currloc += numbytes
        self.file.write(self.fstruct[numbytes].pack(buffer))

    def get(self, numbytes):
        """
        get raw bytes

        
        :param numbytes: number of bytes to read from the file
        :rtype: str with bytes from file
        """
        self._bfile__currloc += numbytes
        rtnval = self.file.read(numbytes)
        return rtnval

    def put(self, buffer):
        """
        put raw bytes

        :param buffer: str with bytes to be written to file
        """
        numbytes = len(buffer)
        self._bfile__currloc += numbytes
        self.file.write(buffer)

    def seek(self, loc):
        """
        seek a new location
        
        :param loc: location to put the read or write pointer for the file
        :rtype: int with the previous location
        """
        prevloc = self.file.tell()
        self.file.seek(loc)
        self._bfile__currloc = loc
        return prevloc

    def currloc(self):
        """
        return the current location in the file
        
        :rtype: int with current location
        """
        return self._bfile__currloc


NDXNDX, LENNDX, SIGNNDX, RNGNDX = list(range(4))
NDXNDX, CNTFNDX, STRUCNDX, HNDLRNDX = list(range(4))
U, TS, S, F = list(range(4))

class invalidSubrecCount(Exception):
    pass


class invalidStruct(Exception):
    pass


class invalidInputKeyNotFound(Exception):
    pass


class invalidCount(Exception):
    pass


def exprfilter(exprstr, varprefix, varsuffix):
    """
    filter an expression string with certain operators, to an updated expression
    string, that has varprefix before each variables (i.e., any part of the string
    which isn't an operator) and has varsuffix after each variable
    
    valid operators are ( ) * +
    
    :param exprstr: expression string, e.g., '((XXX+YY)*Z)'
    :param varprefix: prefix to put on variables within exprstr, e.g., 'x['
    :param varsuffix: suffix to put on variables within exprstr, e.g., ']'
    :rtype: string with variables updated based on varprefix, varsuffix, e.g., '((x[XXX]+x[YY])*x[Z])'.  This is suitable for call to :func:`eval()`
    """
    p = re.compile('[()*+]')
    operators = p.findall(exprstr)
    parencheck = 0
    for o in operators:
        if o == '(':
            parencheck += 1
        else:
            if o == ')':
                parencheck -= 1

    if parencheck != 0:
        raise invalidCount('unmatched parenthesis in {0}'.format(exprstr))
    iter = p.finditer(exprstr)
    retval = ''
    lastend = 0
    for m in iter:
        if lastend == m.start():
            retval += m.group()
        else:
            retval += varprefix + exprstr[lastend:m.start()] + varsuffix
            retval += m.group()
        lastend = m.end()

    if lastend != len(exprstr):
        retval += varprefix + exprstr[lastend:len(exprstr)] + varsuffix
    return retval


class brecord:
    __doc__ = '\n    Generic binary record\n    \n    :param recstruct: dictionary containing binary record structure\n    \n        where\n            recstruct = \n                {\'fieldname\':(index,length,sign[,range]), ...}            "scalar field"\n                \n                or  {\'recordname\':[index,countfield,structure,None], ...}  "record field" (4th entry of list must be "None")\n                \n                    index = incremented from 0 for each field -- this needs to be maintained because python 2.6 does not support ordered dictionaries\n                    \n                    length = length in bytes of field\n                    \n                    sign = bfile.U - unsigned, bfile.TS - timestamp, bfile.S - signed, bfile.F - float\n                    \n                    range = optional tuple with two values for (min,max), or list with possible values for [val1,val2, ..., valn]\n                    \n                    countfield = \'fieldname\' of field which has the count for the number of records in this list\n                    \n                    structure = recstruct pointing to sub-record (recursive)\n                    \n                    None = must be \'None\' (see example) - placeholder for internal use of :class:`bfile.brecord`\n\n    :param dorangecheck: if True, upon :meth:`get`, perform range check with errors to rangeerr, default False\n    :param rangeerr: file handle, default sys.stdout\n    '

    def __init__(self, recstruct, dorangecheck=False, rangeerr=sys.stdout, rangeignore=[]):
        self.recstruct = recstruct
        fieldlist = []
        r = self.recstruct
        for field in list(r.keys()):
            fieldlist += [(r[field][NDXNDX], (field, r[field]))]

        fieldlist.sort()
        self.ordered = [fieldent[1] for fieldent in fieldlist]
        self._dorangecheck = dorangecheck
        self._rangeerr = rangeerr
        self._rangeignore = rangeignore

    def get(self, BF, kwargs):
        """
        Retrieves a record from a binary file.
        Perform range check on fields if :class:`brecord` instantiated with dorangecheck=True
        
        :param BF: bfile object opened in read mode
        :param kwargs: {'errdisplayfields':list} of fields which should be displayed upon unexpectedEOF exception
        :rtype: dictionary with the data from the record, with appropriate field keys.  Subrecords are ordered lists with these dictionaries.
        """

        def _dumperrfields(d, fields):
            dumpstr = ''
            for f in list(d.keys()):
                if f in fields:
                    dumpstr += '{0}={1}, '.format(f, d[f])

            if len(dumpstr) > 0:
                print('Unexpected end of file within record having {0}'.format(dumpstr[0:-2]))

        retval = {}
        errdisplayfields = kwargs.get('errdisplayfields', [])
        for f in self.ordered:
            field = f[0]
            length = f[1][LENNDX]
            start = BF.currloc()
            if isinstance(length, int):
                try:
                    if f[1][SIGNNDX] == U or f[1][SIGNNDX] == TS:
                        retval[field] = BF.uget(length)
                    else:
                        if f[1][SIGNNDX] == S:
                            retval[field] = BF.sget(length)
                        else:
                            if f[1][SIGNNDX] == F:
                                retval[field] = BF.fget(length)
                            else:
                                raise invalidStruct(f)
                    dorangecheck = self._dorangecheck and len(f[1]) >= RNGNDX + 1 and field not in self._rangeignore
                    if dorangecheck:
                        rangecheck(start, field, (retval[field]), (f[1][RNGNDX]), rangeerr=(self._rangeerr))
                except unexpectedEOF:
                    print('Unexpected end of file in {0}'.format(field))
                    _dumperrfields(retval, errdisplayfields)
                    raise

            else:
                retval[field] = []
                countfield = f[1][CNTFNDX]
                count = eval(exprfilter(countfield, 'retval["', '"]'))
                if f[1][HNDLRNDX] == None:
                    recstruct = f[1][STRUCNDX]
                    handler = brecord(recstruct, self._dorangecheck, self._rangeerr, self._rangeignore)
                    f[1][HNDLRNDX] = handler
                handler = f[1][HNDLRNDX]
                for subrec in range(count):
                    try:
                        retval[field] += [handler.get(BF, kwargs)]
                    except unexpectedEOF:
                        print('Unexpected end of file in {0}'.format(field))
                        _dumperrfields(retval, errdisplayfields)
                        raise

        return retval

    def put(self, BF, record):
        """
        Inserts a record into a binary file
        
        :param BF: bfile object opened in write mode
        :param record: dictionary with the data from the record, with appropriate field keys.  Subrecords are ordered lists with these dictionaries.
        """
        for f in self.ordered:
            field = f[0]
            if field not in list(record.keys()):
                raise invalidInputKeyNotFound(field)
            length = f[1][LENNDX]
            if isinstance(length, int):
                if f[1][SIGNNDX] == U or f[1][SIGNNDX] == TS:
                    BF.uput(length, record[field])
                else:
                    if f[1][SIGNNDX] == S:
                        BF.sput(length, record[field])
                    else:
                        if f[1][SIGNNDX] == F:
                            BF.fput(length, record[field])
                        else:
                            raise invalidStruct(f)
            else:
                countfield = f[1][CNTFNDX]
                count = eval(exprfilter(countfield, 'record["', '"]'))
                if f[1][HNDLRNDX] == None:
                    recstruct = f[1][STRUCNDX]
                    handler = brecord(recstruct)
                    f[1][HNDLRNDX] = handler
                handler = f[1][HNDLRNDX]
                if len(record[field]) != count:
                    raise invalidSubrecCount('{0}, count={1}, #subrecs={2}'.format(field, count, len(record[field])))
                for subrec in record[field]:
                    handler.put(BF, subrec)

    def gettsfields(self):
        """
        Get timestamp fields.  Useful in case timestamps need to be shifted in time.
        
        :rtype: parallel dictionary to recstruct (see :class:`bfile.brecord`), which has True value for fields that are of type TS (timestamp)
        """
        retval = {}
        for f in self.ordered:
            field = f[0]
            length = f[1][LENNDX]
            if isinstance(length, int):
                if f[1][SIGNNDX] == TS:
                    retval[field] = True
                else:
                    retval[field] = False
            else:
                if f[1][HNDLRNDX] == None:
                    recstruct = f[1][STRUCNDX]
                    handler = brecord(recstruct)
                    f[1][HNDLRNDX] = handler
                handler = f[1][HNDLRNDX]
                retval[field] = handler.gettsfields()

        return retval

    def getcountfields(self):
        """
        Get count fields.  Useful to automatically process a brecord file
        
        :rtype: parallel dictionary to recstruct (see :class:`bfile.brecord`), which has False value for scalars and {'count':countfield,'rec':subrecord} dictionary for subrecords
        """
        retval = {}
        for f in self.ordered:
            field = f[0]
            length = f[1][LENNDX]
            if isinstance(length, int):
                retval[field] = False
            else:
                if f[1][HNDLRNDX] == None:
                    recstruct = f[1][STRUCNDX]
                    handler = brecord(recstruct)
                    f[1][HNDLRNDX] = handler
                handler = f[1][HNDLRNDX]
                retval[field] = {'count':f[1][CNTFNDX], 
                 'rec':handler.getcountfields()}

        return retval

    def getfieldorder(self):
        """
        Get fields in order.  Useful to automatically process a brecord file.
        
        :rtype: list which is parallel to recstruct (see :class:`bfile.brecord`), ordered list of fieldnames, or (fieldname, [subfields...]) recursively
        """
        retval = []
        for f in self.ordered:
            field = f[0]
            length = f[1][LENNDX]
            if isinstance(length, int):
                retval += [field]
            else:
                if f[1][HNDLRNDX] == None:
                    recstruct = f[1][STRUCNDX]
                    handler = brecord(recstruct)
                    f[1][HNDLRNDX] = handler
                handler = f[1][HNDLRNDX]
                retval += [(field, handler.getfieldorder())]

        return retval