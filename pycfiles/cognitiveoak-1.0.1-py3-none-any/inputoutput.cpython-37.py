# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\seismic\inputoutput.py
# Compiled at: 2019-12-15 17:47:39
# Size of source mod 2**32: 52413 bytes
from PyQt5 import QtCore
import os, sys, numpy as np, math
sys.path.append(os.path.dirname(__file__)[:-8][:-4][:-13])
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.seismic.analysis as seis_ays
from cognitivegeo.src.segpy.header import field
from cognitivegeo.src.segpy.types import Int32
import cognitivegeo.src.segpy.reader as syreader
import cognitivegeo.src.segpy.writer as sywriter
import cognitivegeo.src.segpy.packer as sypacker
from cognitivegeo.src.segpy.binary_reel_header import BinaryReelHeader
from cognitivegeo.src.segpy.trace_header import TraceHeaderRev1
__all__ = [
 'inputoutput']

def readSeisDataFromSegy(segyfile, seisinfo, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True, qpgsdlg=None):
    """
    Read seismic data from segy file (by segpy)

    Args:
        segyfile:           segy file for reading
        seisinfo:           seismic information dictionary
        traceheaderformat:  Trace header format. Default is TraceHeaderRev1
        endian:             Endian ('>' or '<'). Default is '>'
        verbose:            Verbose option
        qpgsdlg:            Qt preogress dialog

    Return:
        seisdata:   Seismic data in 3D matrix
        traceflag:  Flag for seismic traces. 1 for missing traces
    """
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']
    seisdata = np.zeros([znum, xlnum, inlnum])
    traceflag = np.zeros([xlnum, inlnum])
    traceheaderpacker = sypacker.HeaderPacker(traceheaderformat, endian)
    dataformat = np.array([4, 4, 2, 4, 4, 0, 0, 1])
    with open(segyfile, 'rb') as (sid):
        dat = syreader.create_reader(sid, trace_header_format=traceheaderformat, endian=endian)
        binary_header = syreader.read_binary_reel_header(sid, endian=endian)
        databyte = dataformat[(binary_header.data_sample_format - 1)]
        pos = np.int64(3600)
        if qpgsdlg is not None:
            qpgsdlg.setMaximum(inlnum * xlnum)
        for itrace in dat.trace_indexes():
            if qpgsdlg is not None:
                QtCore.QCoreApplication.instance().processEvents()
                qpgsdlg.setValue(itrace)
            if verbose:
                sys.stdout.write('\r>>> Read %d traces: %.1f%% ' % (inlnum * xlnum, float(itrace) / float(inlnum * xlnum) * 100))
                sys.stdout.flush()
            header = syreader.read_trace_header(sid, trace_header_packer=traceheaderpacker, pos=pos)
            pos = pos + 240 + header.num_samples * databyte
            idx_xl = int((header.crossline_number - xlstart) / xlstep)
            idx_inl = int((header.inline_number - inlstart) / inlstep)
            idx = idx_xl + idx_inl * xlnum
            if idx < inlnum * xlnum:
                seisdata[:, idx_xl, idx_inl] = dat.trace_samples(itrace)
                traceflag[(idx_xl, idx_inl)] = 0

        if qpgsdlg is not None:
            qpgsdlg.setValue(inlnum * xlnum)
        if verbose:
            print('Done')
    return (seisdata, traceflag)


def readSeisInfoFromSegy(segyfile, traceheaderformat=TraceHeaderRev1, endian='>'):
    """
    Read basic information of a 3D seismic survey from a segy file

    Args:
        segyfile:           file name of seismic file in segy format
        traceheaderformat:  The class defining the layout of the trace header.
        endian:             '>' for big-endian data (the standard and default), '<'
                                for little-endian (non-standard)
    Returns:
        Seismic information dictionary as defined in analysis.py

    Note:
        negative z is used in the vertical direction
    """
    if os.path.isfile(segyfile) is False:
        vis_msg.print(('ERROR in readSeisInfoFromSegy: ' + segyfile + ' not found'), type='error')
        sys.exit()
    with open(segyfile, 'rb') as (sid):
        dat = syreader.create_reader(sid, trace_header_format=traceheaderformat, endian=endian)
        if dat.dimensionality > 3:
            if dat.dimensionality <= 0:
                vis_msg.print(('ERROR in readSeisInfoFromSegy: ' + segyfile + ' contains no seismic survey'), type='error')
                sys.exit()
        if dat.dimensionality == 1:
            vis_msg.print(('WARNING in readSeisInfoFromSegy: ' + segyfile + ' contains 1D seismic survey'), type='warning')
            inlstart = 0
            inlend = 0
            inlnum = 1
            xlstart = 0
            xlend = 0
            xlnum = 1
        if dat.dimensionality == 2:
            vis_msg.print(('WARNING in readSeisInfoFromSegy: ' + segyfile + ' contains 2D seismic survey'), type='warning')
            inlstart = 0
            inlend = 0
            inlnum = 1
            xlstart = 0
            xlend = dat.num_traces() - 1
            xlnum = dat.num_traces()
        if dat.dimensionality == 3:
            inlstart = dat.inline_range()[0]
            inlend = dat.inline_range()[(-1)]
            inlnum = dat.num_inlines()
            xlstart = dat.xline_range()[0]
            xlend = dat.xline_range()[(-1)]
            xlnum = dat.num_xlines()
        seisinfo = seis_ays.makeSeisInfo()
        inlstep = 1
        if inlnum > 1:
            inlstep = (inlend - inlstart) / (inlnum - 1)
        inlstart = np.round(inlstart).astype(np.int32)
        inlstep = np.round(inlstep).astype(np.int32)
        inlnum = np.round(inlnum).astype(np.int32)
        if inlstep == 0:
            inlstep = 1
        inlend = (inlstart + (inlnum - 1) * inlstep).astype(np.int32)
        inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
        seisinfo['ILStart'] = inlstart
        seisinfo['ILEnd'] = inlend
        seisinfo['ILStep'] = inlstep
        seisinfo['ILNum'] = inlnum
        seisinfo['ILRange'] = inlrange
        xlstep = 1
        if xlnum > 1:
            xlstep = (xlend - xlstart) / (xlnum - 1)
        xlstart = np.round(xlstart).astype(np.int32)
        xlstep = np.round(xlstep).astype(np.int32)
        xlnum = np.round(xlnum).astype(np.int32)
        if xlstep == 0:
            xlstep = 1
        xlend = (xlstart + (xlnum - 1) * xlstep).astype(np.int32)
        xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
        seisinfo['XLStart'] = xlstart
        seisinfo['XLEnd'] = xlend
        seisinfo['XLStep'] = xlstep
        seisinfo['XLNum'] = xlnum
        seisinfo['XLRange'] = xlrange
        zstart = dat.trace_header(0).lag_time_a
        zstep = -dat.trace_header(0).sample_interval / 1000
        znum = dat.trace_header(0).num_samples
        zstart = np.round(zstart).astype(np.int32)
        zstep = np.round(zstep).astype(np.int32)
        znum = np.round(znum).astype(np.int32)
        if zstart > 0:
            zstart = -zstart
        if zstep == 0:
            zstep = -1
        zend = (zstart + (znum - 1) * zstep).astype(np.int32)
        zrange = np.linspace(zstart, zend, znum).astype(np.int32)
        seisinfo['ZStart'] = zstart
        seisinfo['ZEnd'] = zend
        seisinfo['ZStep'] = zstep
        seisinfo['ZNum'] = znum
        seisinfo['ZRange'] = zrange
    return seisinfo


def readSeis2DMatFromSegyWithInfo(segyfile, seisinfo=None, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True, qpgsdlg=None):
    """
    Read seismic data from a segy file, as a 2D matrix, with seismic information provided

    Args:
        segyfile:           file name of seismic file in segy format
        seisinfo:           Seismic information dictionary. If not provided, a scanning will run on the segy file.
        traceheaderformat:  The class defining the layout of the trace header.
        endian:             '>' for big-endian data (the standard and default), '<'
                                for little-endian (non-standard)

    Returns:
        seis2dmat:  a 2D matrix of four cloumns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSeis2DMatFromSegyWithInfo: ' + segyfile + ' not found'), type='error')
        sys.exit()
    if seisinfo is None or seis_ays.checkSeisInfo(seisinfo) is False:
        seisinfo = readSeisInfoFromSegy(segyfile, traceheaderformat=traceheaderformat, endian=endian)
    seis3dmat, traceflag = readSeis3DMatFromSegyWithInfo(segyfile, seisinfo, traceheaderformat=traceheaderformat,
      endian=endian,
      verbose=verbose,
      qpgsdlg=qpgsdlg)
    seis2dmat = seis_ays.convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
    return seis2dmat


def readSeis2DMatFromSegyNoInfo(segyfile, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True, qpgsdlg=None):
    """
    Read seismic data from a segy file, as a 2D matrix, without seismic information provided

    Args:
        segyfile:           File name of seismic file in segy format
        traceheaderformat:  The class defining the layout of the trace header.
        endian:             '>' for big-endian data (the standard and default), '<'
                                for little-endian (non-standard)

    Returns:
        seis2dmat:  a 2D matrix of four cloumns [IL, XL, Z, Value]

    Note:
        Negative z is used in the vertical direction
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSeis2DMatFromSegyNoInfo: ' + segyfile + ' not found'), type='error')
        sys.exit()
    seis3dmat, seisinfo = readSeis3DMatFromSegyNoInfo(segyfile, traceheaderformat=traceheaderformat,
      endian=endian,
      verbose=verbose,
      qpgsdlg=qpgsdlg)
    seis2dmat = seis_ays.convertSeis3DMatTo2DMat(seis3dmat, seisinfo)
    return seis2dmat


def readSeis3DMatFromSegyWithInfo(segyfile, seisinfo=None, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True, qpgsdlg=None):
    """
    Read seismic data from a segy file, as a 3D matrix, with seismic information provided

    Args:
        segyfile:           File name of seismic file in segy format
        seisinfo:           Seismic information dictionary. If not provided, a scanning will run on the segy file.
        traceheaderformat:  The class defining the layout of the trace header.
        endian:             '>' for big-endian data (the standard and default), '<'
                                for little-endian (non-standard)
        verbose:            Message display. Default is True
        qpgsdlg:            Qt progress dialog

    Returns:
        seis3dmat:  a 3D matrix [Z/Crossline/Inline]

    Note:
        Negative z is used in the vertical direction
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSeis3DMatFromSegy: ' + segyfile + ' not found'), type='error')
        sys.exit()
    if seisinfo is None or seis_ays.checkSeisInfo(seisinfo) is False:
        seisinfo = readSeisInfoFromSegy(segyfile, traceheaderformat=traceheaderformat, endian=endian)
    seis3dmat, traceflag = readSeisDataFromSegy(segyfile, seisinfo, traceheaderformat=traceheaderformat,
      endian=endian,
      verbose=verbose,
      qpgsdlg=qpgsdlg)
    return seis3dmat


def readSeis3DMatFromSegyNoInfo(segyfile, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True, qpgsdlg=None):
    """
    Read seismic data from a segy file, as a 3D matrix, without seismic information provided

    Args:
        segyfile:           File name of seismic file in segy format
        traceheaderformat:  The class defining the layout of the trace header.
        endian:             '>' for big-endian data (the standard and default), '<'
                                for little-endian (non-standard)
        verbose:            Message display. Default is True
        qpgsdlg:            Qt progress dialog

    Returns:
        seis3dmat:  a 3D matrix [Z/Crossline/Inline]

    Note:
        Negative z is used in the vertical direction
    """
    if os.path.isfile(segyfile) is False:
        vis_msg.print(('ERROR in readSeisInfoFromSegy: ' + segyfile + ' not found'), type='error')
        sys.exit()
    traceheaderpacker = sypacker.HeaderPacker(traceheaderformat, endian)
    dataformat = np.array([4, 4, 2, 4, 4, 0, 0, 1])
    with open(segyfile, 'rb') as (sid):
        dat = syreader.create_reader(sid, trace_header_format=traceheaderformat, endian=endian)
        binary_header = syreader.read_binary_reel_header(sid, endian=endian)
        databyte = dataformat[(binary_header.data_sample_format - 1)]
        if dat.dimensionality > 3:
            if dat.dimensionality <= 0:
                vis_msg.print(('ERROR in readSeis3DMatFromSegyNoInfo: ' + segyfile + ' contains no seismic survey'), type='error')
                sys.exit()
        if dat.dimensionality == 1:
            vis_msg.print(('WARNING in readSeisInfoFromSegy: ' + segyfile + ' contains 1D seismic survey'), type='warning')
            inlstart = 0
            inlend = 0
            inlnum = 1
            xlstart = 0
            xlend = 0
            xlnum = 1
        if dat.dimensionality == 2:
            vis_msg.print(('WARNING in readSeis3DMatFromSegyNoInfo: ' + segyfile + ' contains 2D seismic survey'), type='warning')
            inlstart = 0
            inlend = 0
            inlnum = 1
            xlstart = 0
            xlend = dat.num_traces() - 1
            xlnum = dat.num_traces()
        if dat.dimensionality == 3:
            inlstart = dat.inline_range()[0]
            inlend = dat.inline_range()[(-1)]
            inlnum = dat.num_inlines()
            xlstart = dat.xline_range()[0]
            xlend = dat.xline_range()[(-1)]
            xlnum = dat.num_xlines()
        seisinfo = seis_ays.makeSeisInfo()
        inlstep = 1
        if inlnum > 1:
            inlstep = (inlend - inlstart) / (inlnum - 1)
        inlstart = np.round(inlstart).astype(np.int32)
        inlstep = np.round(inlstep).astype(np.int32)
        inlnum = np.round(inlnum).astype(np.int32)
        if inlstep == 0:
            inlstep = 1
        inlend = (inlstart + (inlnum - 1) * inlstep).astype(np.int32)
        inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
        seisinfo['ILStart'] = inlstart
        seisinfo['ILEnd'] = inlend
        seisinfo['ILStep'] = inlstep
        seisinfo['ILNum'] = inlnum
        seisinfo['ILRange'] = inlrange
        xlstep = 1
        if xlnum > 1:
            xlstep = (xlend - xlstart) / (xlnum - 1)
        xlstart = np.round(xlstart).astype(np.int32)
        xlstep = np.round(xlstep).astype(np.int32)
        xlnum = np.round(xlnum).astype(np.int32)
        if xlstep == 0:
            xlstep = 1
        xlend = (xlstart + (xlnum - 1) * xlstep).astype(np.int32)
        xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
        seisinfo['XLStart'] = xlstart
        seisinfo['XLEnd'] = xlend
        seisinfo['XLStep'] = xlstep
        seisinfo['XLNum'] = xlnum
        seisinfo['XLRange'] = xlrange
        zstart = dat.trace_header(0).lag_time_a
        zstep = -dat.trace_header(0).sample_interval / 1000
        znum = dat.trace_header(0).num_samples
        zstart = np.round(zstart).astype(np.int32)
        zstep = np.round(zstep).astype(np.int32)
        znum = np.round(znum).astype(np.int32)
        if zstart > 0:
            zstart = -zstart
        if zstep == 0:
            zstep = -1
        zend = (zstart + (znum - 1) * zstep).astype(np.int32)
        zrange = np.linspace(zstart, zend, znum).astype(np.int32)
        seisinfo['ZStart'] = zstart
        seisinfo['ZEnd'] = zend
        seisinfo['ZStep'] = zstep
        seisinfo['ZNum'] = znum
        seisinfo['ZRange'] = zrange
        seisdata = np.zeros([znum, xlnum, inlnum])
        traceflag = np.zeros([xlnum, inlnum])
        pos = np.int64(3600)
        if qpgsdlg is not None:
            qpgsdlg.setMaximum(inlnum * xlnum)
        for itrace in dat.trace_indexes():
            if qpgsdlg is not None:
                QtCore.QCoreApplication.instance().processEvents()
                qpgsdlg.setValue(itrace)
            if verbose:
                sys.stdout.write('\r>>> Scan %s: %d traces ' % (segyfile, itrace + 1))
                sys.stdout.flush()
            header = syreader.read_trace_header(sid, trace_header_packer=traceheaderpacker, pos=pos)
            pos = pos + 240 + header.num_samples * databyte
            idx_xl = int((header.crossline_number - xlstart) / xlstep)
            idx_inl = int((header.inline_number - inlstart) / inlstep)
            idx = idx_xl + idx_inl * xlnum
            if idx < inlnum * xlnum:
                seisdata[:, idx_xl, idx_inl] = dat.trace_samples(itrace)
                traceflag[(idx_xl, idx_inl)] = 0

        if qpgsdlg is not None:
            qpgsdlg.setValue(inlnum * xlnum)
        if verbose:
            print('Done')
    return (seisdata, seisinfo)


def writeSeis2DMatToSegyWithRef(seis2dmat, seisfile, refsegy, datacol=3, verbose=True, qpgsdlg=None):
    """
    Write seismic data from a 2D matrix to segy file, with survey information from a reference segy file

    Args:
        seis2dmat:  seismic data in a 2D matrix containing at least one columns [Value, ...]
                    Default setting is for a 4-column 2D matrix [IL, XL, Z, Value]
                    Adjust targetcol correspondingly.
        seisfile:   name of the output segy file
        refsefy:    reference segy file for copying the header information
        datacol:    index of the data column for output (indexing from 0)
                    Default is 3 (the fourth column)
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None

    Returns:
        N/A
    """
    if not os.path.isfile(refsegy):
        vis_msg.print(('ERROR in writeSeis2DMatToSegyWithRef: ' + refsegy + ' not found'), type='error')
        sys.exit()
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in writeSeis2DMatToSegyWithRef: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in writeSeis2DMatToSegyWithRef: No data column found in 2D seismic matrix', type='error')
        sys.exit()
    seis2dmat = seis2dmat[:, datacol]
    with open(refsegy, 'rb') as (refid):
        with open(seisfile, 'wb') as (sid):
            seisdata = syreader.create_reader(refid)
            znum = seisdata.trace_header(0).num_samples
            samplenum = len(seis2dmat)
            tracenum = int(samplenum / znum)
            seis2dmat = seis2dmat.transpose()
            seis2dmat = np.reshape(seis2dmat, [tracenum, znum])
            seis2dmat = seis2dmat.transpose()
            sywriter.write_textual_reel_header(sid, (seisdata.textual_reel_header),
              encoding=(seisdata.encoding))
            sywriter.write_binary_reel_header(sid, (seisdata.binary_reel_header),
              endian=(seisdata.endian))
            sywriter.write_extended_textual_headers(sid, (seisdata.extended_textual_header),
              encoding=(seisdata.encoding))
            traceheaderpacker = sypacker.HeaderPacker(TraceHeaderRev1, endian=(seisdata.endian))
            if qpgsdlg is not None:
                qpgsdlg.setMaximum(tracenum)
            for itrace in seisdata.trace_indexes():
                if qpgsdlg is not None:
                    QtCore.QCoreApplication.instance().processEvents()
                    qpgsdlg.setValue(itrace)
                if verbose:
                    sys.stdout.write('\r>>> Write %d traces into SEG-Y: proceeding %.1f%% ' % (
                     tracenum, float(itrace + 1) / float(tracenum) * 100))
                    sys.stdout.flush()
                sywriter.write_trace_header(sid, (seisdata.trace_header(itrace)),
                  trace_header_packer=traceheaderpacker)
                sywriter.write_trace_samples(sid, (seis2dmat[:, itrace]),
                  (seisdata.data_sample_format),
                  endian=(seisdata.endian))
                if itrace >= tracenum:
                    vis_msg.print(('WARNING in writeSeis2DMatToSegyWithRef: Reference segy file ' + refsegy + ' contains more traces than 2D seismic matrix'),
                      type='warning')
                    break

            if verbose:
                print('Done --> output file saved as ' + seisfile)
            if qpgsdlg is not None:
                qpgsdlg.setValue(tracenum)
    return True


def writeSeis3DMatToSegyWithRef(seis3dmat, seisfile, refsegy, verbose=True, qpgsdlg=None):
    """
    Write seismic data from a 3D matrix to segy file, with survey information from a reference segy file

    Args:
        seis3dmat:  seismic data in a 3D matrix [Z/Crossline/Inline]
        seisfile:   name of the output segy file
        refsegy:    reference segy file for copying the header information
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None

    Returns:
        N/A
    """
    if os.path.isfile(refsegy) == False:
        vis_msg.print(('ERROR in writeSeis3DMatToSegyWithRef: ' + refsegy + ' not found'), type='error')
        sys.exit()
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in writeSeis3DMatToSegyWithRef: 3D seismic matrix expected', type='error')
        sys.exit()
    with open(refsegy, 'rb') as (refid):
        with open(seisfile, 'wb') as (sid):
            seisdata = syreader.create_reader(refid)
            znum, xlnum, inlnum = np.shape(seis3dmat)
            znum = np.round(znum).astype(np.int32)
            xlnum = np.round(xlnum).astype(np.int32)
            inlnum = np.round(inlnum).astype(np.int32)
            tracenum = (inlnum * xlnum).astype(np.int64)
            seis3dmat = seis3dmat.transpose()
            seis3dmat = np.reshape(seis3dmat, [inlnum * xlnum, znum])
            seis3dmat = seis3dmat.transpose()
            sywriter.write_textual_reel_header(sid, (seisdata.textual_reel_header),
              encoding=(seisdata.encoding))
            sywriter.write_binary_reel_header(sid, (seisdata.binary_reel_header),
              endian=(seisdata.endian))
            sywriter.write_extended_textual_headers(sid, (seisdata.extended_textual_header),
              encoding=(seisdata.encoding))
            traceheaderpacker = sypacker.HeaderPacker(TraceHeaderRev1, endian=(seisdata.endian))
            if qpgsdlg is not None:
                qpgsdlg.setMaximum(tracenum)
            for itrace in seisdata.trace_indexes():
                if qpgsdlg is not None:
                    QtCore.QCoreApplication.instance().processEvents()
                    qpgsdlg.setValue(itrace)
                if verbose:
                    sys.stdout.write('\r>>> Write %d traces into SEG-Y: proceeding %.1f%%' % (tracenum, float(itrace + 1) / float(tracenum) * 100))
                    sys.stdout.flush()
                sywriter.write_trace_header(sid, (seisdata.trace_header(itrace)),
                  trace_header_packer=traceheaderpacker)
                sywriter.write_trace_samples(sid, (seis3dmat[:, itrace]),
                  (seisdata.data_sample_format),
                  endian=(seisdata.endian))
                if itrace >= tracenum:
                    vis_msg.print(('WARNING in writeSeis3DMatToSegyWithRef: Reference segy file ' + refsegy + ' contains more traces than input 3D seismic matrix'),
                      type='warning')
                    break

            if verbose:
                print('Done --> output file saved as ' + seisfile)
            if qpgsdlg is not None:
                qpgsdlg.setValue(tracenum)
    return True


def writeSeis2DMatToSegyNoRef(seis2dmat, seisfile, xcoorstart=0.0, ycoorstart=0.0, inlbinsize=1.0, xlbinsize=1.0, orientation=90, inlcol=0, xlcol=1, zcol=2, datacol=3, verbose=True, qpgsdlg=None):
    """
    Write seismic data from a 3D matrix to segy file, with user-defined survey information

    Args:
        seis2dmat:      seismic data in a 2D matrix containing at least one columns [Value, ...]
                        Default setting is for a 4-column 2D matrix [IL, XL, Z, Value]
                        Adjust targetcol correspondingly.
        seisfile:       name of the output segy file
        xcoorstart:     x coordinate of first trace. Default is 0.0
        ycoorstart:     y coordinate of first trace. Default is 0.0
        inlbinsize:     inline bin size. Default is 1.0
        xlbinsize:      crossline bin size. Default is 1.0
        orientation:    orienation of the first crossline from N direction in degree. Default is 90
        inlcol:         index of inline column. Default is the first column (0)
        xlcol:          index of crossline column. Default is the second column (1)
        zcol:           index of z column. Default is the third column (2)
        datacol:        index of the data column for output (indexing from 0)
                        Default is 3 (the fourth column)
        verbose:        flag for message display. Default is True
        qpgsdlg:        QProgressDialog for displaying progress. Default is None

    Returns:
        N/A

    Note:
        Negative z is used in the vertical direction
        ASCII is used for textual header
        IBM floating is used for data format
    """
    if np.ndim(seis2dmat) != 2:
        vis_msg.print('ERROR in writeSeis2DMatToSegyNoRef: 2D seismic matrix expected', type='error')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        vis_msg.print('ERROR in writeSeis2DMatToSegyNoRef: No data column found in 2D seismic matrix', type='error')
        sys.exit()
    seis3dmat = seis_ays.convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol)
    seisinfo = seis_ays.getSeisInfoFrom2DMat(seis2dmat, inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    with open(seisfile, 'wb') as (sid):
        znum, xlnum, inlnum = np.shape(seis3dmat)
        znum = np.round(znum).astype(np.int32)
        xlnum = np.round(xlnum).astype(np.int32)
        inlnum = np.round(inlnum).astype(np.int32)
        tracenum = (inlnum * xlnum).astype(np.int64)
        seis3dmat = seis3dmat.transpose()
        seis3dmat = np.reshape(seis3dmat, [inlnum * xlnum, znum])
        seis3dmat = seis3dmat.transpose()
        textualheader = createSegyTextualHeader()
        sywriter.write_textual_reel_header(sid, textualheader,
          encoding='ascii')
        binaryheader = createSegyBinaryHeader(znum, zstep)
        sywriter.write_binary_reel_header(sid, binaryheader)
        traceheaderpacker = sypacker.HeaderPacker(TraceHeaderRev1)
        if qpgsdlg is not None:
            qpgsdlg.setMaximum(tracenum)
        for itrace in range(tracenum):
            if qpgsdlg is not None:
                QtCore.QCoreApplication.instance().processEvents()
                qpgsdlg.setValue(itrace)
            if verbose:
                sys.stdout.write('\r>>> Write %d traces into SEG-Y: proceeding %.1f%%' % (
                 tracenum, float(itrace + 1) / float(tracenum) * 100))
                sys.stdout.flush()
            xcoor = xcoorstart - int(itrace / xlnum) * inlbinsize * math.cos(orientation * math.pi / 180)
            ycoor = ycoorstart + int(itrace / xlnum) * inlbinsize * math.sin(orientation * math.pi / 180)
            traceheader = createSegyTraceHeader(inlstart + int(itrace / xlnum) * inlstep, xlstart + int(itrace % xlnum) * xlstep, xcoor + int(itrace % xlnum) * xlbinsize * math.sin(orientation * math.pi / 180), ycoor + int(itrace % xlnum) * xlbinsize * math.cos(orientation * math.pi / 180), znum, zstep, zstart)
            sywriter.write_trace_header(sid, traceheader,
              trace_header_packer=traceheaderpacker)
            sywriter.write_trace_samples(sid, seis3dmat[:, itrace], 'ibm')

        if verbose:
            print('Done --> output file saved as ' + seisfile)
        if qpgsdlg is not None:
            qpgsdlg.setValue(tracenum)
    return True


def writeSeis3DMatToSegyNoRef(seis3dmat, seisfile, xcoorstart=0.0, ycoorstart=0.0, inlbinsize=1.0, xlbinsize=1.0, orientation=90, inlstart=1, inlstep=1, xlstart=1, xlstep=1, zstart=0, zstep=-1, verbose=True, qpgsdlg=None):
    """
    Write seismic data from a 3D matrix to segy file, with user-defined survey information

    Args:
        seis3dmat:      seismic data in a 3D matrix [Z/Crossline/Inline]
        seisfile:       name of the output segy file
        xcoorstart:     x coordinate of first trace. Default is 0.0
        ycoorstart:     y coordinate of first trace. Default is 0.0
        inlbinsize:     inline bin size. Default is 1.0
        xlbinsize:      crossline bin size. Default is 1.0
        orientation:    orienation of the first crossline from N direction in degree. Default is 90
        inlstart:       inline number of first trace. Default is 1
        inlstep:        inline step. Default is 1
        xlstart:        crossline number of first trace. Default is 1
        xlstep:         crossline step. Default is 1
        zstart:         z value of first sample. Default is 0
        zstep:          z step. Default is -1
        verbose:        flag for message display. Default is True
        qpgsdlg:        QProgressDialog for displaying progress. Default is None

    Returns:
        N/A

    Note:
        Negative z is used in the vertical direction
        ASCII is used for textual header
        IBM floating is used for data format
    """
    if np.ndim(seis3dmat) != 3:
        vis_msg.print('ERROR in writeSeis3DMatToSegyNoRef: 3D seismic matrix expected', type='error')
        sys.exit()
    with open(seisfile, 'wb') as (sid):
        znum, xlnum, inlnum = np.shape(seis3dmat)
        znum = np.round(znum).astype(np.int32)
        xlnum = np.round(xlnum).astype(np.int32)
        inlnum = np.round(inlnum).astype(np.int32)
        tracenum = (inlnum * xlnum).astype(np.int64)
        seis3dmat = seis3dmat.transpose()
        seis3dmat = np.reshape(seis3dmat, [inlnum * xlnum, znum])
        seis3dmat = seis3dmat.transpose()
        textualheader = createSegyTextualHeader()
        sywriter.write_textual_reel_header(sid, textualheader,
          encoding='ascii')
        binaryheader = createSegyBinaryHeader(znum, zstep)
        sywriter.write_binary_reel_header(sid, binaryheader)
        traceheaderpacker = sypacker.HeaderPacker(TraceHeaderRev1)
        if qpgsdlg is not None:
            qpgsdlg.setMaximum(tracenum)
        for itrace in range(tracenum):
            if qpgsdlg is not None:
                QtCore.QCoreApplication.instance().processEvents()
                qpgsdlg.setValue(itrace)
            if verbose:
                sys.stdout.write('\r>>> Write %d traces into SEG-Y: proceeding %.1f%%' % (
                 tracenum, float(itrace + 1) / float(tracenum) * 100))
                sys.stdout.flush()
            xcoor = xcoorstart - int(itrace / xlnum) * inlbinsize * math.cos(orientation * math.pi / 180)
            ycoor = ycoorstart + int(itrace / xlnum) * inlbinsize * math.sin(orientation * math.pi / 180)
            traceheader = createSegyTraceHeader(inlstart + int(itrace / xlnum) * inlstep, xlstart + int(itrace % xlnum) * xlstep, xcoor + int(itrace % xlnum) * xlbinsize * math.sin(orientation * math.pi / 180), ycoor + int(itrace % xlnum) * xlbinsize * math.cos(orientation * math.pi / 180), znum, zstep, zstart)
            sywriter.write_trace_header(sid, traceheader,
              trace_header_packer=traceheaderpacker)
            sywriter.write_trace_samples(sid, seis3dmat[:, itrace], 'ibm')

        if verbose:
            print('Done --> output file saved as ' + seisfile)
        if qpgsdlg is not None:
            qpgsdlg.setValue(tracenum)
    return True


def createSegyTextualHeader():
    """
    Create 3200-byte Seg-Y textual header

    Args:
        None

    Returns:
        header: A tuple of forty Unicode strings containing the transcoded header data.
    """
    header = ()
    header = header + ('C01 Created By: Cognitive Geo                                                   ', )
    header = header + ('C02 Author: GeoPy Team (geopy.info@gmail.com)                                   ', )
    header = header + ('C03                                                                             ', )
    header = header + ('C04                                                                             ', )
    header = header + ('C05                                                                             ', )
    header = header + ('C06                                                                             ', )
    header = header + ('C07                                                                             ', )
    header = header + ('C08                                                                             ', )
    header = header + ('C09                                                                             ', )
    header = header + ('C10                                                                             ', )
    header = header + ('C11 Key Parameters:                                                             ', )
    header = header + ('C12 a. 4-byte IBM Floating-point Data Format                                    ', )
    header = header + ('C13 b. SEG-Y Format Revision 1.0                                                ', )
    header = header + ('C14 c. Fixed Length for All Traces                                              ', )
    header = header + ('C15 d. No 3200-byte Extended Textual Header                                     ', )
    header = header + ('C16                                                                             ', )
    header = header + ('C17                                                                             ', )
    header = header + ('C18                                                                             ', )
    header = header + ('C19                                                                             ', )
    header = header + ('C20                                                                             ', )
    header = header + ('C21 Key Header Information:                                                     ', )
    header = header + ('C22 a. Inline No. at Bytes 9 & 189                                              ', )
    header = header + ('C23 b. Crossline No. at Bytes 21 & 193                                          ', )
    header = header + ('C24 c. X Coordinate at Bytee 73 & 181                                           ', )
    header = header + ('C25 d. Y Coordinate at Bytes 77 & 185                                           ', )
    header = header + ('C26 e. Number of Samples per Trace at Byte 115                                  ', )
    header = header + ('C27 f. Sampling Interval in Microseconds at Byte 117                            ', )
    header = header + ('C28                                                                             ', )
    header = header + ('C29                                                                             ', )
    header = header + ('C30                                                                             ', )
    header = header + ('C31                                                                             ', )
    header = header + ('C32                                                                             ', )
    header = header + ('C33                                                                             ', )
    header = header + ('C34                                                                             ', )
    header = header + ('C35                                                                             ', )
    header = header + ('C36                                                                             ', )
    header = header + ('C37                                                                             ', )
    header = header + ('C38                                                                             ', )
    header = header + ('C39                                                                             ', )
    header = header + ('C40 End of Textual Header                                                       ', )
    return header


def createSegyBinaryHeader(znum, zstep):
    """
    Create 400-byte Segy-Y binary header

    Args:
        znum:   number of samples per trace. (offset=3221)
        zstep:  sample interval in millisecond. (offset=3217)

    Returns:
        header: Binary header information stored as class BinaryReelHeader

    Note:
        Negative z is used in the vertical direction
        IBM floating is used as data format [1]
    """
    if znum <= 0:
        vis_msg.print('ERROR in createSegyBinaryHeader: Positive num of samples per trace expected', type='error')
        sys.exit()
    if zstep >= 0:
        vis_msg.print('ERROR in createSegyBinaryHeader: Negative sample interval in milliseconds (ms) expected', type='error')
        sys.exit()
    header = BinaryReelHeader()
    header.num_samples = znum
    header.sample_interval = -zstep * 1000
    header.data_sample_format = 1
    header.format_revision_num = 256
    header.fixed_length_trace_flag = 1
    header.num_extended_textual_headers = 0
    return header


def createSegyTraceHeader(inlidx, xlidx, xcoor, ycoor, znum, zstep, zlag):
    """
    Create 240-byte Seg-Y trace header

    Args:
        inlidx: inline number. (offset = 9 and 189)
        xlidx:  crossline number. (offset = 21 and 193)
        xcoor:  x-coordinate (offset = 73 and 181)
        ycoor:  y-coordinate (offset = 77 and 185)
        znum:   number of samples per trace. (offset = 115)
        zstep:  sample interval in millisecond. (offset = 117)
        zlag:   vertical z lag-time in millisecond. (offset = 105 and 109)

    Return:
        header: Trace header information stored as class TraceHeaderRev1

    Note:
        Negative z is used in the vertical direction
    """
    if inlidx < 0:
        vis_msg.print('ERROR in createSegyTraceHeader: Non-negative inline number expected', type='error')
        sys.exit()
    if xlidx < 0:
        vis_msg.print('ERROR in createSegyTraceHeader: Non-negative crossline number expected', type='error')
        sys.exit()
    if znum <= 0:
        vis_msg.print('ERROR in createSegyTraceHeader: Positive num of samples per trace expected', type='error')
        sys.exit()
    if zstep >= 0:
        vis_msg.print('ERROR in createSegyTraceHeader: Negative sample interval in milliseconds (ms) expected', type='error')
        sys.exit()
    if zlag > 0:
        vis_msg.print('ERROR in createSegyTraceHeader: Non-positive vertical lag-time in millisecond (ms) expected', type='error')
        sys.exit()
    header = TraceHeaderRev1()
    header.field_record_num = inlidx
    header.ensemble_num = xlidx
    header.source_x = xcoor
    header.source_y = ycoor
    header.lag_time_a = zlag
    header.delay_recording_time = -zlag
    header.num_samples = znum
    header.sample_interval = -zstep * 1000
    header.cdp_x = xcoor
    header.cdp_y = ycoor
    header.inline_number = inlidx
    header.crossline_number = xlidx
    return header


def defSegyTraceHeaderFormat(x_byte=181, y_byte=185, inl_byte=189, xl_byte=193):
    """
    Define trace hearder format with the given keywords

    Args:
        x_byte:     byte of x coordinate. Default is 181
        y_byte:     byte of y coordinate. Default is 185
        inl_byte:   byte of inline number. Default is 189
        xl_byte:    byte of crossline number. Default is 193

    Return:
        The defined trace header format
    """

    class SegyTraceHeaderFormat(TraceHeaderRev1):
        cdp_x = field(Int32,
          offset=x_byte, default=0, documentation='X coordinate of ensemble (CDP) position of this trace. The coordinate reference system should be identified through an extended header Location Data stanza. The xy_scalar field applies to this value.')
        cdp_y = field(Int32,
          offset=y_byte, default=0, documentation='Y coordinate of ensemble (CDP) position of this trace. The coordinate reference system should be identified through an extended header Location Data stanza. The xy_scalar field applies to this value.')
        inline_number = field(Int32,
          offset=inl_byte, default=0, documentation='In-line number for 3-D poststack data. If one in-line per SEG Y file is being recorded, this value should be the same for all traces in the file and the same value will be recorded in bytes 3205-3208 of the Binary File Header.')
        crossline_number = field(Int32,
          offset=xl_byte, default=0, documentation='Cross-line number for 3-D poststack data. This will typically be the same value as the ensemble (CDP) number in Trace Header ensemble_num field, but this does not have to be the case.')

    return SegyTraceHeaderFormat


def readSegyTextualHeader(segyfile, encoding=None):
    """
    Read textual header from a segy file

    Args:
        segyfile:   segy file
        encoding:   encoding

    Return:
        A tuple of forty Unicode strings containing the transcoded header data
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSegyTextualHeader: ' + segyfile + ' not found'), type='error')
        sys.exit()
    with open(segyfile, 'rb') as (sid):
        if encoding is None:
            encoding = syreader.guess_textual_header_encoding(sid)
        header = syreader.read_textual_reel_header(sid, encoding=encoding)
    return header


def readSegyBinaryHeader(segyfile, endian='>'):
    """
    Read binary header from a segy file

    Args:
        segyfile:   segy file
        endian:     endian. Default is '>'

    Return:
        A binary header object (defined in segpy)
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSegyBinaryHeader: ' + segyfile + ' not found'), type='error')
        sys.exit()
    with open(segyfile, 'rb') as (sid):
        header = syreader.read_binary_reel_header(sid, endian=endian)
    return header


def readSegyTraceHeader(segyfile, traceidx=0, traceheaderformat=TraceHeaderRev1, endian='>'):
    """
    Read trace header at a given trace from a segy file

    Args:
        segyfile:           segy file
        traceidx:           index of the target trace. Default is 0
        traceheaderformat:  trace header format. Default is TraceHeaderRev1
        endian:             endian. Default is '>'

    Return:
        A trace header object (defined in segpy)
    """
    if os.path.isfile(segyfile) == False:
        vis_msg.print(('ERROR in readSegyTraceHeader: ' + segyfile + ' not found'), type='error')
        sys.exit()
    traceheaderpacker = sypacker.HeaderPacker(traceheaderformat, endian)
    pos = np.int64(3600)
    dataformat = np.array([4, 4, 2, 4, 4, 0, 0, 1])
    with open(segyfile, 'rb') as (sid):
        databyte = syreader.read_binary_reel_header(sid, endian=endian)
        databyte = dataformat[(databyte.data_sample_format - 1)]
        for i in range(traceidx):
            header = syreader.read_trace_header(sid, trace_header_packer=traceheaderpacker, pos=pos)
            pos = pos + 240 + header.num_samples * databyte

        header = syreader.read_trace_header(sid, trace_header_packer=traceheaderpacker, pos=pos)
    return header


class inputoutput:
    readSeisInfoFromSegy = readSeisInfoFromSegy
    readSeisDataFromSegy = readSeisDataFromSegy
    readSeis2DMatFromSegyWithInfo = readSeis2DMatFromSegyWithInfo
    readSeis3DMatFromSegyWithInfo = readSeis3DMatFromSegyWithInfo
    readSeis2DMatFromSegyNoInfo = readSeis2DMatFromSegyNoInfo
    readSeis3DMatFromSegyNoInfo = readSeis3DMatFromSegyNoInfo
    writeSeis2DMatToSegyWithRef = writeSeis2DMatToSegyWithRef
    writeSeis3DMatToSegyWithRef = writeSeis3DMatToSegyWithRef
    writeSeis2DMatToSegyNoRef = writeSeis2DMatToSegyNoRef
    writeSeis3DMatToSegyNoRef = writeSeis3DMatToSegyNoRef
    createSegyTextualHeader = createSegyTextualHeader
    createSegyBinaryHeader = createSegyBinaryHeader
    createSegyTraceHeader = createSegyTraceHeader
    defSegyTraceHeaderFormat = defSegyTraceHeaderFormat
    readSegyTextualHeader = readSegyTextualHeader
    readSegyBinaryHeader = readSegyBinaryHeader
    readSegyTraceHeader = readSegyTraceHeader