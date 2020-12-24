# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/gis/scripts/gdal_calculations.py
# Compiled at: 2014-08-06 10:27:53
try:
    from osgeo import gdal
    from osgeo.gdalnumeric import *
except ImportError:
    import gdal
    from gdalnumeric import *

from optparse import OptionParser
import os, sys
DefaultNDVLookup = {'Byte': 255, 'UInt16': 65535, 'Int16': -32767, 'UInt32': 4294967293, 'Int32': -2147483647, 'Float32': 1.175494351e-38, 'Float64': 1.7976931348623157e+308}

def doit(opts, AlphaList, len_argv):
    if opts.debug:
        print 'gdal_calc.py starting calculation %s' % opts.calc
    myFiles = []
    myBands = []
    myAlphaList = []
    myDataType = []
    myDataTypeNum = []
    myNDV = []
    DimensionsCheck = None
    for i, myI in enumerate(AlphaList[0:len_argv - 1]):
        myF = eval('opts.%s' % myI)
        myBand = eval('opts.%s_band' % myI)
        if myF:
            myFiles.append(gdal.Open(myF, gdal.GA_ReadOnly))
            if myBand:
                myBands.append(myBand)
            else:
                myBands.append(1)
            myAlphaList.append(myI)
            myDataType.append(gdal.GetDataTypeName(myFiles[i].GetRasterBand(myBands[i]).DataType))
            myDataTypeNum.append(myFiles[i].GetRasterBand(myBands[i]).DataType)
            myNDV.append(myFiles[i].GetRasterBand(myBands[i]).GetNoDataValue())
            if DimensionsCheck:
                if DimensionsCheck != [myFiles[i].RasterXSize, myFiles[i].RasterYSize]:
                    print 'Error! Dimensions of file %s (%i, %i) are different from other files (%i, %i).  Cannot proceed' % (
                     myF, myFiles[i].RasterXSize, myFiles[i].RasterYSize, DimensionsCheck[0], DimensionsCheck[1])
                    return
            else:
                DimensionsCheck = [
                 myFiles[i].RasterXSize, myFiles[i].RasterYSize]
            if opts.debug:
                print 'file %s: %s, dimensions: %s, %s, type: %s' % (myI, myF, DimensionsCheck[0], DimensionsCheck[1], myDataType[i])

    if os.path.isfile(opts.outF) and not opts.overwrite:
        if opts.debug:
            print 'Output file %s exists - filling in results into file' % opts.outF
        myOut = gdal.Open(opts.outF, gdal.GA_Update)
        if [myOut.RasterXSize, myOut.RasterYSize] != DimensionsCheck:
            print 'Error! Output exists, but is the wrong size.  Use the --overwrite option to automatically overwrite the existing file'
            return
        myOutB = myOut.GetRasterBand(1)
        myOutNDV = myOutB.GetNoDataValue()
        myOutType = gdal.GetDataTypeName(myOutB.DataType)
    else:
        if os.path.isfile(opts.outF):
            os.remove(opts.outF)
        if opts.debug:
            print 'Generating output file %s' % opts.outF
        if not opts.type:
            myOutType = gdal.GetDataTypeName(max(myDataTypeNum))
        else:
            myOutType = opts.type
        myOutDrv = gdal.GetDriverByName(opts.format)
        myOut = myOutDrv.Create(opts.outF, DimensionsCheck[0], DimensionsCheck[1], 1, gdal.GetDataTypeByName(myOutType), opts.creation_options)
        myOut.SetGeoTransform(myFiles[0].GetGeoTransform())
        myOut.SetProjection(myFiles[0].GetProjection())
        myOutB = myOut.GetRasterBand(1)
        if opts.NoDataValue != None:
            myOutNDV = opts.NoDataValue
        else:
            myOutNDV = DefaultNDVLookup[myOutType]
        myOutB.SetNoDataValue(myOutNDV)
        myOutB = None
        myOutB = myOut.GetRasterBand(1)
    if opts.debug:
        print 'output file: %s, dimensions: %s, %s, type: %s' % (opts.outF, myOut.RasterXSize, myOut.RasterYSize, gdal.GetDataTypeName(myOutB.DataType))
    myBlockSize = myFiles[0].GetRasterBand(myBands[0]).GetBlockSize()
    nXValid = myBlockSize[0]
    nYValid = myBlockSize[1]
    nXBlocks = int((DimensionsCheck[0] + myBlockSize[0] - 1) / myBlockSize[0])
    nYBlocks = int((DimensionsCheck[1] + myBlockSize[1] - 1) / myBlockSize[1])
    myBufSize = myBlockSize[0] * myBlockSize[1]
    if opts.debug:
        print 'using blocksize %s x %s' % (myBlockSize[0], myBlockSize[1])
    ProgressCt = -1
    ProgressMk = -1
    ProgressEnd = nXBlocks * nYBlocks
    for X in range(0, nXBlocks):
        if X == nXBlocks - 1:
            nXValid = DimensionsCheck[0] - X * myBlockSize[0]
            myBufSize = nXValid * nYValid
        myX = X * myBlockSize[0]
        nYValid = myBlockSize[1]
        myBufSize = nXValid * nYValid
        for Y in range(0, nYBlocks):
            ProgressCt += 1
            if 10 * ProgressCt / ProgressEnd % 10 != ProgressMk:
                ProgressMk = 10 * ProgressCt / ProgressEnd % 10
                from sys import version_info
                if version_info >= (3, 0, 0):
                    exec 'print("%d.." % (10*ProgressMk), end=" ")'
                else:
                    exec 'print 10*ProgressMk, "..",'
            if Y == nYBlocks - 1:
                nYValid = DimensionsCheck[1] - Y * myBlockSize[1]
                myBufSize = nXValid * nYValid
            myY = Y * myBlockSize[1]
            myNDVs = numpy.zeros(myBufSize)
            myNDVs.shape = (nYValid, nXValid)
            for i, Alpha in enumerate(myAlphaList):
                myval = BandReadAsArray(myFiles[i].GetRasterBand(myBands[i]), xoff=myX, yoff=myY, win_xsize=nXValid, win_ysize=nYValid)
                myNDVs = 1 * numpy.logical_or(myNDVs == 1, myval == myNDV[i])
                exec '%s=myval' % Alpha
                myval = None

            try:
                myResult = eval(opts.calc)
            except:
                print 'evaluation of calculation %s failed' % opts.calc
                raise

            myResult = 1 * (myNDVs == 0) * myResult + myOutNDV * myNDVs
            BandWriteArray(myOutB, myResult, xoff=myX, yoff=myY)

    return


def main():
    print 'gdal_calculations ' + str(sys.argv)
    index = 0
    for args in sys.argv:
        if 'alphalist' in args:
            AlphaList = sys.argv[(index + 1)]
        index += 1

    AlphaList = eval(AlphaList)
    parser = OptionParser()
    parser.add_option('--calc', dest='calc', help='calculation in gdalnumeric syntax using +-/* or any numpy array functions (i.e. logical_and())')
    for myAlpha in AlphaList[0:len(sys.argv) - 1]:
        eval('parser.add_option("--%s", dest="%s", help="input gdal raster file, note you can use any letter A-Z")' % (myAlpha, myAlpha))
        eval('parser.add_option("--%s_band", dest="%s_band", default=0, type=int, help="number of raster band for file %s")' % (myAlpha, myAlpha, myAlpha))

    parser.add_option('--alphalist', dest='', default='', help='')
    parser.add_option('--outfile', dest='outF', default='gdal_calc.tif', help='output file to generate or fill.')
    parser.add_option('--NoDataValue', dest='NoDataValue', type=float, help='set output nodatavalue (Defaults to datatype specific values)')
    parser.add_option('--type', dest='type', help='set datatype must be one of %s' % list(DefaultNDVLookup.keys()))
    parser.add_option('--format', dest='format', default='GTiff', help="GDAL format for output file (default 'GTiff')")
    parser.add_option('--creation-option', '--co', dest='creation_options', default=[], action='append', help='Passes a creation option to the output format driver. Multipleoptions may be listed. See format specific documentation for legalcreation options for each format.')
    parser.add_option('--overwrite', dest='overwrite', action='store_true', help='overwrite output file if it already exists')
    parser.add_option('--debug', dest='debug', action='store_true', help='print debugging information')
    opts, args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    elif not opts.calc:
        print 'No calculation provided.  Nothing to do!'
        parser.print_help()
    else:
        doit(opts, AlphaList, len(sys.argv))


if __name__ == '__main__':
    main()