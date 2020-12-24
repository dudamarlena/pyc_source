# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/regrid/flowgrid/FlowGrid.py
# Compiled at: 2019-11-10 20:34:08
# Size of source mod 2**32: 33977 bytes
import os, io, numpy as np
from datetime import *
import getpass
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import vtk
from vtk.util.numpy_support import numpy_to_vtk
import pkg_resources
version = pkg_resources.require('ReGrid')[0].version
f2m = 0.3048

class FlowGrid(object):

    def __init__(self):
        self.skip = 0
        self.Prop = {}

    def exportVTK(self, fname):
        """ Saves the grid as a VTK file, either a VTKStructuredGrid (.vts)
            or a VTKUnstructuredGrid (.vtu) depending on mesh type. 
            fname = the filename it will be saved at, if no extension is given, 
            .vts is appended 
        """
        filename, ext = os.path.splitext(fname)
        if self.GridType == 'vtkStructuredGrid':
            sWrite = vtk.vtkXMLStructuredGridWriter()
            sWrite.SetInputData(self.Grid)
            sWrite.SetFileName(filename + '.vts')
            sWrite.Write()
        else:
            if self.GridType == 'vtkUnstructuredGrid':
                sWrite = vtk.vtkXMLUnstructuredGridWriter()
                sWrite.SetInputData(self.Grid)
                sWrite.SetFileName(filename + '.vtu')
                sWrite.Write()
            else:
                print('Grid type is not recognized')

    def printCOORDS(self, f, p, fstr):
        MAXL = 132
        for point in p:
            up = ' %2.2f' % point
            if len(fstr) + len(up) > MAXL:
                f.write(fstr + '\n')
                fstr = ' '
            fstr += up
        else:
            return fstr

    def printAC(self, f, p, N, fstr):
        MAXL = 132
        if N == 1:
            up = ' %i' % p
        else:
            up = ' %i*%i' % (N, p)
        if len(fstr) + len(up) > MAXL:
            f.write(fstr + '\n')
            fstr = ' '
        fstr += up
        return fstr

    def printPROP(self, f, p, N, fstr):
        MAXL = 132
        if N == 1:
            up = ' %1.4e' % p
        else:
            up = ' %i*%1.4e' % (N, p)
        if len(fstr) + len(up) > MAXL:
            f.write(fstr + '\n')
            fstr = ' '
        fstr += up
        return fstr

    def exportTOUGH2(self, fname):
        """Saves the grid as a fixed format TOUGH(2) grid. 
        """
        STR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.ne, self.nn, self.nz = np.array(self.Grid.GetDimensions())
        filename, ext = os.path.splitext(fname)
        if self.GridType == 'vtkStructuredGrid':
            with io.open(filename, 'w', newline='\r\n') as (f):
                f.write('ELEME')
                f.write('\n1        10        20        30        40        50        60        70        80\n|--------|---------|---------|---------|---------|---------|---------|---------|\n12345678901234567890123456789012345678901234567890123456789012345678901234567890\n')
                ii = 0
                for iy in range(self.nn):
                    for ix in range(self.ne):
                        b2 = ii // (len(STR) * len(STR))
                        b1 = (ii - len(STR) * b2) // len(STR)
                        b0 = ii % len(STR)
                        f.write(STR[b2] + STR[b1] + STR[b0] + '\t' + str(ii) + '\n')
                        ii += 1

    def exportECL(self, fname):
        """ Saves the grid as an ECLIPSE grid. For the purposes of ECLIPSE  
        """
        self.ne, self.nn, self.nz = np.array(self.Grid.GetDimensions()) - 1
        filename, ext = os.path.splitext(fname)
        if self.GridType == 'vtkStructuredGrid':
            with io.open((filename + '.GRDECL'), 'w', newline='\r\n') as (f):
                f.write('-- Generated [\n')
                f.write('-- Format      : ECLIPSE keywords (grid geometry and properties) (ASCII)\n')
                f.write('-- Exported by : ReGrid v.' + version + '\n')
                f.write('-- User name   : ' + getpass.getuser() + '\n')
                f.write('-- Date        : ' + datetime.now().strftime('%A, %B %d %Y %H:%M:%S') + '\n')
                f.write('-- Project     : ReGrid project\n')
                f.write('-- Grid        : Description\n')
                f.write('-- Generated ]\n\n')
                f.write('SPECGRID                               -- Generated : ReGrid\n')
                f.write('  %i %i %i 1 F /\n\n' % (self.ne, self.nn, self.nz))
                f.write('COORDSYS                               -- Generated : ReGrid\n')
                f.write('  1 4 /\n\n')
                f.write('COORD                                  -- Generated : ReGrid\n')
                nz = self.nz
                fstr = str(' ')
                for iy in range(self.nn):
                    for ix in range(self.ne):
                        p0 = self.Grid.GetCell(ix, iy, 0).GetPoints().GetPoint(0)
                        fstr = self.printCOORDS(f, p0, fstr)
                        p1 = self.Grid.GetCell(ix, iy, nz - 1).GetPoints().GetPoint(4)
                        fstr = self.printCOORDS(f, p1, fstr)
                    else:
                        p2 = self.Grid.GetCell(ix, iy, 0).GetPoints().GetPoint(1)
                        fstr = self.printCOORDS(f, p2, fstr)
                        p3 = self.Grid.GetCell(ix, iy, nz - 1).GetPoints().GetPoint(5)
                        fstr = self.printCOORDS(f, p3, fstr)

                else:
                    for ix in range(self.ne):
                        p8 = self.Grid.GetCell(ix, iy, 0).GetPoints().GetPoint(3)
                        fstr = self.printCOORDS(f, p8, fstr)
                        p9 = self.Grid.GetCell(ix, iy, nz - 1).GetPoints().GetPoint(7)
                        fstr = self.printCOORDS(f, p9, fstr)
                    else:
                        p14 = self.Grid.GetCell(ix, iy, 0).GetPoints().GetPoint(2)
                        fstr = self.printCOORDS(f, p14, fstr)
                        p15 = self.Grid.GetCell(ix, iy, nz - 1).GetPoints().GetPoint(6)
                        fstr = self.printCOORDS(f, p15, fstr)
                        f.write(fstr)
                        fstr = ' '
                        f.write(' /')
                        f.write('\n')
                        f.write('\n')
                        f.write('ZCORN                                  -- Generated : ReGrid\n')
                        for iz in range(self.nz):
                            for iy in range(self.nn):
                                for ix in range(self.ne):
                                    p0 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(0)
                                    p1 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(1)
                                    fstr = self.printCOORDS(f, [p0[2]], fstr)
                                    fstr = self.printCOORDS(f, [p1[2]], fstr)

                        for ix in range(self.ne):
                            p0 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(3)
                            p1 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(2)
                            fstr = self.printCOORDS(f, [p0[2]], fstr)
                            fstr = self.printCOORDS(f, [p1[2]], fstr)
                        else:
                            for iy in range(self.nn):
                                for ix in range(self.ne):
                                    p0 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(4)
                                    p1 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(5)
                                    fstr = self.printCOORDS(f, [p0[2]], fstr)
                                    fstr = self.printCOORDS(f, [p1[2]], fstr)
                                else:
                                    for ix in range(self.ne):
                                        p0 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(7)
                                        p1 = self.Grid.GetCell(ix, iy, iz).GetPoints().GetPoint(6)
                                        fstr = self.printCOORDS(f, [p0[2]], fstr)
                                        fstr = self.printCOORDS(f, [p1[2]], fstr)

                            else:
                                f.write(fstr)
                                fstr = ' '
                                f.write(' /')
                                f.write('\n')
                                f.write('\n')
                                f.write('ACTNUM                                 -- Generated : ReGrid\n')
                                c = -999
                                N = 0
                                for iac in self.ActiveCells.flatten(order='F'):
                                    if iac == c:
                                        N += 1
                                    else:
                                        if c != -999:
                                            fstr = self.printAC(f, c, N, fstr)
                                        c = iac
                                        N = 1
                                else:
                                    fstr = self.printAC(f, c, N, fstr)
                                    f.write(fstr)
                                    f.write(' /')
                                    f.write('\n')
                                    f.write('\n')

        else:
            print('Only structured grids can be converted to ECLIPSE files')

    def exportECLPropertyFiles(self, fname):
        """ Convert any point data to cell data
        """
        pointConvert = True
        if pointConvert:
            p2c = vtk.vtkPointDataToCellData()
            p2c.SetInputDataObject(self.Grid)
            p2c.PassPointDataOn()
            p2c.Update()
            self.Grid = p2c.GetOutput()
        filename, ext = os.path.splitext(fname)
        for ia in range(self.Grid.GetCellData().GetNumberOfArrays()):
            prop = self.Grid.GetCellData().GetArray(ia).GetName()
            print('exporting prop', prop)
            if self.GridType == 'vtkStructuredGrid':
                with io.open((filename + 'prop-' + prop.lower() + '.GRDECL'), 'w', newline='\r\n') as (f):
                    f.write('-- Generated [\n')
                    f.write('-- Format      : ECLIPSE keywords (grid properties) (ASCII)\n')
                    f.write('-- Exported by : ReGrid v.' + version + '\n')
                    f.write('-- User name   : ' + getpass.getuser() + '\n')
                    f.write('-- Date        : ' + datetime.now().strftime('%A, %B %d %Y %H:%M:%S') + '\n')
                    f.write('-- Project     : ReGrid project\n')
                    f.write('-- Grid        : Description\n')
                    f.write('-- Unit system : ECLIPSE-Field\n')
                    f.write('-- Generated ]\n\n')
                    f.write(prop.upper() + '                                 -- Generated : ReGrid\n')
                    f.write('-- Property name in Petrel : ' + prop + '\n')
                    c = -999.9999
                    N = 0
                    ii = 0
                    fstr = ' '
                    for iz in range(self.nz):
                        for iy in range(self.nn):
                            for ix in range(self.ne):
                                iac = '{:0.4e}'.format(self.Grid.GetCellData().GetArray(ia).GetTuple1(ii))
                                print(iac)
                                ii += 1
                                if iac == c:
                                    N += 1
                                else:
                                    if c != -999.9999:
                                        fstr = self.printPROP(f, c, N, fstr)
                                    c = eval(iac)
                                    N = 1

                        else:
                            fstr = self.printPROP(f, c, N, fstr)
                            f.write(fstr)
                            f.write(' /')
                            f.write('\n')


class GRDECL(FlowGrid):
    __doc__ = ' GRDECL processes Schlumberger ECLIPSE files\n    '

    def __init__(self):
        super(GRDECL, self).__init__()
        nx, ny, nz = (0, 0, 0)

    def loadNodes--- This code section failed: ---

 L. 294         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'fname'
                4  LOAD_STR                 'r'
                6  CALL_FUNCTION_2       2  ''
             8_10  SETUP_WITH          506  'to 506'
               12  STORE_FAST               'fp'

 L. 297        14  LOAD_FAST                'fp'
               16  GET_ITER         
             18_0  COME_FROM           122  '122'
             18_1  COME_FROM            40  '40'
               18  FOR_ITER            130  'to 130'
               20  STORE_FAST               'line'

 L. 298        22  LOAD_FAST                'line'
               24  LOAD_METHOD              split
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'item'

 L. 299        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'item'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               0
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    18  'to 18'

 L. 300        42  LOAD_FAST                'item'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 'SPECGRID'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    86  'to 86'

 L. 301        54  LOAD_GLOBAL              np
               56  LOAD_ATTR                array
               58  LOAD_FAST                'fp'
               60  LOAD_METHOD              readline
               62  CALL_METHOD_0         0  ''
               64  LOAD_METHOD              split
               66  CALL_METHOD_0         0  ''
               68  LOAD_CONST               0
               70  LOAD_CONST               3
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  LOAD_GLOBAL              int
               78  LOAD_CONST               ('dtype',)
               80  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               SPECGRID
             86_0  COME_FROM            52  '52'

 L. 302        86  LOAD_FAST                'item'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_STR                 'COORDSYS'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L. 303        98  LOAD_FAST                'fp'
              100  LOAD_METHOD              readline
              102  CALL_METHOD_0         0  ''
              104  LOAD_METHOD              split
              106  CALL_METHOD_0         0  ''
              108  LOAD_FAST                'self'
              110  STORE_ATTR               COORDSYS
            112_0  COME_FROM            96  '96'

 L. 304       112  LOAD_FAST                'item'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_STR                 'COORD'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE    18  'to 18'

 L. 305       124  POP_TOP          
              126  BREAK_LOOP          130  'to 130'
              128  JUMP_BACK            18  'to 18'

 L. 308       130  BUILD_LIST_0          0 
              132  LOAD_FAST                'self'
              134  STORE_ATTR               coords

 L. 309       136  LOAD_FAST                'fp'
              138  GET_ITER         
              140  FOR_ITER            212  'to 212'
              142  STORE_FAST               'line'

 L. 310       144  LOAD_FAST                'line'
              146  LOAD_METHOD              split
              148  CALL_METHOD_0         0  ''
              150  LOAD_CONST               -1
              152  BINARY_SUBSCR    
              154  LOAD_STR                 '/'
              156  COMPARE_OP               !=
              158  POP_JUMP_IF_FALSE   180  'to 180'

 L. 311       160  LOAD_FAST                'self'
              162  DUP_TOP          
              164  LOAD_ATTR                coords
              166  LOAD_FAST                'line'
              168  LOAD_METHOD              split
              170  CALL_METHOD_0         0  ''
              172  INPLACE_ADD      
              174  ROT_TWO          
              176  STORE_ATTR               coords
              178  JUMP_BACK           140  'to 140'
            180_0  COME_FROM           158  '158'

 L. 313       180  LOAD_FAST                'self'
              182  DUP_TOP          
              184  LOAD_ATTR                coords
              186  LOAD_FAST                'line'
              188  LOAD_METHOD              split
              190  CALL_METHOD_0         0  ''
              192  LOAD_CONST               0
              194  LOAD_CONST               -1
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  INPLACE_ADD      
              202  ROT_TWO          
              204  STORE_ATTR               coords

 L. 314       206  POP_TOP          
              208  BREAK_LOOP          212  'to 212'
              210  JUMP_BACK           140  'to 140'

 L. 317       212  BUILD_LIST_0          0 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               zcorn

 L. 318       218  LOAD_FAST                'fp'
              220  GET_ITER         
            222_0  COME_FROM           356  '356'
              222  FOR_ITER            366  'to 366'
              224  STORE_FAST               'line'

 L. 319       226  LOAD_FAST                'line'
              228  LOAD_METHOD              split
              230  CALL_METHOD_0         0  ''
              232  STORE_FAST               'item'

 L. 320       234  LOAD_GLOBAL              len
              236  LOAD_FAST                'item'
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_CONST               0
              242  COMPARE_OP               >
          244_246  POP_JUMP_IF_FALSE   344  'to 344'

 L. 321       248  LOAD_FAST                'item'
              250  LOAD_CONST               0
              252  BINARY_SUBSCR    
              254  LOAD_STR                 'ZCORN'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   344  'to 344'

 L. 322       262  LOAD_FAST                'fp'
              264  GET_ITER         
              266  FOR_ITER            344  'to 344'
              268  STORE_FAST               'line'

 L. 323       270  LOAD_FAST                'line'
              272  LOAD_METHOD              split
              274  CALL_METHOD_0         0  ''
              276  LOAD_CONST               -1
              278  BINARY_SUBSCR    
              280  LOAD_STR                 '/'
              282  COMPARE_OP               !=
          284_286  POP_JUMP_IF_FALSE   308  'to 308'

 L. 324       288  LOAD_FAST                'self'
              290  DUP_TOP          
              292  LOAD_ATTR                zcorn
              294  LOAD_FAST                'line'
              296  LOAD_METHOD              split
              298  CALL_METHOD_0         0  ''
              300  INPLACE_ADD      
              302  ROT_TWO          
              304  STORE_ATTR               zcorn
              306  JUMP_BACK           266  'to 266'
            308_0  COME_FROM           284  '284'

 L. 326       308  LOAD_FAST                'self'
              310  DUP_TOP          
              312  LOAD_ATTR                zcorn
              314  LOAD_FAST                'line'
              316  LOAD_METHOD              split
              318  CALL_METHOD_0         0  ''
              320  LOAD_CONST               0
              322  LOAD_CONST               -1
              324  BUILD_SLICE_2         2 
              326  BINARY_SUBSCR    
              328  INPLACE_ADD      
              330  ROT_TWO          
              332  STORE_ATTR               zcorn

 L. 327       334  POP_TOP          
          336_338  BREAK_LOOP          344  'to 344'
          340_342  JUMP_BACK           266  'to 266'
            344_0  COME_FROM           258  '258'
            344_1  COME_FROM           244  '244'

 L. 328       344  LOAD_GLOBAL              len
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                zcorn
              350  CALL_FUNCTION_1       1  ''
              352  LOAD_CONST               0
              354  COMPARE_OP               >
              356  POP_JUMP_IF_FALSE   222  'to 222'

 L. 329       358  POP_TOP          
          360_362  BREAK_LOOP          366  'to 366'
              364  JUMP_BACK           222  'to 222'

 L. 332       366  BUILD_LIST_0          0 
              368  LOAD_FAST                'self'
              370  STORE_ATTR               active

 L. 333       372  LOAD_FAST                'fp'
              374  GET_ITER         
            376_0  COME_FROM           412  '412'
            376_1  COME_FROM           398  '398'
              376  FOR_ITER            502  'to 502'
              378  STORE_FAST               'line'

 L. 334       380  LOAD_FAST                'line'
              382  LOAD_METHOD              split
              384  CALL_METHOD_0         0  ''
              386  STORE_FAST               'item'

 L. 335       388  LOAD_GLOBAL              len
              390  LOAD_FAST                'item'
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_CONST               0
              396  COMPARE_OP               >
          398_400  POP_JUMP_IF_FALSE   376  'to 376'

 L. 336       402  LOAD_FAST                'item'
              404  LOAD_CONST               0
              406  BINARY_SUBSCR    
              408  LOAD_STR                 'ACTNUM'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   376  'to 376'

 L. 337       416  LOAD_FAST                'fp'
              418  GET_ITER         
              420  FOR_ITER            498  'to 498'
              422  STORE_FAST               'line'

 L. 338       424  LOAD_FAST                'line'
              426  LOAD_METHOD              split
              428  CALL_METHOD_0         0  ''
              430  LOAD_CONST               -1
              432  BINARY_SUBSCR    
              434  LOAD_STR                 '/'
              436  COMPARE_OP               !=
          438_440  POP_JUMP_IF_FALSE   462  'to 462'

 L. 339       442  LOAD_FAST                'self'
              444  DUP_TOP          
              446  LOAD_ATTR                active
              448  LOAD_FAST                'line'
              450  LOAD_METHOD              split
              452  CALL_METHOD_0         0  ''
              454  INPLACE_ADD      
              456  ROT_TWO          
              458  STORE_ATTR               active
              460  JUMP_BACK           420  'to 420'
            462_0  COME_FROM           438  '438'

 L. 341       462  LOAD_FAST                'self'
              464  DUP_TOP          
              466  LOAD_ATTR                active
              468  LOAD_FAST                'line'
              470  LOAD_METHOD              split
              472  CALL_METHOD_0         0  ''
              474  LOAD_CONST               0
              476  LOAD_CONST               -1
              478  BUILD_SLICE_2         2 
              480  BINARY_SUBSCR    
              482  INPLACE_ADD      
              484  ROT_TWO          
              486  STORE_ATTR               active

 L. 342       488  POP_TOP          
          490_492  CONTINUE            376  'to 376'
          494_496  JUMP_BACK           420  'to 420'
          498_500  JUMP_BACK           376  'to 376'
              502  POP_BLOCK        
              504  BEGIN_FINALLY    
            506_0  COME_FROM_WITH        8  '8'
              506  WITH_CLEANUP_START
              508  WITH_CLEANUP_FINISH
              510  END_FINALLY      

 L. 344       512  LOAD_GLOBAL              np
              514  LOAD_ATTR                array
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                coords
              520  LOAD_GLOBAL              float
              522  LOAD_CONST               ('dtype',)
              524  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              526  LOAD_FAST                'self'
              528  STORE_ATTR               coords

 L. 347       530  LOAD_FAST                'self'
              532  LOAD_ATTR                SPECGRID
              534  LOAD_CONST               0
              536  BINARY_SUBSCR    
              538  LOAD_FAST                'self'
              540  STORE_ATTR               ne

 L. 348       542  LOAD_FAST                'self'
              544  LOAD_ATTR                SPECGRID
              546  LOAD_CONST               1
              548  BINARY_SUBSCR    
              550  LOAD_FAST                'self'
              552  STORE_ATTR               nn

 L. 349       554  LOAD_FAST                'self'
              556  LOAD_ATTR                SPECGRID
              558  LOAD_CONST               2
              560  BINARY_SUBSCR    
              562  LOAD_FAST                'self'
              564  STORE_ATTR               nz

 L. 352       566  LOAD_FAST                'self'
              568  LOAD_ATTR                buildGrid
              570  LOAD_CONST               False
              572  LOAD_CONST               ('plot',)
              574  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              576  POP_TOP          

 L. 353       578  LOAD_FAST                'self'
              580  LOAD_ATTR                buildActiveCells
              582  LOAD_CONST               False
              584  LOAD_CONST               ('plot',)
              586  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              588  POP_TOP          

 L. 354       590  LOAD_FAST                'self'
              592  LOAD_ATTR                buildZGrid
              594  LOAD_CONST               False
              596  LOAD_CONST               ('plot',)
              598  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              600  POP_TOP          

 L. 355       602  LOAD_FAST                'self'
              604  LOAD_ATTR                calculateVolumes
              606  LOAD_CONST               False
              608  LOAD_CONST               ('plot',)
              610  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              612  POP_TOP          

 L. 358       614  LOAD_STR                 'vtkStructuredGrid'
              616  LOAD_FAST                'self'
              618  STORE_ATTR               GridType

 L. 359       620  LOAD_GLOBAL              vtk
              622  LOAD_METHOD              vtkStructuredGrid
              624  CALL_METHOD_0         0  ''
              626  LOAD_FAST                'self'
              628  STORE_ATTR               Grid

 L. 360       630  LOAD_FAST                'self'
              632  LOAD_ATTR                Grid
              634  LOAD_METHOD              SetDimensions
              636  LOAD_FAST                'self'
              638  LOAD_ATTR                ne
              640  LOAD_CONST               1
              642  BINARY_ADD       
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                nn
              648  LOAD_CONST               1
              650  BINARY_ADD       
              652  LOAD_FAST                'self'
              654  LOAD_ATTR                nz
              656  LOAD_CONST               1
              658  BINARY_ADD       
              660  CALL_METHOD_3         3  ''
              662  POP_TOP          

 L. 361       664  LOAD_GLOBAL              vtk
              666  LOAD_METHOD              vtkPoints
              668  CALL_METHOD_0         0  ''
              670  STORE_FAST               'vtk_points'

 L. 362       672  LOAD_CONST               1.0
              674  STORE_FAST               've'

 L. 364       676  LOAD_GLOBAL              range
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                nz
              682  CALL_FUNCTION_1       1  ''
              684  GET_ITER         
              686  FOR_ITER            896  'to 896'
              688  STORE_FAST               'iz'

 L. 365       690  LOAD_FAST                'iz'
              692  LOAD_CONST               0
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   796  'to 796'

 L. 366       700  LOAD_GLOBAL              range
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                nn
              706  LOAD_CONST               1
              708  BINARY_ADD       
              710  CALL_FUNCTION_1       1  ''
              712  GET_ITER         
              714  FOR_ITER            796  'to 796'
              716  STORE_FAST               'iy'

 L. 367       718  LOAD_GLOBAL              range
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                ne
              724  LOAD_CONST               1
              726  BINARY_ADD       
              728  CALL_FUNCTION_1       1  ''
              730  GET_ITER         
              732  FOR_ITER            792  'to 792'
              734  STORE_FAST               'ix'

 L. 368       736  LOAD_FAST                'vtk_points'
              738  LOAD_METHOD              InsertNextPoint
              740  LOAD_FAST                'self'
              742  LOAD_ATTR                X0
              744  LOAD_FAST                'ix'
              746  LOAD_FAST                'iy'
              748  BUILD_TUPLE_2         2 
              750  BINARY_SUBSCR    

 L. 369       752  LOAD_FAST                'self'
              754  LOAD_ATTR                Y0
              756  LOAD_FAST                'ix'
              758  LOAD_FAST                'iy'
              760  BUILD_TUPLE_2         2 
              762  BINARY_SUBSCR    

 L. 370       764  LOAD_FAST                've'
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                ZZT
              770  LOAD_FAST                'iz'
              772  BINARY_SUBSCR    
              774  LOAD_FAST                'ix'
              776  LOAD_FAST                'iy'
              778  BUILD_TUPLE_2         2 
              780  BINARY_SUBSCR    
              782  BINARY_MULTIPLY  

 L. 368       784  CALL_METHOD_3         3  ''
              786  POP_TOP          
          788_790  JUMP_BACK           732  'to 732'
          792_794  JUMP_BACK           714  'to 714'
            796_0  COME_FROM           696  '696'

 L. 371       796  LOAD_GLOBAL              range
              798  LOAD_FAST                'self'
              800  LOAD_ATTR                nn
              802  LOAD_CONST               1
              804  BINARY_ADD       
              806  CALL_FUNCTION_1       1  ''
              808  GET_ITER         
              810  FOR_ITER            892  'to 892'
              812  STORE_FAST               'iy'

 L. 372       814  LOAD_GLOBAL              range
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                ne
              820  LOAD_CONST               1
              822  BINARY_ADD       
              824  CALL_FUNCTION_1       1  ''
              826  GET_ITER         
              828  FOR_ITER            888  'to 888'
              830  STORE_FAST               'ix'

 L. 373       832  LOAD_FAST                'vtk_points'
              834  LOAD_METHOD              InsertNextPoint
              836  LOAD_FAST                'self'
              838  LOAD_ATTR                X0
              840  LOAD_FAST                'ix'
              842  LOAD_FAST                'iy'
              844  BUILD_TUPLE_2         2 
              846  BINARY_SUBSCR    

 L. 374       848  LOAD_FAST                'self'
              850  LOAD_ATTR                Y0
              852  LOAD_FAST                'ix'
              854  LOAD_FAST                'iy'
              856  BUILD_TUPLE_2         2 
              858  BINARY_SUBSCR    

 L. 375       860  LOAD_FAST                've'
              862  LOAD_FAST                'self'
              864  LOAD_ATTR                ZZB
              866  LOAD_FAST                'iz'
              868  BINARY_SUBSCR    
              870  LOAD_FAST                'ix'
              872  LOAD_FAST                'iy'
              874  BUILD_TUPLE_2         2 
              876  BINARY_SUBSCR    
              878  BINARY_MULTIPLY  

 L. 373       880  CALL_METHOD_3         3  ''
              882  POP_TOP          
          884_886  JUMP_BACK           828  'to 828'
          888_890  JUMP_BACK           810  'to 810'
          892_894  JUMP_BACK           686  'to 686'

 L. 376       896  LOAD_FAST                'self'
              898  LOAD_ATTR                Grid
              900  LOAD_METHOD              SetPoints
              902  LOAD_FAST                'vtk_points'
              904  CALL_METHOD_1         1  ''
              906  POP_TOP          

 L. 379       908  LOAD_GLOBAL              vtk
              910  LOAD_METHOD              vtkIntArray
              912  CALL_METHOD_0         0  ''
              914  STORE_FAST               'ac'

 L. 380       916  LOAD_FAST                'ac'
              918  LOAD_METHOD              SetName
              920  LOAD_STR                 'ActiveCells'
              922  CALL_METHOD_1         1  ''
              924  POP_TOP          

 L. 381       926  LOAD_FAST                'self'
              928  LOAD_ATTR                ActiveCells
              930  LOAD_ATTR                flatten
              932  LOAD_STR                 'F'
              934  LOAD_CONST               ('order',)
              936  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              938  GET_ITER         
              940  FOR_ITER            958  'to 958'
              942  STORE_FAST               'iac'

 L. 382       944  LOAD_FAST                'ac'
              946  LOAD_METHOD              InsertNextTuple1
              948  LOAD_FAST                'iac'
              950  CALL_METHOD_1         1  ''
              952  POP_TOP          
          954_956  JUMP_BACK           940  'to 940'

 L. 383       958  LOAD_FAST                'self'
              960  LOAD_ATTR                Grid
              962  LOAD_METHOD              GetCellData
              964  CALL_METHOD_0         0  ''
              966  LOAD_METHOD              AddArray
              968  LOAD_FAST                'ac'
              970  CALL_METHOD_1         1  ''
              972  POP_TOP          

Parse error at or near `CONTINUE' instruction at offset 490_492

    def buildGrid(self, plot=False):
        """
        Topology of COORD mesh, only describes first layer..
         
                  8--------10-------12-------14
                 /|       /|       /|       /|
                / |      / |      / |      / |
               0--------2--------4--------6  |
               |  9-----|--11----|--13----|--15
               | /      | /      | /      | / 
               |/       |/       |/       |/  
               1--------3--------5--------7            7  -->   (2*(NE+1))
                                                      15  -->   (2*(NE+1)*(NN+1))
        """
        print('Constructing grid')
        self.ndx = self.ne + 1
        self.ndy = self.nn + 1
        self.ndz = self.nz + 1
        self.points = {}
        self.points['e'] = self.coords[0::3]
        self.points['n'] = self.coords[1::3]
        self.points['z'] = self.coords[2::3]
        self.X0 = np.reshape((self.points['e'][0::2]), (self.ndx, self.ndy), order='F')
        self.Y0 = np.reshape((self.points['n'][0::2]), (self.ndx, self.ndy), order='F')
        self.Z0 = np.reshape((self.points['z'][0::2]), (self.ndx, self.ndy), order='F')
        self.X1 = np.reshape((self.points['e'][1::2]), (self.ndx, self.ndy), order='F')
        self.Y1 = np.reshape((self.points['n'][1::2]), (self.ndx, self.ndy), order='F')
        self.Z1 = np.reshape((self.points['z'][1::2]), (self.ndx, self.ndy), order='F')
        if plot:
            print('plotting')
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_wireframe((f2m * self.X0), (f2m * self.Y0), (f2m * self.Z0), rstride=1, cstride=1)
            ax.plot_wireframe((f2m * self.X1), (f2m * self.Y1), (f2m * self.Z1), rstride=1, cstride=1)
            plt.show()

    def buildZGrid(self, plot=False):
        """ 
            Petrel provides the ZCORN in a truly arcane ordering--it's awful--and really, the programmers 
            deserve a special place in hell for doing this. The ordering is as follows, for a given plane:
             
             29    36  30   37 31    38 32    39 33    40 34    41 35    42
              _______  _______  ______  _______  _______  _______  _______
             /      / /      / /     / /      / /      / /      / /      /|
            /      / /      / /     / /      / /      / /      / /      / |
           00----01 02----03 04----05 06----07 08----09 10----11 12----13 /
            |  A  | |  B   | |   C  | |   D  | |   E  | |  F   | |   G  |/
           14----15 16----17 18----19 20----21 22----23 24----25 26----27
           
            
            This pattern is then repeated for each depth layer, it isn't that clear, but my ASCII art skills
            are already sufficiently challenged. 
 
        """
        print('Constructing Z corners')
        temp = []
        count = 0
        for item in self.zcorn:
            if '*' in item:
                ct = int(item.split('*')[0])
                vl = float(item.split('*')[1])
                temp += np.tile(vl, ct).tolist()
                count += ct
            else:
                temp += [float(item)]
                count += 1
        else:
            layers = np.resize(temp, (self.nz * 2, self.ne * self.nn * 4))
            self.ZZT = {}
            self.ZZB = {}
            for ilay in range(self.nz):
                self.ZZT[ilay] = np.zeros((self.ndx, self.ndy))
                self.ZZB[ilay] = np.zeros((self.ndx, self.ndy))
                iis = 0
                for iin in range(self.nn):
                    nears = {}
                    fars = {}
                    bnears = {}
                    bfars = {}
                    for iif in range(2):
                        nears[iif] = layers[(ilay * 2)][iis:iis + 2 * self.ne][0::2].tolist()
                        fars[iif] = layers[(ilay * 2)][iis:iis + 2 * self.ne][1::2].tolist()
                        layers[(ilay * 2)][iis:iis + 2 * self.ne][0::2] *= 0.0
                        layers[(ilay * 2)][iis:iis + 2 * self.ne][1::2] *= 0.0
                        nears[iif].append(fars[iif][(-1)])
                        fars[iif] = [nears[iif][0]] + fars[iif]
                        bnears[iif] = layers[(ilay * 2 + 1)][iis:iis + 2 * self.ne][0::2].tolist()
                        bfars[iif] = layers[(ilay * 2 + 1)][iis:iis + 2 * self.ne][1::2].tolist()
                        layers[(ilay * 2 + 1)][iis:iis + 2 * self.ne][0::2] *= 0.0
                        layers[(ilay * 2 + 1)][iis:iis + 2 * self.ne][1::2] *= 0.0
                        bnears[iif].append(bfars[iif][(-1)])
                        bfars[iif] = [bnears[iif][0]] + bfars[iif]
                        iis += 2 * self.ne
                    else:
                        self.ZZT[ilay][:, iin] = nears[0]
                        self.ZZB[ilay][:, iin] = bnears[0]

                    if iin == self.nn - 1:
                        self.ZZT[ilay][:, iin + 1] = fars[1]
                        self.ZZB[ilay][:, iin + 1] = bfars[1]
                else:
                    print('Layers ||', np.linalg.norm(layers), '||')
                    if plot:
                        fig = plt.figure()
                        ax = fig.add_subplot(111, projection='3d')
                        ax.plot_wireframe((self.X0), (self.Y0), (self.ZZT[0]), rstride=1, cstride=1, color='blue')
                        plt.gca().set_xlim(np.min(self.X0), np.max(self.X0))
                        plt.gca().set_ylim(np.max(self.Y0), np.min(self.Y0))
                        plt.gca().set_zlim(5000, 4000)
                        plt.savefig('mesh.png')
                        plt.show()

    def buildActiveCells(self, plot=False):
        print('Constructing active cells')
        self.ActiveCells = np.zeros((self.ne * self.nn * self.nz), dtype=int)
        count = 0
        for item in self.active:
            if '*' in item:
                ct = int(item.split('*')[0])
                vl = int(item.split('*')[1])
                self.ActiveCells[count:count + ct] = vl
                count += ct
            else:
                self.ActiveCells[count] = int(item)
                count += 1
        else:
            self.ActiveCells = np.reshape((self.ActiveCells), (self.ne, self.nn, self.nz), order='F')
            if plot:
                plt.pcolor((self.X0.T), (self.Y0.T), (self.ActiveCells[:, :, 0].T), edgecolors='w', linewidths=0.1)
                plt.xlabel('easting')
                plt.ylabel('northing')
                plt.gca().set_xlim(np.min(self.X0), np.max(self.X0))
                plt.gca().set_ylim(np.max(self.Y0), np.min(self.Y0))
                plt.gca().xaxis.tick_top()
                plt.gca().xaxis.set_label_position('top')
                plt.show()

    def calculateVolumes(self, plot=False):
        self.Volumes = np.zeros((self.ne, self.nn, self.nz))
        for iiz in range(self.nz):
            for iie in range(self.ne):
                for iin in range(self.nn):
                    if self.ActiveCells[(iie, iin, iiz)]:
                        u = np.array((self.X0[(iie, iin)], self.Y0[(iie, iin)], self.ZZT[iiz][(iie, iin)])) - np.array((self.X0[(iie + 1, iin)], self.Y0[(iie + 1, iin)], self.ZZT[iiz][(iie, iin)]))
                        v = np.array((self.X0[(iie, iin)], self.Y0[(iie, iin)], self.ZZT[iiz][(iie, iin)])) - np.array((self.X0[(iie, iin + 1)], self.Y0[(iie, iin + 1)], self.ZZT[iiz][(iie, iin)]))
                        w = np.array((self.X0[(iie, iin)], self.Y0[(iie, iin)], self.ZZT[iiz][(iie, iin)])) - np.array((self.X0[(iie, iin)], self.Y0[(iie, iin)], self.ZZB[iiz][(iie, iin)]))
                        if np.any(u != u) or np.any(v != v) or np.any(w != w):
                            print('NAN!', iie, iin, iiz)
                            exit()
                        V = np.linalg.det(np.array((f2m * u, f2m * v, f2m * w)))
                        self.Volumes[(iie, iin, iiz)] = np.abs(V)
                else:
                    vr = (3.0 / (4.0 * np.pi) * self.Volumes) ** 0.3333333333333333
                    print('Total grid volume: ' + str(np.sum(self.Volumes)) + ' m^3')

    def readProperty--- This code section failed: ---

 L. 617         0  BUILD_LIST_0          0 
                2  STORE_FAST               'temp'

 L. 618         4  LOAD_GLOBAL              open
                6  LOAD_FAST                'fname'
                8  LOAD_STR                 'r'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH          186  'to 186'
               14  STORE_FAST               'fp'

 L. 619        16  LOAD_FAST                'fp'
               18  GET_ITER         
             20_0  COME_FROM            54  '54'
             20_1  COME_FROM            42  '42'
               20  FOR_ITER            182  'to 182'
               22  STORE_FAST               'line'

 L. 620        24  LOAD_FAST                'line'
               26  LOAD_METHOD              split
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'item'

 L. 621        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'item'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    20  'to 20'

 L. 622        44  LOAD_FAST                'item'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_STR                 '--'
               52  COMPARE_OP               !=
               54  POP_JUMP_IF_FALSE    20  'to 20'

 L. 623        56  LOAD_FAST                'item'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  STORE_FAST               'tag'

 L. 624        64  LOAD_FAST                'fp'
               66  LOAD_METHOD              readline
               68  CALL_METHOD_0         0  ''
               70  LOAD_METHOD              split
               72  CALL_METHOD_0         0  ''
               74  LOAD_CONST               -1
               76  BINARY_SUBSCR    
               78  STORE_FAST               'attribute'

 L. 625        80  LOAD_FAST                'attribute'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                Prop
               86  LOAD_FAST                'tag'
               88  STORE_SUBSCR     

 L. 626        90  LOAD_GLOBAL              print
               92  LOAD_STR                 'loading'
               94  LOAD_FAST                'attribute'
               96  CALL_FUNCTION_2       2  ''
               98  POP_TOP          

 L. 627       100  LOAD_FAST                'fp'
              102  GET_ITER         
            104_0  COME_FROM           122  '122'
              104  FOR_ITER            180  'to 180'
              106  STORE_FAST               'line'

 L. 628       108  LOAD_FAST                'line'
              110  LOAD_METHOD              split
              112  CALL_METHOD_0         0  ''
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_STR                 '--'
              120  COMPARE_OP               !=
              122  POP_JUMP_IF_FALSE   104  'to 104'

 L. 629       124  LOAD_FAST                'line'
              126  LOAD_METHOD              split
              128  CALL_METHOD_0         0  ''
              130  LOAD_CONST               -1
              132  BINARY_SUBSCR    
              134  LOAD_STR                 '/'
              136  COMPARE_OP               !=
              138  POP_JUMP_IF_FALSE   154  'to 154'

 L. 630       140  LOAD_FAST                'temp'
              142  LOAD_FAST                'line'
              144  LOAD_METHOD              split
              146  CALL_METHOD_0         0  ''
              148  INPLACE_ADD      
              150  STORE_FAST               'temp'
              152  JUMP_BACK           104  'to 104'
            154_0  COME_FROM           138  '138'

 L. 632       154  LOAD_FAST                'temp'
              156  LOAD_FAST                'line'
              158  LOAD_METHOD              split
              160  CALL_METHOD_0         0  ''
              162  LOAD_CONST               0
              164  LOAD_CONST               -1
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  INPLACE_ADD      
              172  STORE_FAST               'temp'

 L. 633       174  POP_TOP          
              176  CONTINUE             20  'to 20'
              178  JUMP_BACK           104  'to 104'
              180  JUMP_BACK            20  'to 20'
              182  POP_BLOCK        
              184  BEGIN_FINALLY    
            186_0  COME_FROM_WITH       12  '12'
              186  WITH_CLEANUP_START
              188  WITH_CLEANUP_FINISH
              190  END_FINALLY      

 L. 635       192  LOAD_GLOBAL              np
              194  LOAD_ATTR                zeros
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                ne
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                nn
              204  BINARY_MULTIPLY  
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                nz
              210  BINARY_MULTIPLY  
              212  LOAD_GLOBAL              float
              214  LOAD_CONST               ('dtype',)
              216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              218  STORE_FAST               'data'

 L. 636       220  LOAD_CONST               0
              222  STORE_FAST               'count'

 L. 637       224  LOAD_FAST                'temp'
              226  GET_ITER         
              228  FOR_ITER            326  'to 326'
              230  STORE_FAST               'item'

 L. 638       232  LOAD_STR                 '*'
              234  LOAD_FAST                'item'
              236  COMPARE_OP               in
          238_240  POP_JUMP_IF_FALSE   304  'to 304'

 L. 639       242  LOAD_GLOBAL              int
              244  LOAD_FAST                'item'
              246  LOAD_METHOD              split
              248  LOAD_STR                 '*'
              250  CALL_METHOD_1         1  ''
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  CALL_FUNCTION_1       1  ''
              258  STORE_FAST               'ct'

 L. 640       260  LOAD_GLOBAL              float
              262  LOAD_FAST                'item'
              264  LOAD_METHOD              split
              266  LOAD_STR                 '*'
              268  CALL_METHOD_1         1  ''
              270  LOAD_CONST               1
              272  BINARY_SUBSCR    
              274  CALL_FUNCTION_1       1  ''
              276  STORE_FAST               'vl'

 L. 641       278  LOAD_FAST                'vl'
              280  LOAD_FAST                'data'
              282  LOAD_FAST                'count'
              284  LOAD_FAST                'count'
              286  LOAD_FAST                'ct'
              288  BINARY_ADD       
              290  BUILD_SLICE_2         2 
              292  STORE_SUBSCR     

 L. 642       294  LOAD_FAST                'count'
              296  LOAD_FAST                'ct'
              298  INPLACE_ADD      
              300  STORE_FAST               'count'
              302  JUMP_BACK           228  'to 228'
            304_0  COME_FROM           238  '238'

 L. 644       304  LOAD_GLOBAL              float
              306  LOAD_FAST                'item'
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_FAST                'data'
              312  LOAD_FAST                'count'
              314  STORE_SUBSCR     

 L. 645       316  LOAD_FAST                'count'
              318  LOAD_CONST               1
              320  INPLACE_ADD      
              322  STORE_FAST               'count'
              324  JUMP_BACK           228  'to 228'

 L. 647       326  LOAD_GLOBAL              np
              328  LOAD_ATTR                reshape
              330  LOAD_FAST                'data'
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                ne
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                nn
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                nz
              344  BUILD_TUPLE_3         3 
              346  LOAD_STR                 'F'
              348  LOAD_CONST               ('order',)
              350  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              352  STORE_FAST               'data'

 L. 650       354  LOAD_GLOBAL              vtk
              356  LOAD_METHOD              vtkDoubleArray
              358  CALL_METHOD_0         0  ''
              360  STORE_FAST               'ac'

 L. 651       362  LOAD_FAST                'ac'
              364  LOAD_METHOD              SetName
              366  LOAD_FAST                'attribute'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 652       372  LOAD_FAST                'data'
              374  LOAD_ATTR                flatten
              376  LOAD_STR                 'F'
              378  LOAD_CONST               ('order',)
              380  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              382  GET_ITER         
              384  FOR_ITER            402  'to 402'
              386  STORE_FAST               'iac'

 L. 653       388  LOAD_FAST                'ac'
              390  LOAD_METHOD              InsertNextTuple1
              392  LOAD_FAST                'iac'
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
          398_400  JUMP_BACK           384  'to 384'

 L. 654       402  LOAD_FAST                'self'
              404  LOAD_ATTR                Grid
              406  LOAD_METHOD              GetCellData
              408  CALL_METHOD_0         0  ''
              410  LOAD_METHOD              AddArray
              412  LOAD_FAST                'ac'
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          

Parse error at or near `CONTINUE' instruction at offset 176


class SUTRA(FlowGrid):
    __doc__ = ' SUTRA is a USGS flow modelling code.  \n    '

    def __init__(self):
        super(SUTRA, self).__init__()
        nx, ny, nz = (0, 0, 0)

    def loadNodes(self, fname, nx, ny, nz, ve=-1):
        """ Reads in the points of the grid, ususally in a file called nodewise
            fname = nodes file 
            nx = number of cells in the easting(x) direction 
            ny = number of cells in the northing (y) direction 
            nz = number of cells in depth, positive up 
            ve = vertical exaggeration, default is 1 (none)
            This method results in the generation of a VtkStructuredGrid
        """
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.ActiveCells = np.ones((self.nx * self.ny * self.nz), dtype=int)
        X = np.loadtxt(fname, comments='#')
        self.points = np.reshape(np.array((X[:, 2], X[:, 3], X[:, 4])).T, (nx, ny, nz, 3))
        self.GridType = 'vtkStructuredGrid'
        self.Grid = vtk.vtkStructuredGrid()
        self.Grid.SetDimensions(nx, ny, nz)
        vtk_points = vtk.vtkPoints()
        for iz in range(nz):
            for iy in range(ny):
                for ix in range(nx):
                    vtk_points.InsertNextPoint(self.points[(ix, iy, iz)][0], self.points[(ix, iy, iz)][1], ve * self.points[(ix, iy, iz)][2])

        else:
            self.Grid.SetPoints(vtk_points)

    def loadNodesConnections(self, nodes, connections):
        """ In contrast to the above method, the points and connections can be loaded instead. 
            For non-regular grids this is necessary. This method results in the generation 
            of a vtkUnstructuredGrid. 
            nodes = node file, often called nodewise
            connections = element connections, often called incident
        """
        X = np.loadtxt(nodes, comments='#')
        points = np.array((X[:, 2], X[:, 3], X[:, 4])).T
        self.GridType = 'vtkUnstructuredGrid'
        self.Grid = vtk.vtkUnstructuredGrid()
        vtk_points = vtk.vtkPoints()
        for point in range(np.shape(points)[0]):
            vtk_points.InsertNextPoint(points[(point, 0)], points[(point, 1)], points[(point, 2)])
        else:
            self.Grid.SetPoints(vtk_points)
            C = np.loadtxt(connections, comments='#', skiprows=2, dtype=int)
            for line in range(np.shape(C)[0]):
                idList = vtk.vtkIdList()
                for node in C[line, :][1:]:
                    idList.InsertNextId(node - 1)
                else:
                    self.Grid.InsertNextCell(vtk.VTK_HEXAHEDRON, idList)

    def readPermeability(self, fname, label=('$\\kappa_x$', '$\\kappa_y$', '$\\kappa_z$')):
        """ Reads in SUTRA permeability data 
        """
        k = np.loadtxt(fname, comments='#')
        nr, nc = np.shape(k)
        if self.GridType == 'vtkStructuredGrid':
            k = np.reshape(k, (self.nx - 1, self.ny - 1, self.nz - 1, np.shape(k)[1]))
            k = np.reshape(k, (nr, nc), order='F')
        kx = vtk.vtkDoubleArray()
        kx.SetName(label[0])
        ky = vtk.vtkDoubleArray()
        ky.SetName(label[1])
        kz = vtk.vtkDoubleArray()
        kz.SetName(label[2])
        for ik, K in enumerate(k):
            kx.InsertNextTuple1(K[2])
            ky.InsertNextTuple1(K[3])
            kz.InsertNextTuple1(K[4])
        else:
            self.Grid.GetCellData().AddArray(kx)
            self.Grid.GetCellData().AddArray(ky)
            self.Grid.GetCellData().AddArray(kz)

    def readPorosity(self, fname, label='phi'):
        phi = np.loadtxt(fname)
        nr, nc = np.shape(phi)
        if self.GridType == 'vtkStructuredGrid':
            phi = np.reshape(phi, (self.nx, self.ny, self.nz, np.shape(phi)[1]))
            phi = np.reshape(phi, (nr, nc), order='F')
        vphi = vtk.vtkDoubleArray()
        vphi.SetName(label)
        for ik, K in enumerate(phi):
            vphi.InsertNextTuple1(K[5])
        else:
            self.Grid.GetPointData().AddArray(vphi)

    def readPressure(self, fname, ts=2, label='$P$'):
        nnodes = self.nx * self.ny * self.nz
        P = np.loadtxt(fname, comments='#')[ts * nnodes:(ts + 1) * nnodes, :]
        C = np.loadtxt(fname, comments='#')[ts * nnodes:(ts + 1) * nnodes, :]
        nr, nc = np.shape(P)
        if self.GridType == 'vtkStructuredGrid':
            P = np.reshape(P, (self.nx, self.ny, self.nz, np.shape(P)[1]))
            P = np.reshape(P, (nr, nc), order='F')
            C = np.reshape(C, (self.nx, self.ny, self.nz, np.shape(C)[1]))
            C = np.reshape(C, (nr, nc), order='F')
        vP = vtk.vtkDoubleArray()
        vP.SetName(label)
        vC = vtk.vtkDoubleArray()
        vC.SetName('Concentration')
        for ik in range(nnodes):
            vP.InsertNextTuple1(P[(ik, 3)])
            vC.InsertNextTuple1(C[(ik, 4)])
        else:
            self.Grid.GetPointData().AddArray(vP)
            self.Grid.GetPointData().AddArray(vC)