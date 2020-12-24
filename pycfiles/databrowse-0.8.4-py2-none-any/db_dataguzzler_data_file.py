# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_dataguzzler_data_file\db_dataguzzler_data_file.py
# Compiled at: 2018-09-22 17:12:57
""" plugins/renderers/db_dataguzzler.py - Default Renderer - Basic Output for Any Dataguzzler File """
import os, os.path, platform
from lxml import etree
from databrowse.support.renderer_support import renderer_class
import magic, dg_file as dgf, dg_eval as dge, dg_metadata as dgm, struct
from scipy import io as sio
import numpy, tempfile, subprocess
from PIL import Image
import matplotlib
BACKEND = 'Agg'
if matplotlib.get_backend().lower() != BACKEND.lower():
    matplotlib.use(BACKEND)
import matplotlib.pyplot as plt
dgf_nestedchunks = set(['DATAGUZZ', 'GUZZNWFM', 'GUZZWFMD', 'METADATA', 'METDATUM', 'SNAPSHOT', 'SNAPSHTS', 'VIBRDATA', 'VIBFCETS', 'VIBFACET'])
dgf_stringchunks = set(['WAVENAME', 'METDNAME', 'METDSTRV'])
dgf_int64chunks = set(['METDINTV'])
dgf_float64chunks = set(['METDDBLV'])

class db_dataguzzler_data_file(renderer_class):
    """ Default Renderer - Basic Output for Any Dataguzzler File """
    _namespace_uri = 'http://thermal.cnde.iastate.edu/dataguzzler'
    _namespace_local = 'dg'
    _default_content_mode = 'full'
    _default_style_mode = 'examine_file_contents'
    _default_recursion_depth = 2

    def dumpxmlchunk(self, dgfh, nestdepth=-1):
        ellist = []
        Chunk = dgf.nextchunk(dgfh)
        while Chunk:
            newel = etree.Element('{%s}%s' % (self._namespace_uri, Chunk.Name), nsmap=self.nsmap)
            if Chunk.Name in dgf_nestedchunks:
                if nestdepth > 0:
                    nestedchunks = self.dumpxmlchunk(dgfh, nestdepth - 1)
                    for nestedchunk in nestedchunks:
                        newel.append(nestedchunk)

                else:
                    nestedchunks = self.dumpxmlchunk(dgfh, -1)
                    for nestedchunk in nestedchunks:
                        newel.append(nestedchunk)

            elif Chunk.Name in dgf_stringchunks:
                newel.text = dgf.readdata(dgfh, Chunk.ChunkLen)
            elif Chunk.Name in dgf_int64chunks:
                textdata = ''
                for cnt in range(Chunk.ChunkLen / 8):
                    textdata += '%d\n' % struct.unpack('@Q', dgf.readdata(dgfh, 8))

                newel.text = textdata
            elif Chunk.Name in dgf_float64chunks:
                textdata = ''
                for cnt in range(Chunk.ChunkLen / 8):
                    textdata += '%.10g\n' % struct.unpack('@d', dgf.readdata(dgfh, 8))

                newel.text = textdata
            elif Chunk.Name == 'WFMDIMNS':
                length = struct.unpack('@Q', dgf.readdata(dgfh, 8))[0]
                ndim = struct.unpack('@Q', dgf.readdata(dgfh, 8))[0]
                dimlen = numpy.zeros(ndim, dtype='Q')
                for dimcnt in range(ndim):
                    dimlen[dimcnt] = struct.unpack('@Q', dgf.readdata(dgfh, 8))[0]

                newel.text = str(length) + '\n' + str(ndim) + '\n' + ('\n').join(str(dimcnt) for dimcnt in dimlen) + '\n'
                if ndim == 1 and dimlen[0] == 1:
                    dgf.chunkdone(dgfh, None)
                    ellist.append(newel)
                    Chunk = dgf.nextchunk(dgfh)
                    if Chunk.Name in ('DATARRYF', 'DATARRYD'):
                        newel = etree.Element('{%s}%s' % (self._namespace_uri, 'DATASVAL'), nsmap=self.nsmap)
                        if Chunk.Name == 'DATARRYF':
                            dtype = 'f'
                            dsize = 4
                        elif Chunk.Name == 'DATARRYD':
                            dtype = 'd'
                            dsize = 8
                        data = numpy.fromstring(dgf.readdata(dgfh, dsize * long(length)), dtype=dtype).reshape(dimlen, order='F')
                        newel.text = str(data[0])
            else:
                newel.text = '%s\n' % self.ConvertUserFriendlySize(Chunk.ChunkLen)
            dgf.chunkdone(dgfh, None)
            Chunk = dgf.nextchunk(dgfh)
            ellist.append(newel)

        return ellist

    def GetDataguzzlerWaveformDgzFile(self):
        dgfh = dgf.open(self._fullpath)
        chunk = dgf.nextchunk(dgfh)
        waveformname = ''
        if chunk.Name in ('SNAPSHTS', 'SNAPSHOT'):
            if 'snapshot' not in self._web_support.req.form:
                snapshotnumber = 1
            else:
                snapshotnumber = int(self._web_support.req.form['snapshot'].value)
            if 'waveform' not in self._web_support.req.form:
                raise self.RendererException('Waveform Name Must Be Specified')
            else:
                waveformname = self._web_support.req.form['waveform'].value
            if chunk.Name == 'SNAPSHTS':
                count = 0
                while count != snapshotnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'SNAPSHOT':
                        count = count + 1
                    if count == snapshotnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

            elif chunk.Name == 'SNAPSHOT':
                if 'snapshot' in self._web_support.req.form and int(self._web_support.req.form['snapshot'].value) != 1:
                    raise self.RendererException('Looking for SNAPSHTS but found SNAPSHOT')
            filename = 'SNAPSHOT' + str(snapshotnumber) + '_' + waveformname
            mdata, wfms, wfmdict = dgf.procSNAPSHOT(dgfh, memmapok=True)
            waveform = wfmdict[waveformname]
            if 'IRstack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                mean = wfmdict['IRstack'].data[:, :, 0].mean(dtype=numpy.float64)
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(mean)))
            if 'DiffStack' in wfmdict and wfmdict['DiffStack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFit' in wfmdict and wfmdict['VibroFit'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFitImg' in wfmdict and wfmdict['VibroFitImg'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'ProcExpr' in waveform.MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(waveform)
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                waveform = dge.eval(waveform, wfmdict, ndim, rgba=False, *inivalstepdimlen)
        elif chunk.Name == 'GUZZWFMD':
            if 'waveform' not in self._web_support.req.form:
                waveformnumber = 1
            else:
                waveformnumber = int(self._web_support.req.form['waveform'].value)
            count = 1
            if count != waveformnumber:
                dgf.chunkdone(dgfh, chunk)
            while count != waveformnumber:
                chunk = dgf.nextchunk(dgfh)
                if chunk.Name == 'GUZZWFMD':
                    count = count + 1
                if count == waveformnumber:
                    break
                else:
                    dgf.chunkdone(dgfh, chunk)

            filename = 'WAVEFORM' + str(waveformnumber)
            waveform = dgf.procGUZZWFMD(dgfh, None)
            waveformname = 'Unnamed Waveform ' + str(waveformnumber)
        else:
            raise self.RendererException('Unexpected ' + chunk.Name + ' Chunk Found')
        outputfile = self.getCacheFileName(filename, 'dgz')
        outfile = dgf.creat(outputfile)
        if not outfile:
            raise self.RendererException('Error: could not open "%s" for write' % outputfile)
        dgf.writewfm(outfile, waveform)
        dgf.close(outfile)
        dgf.rewind(dgfh)
        dgf.close(dgfh)
        size = os.path.getsize(self.getCacheFileName(filename, 'dgz'))
        return (self.getCacheFileHandler('rb', filename, 'dgz'), size)

    def GetDataguzzlerWaveformCsvFile(self):
        dgfh = dgf.open(self._fullpath)
        chunk = dgf.nextchunk(dgfh)
        waveformname = ''
        if chunk.Name in ('SNAPSHTS', 'SNAPSHOT'):
            if 'snapshot' not in self._web_support.req.form:
                snapshotnumber = 1
            else:
                snapshotnumber = int(self._web_support.req.form['snapshot'].value)
            if 'waveform' not in self._web_support.req.form:
                raise self.RendererException('Waveform Name Must Be Specified')
            else:
                waveformname = self._web_support.req.form['waveform'].value
            if chunk.Name == 'SNAPSHTS':
                count = 0
                while count != snapshotnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'SNAPSHOT':
                        count = count + 1
                    if count == snapshotnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

            elif chunk.Name == 'SNAPSHOT':
                if 'snapshot' in self._web_support.req.form and int(self._web_support.req.form['snapshot'].value) != 1:
                    raise self.RendererException('Looking for SNAPSHTS but found SNAPSHOT')
            filename = 'SNAPSHOT' + str(snapshotnumber) + '_' + waveformname
            mdata, wfms, wfmdict = dgf.procSNAPSHOT(dgfh, memmapok=True)
            waveform = wfmdict[waveformname]
            if 'IRstack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                mean = wfmdict['IRstack'].data[:, :, 0].mean(dtype=numpy.float64)
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(mean)))
            if 'DiffStack' in wfmdict and wfmdict['DiffStack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFit' in wfmdict and wfmdict['VibroFit'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFitImg' in wfmdict and wfmdict['VibroFitImg'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'ProcExpr' in waveform.MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(waveform)
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                waveform = dge.eval(waveform, wfmdict, ndim, rgba=False, *inivalstepdimlen)
        elif chunk.Name == 'GUZZWFMD':
            if 'waveform' not in self._web_support.req.form:
                waveformnumber = 1
            else:
                waveformnumber = int(self._web_support.req.form['waveform'].value)
            count = 1
            if count != waveformnumber:
                dgf.chunkdone(dgfh, chunk)
            while count != waveformnumber:
                chunk = dgf.nextchunk(dgfh)
                if chunk.Name == 'GUZZWFMD':
                    count = count + 1
                if count == waveformnumber:
                    break
                else:
                    dgf.chunkdone(dgfh, chunk)

            filename = 'WAVEFORM' + str(waveformnumber)
            waveform = dgf.procGUZZWFMD(dgfh, None)
            waveformname = 'Unnamed Waveform ' + str(waveformnumber)
        else:
            raise self.RendererException('Unexpected ' + chunk.Name + ' Chunk Found')
        f = self.getCacheFileHandler('wb', filename, 'csv')
        numpy.savetxt(f, waveform.data, delimiter=',')
        f.close()
        dgf.rewind(dgfh)
        dgf.close(dgfh)
        size = os.path.getsize(self.getCacheFileName(filename, 'csv'))
        return (self.getCacheFileHandler('rb', filename, 'csv'), size)

    def GetDataguzzlerWaveformMatFile(self):
        dgfh = dgf.open(self._fullpath)
        chunk = dgf.nextchunk(dgfh)
        waveformname = ''
        if chunk.Name in ('SNAPSHTS', 'SNAPSHOT'):
            if 'snapshot' not in self._web_support.req.form:
                snapshotnumber = 1
            else:
                snapshotnumber = int(self._web_support.req.form['snapshot'].value)
            if 'waveform' not in self._web_support.req.form:
                raise self.RendererException('Waveform Name Must Be Specified')
            else:
                waveformname = self._web_support.req.form['waveform'].value
            if chunk.Name == 'SNAPSHTS':
                count = 0
                while count != snapshotnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'SNAPSHOT':
                        count = count + 1
                    if count == snapshotnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

            elif chunk.Name == 'SNAPSHOT':
                if 'snapshot' in self._web_support.req.form and int(self._web_support.req.form['snapshot'].value) != 1:
                    raise self.RendererException('Looking for SNAPSHTS but found SNAPSHOT')
            filename = 'SNAPSHOT' + str(snapshotnumber) + '_' + waveformname
            mdata, wfms, wfmdict = dgf.procSNAPSHOT(dgfh, memmapok=True)
            waveform = wfmdict[waveformname]
            if 'IRstack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                mean = wfmdict['IRstack'].data[:, :, 0].mean(dtype=numpy.float64)
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(mean)))
            if 'DiffStack' in wfmdict and wfmdict['DiffStack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFit' in wfmdict and wfmdict['VibroFit'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFitImg' in wfmdict and wfmdict['VibroFitImg'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'ProcExpr' in waveform.MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(waveform)
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                waveform = dge.eval(waveform, wfmdict, ndim, rgba=False, *inivalstepdimlen)
        elif chunk.Name == 'GUZZWFMD':
            if 'waveform' not in self._web_support.req.form:
                waveformnumber = 1
            else:
                waveformnumber = int(self._web_support.req.form['waveform'].value)
            count = 1
            if count != waveformnumber:
                dgf.chunkdone(dgfh, chunk)
            while count != waveformnumber:
                chunk = dgf.nextchunk(dgfh)
                if chunk.Name == 'GUZZWFMD':
                    count = count + 1
                if count == waveformnumber:
                    break
                else:
                    dgf.chunkdone(dgfh, chunk)

            filename = 'WAVEFORM' + str(waveformnumber)
            waveform = dgf.procGUZZWFMD(dgfh, None)
            waveformname = 'Unnamed Waveform ' + str(waveformnumber)
        else:
            raise self.RendererException('Unexpected ' + chunk.Name + ' Chunk Found')
        f = self.getCacheFileHandler('wb', filename, 'mat')
        sio.savemat(f, {'waveform': waveform})
        f.close()
        dgf.rewind(dgfh)
        dgf.close(dgfh)
        size = os.path.getsize(self.getCacheFileName(filename, 'mat'))
        return (self.getCacheFileHandler('rb', filename, 'mat'), size)

    def GetDataguzzlerWaveformVideo(self):
        dgfh = dgf.open(self._fullpath)
        chunk = dgf.nextchunk(dgfh)
        waveformname = ''
        rgbawaveform = None
        if chunk.Name in ('SNAPSHTS', 'SNAPSHOT'):
            if 'snapshot' not in self._web_support.req.form:
                snapshotnumber = 1
            else:
                snapshotnumber = int(self._web_support.req.form['snapshot'].value)
            if 'waveform' not in self._web_support.req.form:
                raise self.RendererException('Waveform Name Must Be Specified')
            else:
                waveformname = self._web_support.req.form['waveform'].value
            if chunk.Name == 'SNAPSHTS':
                count = 0
                while count != snapshotnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'SNAPSHOT':
                        count = count + 1
                    if count == snapshotnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

            elif chunk.Name == 'SNAPSHOT':
                if 'snapshot' in self._web_support.req.form and int(self._web_support.req.form['snapshot'].value) != 1:
                    raise self.RendererException('Looking for SNAPSHTS but found SNAPSHOT')
            filename = 'SNAPSHOT' + str(snapshotnumber) + '_' + waveformname
            mdata, wfms, wfmdict = dgf.procSNAPSHOT(dgfh, memmapok=True)
            waveform = wfmdict[waveformname]
            if 'IRstack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                mean = wfmdict['IRstack'].data[:, :, 0].mean(dtype=numpy.float64)
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(mean)))
            if 'DiffStack' in wfmdict and wfmdict['DiffStack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFit' in wfmdict and wfmdict['VibroFit'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'VibroFitImg' in wfmdict and wfmdict['VibroFitImg'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeOffset', float(1)))
            if 'ProcExpr' in waveform.MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(waveform)
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                waveform = dge.eval(waveform, wfmdict, ndim, rgba=False, *inivalstepdimlen)
            rgbawaveform = None
            if 'ProcRGBA' in wfmdict[waveformname].MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(wfmdict[waveformname])
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                rgbawaveform = dge.eval(wfmdict[waveformname], wfmdict, ndim, rgba=True, *inivalstepdimlen)
        else:
            if chunk.Name == 'GUZZWFMD':
                if 'waveform' not in self._web_support.req.form:
                    waveformnumber = 1
                else:
                    waveformnumber = int(self._web_support.req.form['waveform'].value)
                count = 1
                if count != waveformnumber:
                    dgf.chunkdone(dgfh, chunk)
                while count != waveformnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'GUZZWFMD':
                        count = count + 1
                    if count == waveformnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

                filename = 'WAVEFORM' + str(waveformnumber)
                waveform = dgf.procGUZZWFMD(dgfh, None)
                waveformname = 'Unnamed Waveform ' + str(waveformnumber)
            else:
                raise self.RendererException('Unexpected ' + chunk.Name + ' Chunk Found')
            ndim, dimlen, inival, step, bases = dge.geom(waveform)
            coord = []
            units = []
            for i in range(ndim):
                try:
                    coord.append(waveform.MetaData[('ProcCoord' + str(i + 1))].Value if 'ProcCoord' + str(i + 1) in waveform.MetaData else waveform.MetaData[('Coord' + str(i + 1))].Value)
                    units.append(waveform.MetaData[('ProcUnits' + str(i + 1))].Value if 'ProcUnits' + str(i + 1) in waveform.MetaData else waveform.MetaData[('Units' + str(i + 1))].Value)
                except:
                    pass

            try:
                coord.append(waveform.MetaData['ProcAmplCoord'].Value if 'ProcAmplCoord' in waveform.MetaData else waveform.MetaData['AmplCoord'].Value)
                units.append(waveform.MetaData['ProcAmplUnits'].Value if 'ProcAmplUnits' in waveform.MetaData else waveform.MetaData['AmplUnits'].Value)
            except:
                pass

            if waveformname == 'VibroFitImg':
                cmap = 'hsv'
            else:
                cmap = 'hot'
            filelist = []
            if len(waveform.data.shape) == 3:
                tmpdir = tempfile.mkdtemp('', 'db_dataguzzler_video')
                loop = range(dimlen[2])
                extent = [inival[0], waveform.data.shape[0] * step[0] + inival[0], inival[1], waveform.data.shape[1] * step[1] + inival[1]]
                vmin = waveform.data.min()
                vmax = waveform.data.max()
                for framenumber in loop:
                    imagefilename = filename + '_%5.5d' % framenumber
                    if 'Coord3' in waveform.MetaData:
                        t = numpy.arange(0, waveform.data.shape[2], dtype='d') * step[2] + inival[2]
                        title = waveformname + ' (' + coord[2] + ': ' + str(t[framenumber]) + ' ' + units[2] + ')'
                    else:
                        title = waveformname + ' (Frame ' + str(framenumber) + ')'
                    plt.imshow(waveform.data[:, :, framenumber].T, cmap=cmap, origin='lower', extent=extent, vmin=vmin, vmax=vmax)
                    cb = plt.colorbar()
                    cb.set_label(coord[(-1)] + ' (' + units[(-1)] + ')')
                    if rgbawaveform is not None:
                        RGBAdat = rgbawaveform.data[:, :, framenumber].transpose().tostring()
                        sz = len(RGBAdat)
                        RGBAmat = numpy.fromstring(RGBAdat, 'B').reshape(sz / 4, 4)
                        RGBAmat2 = RGBAmat.copy()
                        RGBAmat2[:, 0] = RGBAmat[:, 3]
                        RGBAmat2[:, 1] = RGBAmat[:, 2]
                        RGBAmat2[:, 2] = RGBAmat[:, 1]
                        RGBAmat2[:, 3] = RGBAmat[:, 0]
                        plt.imshow(Image.fromstring('RGBA', (rgbawaveform.data.shape[0], rgbawaveform.data.shape[1]), RGBAmat2.tostring()), origin='lower', extent=extent)
                    plt.title(title)
                    plt.xlabel(coord[0] + ' (' + units[0] + ')')
                    plt.ylabel(coord[1] + ' (' + units[1] + ')')
                    plt.savefig(os.path.join(tmpdir, imagefilename + '.png'))
                    filelist.append(os.path.join(tmpdir, imagefilename + '.png'))
                    plt.clf()

            else:
                raise self.RendererException('Only Three Dimensional Waveforms May Be Converted To Video')
            dgf.rewind(dgfh)
            dgf.close(dgfh)
            cachefile = self.getCacheFileName(filename, 'avi')
            if dimlen[2] > 10:
                fps = 1.0 / float(step[2]) * 0.1
            else:
                fps = float(1.0)
            myproc = subprocess.Popen(('/usr/local/bin/mencoder', '-fps', '%g' % fps, '-ovc', 'lavc', '-lavcopts', 'vcodec=ljpeg', 'mf://%s/*.png' % tmpdir, '-o', '%s' % os.path.join(tmpdir, filename + '.avi')))
            os.waitpid(myproc.pid, 0)
            filelist.append(os.path.join(tmpdir, filename + '.avi'))
            myproc = subprocess.Popen(('/usr/local/bin/ffmpeg', '-i', '%s' % os.path.join(tmpdir, filename + '.avi'), '-vcodec', 'mjpeg', '-r', '%g' % fps, '-b', '2000k', '-y', '%s' % cachefile))
            os.waitpid(myproc.pid, 0)
            for name in filelist:
                os.remove(name)

        os.rmdir(tmpdir)
        size = os.path.getsize(self.getCacheFileName(filename, 'avi'))
        return (self.getCacheFileHandler('rb', filename, 'avi'), size)

    def GetDataguzzlerWaveformImage(self):
        dgfh = dgf.open(self._fullpath)
        chunk = dgf.nextchunk(dgfh)
        waveformname = ''
        rgbawaveform = None
        if chunk.Name in ('SNAPSHTS', 'SNAPSHOT'):
            if 'snapshot' not in self._web_support.req.form:
                snapshotnumber = 1
            else:
                snapshotnumber = int(self._web_support.req.form['snapshot'].value)
            if 'waveform' not in self._web_support.req.form:
                raise self.RendererException('Waveform Name Must Be Specified')
            else:
                waveformname = self._web_support.req.form['waveform'].value
            if chunk.Name == 'SNAPSHTS':
                count = 0
                while count != snapshotnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'SNAPSHOT':
                        count = count + 1
                    if count == snapshotnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

            elif chunk.Name == 'SNAPSHOT':
                if 'snapshot' in self._web_support.req.form and int(self._web_support.req.form['snapshot'].value) != 1:
                    raise self.RendererException('Looking for SNAPSHTS but found SNAPSHOT')
            filename = 'SNAPSHOT' + str(snapshotnumber) + '_' + waveformname
            mdata, wfms, wfmdict = dgf.procSNAPSHOT(dgfh, memmapok=True)
            waveform = wfmdict[waveformname]
            ndim, dimlen, inival, step, bases = dge.geom(waveform)
            ROIX1 = dgm.GetMetaDatumWIDbl(waveform, 'ROIX1', -1000000000000.0)
            ROIX2 = dgm.GetMetaDatumWIDbl(waveform, 'ROIX2', 1000000000000.0)
            ROIY1 = dgm.GetMetaDatumWIDbl(waveform, 'ROIY1', -1000000000000.0)
            ROIY2 = dgm.GetMetaDatumWIDbl(waveform, 'ROIY2', 1000000000000.0)
            if ROIX1 != -1000000000000.0 and ROIX2 != 1000000000000.0 and ROIY1 != -1000000000000.0 and ROIY2 != 1000000000000.0:
                ROICOORDX1 = int((ROIX1 - inival[0]) * (1 / step[0]))
                ROICOORDX2 = int((ROIX2 - inival[0]) * (1 / step[0]))
                ROICOORDY1 = int((ROIY1 - inival[1]) * (1 / step[1]))
                ROICOORDY2 = int((ROIY2 - inival[1]) * (1 / step[1]))
                if ROICOORDY1 < ROICOORDY2:
                    ROICOORDY1 = int((ROIY2 - inival[1]) * (1 / step[1]))
                    ROICOORDY2 = int((ROIY1 - inival[1]) * (1 / step[1]))
            else:
                ROICOORDX1 = None
                ROICOORDX2 = None
                ROICOORDY1 = None
                ROICOORDY2 = None
            if 'IRstack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                if ROICOORDX1 is not None and ROICOORDX2 is not None and ROICOORDY1 is not None and ROICOORDY2 is not None:
                    mean = wfmdict['IRstack'].data[ROICOORDX1:ROICOORDX2, ROICOORDY2:ROICOORDY1, 0].mean(dtype=numpy.float64)
                else:
                    mean = wfmdict['IRstack'].data[:, :, 0].mean(dtype=numpy.float64)
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['IRstack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(mean)))
            if 'DiffStack' in wfmdict and wfmdict['IRstack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(1)))
                dgm.AddMetaDatumWI(wfmdict['DiffStack'], dgm.CreateMetaDatumDbl('ScopeOffset', float(0.5)))
            if 'VibroFit' in wfmdict and wfmdict['IRstack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(1)))
                dgm.AddMetaDatumWI(wfmdict['VibroFit'], dgm.CreateMetaDatumDbl('ScopeOffset', float(0)))
            if 'VibroFitImg' in wfmdict and wfmdict['IRstack'].data.size > 1:
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeUnitsPerDiv', float(2)))
                dgm.AddMetaDatumWI(wfmdict['VibroFitImg'], dgm.CreateMetaDatumDbl('ScopeOffset', float(0)))
            if 'ProcExpr' in waveform.MetaData:
                ndim, dimlen, inival, step, bases = dge.geom(waveform)
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                waveform = dge.eval(waveform, wfmdict, ndim, rgba=False, *inivalstepdimlen)
            rgbawaveform = None
            if 'ProcRGBA' in wfmdict[waveformname].MetaData and waveformname != 'DiffStack':
                ndim, dimlen, inival, step, bases = dge.geom(wfmdict[waveformname])
                inivalstepdimlen = []
                for i in range(ndim):
                    inivalstepdimlen.append(inival[i])
                    inivalstepdimlen.append(step[i])
                    inivalstepdimlen.append(dimlen[i])

                rgbawaveform = dge.eval(wfmdict[waveformname], wfmdict, ndim, rgba=True, *inivalstepdimlen)
        else:
            if chunk.Name == 'GUZZWFMD':
                if 'waveform' not in self._web_support.req.form:
                    waveformnumber = 1
                else:
                    waveformnumber = int(self._web_support.req.form['waveform'].value)
                count = 1
                if count != waveformnumber:
                    dgf.chunkdone(dgfh, chunk)
                while count != waveformnumber:
                    chunk = dgf.nextchunk(dgfh)
                    if chunk.Name == 'GUZZWFMD':
                        count = count + 1
                    if count == waveformnumber:
                        break
                    else:
                        dgf.chunkdone(dgfh, chunk)

                filename = 'WAVEFORM' + str(waveformnumber)
                waveform = dgf.procGUZZWFMD(dgfh, None)
                waveformname = 'Unnamed Waveform ' + str(waveformnumber)
            else:
                raise self.RendererException('Unexpected ' + chunk.Name + ' Chunk Found')
            ndim, dimlen, inival, step, bases = dge.geom(waveform)
            coord = []
            units = []
            for i in range(ndim):
                try:
                    coord.append(waveform.MetaData[('ProcCoord' + str(i + 1))].Value if 'ProcCoord' + str(i + 1) in waveform.MetaData else waveform.MetaData[('Coord' + str(i + 1))].Value)
                    units.append(waveform.MetaData[('ProcUnits' + str(i + 1))].Value if 'ProcUnits' + str(i + 1) in waveform.MetaData else waveform.MetaData[('Units' + str(i + 1))].Value)
                except:
                    pass

            try:
                coord.append(waveform.MetaData['ProcAmplCoord'].Value if 'ProcAmplCoord' in waveform.MetaData else waveform.MetaData['AmplCoord'].Value)
                units.append(waveform.MetaData['ProcAmplUnits'].Value if 'ProcAmplUnits' in waveform.MetaData else waveform.MetaData['AmplUnits'].Value)
            except:
                pass

        if waveformname == 'VibroFitImg':
            cmap = 'hsv'
        else:
            cmap = 'hot'
        if len(waveform.data.shape) == 3:
            if 'frame' not in self._web_support.req.form:
                framenumber = 0
            else:
                framenumber = int(self._web_support.req.form['frame'].value)
            filename = filename + '_' + str(framenumber)
            extent = [inival[0], waveform.data.shape[0] * step[0] + inival[0], inival[1], waveform.data.shape[1] * step[1] + inival[1]]
            if ROICOORDX1 is not None and ROICOORDX2 is not None and ROICOORDY1 is not None and ROICOORDY2 is not None:
                if waveformname == 'DiffStack':
                    vmin = 0
                else:
                    vmin = waveform.data[ROICOORDX1:ROICOORDX2, ROICOORDY2:ROICOORDY1, :].min()
                vmax = waveform.data[ROICOORDX1:ROICOORDX2, ROICOORDY2:ROICOORDY1, :].max()
            else:
                if waveformname == 'DiffStack':
                    vmin = 0
                else:
                    vmin = waveform.data.min()
                vmax = waveform.data.max()
            if 'Coord3' in waveform.MetaData:
                t = numpy.arange(0, waveform.data.shape[2], dtype='d') * step[2] + inival[2]
                title = waveformname + ' (' + coord[2] + ': ' + str(t[framenumber]) + ' ' + units[2] + ')'
            else:
                title = waveformname + ' (Frame ' + str(framenumber) + ')'
            plt.imshow(waveform.data[:, :, framenumber].T, cmap=cmap, origin='lower', extent=extent, vmin=vmin, vmax=vmax)
            cb = plt.colorbar()
            cb.set_label(coord[(-1)] + ' (' + units[(-1)] + ')')
            if rgbawaveform is not None:
                RGBAdat = rgbawaveform.data[:, :, framenumber].transpose().tostring()
                sz = len(RGBAdat)
                RGBAmat = numpy.fromstring(RGBAdat, 'B').reshape(sz / 4, 4)
                RGBAmat2 = RGBAmat.copy()
                RGBAmat2[:, 0] = RGBAmat[:, 3]
                RGBAmat2[:, 1] = RGBAmat[:, 2]
                RGBAmat2[:, 2] = RGBAmat[:, 1]
                RGBAmat2[:, 3] = RGBAmat[:, 0]
                plt.imshow(Image.fromstring('RGBA', (rgbawaveform.data.shape[0], rgbawaveform.data.shape[1]), RGBAmat2.tostring()), origin='lower', extent=extent)
            self.plotroi(waveform)
            plt.title(title)
            plt.xlabel(coord[0] + ' (' + units[0] + ')')
            plt.ylabel(coord[1] + ' (' + units[1] + ')')
        elif len(waveform.data.shape) == 2:
            extent = [
             inival[0], waveform.data.shape[0] * step[0] + inival[0], inival[1], waveform.data.shape[1] * step[1] + inival[1]]
            if ROICOORDX1 is not None and ROICOORDX2 is not None and ROICOORDY1 is not None and ROICOORDY2 is not None:
                vmin = waveform.data[ROICOORDX1:ROICOORDX2, ROICOORDY2:ROICOORDY1].min()
                vmax = waveform.data[ROICOORDX1:ROICOORDX2, ROICOORDY2:ROICOORDY1].max()
            else:
                vmin = waveform.data.min()
                vmax = waveform.data.max()
            plt.imshow(waveform.data[:, :].T, cmap=cmap, origin='lower', extent=extent, vmin=vmin, vmax=vmax)
            cb = plt.colorbar()
            cb.set_label(coord[(-1)] + ' (' + units[(-1)] + ')')
            if rgbawaveform is not None:
                RGBAdat = rgbawaveform.data[:, :].transpose().tostring()
                sz = len(RGBAdat)
                RGBAmat = numpy.fromstring(RGBAdat, 'B').reshape(sz / 4, 4)
                RGBAmat2 = RGBAmat.copy()
                RGBAmat2[:, 0] = RGBAmat[:, 3]
                RGBAmat2[:, 1] = RGBAmat[:, 2]
                RGBAmat2[:, 2] = RGBAmat[:, 1]
                RGBAmat2[:, 3] = RGBAmat[:, 0]
                plt.imshow(Image.fromstring('RGBA', (rgbawaveform.data.shape[0], rgbawaveform.data.shape[1]), RGBAmat2.tostring()), origin='lower', extent=extent)
            self.plotroi(waveform)
            plt.title(waveformname)
            plt.xlabel(coord[0] + ' (' + units[0] + ')')
            plt.ylabel(coord[1] + ' (' + units[1] + ')')
        elif len(waveform.data.shape) == 1 and waveform.data.shape[0] != 1:
            n = waveform.data.shape[0]
            x = numpy.arange(0, n, dtype='d') * step[0] + inival[0]
            y = waveform.data
            if n > 10000:
                chunksize = 1000
                numchunks = y.size // chunksize
                ychunks = y[:chunksize * numchunks].reshape((-1, chunksize))
                xchunks = x[:chunksize * numchunks].reshape((-1, chunksize))
                max_env = ychunks.max(axis=1)
                min_env = ychunks.min(axis=1)
                ycenters = ychunks.mean(axis=1)
                xcenters = xchunks.mean(axis=1)
                plt.fill_between(xcenters, min_env, max_env, edgecolor='none')
                plt.plot(xcenters, ycenters)
            else:
                plt.plot(x, y)
            plt.title(waveformname)
            plt.xlabel(coord[0] + ' (' + units[0] + ')')
            plt.ylabel(coord[(-1)] + ' (' + units[(-1)] + ')')
            plt.grid(True)
        elif len(waveform.data.shape) != 0 and waveform.data.shape[0] == 1:
            plt.plot(waveform.data, marker='o', color='b')
            plt.title(waveformname)
            if 'Coord1' in waveform.MetaData:
                plt.xlabel(coord[0] + ' (' + units[0] + ')')
            plt.ylabel(coord[(-1)] + ' (' + units[(-1)] + ')')
            plt.grid(True)
        else:
            plt.xlabel('NaN')
            plt.ylabel('NaN')
            plt.grid(True)
            plt.title('No Figure')
        f = self.getCacheFileHandler('wb', filename, 'png')
        plt.savefig(f)
        f.close()
        plt.clf()
        dgf.rewind(dgfh)
        dgf.close(dgfh)
        size = os.path.getsize(self.getCacheFileName(filename, 'png'))
        return (self.getCacheFileHandler('rb', filename, 'png'), size, 'image/png')

    def plotroi(self, waveform):
        ROIX1 = dgm.GetMetaDatumWIDbl(waveform, 'ROIX1', -1000000000000.0)
        ROIX2 = dgm.GetMetaDatumWIDbl(waveform, 'ROIX2', 1000000000000.0)
        ROIY1 = dgm.GetMetaDatumWIDbl(waveform, 'ROIY1', -1000000000000.0)
        ROIY2 = dgm.GetMetaDatumWIDbl(waveform, 'ROIY2', 1000000000000.0)
        if ROIX1 != -1000000000000.0 and ROIX2 != 1000000000000.0 and ROIY1 != -1000000000000.0 and ROIY2 != 1000000000000.0:
            xlim = plt.xlim()
            ylim = plt.ylim()
            plt.plot([ROIX1, ROIX2], [ROIY1, ROIY1], 'b-')
            plt.plot([ROIX1, ROIX2], [ROIY2, ROIY2], 'b-')
            plt.plot([ROIX1, ROIX1], [ROIY1, ROIY2], 'b-')
            plt.plot([ROIX2, ROIX2], [ROIY1, ROIY2], 'b-')
            plt.xlim(xlim)
            plt.ylim(ylim)

    def getContent(self):
        if self._caller != 'databrowse':
            return
        else:
            if self._content_mode == 'full' or self._content_mode == 'summary':
                nestdepth = -1
                if self._content_mode == 'summary':
                    nestdepth = 3
                dgfh = dgf.open(self._fullpath)
                if dgfh:
                    xmlchunk = self.dumpxmlchunk(dgfh, nestdepth=nestdepth)
                    dgf.close(dgfh)
                if len(xmlchunk) > 1:
                    xmlcontent = etree.Element('{http://thermal.cnde.iastate.edu/dataguzzler}DATAGUZZ', nsmap=self.nsmap)
                    for x in xmlchunk:
                        xmlcontent.append(x)

                else:
                    if len(xmlchunk) == 1:
                        if xmlchunk[0].xpath('local-name()') == 'GUZZWFMD':
                            xmlcontent = etree.Element('{http://thermal.cnde.iastate.edu/dataguzzler}DATAGUZZ', nsmap=self.nsmap)
                            xmlcontent.append(xmlchunk[0])
                        else:
                            xmlcontent = xmlchunk[0]
                    else:
                        raise self.RendererException('Empty Dataguzzler File')
                    extension = os.path.splitext(self._fullpath)[1][1:]
                    icon = self._handler_support.GetIcon('application/octet-stream', extension)
                    downlink = self.getURL(self._relpath, content_mode='raw', download='true')
                    imagelink = self.getURL(self._relpath, content_mode='raw', image='true')
                    matlink = self.getURL(self._relpath, content_mode='raw', matfile='true')
                    csvlink = self.getURL(self._relpath, content_mode='raw', csvfile='true')
                    dgzlink = self.getURL(self._relpath, content_mode='raw', dgzfile='true')
                    avilink = self.getURL(self._relpath, content_mode='raw', avifile='true')
                    try:
                        __import__('imp').find_module('NDI_app')
                        nditoolboxlink = self.getURL(self._relpath, content_mode='nditoolbox')
                    except ImportError:
                        nditoolboxlink = ''

                self.nsmap['dbdg'] = 'http://thermal.cnde.iastate.edu/databrowse/dataguzzler'
                xmlroot = etree.Element('{%s}dbdg' % 'http://thermal.cnde.iastate.edu/databrowse/dataguzzler', nsmap=self.nsmap, name=os.path.basename(self._relpath), resurl=self._web_support.resurl, downlink=downlink, icon=icon, imagelink=imagelink, matlink=matlink, csvlink=csvlink, dgzlink=dgzlink, avilink=avilink, nditoolboxlink=nditoolboxlink)
                xmlroot.append(xmlcontent)
                return xmlroot
            if self._content_mode == 'nditoolbox' and 'ajax' in self._web_support.req.form:
                import NDI_app
                subprocess.Popen(['python', NDI_app.__file__, self._fullpath], cwd=os.path.dirname(NDI_app.__file__))
                self._web_support.req.output = 'NDITOOlBOX Called Successfully'
                self._web_support.req.response_headers['Content-Type'] = 'text/plain'
                return [
                 self._web_support.req.return_page()]
            if self._content_mode == 'raw':
                if 'image' in self._web_support.req.form:
                    f = None
                    if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form and 'frame' in self._web_support.req.form:
                        if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value + '_' + self._web_support.req.form['frame'].value, 'png'):
                            size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value + '_' + self._web_support.req.form['frame'].value, 'png'))
                            f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value + '_' + self._web_support.req.form['frame'].value, 'png')
                            contenttype = 'image/png'
                    else:
                        if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'png'):
                                size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'png'))
                                f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'png')
                                contenttype = 'image/png'
                        elif 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('WAVEFORM' + self._web_support.req.form['waveform'].value, 'png'):
                                size = os.path.getsize(self.getCacheFileName('WAVEFORM' + self._web_support.req.form['waveform'].value, 'png'))
                                f = self.getCacheFileHandler('rb', 'WAVEFORM' + self._web_support.req.form['waveform'].value, 'png')
                                contenttype = 'image/png'
                        if f is None:
                            f, size, contenttype = self.GetDataguzzlerWaveformImage()
                        self._web_support.req.response_headers['Content-Disposition'] = 'filename=' + os.path.basename(f.name)
                        self._web_support.req.response_headers['Content-Type'] = contenttype
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
                elif 'matfile' in self._web_support.req.form:
                    f = None
                    if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form:
                        if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'mat'):
                            size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'mat'))
                            f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'mat')
                    else:
                        if 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('WAVEFORM' + self._web_support.req.form['waveform'].value, 'mat'):
                                size = os.path.getsize(self.getCacheFileName('WAVEFORM' + self._web_support.req.form['waveform'].value, 'mat'))
                                f = self.getCacheFileHandler('rb', 'WAVEFORM' + self._web_support.req.form['waveform'].value, 'mat')
                        if f is None:
                            f, size = self.GetDataguzzlerWaveformMatFile()
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f.name)
                        self._web_support.req.response_headers['Content-Type'] = 'application/octet-stream'
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
                elif 'csvfile' in self._web_support.req.form:
                    f = None
                    if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form:
                        if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'csv'):
                            size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'csv'))
                            f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'csv')
                    else:
                        if 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('WAVEFORM' + self._web_support.req.form['waveform'].value, 'csv'):
                                size = os.path.getsize(self.getCacheFileName('WAVEFORM' + self._web_support.req.form['waveform'].value, 'csv'))
                                f = self.getCacheFileHandler('rb', 'WAVEFORM' + self._web_support.req.form['waveform'].value, 'csv')
                        if f is None:
                            f, size = self.GetDataguzzlerWaveformCsvFile()
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f.name)
                        self._web_support.req.response_headers['Content-Type'] = 'text/csv'
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
                elif 'dgzfile' in self._web_support.req.form:
                    f = None
                    if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form:
                        if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'dgz'):
                            size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'dgz'))
                            f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'dgz')
                    else:
                        if 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('WAVEFORM' + self._web_support.req.form['waveform'].value, 'dgz'):
                                size = os.path.getsize(self.getCacheFileName('WAVEFORM' + self._web_support.req.form['waveform'].value, 'dgz'))
                                f = self.getCacheFileHandler('rb', 'WAVEFORM' + self._web_support.req.form['waveform'].value, 'dgz')
                        if f is None:
                            f, size = self.GetDataguzzlerWaveformDgzFile()
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f.name)
                        self._web_support.req.response_headers['Content-Type'] = 'application/x-dataguzzler-waveform'
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
                elif 'avifile' in self._web_support.req.form:
                    f = None
                    if 'snapshot' in self._web_support.req.form and 'waveform' in self._web_support.req.form:
                        if self.CacheFileExists('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'avi'):
                            size = os.path.getsize(self.getCacheFileName('SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'avi'))
                            f = self.getCacheFileHandler('rb', 'SNAPSHOT' + str(self._web_support.req.form['snapshot'].value) + '_' + self._web_support.req.form['waveform'].value, 'avi')
                    else:
                        if 'waveform' in self._web_support.req.form:
                            if self.CacheFileExists('WAVEFORM' + self._web_support.req.form['waveform'].value, 'avi'):
                                size = os.path.getsize(self.getCacheFileName('WAVEFORM' + self._web_support.req.form['waveform'].value, 'avi'))
                                f = self.getCacheFileHandler('rb', 'WAVEFORM' + self._web_support.req.form['waveform'].value, 'avi')
                        if f is None:
                            f, size = self.GetDataguzzlerWaveformVideo()
                        self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f.name)
                        self._web_support.req.response_headers['Content-Type'] = 'application/x-msvideo'
                        self._web_support.req.response_headers['Content-Length'] = str(size)
                        self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                        self._web_support.req.output_done = True
                        if 'wsgi.file_wrapper' in self._web_support.req.environ:
                            return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
                else:
                    size = os.path.getsize(self._fullpath)
                    if platform.system() is 'Windows':
                        contenttype = magic.from_file(self._fullpath, mime=True)
                    else:
                        magicstore = magic.open(magic.MAGIC_MIME)
                        magicstore.load()
                        contenttype = magicstore.file(self._fullpath)
                    f = open(self._fullpath, 'rb')
                    self._web_support.req.response_headers['Content-Type'] = contenttype
                    self._web_support.req.response_headers['Content-Length'] = str(size)
                    self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(self._fullpath)
                    self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                    self._web_support.req.output_done = True
                    if 'wsgi.file_wrapper' in self._web_support.req.environ:
                        return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                    return iter(lambda : f.read(1024), '')
            else:
                raise self.RendererException('Invalid Content Mode')
            return