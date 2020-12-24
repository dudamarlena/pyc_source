# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\statlib\io.py
# Compiled at: 2016-03-08 18:42:10
"""
Defines a number of functions for pseudo-command-line OS functionality.

    cd(directory)
    pwd                 <-- can be used WITHOUT parens
    ls(d='.')
    rename(from,to)
    get(namepatterns,verbose=1)
    getstrings(namepatterns,verbose=1)
    put(outlist,filename,writetype='w')
    aget(namepatterns,verbose=1)
    aput(outarray,filename,writetype='w')
    bget(filename,numslices=1,xsize=64,ysize=64)
    braw(filename,btype)
    bput(outarray,filename,writeheader=0,packstring='h',writetype='wb')
    mrget(filename)
    find_dirs(sourcedir)
"""
try:
    import mmapfile
except:
    pass

import glob, re, string, os, struct, copy, time, tempfile
from types import *
from b3.tools.debug.statlib import pstat
import numpy
N = numpy
__version__ = 0.5

def wrap(f):
    """
Wraps a function so that if it's entered *by itself*
in the interpreter without ()'s, it gets called anyway
"""

    class W:

        def __init__(self, f):
            self.f = f

        def __repr__(self):
            x = apply(self.f)
            if x:
                return repr(x)
            else:
                return ''

    return W(f)


def cd(directory):
    """
Changes the working python directory for the interpreter.

Usage:   cd(directory)      where 'directory' is a string
"""
    os.chdir(directory)


def pwd():
    """
Changes the working python directory for the interpreter.

Usage:   pwd       (no parens needed)
"""
    return os.getcwd()


pwd = wrap(pwd)

def ls(d='.'):
    """
Produces a directory listing.  Default is the current directory.

Usage:   ls(d='.')
"""
    os.system('ls ' + d)
    return


def rename(source, dest):
    """
Renames files specified by UNIX inpattern to those specified by UNIX
outpattern.  Can only handle a single '*' in the two patterns!!!

Usage:   rename (source, dest)     e.g., rename('*.txt', '*.c')
"""
    infiles = glob.glob(source)
    outfiles = []
    incutindex = string.index(source, '*')
    outcutindex = string.index(source, '*')
    findpattern1 = source[0:incutindex]
    findpattern2 = source[incutindex + 1:]
    replpattern1 = dest[0:incutindex]
    replpattern2 = dest[incutindex + 1:]
    for fname in infiles:
        if incutindex > 0:
            newname = re.sub(findpattern1, replpattern1, fname, 1)
        if outcutindex < len(dest) - 1:
            if incutindex > 0:
                lastone = string.rfind(newname, replpattern2)
                newname = newname[0:lastone] + re.sub(findpattern2, replpattern2, fname[lastone:], 1)
            else:
                lastone = string.rfind(fname, findpattern2)
                if lastone != -1:
                    newname = fname[0:lastone]
                    newname = newname + re.sub(findpattern2, replpattern2, fname[lastone:], 1)
        os.rename(fname, newname)


def get(namepatterns, verbose=1):
    """
Loads a list of lists from text files (specified by a UNIX-style
wildcard filename pattern) and converts all numeric values to floats.
Uses the glob module for filename pattern conversion.  Loaded filename
is printed if verbose=1.

Usage:   get (namepatterns,verbose=1)
Returns: a 1D or 2D list of lists from whitespace delimited text files
         specified by namepatterns; numbers that can be converted to floats
         are so converted
"""
    fnames = []
    if type(namepatterns) in [ListType, TupleType]:
        for item in namepatterns:
            fnames = fnames + glob.glob(item)

    else:
        fnames = glob.glob(namepatterns)
    if len(fnames) == 0:
        if verbose:
            print 'NO FILENAMES MATCH (' + namepatterns + ') !!'
        return None
    if verbose:
        print fnames
    elements = []
    for i in range(len(fnames)):
        file = open(fnames[i])
        newelements = map(string.split, file.readlines())
        for i in range(len(newelements)):
            for j in range(len(newelements[i])):
                try:
                    newelements[i][j] = string.atoi(newelements[i][j])
                except ValueError:
                    try:
                        newelements[i][j] = string.atof(newelements[i][j])
                    except:
                        pass

        elements = elements + newelements

    if len(elements) == 1:
        elements = elements[0]
    return elements


def getstrings(namepattern, verbose=1):
    """
Loads a (set of) text file(s), with all elements left as string type.
Uses UNIX-style wildcards (i.e., function uses glob).  Loaded filename
is printed if verbose=1.

Usage:   getstrings (namepattern, verbose=1)
Returns: a list of strings, one per line in each text file specified by
         namepattern
"""
    fnames = glob.glob(namepattern)
    if len(fnames) == 0:
        if verbose:
            print 'NO FILENAMES MATCH (' + namepattern + ') !!'
        return None
    if verbose:
        print fnames
    elements = []
    for filename in fnames:
        file = open(filename)
        newelements = map(string.split, file.readlines())
        elements = elements + newelements

    return elements


def put(outlist, fname, writetype='w', oneperline=0, delimit=' '):
    """
Writes a passed mixed-type list (str and/or numbers) to an output
file, and then closes the file.  Default is overwrite the destination
file.

Usage:   put (outlist,fname,writetype='w',oneperline=0,delimit=' ')
Returns: None
"""
    if type(outlist) in [N.ArrayType]:
        aput(outlist, fname, writetype)
        return
    else:
        if type(outlist[0]) not in [ListType, TupleType]:
            outfile = open(fname, writetype)
            if not oneperline:
                outlist = pstat.list2string(outlist, delimit)
                outfile.write(outlist)
                outfile.write('\n')
            else:
                for item in outlist:
                    outfile.write(str(item) + '\n')

            outfile.close()
        else:
            outfile = open(fname, writetype)
            for row in outlist:
                outfile.write(pstat.list2string(row, delimit))
                outfile.write('\n')

            outfile.close()
        return


def isstring(x):
    if type(x) == StringType:
        return 1
    else:
        return 0


def aget(namepattern, verbose=1):
    """
Loads an array from 2D text files (specified by a UNIX-style wildcard
filename pattern).  ONLY 'GET' FILES WITH EQUAL NUMBERS OF COLUMNS
ON EVERY ROW (otherwise returned array will be zero-dimensional).

Usage:   aget (namepattern)
Returns: an array of integers, floats or objects (type='O'), depending on the
         contents of the files specified by namepattern
"""
    fnames = glob.glob(namepattern)
    if len(fnames) == 0:
        if verbose:
            print 'NO FILENAMES MATCH (' + namepattern + ') !!'
            return None
    if verbose:
        print fnames
    elements = []
    for filename in fnames:
        file = open(filename)
        newelements = file.readlines()
        del_list = []
        for row in range(len(newelements)):
            if newelements[row][0] == '%' or newelements[row][0] == '#' or len(newelements[row]) == 1:
                del_list.append(row)

        del_list.reverse()
        for i in del_list:
            newelements.pop(i)

        newelements = map(string.split, newelements)
        for i in range(len(newelements)):
            for j in range(len(newelements[i])):
                try:
                    newelements[i][j] = string.atof(newelements[i][j])
                except:
                    pass

        elements = elements + newelements

    for row in range(len(elements)):
        if N.add.reduce(N.array(map(isstring, elements[row]))) == len(elements[row]):
            print 'A row of strings was found.  Returning a LIST.'
            return elements

    try:
        elements = N.array(elements)
    except TypeError:
        elements = N.array(elements, 'O')

    return elements


def aput(outarray, fname, writetype='w', delimit=' '):
    """
Sends passed 1D or 2D array to an output file and closes the file.

Usage:   aput (outarray,fname,writetype='w',delimit=' ')
Returns: None
"""
    outfile = open(fname, writetype)
    if len(outarray.shape) == 1:
        outarray = outarray[N.NewAxis, :]
    if len(outarray.shape) > 2:
        raise TypeError, 'put() and aput() require 1D or 2D arrays.  Otherwise use some kind of pickling.'
    else:
        for row in outarray:
            outfile.write(string.join(map(str, row), delimit))
            outfile.write('\n')

        outfile.close()
    return


def bget(imfile, shp=None, unpackstr=N.int16, bytesperpixel=2.0, sliceinit=0):
    """
Reads in a binary file, typically with a .bshort or .bfloat extension.
If so, the last 3 parameters are set appropriately.  If not, the last 3
parameters default to reading .bshort files (2-byte integers in big-endian
binary format).

Usage:   bget(imfile,shp=None,unpackstr=N.int16,bytesperpixel=2.0,sliceinit=0)
"""
    if imfile[:3] == 'COR':
        return CORget(imfile)
    else:
        if imfile[-2:] == 'MR':
            return mrget(imfile, unpackstr)
        if imfile[-4:] == 'BRIK':
            return brikget(imfile, unpackstr, shp)
        if imfile[-3:] in ('mnc', 'MNC'):
            return mincget(imfile, unpackstr, shp)
        if imfile[-3:] == 'img':
            return mghbget(imfile, unpackstr, shp)
        if imfile[-6:] == 'bshort' or imfile[-6:] == 'bfloat':
            if shp == None:
                return mghbget(imfile, unpackstr=unpackstr, bytesperpixel=bytesperpixel, sliceinit=sliceinit)
            else:
                return mghbget(imfile, shp[0], shp[1], shp[2], unpackstr, bytesperpixel, sliceinit)

        return


def CORget(infile):
    """
Reads a binary COR-nnn file (flattening file).

Usage:   CORget(imfile)
Returns: 2D array of 16-bit ints
"""
    d = braw(infile, N.Int8)
    d.shape = (256, 256)
    d = N.where(N.greater_equal(d, 0), d, 256 + d)
    return d


def mincget(imfile, unpackstr=N.int16, shp=None):
    """
Loads in a .MNC file.

Usage:  mincget(imfile,unpackstr=N.int16,shp=None)  default shp = -1,20,64,64
"""
    if shp == None:
        shp = (-1, 20, 64, 64)
    os.system('mincextract -short -range 0 4095 -image_range 0 4095 ' + imfile + ' > minctemp.bshort')
    try:
        d = braw('minctemp.bshort', unpackstr)
    except:
        print "Couldn't find file:  " + imfile
        raise IOError, "Couldn't find file in mincget()"

    print shp, d.shape
    d.shape = shp
    os.system('rm minctemp.bshort')
    return d


def brikget(imfile, unpackstr=N.int16, shp=None):
    """
Gets an AFNI BRIK file.

Usage:  brikget(imfile,unpackstr=N.int16,shp=None)  default shp: (-1,48,61,51)
"""
    if shp == None:
        shp = (-1, 48, 61, 51)
    try:
        file = open(imfile, 'rb')
    except:
        print "Couldn't find file:  " + imfile
        raise IOError, "Couldn't find file in brikget()"

    try:
        header = imfile[0:-4] + 'HEAD'
        lines = open(header).readlines()
        for i in range(len(lines)):
            if string.find(lines[i], 'DATASET_DIMENSIONS') != -1:
                dims = string.split(lines[(i + 2)][0:string.find(lines[(i + 2)], ' 0')])
                dims = map(string.atoi, dims)
            if string.find(lines[i], 'BRICK_FLOAT_FACS') != -1:
                count = string.atoi(string.split(lines[(i + 1)])[2])
                mults = []
                for j in range(int(N.ceil(count / 5.0))):
                    mults += map(string.atof, string.split(lines[(i + 2 + j)]))

                mults = N.array(mults)

        dims.reverse()
        shp = [-1] + dims
    except IOError:
        print 'No header file.  Continuing ...'

    lines = None
    print shp
    print 'Using unpackstr:', unpackstr
    file = open(imfile, 'rb')
    bdata = file.read()
    bdata = N.fromstring(bdata, unpackstr)
    littleEndian = struct.pack('i', 1) == struct.pack('<i', 1)
    if littleEndian and os.uname()[0] != 'Linux' or max(bdata) > 1e+30:
        bdata = bdata.byteswapped()
    try:
        bdata.shape = shp
    except:
        print 'Incorrect shape ...', shp, len(bdata)
        raise ValueError, 'Incorrect shape for file size'

    if len(bdata) == 1:
        bdata = bdata[0]
    if N.sum(mults) == 0:
        return bdata
    else:
        try:
            multshape = [
             1] * len(bdata.shape)
            for i in range(len(bdata.shape)):
                if len(mults) == bdata.shape[i]:
                    multshape[i] = len(mults)
                    break

            mults.shape = multshape
            return bdata * mults
        except:
            return bdata

        return


def mghbget(imfile, numslices=-1, xsize=64, ysize=64, unpackstr=N.int16, bytesperpixel=2.0, sliceinit=0):
    """
Reads in a binary file, typically with a .bshort or .bfloat extension.
If so, the last 3 parameters are set appropriately.  If not, the last 3
parameters default to reading .bshort files (2-byte integers in big-endian
binary format).

Usage:   mghbget(imfile, numslices=-1, xsize=64, ysize=64,
                unpackstr=N.int16, bytesperpixel=2.0, sliceinit=0)
"""
    try:
        file = open(imfile, 'rb')
    except:
        print "Couldn't find file:  " + imfile
        raise IOError, "Couldn't find file in bget()"

    try:
        header = imfile[0:-6] + 'hdr'
        vals = get(header, 0)
        if type(vals[0]) == ListType:
            xsize = int(vals[0][0])
            ysize = int(vals[0][1])
            numslices = int(vals[0][2])
        else:
            xsize = int(vals[0])
            ysize = int(vals[1])
            numslices = int(vals[2])
    except:
        print 'No header file.  Continuing ...'

    suffix = imfile[-6:]
    if suffix == 'bshort':
        pass
    elif suffix[-3:] == 'img':
        pass
    elif suffix == 'bfloat':
        unpackstr = N.Float32
        bytesperpixel = 4.0
        sliceinit = 0.0
    else:
        print 'Not a bshort, bfloat or img file.'
        print 'Using unpackstr:', unpackstr, ', bytesperpixel=', bytesperpixel
    imsize = xsize * ysize
    file = open(imfile, 'rb')
    bdata = file.read()
    numpixels = len(bdata) / bytesperpixel
    if numpixels % 1 != 0:
        raise ValueError, 'Incorrect file size in fmri.bget()'
    else:
        bdata = N.fromstring(bdata, unpackstr)
        littleEndian = struct.pack('i', 1) == struct.pack('<i', 1)
        if littleEndian and os.uname()[0] != 'Linux' or max(bdata) > 1e+30:
            bdata = bdata.byteswapped()
    if suffix[-3:] == 'img':
        if numslices == -1:
            numslices = len(bdata) / 8200
            xsize = 64
            ysize = 128
        slices = N.zeros((numslices, xsize, ysize), N.Int)
        for i in range(numslices):
            istart = i * 8 + i * xsize * ysize
            iend = i * 8 + (i + 1) * xsize * ysize
            print i, istart, iend
            slices[i] = N.reshape(N.array(bdata[istart:iend]), (xsize, ysize))

    elif numslices == 1:
        slices = N.reshape(N.array(bdata), [xsize, ysize])
    else:
        slices = N.reshape(N.array(bdata), [numslices, xsize, ysize])
    if len(slices) == 1:
        slices = slices[0]
    return slices


def braw(fname, btype, shp=None):
    """
Opens a binary file, unpacks it, and returns a flat array of the
type specified.  Use Numeric types ... N.Float32, N.Int64, etc.

Usage:   braw(fname,btype,shp=None)
Returns: flat array of floats, or ints (if btype=N.int16)
"""
    file = open(fname, 'rb')
    bdata = file.read()
    bdata = N.fromstring(bdata, btype)
    littleEndian = struct.pack('i', 1) == struct.pack('<i', 1)
    if littleEndian and os.uname()[0] != 'Linux' or max(bdata) > 1e+30:
        bdata = bdata.byteswapped()
    if shp:
        try:
            bdata.shape = shp
            return bdata
        except:
            pass

    return N.array(bdata)


def glget(fname, btype):
    """
Load in a file containing pixels from glReadPixels dump.

Usage:   glget(fname,btype)
Returns: array of 'btype elements with shape 'shape', suitable for im.ashow()
"""
    d = braw(fname, btype)
    d = d[8:]
    f = open(fname, 'rb')
    shp = f.read(8)
    f.close()
    shp = N.fromstring(shp, N.Int)
    shp[0], shp[1] = shp[1], shp[0]
    try:
        carray = N.reshape(d, shp)
        return
    except:
        pass

    try:
        r = d[0::3] + 0
        g = d[1::3] + 0
        b = d[2::3] + 0
        r.shape = shp
        g.shape = shp
        b.shape = shp
        carray = N.array([r, g, b])
    except:
        outstr = 'glget: shape not correct for data of length ' + str(len(d))
        raise ValueError, outstr

    return carray


def mget(fname, btype):
    """
Load in a file that was saved from matlab

Usage:   mget(fname,btype)
"""
    d = braw(fname, btype)
    try:
        header = fname[0:-6] + 'hdr'
        vals = get(header, 0)
        if type(vals[0]) == ListType:
            xsize = int(vals[0][0])
            ysize = int(vals[0][1])
            numslices = int(vals[0][2])
        else:
            xsize = int(vals[0])
            ysize = int(vals[1])
            numslices = int(vals[2])
        print xsize, ysize, numslices, d.shape
    except:
        print 'No header file.  Continuing ...'

    if numslices == 1:
        d.shape = [
         ysize, xsize]
        return N.transpose(d) * 1
    else:
        d.shape = [
         numslices, ysize, xsize]
        return N.transpose(d) * 1


def mput(outarray, fname, writeheader=0, btype=N.int16):
    """
Save a file for use in matlab.
"""
    outarray = N.transpose(outarray)
    outdata = N.ravel(outarray).astype(btype)
    outdata = outdata.tostring()
    outfile = open(fname, 'wb')
    outfile.write(outdata)
    outfile.close()
    if writeheader == 1:
        try:
            suffixindex = string.rfind(fname, '.')
            hdrname = fname[0:suffixindex]
        except ValueError:
            hdrname = fname

        if len(outarray.shape) == 2:
            hdr = [
             outarray.shape[1], outarray.shape[0], 1, 0]
        else:
            hdr = [
             outarray.shape[2], outarray.shape[1], outarray.shape[0], 0, '\n']
        print hdrname + '.hdr'
        outfile = open(hdrname + '.hdr', 'w')
        outfile.write(pstat.list2string(hdr))
        outfile.close()
    return


def bput(outarray, fname, writeheader=0, packtype=N.int16, writetype='wb'):
    """
Writes the passed array to a binary output file, and then closes
the file.  Default is overwrite the destination file.

Usage:   bput (outarray,filename,writeheader=0,packtype=N.int16,writetype='wb')
"""
    suffix = fname[-6:]
    if suffix == 'bshort':
        packtype = N.int16
    elif suffix == 'bfloat':
        packtype = N.Float32
    else:
        print 'Not a bshort or bfloat file.  Using packtype=', packtype
    outdata = N.ravel(outarray).astype(packtype)
    littleEndian = struct.pack('i', 1) == struct.pack('<i', 1)
    if littleEndian and os.uname()[0] != 'Linux':
        outdata = outdata.byteswapped()
    outdata = outdata.tostring()
    outfile = open(fname, writetype)
    outfile.write(outdata)
    outfile.close()
    if writeheader == 1:
        try:
            suffixindex = string.rfind(fname, '.')
            hdrname = fname[0:suffixindex]
        except ValueError:
            hdrname = fname

        if len(outarray.shape) == 2:
            hdr = [
             outarray.shape[0], outarray.shape[1], 1, 0]
        else:
            hdr = [
             outarray.shape[1], outarray.shape[2], outarray.shape[0], 0, '\n']
        print hdrname + '.hdr'
        outfile = open(hdrname + '.hdr', 'w')
        outfile.write(pstat.list2string(hdr))
        outfile.close()
    return


def mrget(fname, datatype=N.int16):
    """
Opens a binary .MR file and clips off the tail data portion of it, returning
the result as an array.

Usage:   mrget(fname,datatype=N.int16)
"""
    d = braw(fname, datatype)
    if len(d) > 262144:
        return N.reshape(d[-262144:], (512, 512))
    else:
        if len(d) > 65536:
            return N.reshape(d[-65536:], (256, 256))
        if len(d) > 16384:
            return N.reshape(d[-16384:], (128, 128))
        if len(d) > 4096:
            return N.reshape(d[-4096:], (64, 64))
        return N.reshape(d[-1024:], (32, 32))


def quickload(fname, linestocut=4):
    """
Quickly loads in a long text file, chopping off first n 'linestocut'.

Usage:   quickload(fname,linestocut=4)
Returns: array filled with data in fname
"""
    f = open(fname, 'r')
    d = f.readlines()
    f.close()
    print fname, 'read in.'
    d = d[linestocut:]
    d = map(string.split, d)
    print 'Done with string.split on lines.'
    for i in range(len(d)):
        d[i] = map(string.atoi, d[i])

    print 'Conversion to ints done.'
    return N.array(d)


def writedelimited(listoflists, delimiter, file, writetype='w'):
    """
Writes a list of lists in columns, separated by character(s) delimiter
to specified file.  File-overwrite is the default.

Usage:   writedelimited (listoflists,delimiter,filename,writetype='w')
Returns: None
"""
    if type(listoflists[0]) not in [ListType, TupleType]:
        listoflists = [
         listoflists]
    outfile = open(file, writetype)
    rowstokill = []
    list2print = copy.deepcopy(listoflists)
    for i in range(len(listoflists)):
        if listoflists[i] == ['\n'] or listoflists[i] == '\n' or listoflists[i] == 'dashes':
            rowstokill = rowstokill + [i]

    rowstokill.reverse()
    for row in rowstokill:
        del list2print[row]

    maxsize = [
     0] * len(list2print[0])
    for row in listoflists:
        if row == ['\n'] or row == '\n':
            outfile.write('\n')
        elif row == ['dashes'] or row == 'dashes':
            dashes = [
             0] * len(maxsize)
            for j in range(len(maxsize)):
                dashes[j] = '------'

            outfile.write(pstat.linedelimited(dashes, delimiter))
        else:
            outfile.write(pstat.linedelimited(row, delimiter))
        outfile.write('\n')

    outfile.close()
    return


def writecc(listoflists, file, writetype='w', extra=2):
    """
Writes a list of lists to a file in columns, customized by the max
size of items within the columns (max size of items in col, +2 characters)
to specified file.  File-overwrite is the default.

Usage:   writecc (listoflists,file,writetype='w',extra=2)
Returns: None
"""
    if type(listoflists[0]) not in [ListType, TupleType]:
        listoflists = [
         listoflists]
    outfile = open(file, writetype)
    rowstokill = []
    list2print = copy.deepcopy(listoflists)
    for i in range(len(listoflists)):
        if listoflists[i] == ['\n'] or listoflists[i] == '\n' or listoflists[i] == 'dashes':
            rowstokill = rowstokill + [i]

    rowstokill.reverse()
    for row in rowstokill:
        del list2print[row]

    maxsize = [
     0] * len(list2print[0])
    for col in range(len(list2print[0])):
        items = pstat.colex(list2print, col)
        items = map(pstat.makestr, items)
        maxsize[col] = max(map(len, items)) + extra

    for row in listoflists:
        if row == ['\n'] or row == '\n':
            outfile.write('\n')
        elif row == ['dashes'] or row == 'dashes':
            dashes = [
             0] * len(maxsize)
            for j in range(len(maxsize)):
                dashes[j] = '-' * (maxsize[j] - 2)

            outfile.write(pstat.lineincustcols(dashes, maxsize))
        else:
            outfile.write(pstat.lineincustcols(row, maxsize))
        outfile.write('\n')

    outfile.close()
    return


def writefc(listoflists, colsize, file, writetype='w'):
    """
Writes a list of lists to a file in columns of fixed size.  File-overwrite
is the default.

Usage:   writefc (listoflists,colsize,file,writetype='w')
Returns: None
"""
    if type(listoflists) == N.ArrayType:
        listoflists = listoflists.tolist()
    if type(listoflists[0]) not in [ListType, TupleType]:
        listoflists = [
         listoflists]
    outfile = open(file, writetype)
    rowstokill = []
    list2print = copy.deepcopy(listoflists)
    for i in range(len(listoflists)):
        if listoflists[i] == ['\n'] or listoflists[i] == '\n' or listoflists[i] == 'dashes':
            rowstokill = rowstokill + [i]

    rowstokill.reverse()
    for row in rowstokill:
        del list2print[row]

    n = [
     0] * len(list2print[0])
    for row in listoflists:
        if row == ['\n'] or row == '\n':
            outfile.write('\n')
        elif row == ['dashes'] or row == 'dashes':
            dashes = [
             0] * colsize
            for j in range(len(n)):
                dashes[j] = '-' * colsize

            outfile.write(pstat.lineincols(dashes, colsize))
        else:
            outfile.write(pstat.lineincols(row, colsize))
        outfile.write('\n')

    outfile.close()
    return


def load(fname, lines_to_ignore=4, type='i'):
    """
Load in huge, flat, 2D text files.  Can handle differing line-lengths AND
can strip #/% on UNIX (or with a better NT grep).  Requires wc, grep, and
mmapfile.lib/.pyd. Type can be 'i', 'f' or 'd', for ints, floats or doubles,
respectively.  Lines_to_ignore determines how many lines at the start of the
file to ignore (required for non-working grep).

Usage:   load(fname,lines_to_ignore=4,type='i')
Returns: numpy array of specified type
"""
    start = time.time()
    if type == 'i':
        intype = int
    else:
        if type in ('f', 'd'):
            intype = float
        else:
            raise ValueError, "type can be 'i', 'f' or 'd' in load()"
        tmpname = tempfile.mktemp()
        if sys.platform == 'win32':
            cmd = "grep.exe -v '%' " + fname + ' > ' + tmpname
            print cmd
            os.system(cmd)
        else:
            cmd = 'cat ' + fname + " | grep -v '%' |grep -v '#' > " + tmpname
            print cmd
            os.system(cmd)
        wc = string.split(os.popen('wc ' + tmpname).read())
        numlines = int(wc[0]) - lines_to_ignore
        tfp = open(tmpname)
        if lines_to_ignore != 0:
            for i in range(lines_to_ignore):
                junk = tfp.readline()

        numcols = len(string.split(tfp.readline()))
        tfp.close()
        a = N.zeros(numlines * numcols, type)
        block = 65536
        data = mmapfile.mmapfile(tmpname, '', 0)
        if lines_to_ignore != 0 and sys.platform == 'win32':
            for i in range(lines_to_ignore):
                junk = data.readline()

        i = 0
        d = ' '
        carryover = ''
        while len(d) != 0:
            d = carryover + data.read(block)
            cutindex = string.rfind(d, '\n')
            carryover = d[cutindex + 1:]
            d = d[:cutindex + 1]
            d = map(intype, string.split(d))
            a[i:(i + len(d))] = d
            i = i + len(d)

    end = time.time()
    print '%d sec' % round(end - start, 2)
    data.close()
    os.remove(tmpname)
    return N.reshape(a, [numlines, numcols])


def find_dirs(sourcedir):
    """Finds and returns all directories in sourcedir

Usage:   find_dirs(sourcedir)
Returns: list of directory names (potentially empty)
"""
    files = os.listdir(sourcedir)
    dirs = []
    for fname in files:
        if os.path.isdir(os.path.join(sourcedir, fname)):
            dirs.append(fname)

    return dirs


save = aput

def binget(fname, btype=None):
    """
Loads a binary file from disk. Assumes associated hdr file is in same
location. You can force an unpacking type, or else it tries to figure
it out from the filename (4th-to-last character). Hence, readable file
formats are ...

1bin=Int8, sbin=int16, ibin=Int32, fbin=Float32, dbin=Float64, etc.

Usage:   binget(fname,btype=None)
Returns: data in file fname of type btype
"""
    file = open(fname, 'rb')
    bdata = file.read()
    file.close()
    if not btype:
        btype = fname[(-4)]
    try:
        bdata = N.fromstring(bdata, btype)
    except:
        raise ValueError, 'Bad unpacking type.'

    if not N.LittleEndian:
        bdata = bdata.byteswapped()
    try:
        header = fname[:-3] + 'hdr'
        vals = get(header, 0)
        print vals
        if type(vals[0]) == ListType:
            xsize = int(vals[0][0])
            ysize = int(vals[0][1])
            numslices = int(vals[0][2])
        else:
            bdata.shape = vals
    except:
        print 'No (or bad) header file. Returning unshaped array.'

    return N.array(bdata)


def binput(outarray, fname, packtype=None, writetype='wb'):
    """
Unravels outarray and writes the data to a file, always in LittleEndian
format, along with a header file containing the original data shape. Default
is overwrite the destination file. Tries to figure out packtype from
4th-to-last character in filename. Thus, the routine understands these
file formats ...

1bin=Int8, sbin=int16, ibin=Int32, fbin=Float32, dbin=Float64, etc.

Usage:  binput(outarray,filename,packtype=None,writetype='wb')
"""
    if not packtype:
        packtype = fname[(-4)]
    if packtype == N.int16 and outarray.typecode() == 'f':
        if max(N.ravel(outarray)) > 32767 or min(N.ravel(outarray)) < -32768:
            print '*** WARNING: CONVERTING FLOAT DATA TO OUT-OF RANGE int16 DATA'
    outdata = N.ravel(outarray).astype(packtype)
    if not N.LittleEndian:
        outdata = outdata.byteswapped()
    outdata = outdata.tostring()
    outfile = open(fname, writetype)
    outfile.write(outdata)
    outfile.close()
    try:
        suffixindex = string.rfind(fname, '.')
        hdrname = fname[0:suffixindex + 2] + 'hdr'
    except ValueError:
        hdrname = fname

    hdr = outarray.shape
    print hdrname
    outfile = open(hdrname, 'w')
    outfile.write(pstat.list2string(hdr))
    outfile.close()
    return


def array2afni(d, brikprefix, voltype=None, TR=2.0, sliceorder='seqplus', geomparent=None, view=None):
    """
Converts an array 'd' to an AFNI BRIK/HEAD combo via putbin and to3d. Tries to
guess the AFNI volume type

voltype = {'-anat','-epan','-fim'}
geomparent = filename of the afni BRIK file with the same geometry
view = {'tlrc', 'acpc' or 'orig'}

Usage:   array2afni(d,brikprefix,voltype=None,TR=2.0,
                    sliceorder='seqplus',geomparent=None,view=None)
Returns: None
"""
    typecodemapping = {'c': 'b', 'b': 'b', 
       'f': 'f', 
       'd': 'f', 
       '1': 'b', 
       's': '', 
       'i': 'i', 
       'l': 'i'}
    if len(d.shape) not in (3, 4):
        raise ValueError, 'A 3D or 4D array is required for array2afni() ... %s' % d.shape
    if d.typecode() == N.Float64:
        outcode = 'f'
    else:
        outcode = d.typecode()
    tmpoutname = 'afnitmp.%sbin' % outcode
    binput(d.astype(outcode), tmpoutname)
    if not voltype:
        if len(d.shape) == 3:
            if d.typecode() in ('s', 'i', 'l'):
                voltype = '-anat'
            else:
                voltype = '-fim'
        else:
            voltype = '-anat'
    if len(d.shape) == 3:
        timepts = 1
        slices = d.shape[0]
        timestr = ''
    elif len(d.shape) == 4:
        timepts = d.shape[0]
        slices = d.shape[1]
        timestr = '-time:zt %d %d %0.3f %s ' % (slices, timepts, TR, sliceorder)
    cmd = 'to3d %s -prefix %s -session . ' % (voltype, brikprefix)
    if view:
        cmd += '-view %s ' % view
    if geomparent:
        cmd += '-geomparent %s ' % geomparent
    cmd += timestr
    cmd += '3D%s:0:0:%d:%d:%d:%s' % (typecodemapping[d.typecode()], d.shape[(-1)], d.shape[(-2)], slices * timepts, tmpoutname)
    print cmd
    os.system(cmd)
    os.remove(tmpoutname)
    os.remove(tmpoutname[:-3] + 'hdr')