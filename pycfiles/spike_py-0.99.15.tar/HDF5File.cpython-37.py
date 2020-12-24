# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/HDF5File.py
# Compiled at: 2020-02-03 12:06:33
# Size of source mod 2**32: 45541 bytes
"""
HDF5File.py

Created by Marc-André Delsuc, Marie-Aude Coutouly on 2011-07-13.

API dealing with HDF5File. For now it is non surclassing tables, you have to use *.hf. to access all tables functionalities
"""
from __future__ import print_function
import sys, os, unittest, numpy as np, time, math, json, tables
from tables.nodes import filenode
if sys.version_info[0] < 3:
    pass
else:
    xrange = range
if sys.version_info[0] < 3:
    __file_version__ = '0.91'
else:
    __file_version__ = b'0.91'
__version__ = '0.902'

def determine_chunkshape(size1, size2):
    """
    returns optimum size for chuncks for a dataset of file size1, size2
    and update cachesize for accomodating dataset
    """
    c1 = int(size1 / 64.0 + 1)
    c2 = int(size2 / 64.0 + 1)
    return (
     c1, c2)


FTICR_AXISvp9 = {'itype':tables.Int32Col(), 
 'size':tables.Int32Col(), 
 'FTICR':tables.StringCol(itemsize=16), 
 'sampling':tables.StringCol(itemsize=16), 
 'specwidth':tables.Float32Col(), 
 'highmass':tables.Float32Col(), 
 'offsetfreq':tables.Float32Col(), 
 'left_point':tables.Int32Col(), 
 'calibA':tables.Float64Col(), 
 'calibB':tables.Float64Col(), 
 'calibC':tables.Float64Col(), 
 'highfreq':tables.Float32Col(), 
 'lowfreq':tables.Float32Col()}

class HDF5File(object):
    __doc__ = '\n    defines the interface to simply (read/write) access HDF5 files\n    standard methods are load() and save()\n\n    standard sequence to read is\n    H = HDF5File(filename,"r")\n    B = H.get_data()      # B is a FTICRdata\n    H.close()\n\n    or\n    H = HDF5File(filename,"r")\n    H.load()\n    B = H.data      # B is a FTICRdata\n    H.close()\n\n\n    and to write\n    H = HDF5File(filename,"w")\n    H.set_data(B)         # where B is a FTICRdata; do not use    H.data = B\n    H.save()\n    H.close()\n\n    \n    HDF5File have the capacity to store and retrieve complete files and python objects:\n        with\n    lis = [any kind of list or tuple]  # works also with dict and nested list and dict\n        then\n    H.store_internal_object(lis, "name_of_storage")\n        will store the object, and\n    lis_back = H.retrieve_object("name_of_storage")\n        will retrieve it\n    data are stored using JSON, so anything compatible will do  \n    '

    def __init__(self, fname, access='r', info=None, nparray=None, fticrd=None, compress=False, debug=0, verbose=False):
        """
        access:
            r: Read-only; no data can be modified.
            w: Write; a new file is created (an existing file with the same name would be deleted).
            a: Append; an existing file is opened for reading and writing, and if the file does not exist it is created.
            r+: It is similar to ‘a’, but the file must already exist.
        """
        from .. import FTICR
        import getpass
        try:
            owner = getpass.getuser()
        except:
            owner = None

        self.debug = debug
        self.fname = fname
        self.info = None
        self.nparray = None
        self.chunks = None
        self.filters = None
        self.correct0p9_0p91 = False
        self.set_compression(compress)
        if access not in ('w', 'r', 'rw', 'a', 'r+'):
            raise Exception(access + ' : acces key not valid')
        elif os.path.isfile(self.fname):
            self.checkversion()
        elif access == 'r':
            if self.debug > 0:
                print('open in read mode')
            self.access = access
            self.hf = tables.open_file(self.fname, self.access)
            if verbose:
                self.get_file_infos()
        else:
            if access == 'w':
                if self.debug > 0:
                    print('Open HDF5 File with writing rights')
                self.access = access
                self.hf = tables.open_file(self.fname, self.access)
                self.create_generic(owner=owner)
                self.hf.create_group('/', 'attached', filters=tables.Filters(complevel=1, complib='zlib'))
                if info is not None:
                    if self.debug > 0:
                        print('Create HDF5 File from info')
                    self.info = info
                    self.data = None
                    self.create_HDF5_info()
                else:
                    if nparray is not None:
                        if self.debug > 0:
                            print('Create HDF5 File from nparray')
                        data = FTICR.FTICRData(buffer=nparray)
                        self.create_from_template(data)
                    else:
                        if fticrd is not None:
                            if self.debug > 0:
                                print('Create HDF5 File from fticrdata')
                            self.create_from_template(fticrd)
                        else:
                            if self.debug > 0:
                                print('without any data nor infos')
            else:
                if access == 'r+':
                    if self.debug > 0:
                        print('open in modifying mode r+')
                    self.access = 'r+'
                    self.hf = tables.open_file(self.fname, self.access)
                    if verbose:
                        self.get_file_infos()
                elif access == 'rw':
                    if self.debug > 0:
                        print('open in modifying mode rw')
                    self.access = 'r+'
                    self.hf = tables.open_file(self.fname, self.access)
                    if verbose:
                        self.get_file_infos()
                elif access == 'a':
                    if self.debug > 0:
                        print('open in modifying mode a')
                    self.access = 'a'
                    self.hf = tables.open_file(self.fname, self.access)
                    if verbose:
                        self.get_file_infos()
                else:
                    raise ' Internal error in HDF5 creation - This should never happen'

    def checkversion(self):
        """
        check file version and exit if incompatible
        """
        self.hf = tables.open_file(self.fname, 'r')
        try:
            infos = self.hf.root.generic_table.read()
        except:
            raise Exception('The file %s does not seem to be a valid file' % self.fname)

        info = infos[0]
        self.hf.close()
        if self.debug > 0:
            print('File_Version', info['File_Version'])
        elif info['File_Version'] != __file_version__:
            if float(info['File_Version']) == 0.9 and float(__file_version__) == 0.91:
                self.correct0p9_0p91 = True
            else:
                if float(info['File_Version']) > float(__file_version__):
                    msg = '\n\nWARNING\nThe file {0} is of version {1} while this program handles file version {2} or lower.\nThe file was written with a more recent version of the program than this one, and is incompatible.\nYou have to upgrade to a newer version of SPIKE.\nto do this, run the following command:\n\n    pip install spike-py --upgrade\n\n'.format(self.fname, info['File_Version'].decode('ascii'), __file_version__.decode('ascii'))
                else:
                    msg = '\n\nWARNING\nThe file {0} is from version {1} while this program handles file version {2}.\nYou have to upgrade your msh5 file applying the update function.\nto do this run the following spike command:\n\nspike.File.HDF5File.update("{0}")\n\nor by running the following program:\n\npython -m spike.File.HDF5File update {0}\n'.format(self.fname, info['File_Version'].decode('ascii'), __file_version__.decode('ascii'))
                raise Exception(msg)
        return True

    def open_internal_file(self, h5name, access='r', where='/attached'):
        """
        opens a node called h5name in the file, which can be accessed as a file.
        returns a file stram which can be used as a classical file.
        
        access is either 
            'r' : for reading an existing node
            'w' : create a node for writing into it
            'a' : for appending in an existing node
        file is stored in a h5 group called h5name

        eg.
        F = h5.open_internal_file('myfile.txt', 'w', where='/files')
        # create a node called '/files/myfile.txt' (node 'myfile.txt' in the group '/files')
        F.writelines(text)
        F.close()
        # and write some text into it

        # then, latter on
        F = h5.open_internal_file('myfile.txt', 'r', where='/files')
        textback = F.read()
        F.close()

        This is used to add parameter files, audit_trail, etc... to spike/hdf5 files
        
        it is based on the filenode module from pytables
        """
        import warnings
        if access == 'r':
            v = self.hf.get_node(where=where, name=h5name)
            F = filenode.open_node(v, 'r')
        else:
            if access == 'a':
                v = self.hf.get_node(where=where, name=h5name)
                F = filenode.open_node(v, 'a+')
            else:
                if access == 'w':
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        F = filenode.new_node((self.hf), where=where, name=h5name)
        return F

    def store_internal_file(self, filename, h5name=None, where='/attached'):
        """
        Store a (text) file into the hdf5 file,
            filename: name of the file to be copied
            h5name: is its internal name (more limitation than in regular filesystems)
                copied from os.path.basename(filename) by default
            where: group where the file is copied into the hdf5
        file content will be retrieved using    open_internal_file(h5name,'r)
        """
        if h5name is None:
            h5name = os.path.basename(filename)
        node = self.open_internal_file(h5name, 'w', where=where)
        with open(filename, 'rb') as (F):
            node.write(F.read())
        node.close()

    def retrieve_internal_file(self, h5name, where='/attached'):
        """
        returns the content of a n internal file stored with store_internal_file() or written directly
        """
        v = self.hf.get_node(where=where, name=h5name)
        F = filenode.open_node(v, 'r')
        content = F.read()
        F.close()
        return content

    def store_internal_object(self, obj, h5name, where='/'):
        """
        store a python object into the hdf5 file
        object are then retrieve with retrieve_object()

        uses JSON to serialize obj
            - so works only on values, lists, dictionary, etc... but not functions or methods
        """
        node = filenode.new_node((self.hf), where=where, name=h5name, filters=tables.Filters(complevel=1, complib='zlib'))
        js = json.dumps(obj, ensure_ascii=True)
        node.write(js.encode())
        node.close()

    def retrieve_object(self, h5name, where='/', access='r'):
        """
        retrieve a python object stored with store_internal_object()
        """
        v = self.hf.get_node(where=where, name=h5name)
        F = filenode.open_node(v, 'r')
        js = F.read()
        F.close()
        obj = json.loads(js.decode())
        return obj

    def set_compression(self, On=False):
        """sets Carray HDF5 file compression to zlib if On is True; to none otherwise"""
        if On:
            self.filters = tables.Filters(complevel=1, complib='zlib')
        else:
            self.filters = None
        return On

    def set_data(self, data, group='resol1'):
        """
        Take the ser_file and the params and put all the informations in the HDF5File
        """
        self.dim = data.dim
        self.create_tables()
        group_resol = self.create_group('/', group)
        group_axe = self.create_group(group_resol, 'axes')
        self.dims = []
        for i in range(self.dim):
            ii = i + 1
            infos = data.axes(ii).__dict__
            self.fill_table(ii, group_axe, infos)
            self.dims.append(infos['size'])

    def set_data_from_fticrd(self, buff, group='resol1'):
        """
        sets the FTICRdata attached to the (to be written) file
        """
        self.dim = buff.dim
        self.create_tables()
        group_resol = self.create_group('/', group)
        group_axe = self.create_group(group_resol, 'axes')
        self.dims = []
        for i in range(self.dim):
            ii = i + 1
            infos = buff.axes(ii).__dict__
            self.fill_table(ii, group_axe, infos)
            self.dims.append(infos['size'])

        self.data = buff.buffer
        self.data_valid = True

    def fill_table(self, table, infos):
        """
        Fill in the given table. Axis is the dimension we are processing
        """
        if self.debug > 0:
            print('table', table)
        rows = table.row
        for i in xrange(len(infos)):
            for key in infos[i].keys():
                if key in self.axis_table:
                    rows[key] = infos[i][key]

            rows.append()

        table.flush()

    def create_generic(self, owner=None):
        """
        A table is created with all generic informations about the file : owner, method, HDF5 Release, CreationDate, Last modification
        """
        import time
        self.generic_table = {}
        self.generic_table['Owner'] = tables.StringCol(itemsize=16)
        self.generic_table['Method'] = tables.StringCol(itemsize=16)
        self.generic_table['HDF5_Version'] = tables.StringCol(itemsize=16)
        self.generic_table['Version'] = tables.StringCol(itemsize=16)
        self.generic_table['File_Version'] = tables.StringCol(itemsize=16)
        self.generic_table['Creation_Date'] = tables.StringCol(itemsize=16)
        self.generic_table['Last_Modification_Date'] = tables.StringCol(itemsize=16)
        generic = self.create_table('/', 'generic_table', self.generic_table)
        rows = generic.row
        if owner is None:
            rows['Owner'] = 'Unknown'
        else:
            rows['Owner'] = owner
        rows['Method'] = 'FTICR-MS'
        rows['HDF5_Version'] = tables.hdf5_version
        rows['Version'] = __version__
        rows['File_Version'] = __file_version__
        rows['Creation_Date'] = time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime(os.path.getctime(self.fname)))
        rows['Last_Modification_Date'] = time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime(os.path.getmtime(self.fname)))
        rows.append()
        generic.flush()
        generic.close()

    def create_tables(self):
        """
        Creates the different tables needed in a HDF5File/FTICR  
        """
        self.axis_table = FTICR_AXISvp9

    def position_array--- This code section failed: ---

 L. 463         0  LOAD_FAST                'self'
                2  LOAD_ATTR                debug
                4  LOAD_CONST               1
                6  COMPARE_OP               >
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 463        10  LOAD_GLOBAL              print
               12  LOAD_GLOBAL              type
               14  LOAD_FAST                'self'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

 L. 464        22  LOAD_FAST                'self'
               24  LOAD_ATTR                dim
               26  LOAD_CONST               2
               28  COMPARE_OP               ==
            30_32  POP_JUMP_IF_FALSE   364  'to 364'

 L. 465        34  LOAD_FAST                'self'
               36  LOAD_ATTR                info
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE    66  'to 66'

 L. 466        44  LOAD_FAST                'self'
               46  LOAD_ATTR                info
               48  LOAD_STR                 'Dim1'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'sizeF1'

 L. 467        54  LOAD_FAST                'self'
               56  LOAD_ATTR                info
               58  LOAD_STR                 'Dim2'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'sizeF2'
               64  JUMP_FORWARD         86  'to 86'
             66_0  COME_FROM            42  '42'

 L. 469        66  LOAD_FAST                'self'
               68  LOAD_ATTR                dims
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  STORE_FAST               'sizeF1'

 L. 470        76  LOAD_FAST                'self'
               78  LOAD_ATTR                dims
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  STORE_FAST               'sizeF2'
             86_0  COME_FROM            64  '64'

 L. 471        86  LOAD_FAST                'self'
               88  LOAD_ATTR                debug
               90  LOAD_CONST               0
               92  COMPARE_OP               >
               94  POP_JUMP_IF_FALSE   106  'to 106'

 L. 471        96  LOAD_GLOBAL              print
               98  LOAD_FAST                'sizeF1'
              100  LOAD_FAST                'sizeF2'
              102  CALL_FUNCTION_2       2  '2 positional arguments'
              104  POP_TOP          
            106_0  COME_FROM            94  '94'

 L. 472       106  LOAD_FAST                'self'
              108  LOAD_ATTR                chunks
              110  LOAD_CONST               None
              112  COMPARE_OP               is-not
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L. 473       116  LOAD_FAST                'self'
              118  LOAD_ATTR                chunks
              120  STORE_FAST               'chunks'
              122  JUMP_FORWARD        134  'to 134'
            124_0  COME_FROM           114  '114'

 L. 475       124  LOAD_GLOBAL              determine_chunkshape
              126  LOAD_FAST                'sizeF1'
              128  LOAD_FAST                'sizeF2'
              130  CALL_FUNCTION_2       2  '2 positional arguments'
              132  STORE_FAST               'chunks'
            134_0  COME_FROM           122  '122'

 L. 477       134  LOAD_FAST                'self'
              136  LOAD_ATTR                debug
              138  LOAD_CONST               0
              140  COMPARE_OP               >
              142  POP_JUMP_IF_FALSE   154  'to 154'

 L. 477       144  LOAD_GLOBAL              print
              146  LOAD_STR                 'chunks'
              148  LOAD_FAST                'chunks'
              150  CALL_FUNCTION_2       2  '2 positional arguments'
              152  POP_TOP          
            154_0  COME_FROM           142  '142'

 L. 478       154  LOAD_FAST                'self'
              156  LOAD_ATTR                create_carray
              158  LOAD_STR                 '/'
              160  LOAD_FAST                'group'
              162  BINARY_ADD       
              164  LOAD_STR                 'data'
              166  LOAD_GLOBAL              tables
              168  LOAD_METHOD              Float64Atom
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  LOAD_FAST                'sizeF1'
              174  LOAD_FAST                'sizeF2'
              176  BUILD_TUPLE_2         2 
              178  LOAD_FAST                'chunks'
              180  LOAD_CONST               ('chunk',)
              182  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              184  STORE_FAST               'Carray'

 L. 480       186  LOAD_FAST                'self'
              188  LOAD_ATTR                nparray
              190  LOAD_CONST               None
              192  COMPARE_OP               is-not
          194_196  POP_JUMP_IF_FALSE   260  'to 260'

 L. 481       198  SETUP_LOOP          362  'to 362'
              200  LOAD_GLOBAL              xrange
              202  LOAD_FAST                'sizeF1'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  GET_ITER         
              208  FOR_ITER            256  'to 256'
              210  STORE_FAST               'i1'

 L. 482       212  LOAD_FAST                'self'
              214  LOAD_ATTR                nparray
              216  LOAD_FAST                'i1'
              218  LOAD_CONST               0
              220  LOAD_FAST                'sizeF2'
              222  BUILD_SLICE_2         2 
              224  BUILD_TUPLE_2         2 
              226  BINARY_SUBSCR    
              228  STORE_FAST               'tbuf'

 L. 483       230  LOAD_FAST                'tbuf'
              232  LOAD_CONST               0
              234  LOAD_FAST                'sizeF2'
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  LOAD_FAST                'Carray'
              242  LOAD_FAST                'i1'
              244  LOAD_CONST               0
              246  LOAD_FAST                'sizeF2'
              248  BUILD_SLICE_2         2 
              250  BUILD_TUPLE_2         2 
              252  STORE_SUBSCR     
              254  JUMP_BACK           208  'to 208'
              256  POP_BLOCK        
              258  JUMP_FORWARD        362  'to 362'
            260_0  COME_FROM           194  '194'

 L. 484       260  LOAD_FAST                'self'
              262  LOAD_ATTR                data
              264  LOAD_CONST               None
              266  COMPARE_OP               is-not
          268_270  POP_JUMP_IF_FALSE   490  'to 490'

 L. 485       272  LOAD_FAST                'self'
              274  LOAD_ATTR                debug
              276  LOAD_CONST               1
              278  COMPARE_OP               >
          280_282  POP_JUMP_IF_FALSE   298  'to 298'

 L. 485       284  LOAD_GLOBAL              print
              286  LOAD_GLOBAL              type
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                data
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  POP_TOP          
            298_0  COME_FROM           280  '280'

 L. 486       298  SETUP_LOOP          490  'to 490'
              300  LOAD_GLOBAL              xrange
              302  LOAD_FAST                'sizeF1'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  GET_ITER         
              308  FOR_ITER            360  'to 360'
              310  STORE_FAST               'i1'

 L. 487       312  LOAD_FAST                'self'
              314  LOAD_ATTR                data
              316  LOAD_ATTR                buffer
              318  LOAD_FAST                'i1'
              320  LOAD_CONST               0
              322  LOAD_FAST                'sizeF2'
              324  BUILD_SLICE_2         2 
              326  BUILD_TUPLE_2         2 
              328  BINARY_SUBSCR    
              330  STORE_FAST               'tbuf'

 L. 488       332  LOAD_FAST                'tbuf'
              334  LOAD_CONST               0
              336  LOAD_FAST                'sizeF2'
              338  BUILD_SLICE_2         2 
              340  BINARY_SUBSCR    
              342  LOAD_FAST                'Carray'
              344  LOAD_FAST                'i1'
              346  LOAD_CONST               0
              348  LOAD_FAST                'sizeF2'
              350  BUILD_SLICE_2         2 
              352  BUILD_TUPLE_2         2 
              354  STORE_SUBSCR     
          356_358  JUMP_BACK           308  'to 308'
              360  POP_BLOCK        
            362_0  COME_FROM_LOOP      298  '298'
            362_1  COME_FROM           258  '258'
            362_2  COME_FROM_LOOP      198  '198'
              362  JUMP_FORWARD        490  'to 490'
            364_0  COME_FROM            30  '30'

 L. 489       364  LOAD_FAST                'self'
              366  LOAD_ATTR                dim
              368  LOAD_CONST               1
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   490  'to 490'

 L. 490       376  LOAD_FAST                'self'
              378  LOAD_ATTR                info
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   400  'to 400'

 L. 491       388  LOAD_FAST                'self'
              390  LOAD_ATTR                info
              392  LOAD_STR                 'Dim1'
              394  BINARY_SUBSCR    
              396  STORE_FAST               'sizeF1'
              398  JUMP_FORWARD        410  'to 410'
            400_0  COME_FROM           384  '384'

 L. 493       400  LOAD_FAST                'self'
              402  LOAD_ATTR                dims
              404  LOAD_CONST               0
              406  BINARY_SUBSCR    
              408  STORE_FAST               'sizeF1'
            410_0  COME_FROM           398  '398'

 L. 494       410  LOAD_FAST                'self'
              412  LOAD_METHOD              create_carray
              414  LOAD_STR                 '/'
              416  LOAD_FAST                'group'
              418  BINARY_ADD       
              420  LOAD_STR                 'data'
              422  LOAD_GLOBAL              tables
              424  LOAD_METHOD              Float64Atom
              426  CALL_METHOD_0         0  '0 positional arguments'
              428  LOAD_FAST                'sizeF1'
              430  BUILD_TUPLE_1         1 
              432  CALL_METHOD_4         4  '4 positional arguments'
              434  STORE_FAST               'Carray'

 L. 496       436  LOAD_FAST                'self'
              438  LOAD_ATTR                nparray
              440  LOAD_CONST               None
              442  COMPARE_OP               is-not
          444_446  POP_JUMP_IF_FALSE   464  'to 464'

 L. 497       448  LOAD_FAST                'self'
              450  LOAD_ATTR                nparray
              452  LOAD_CONST               None
              454  LOAD_CONST               None
              456  BUILD_SLICE_2         2 
              458  BINARY_SUBSCR    
              460  STORE_FAST               'Carray'
              462  JUMP_FORWARD        490  'to 490'
            464_0  COME_FROM           444  '444'

 L. 498       464  LOAD_FAST                'self'
              466  LOAD_ATTR                data
              468  LOAD_CONST               None
              470  COMPARE_OP               is-not
          472_474  POP_JUMP_IF_FALSE   490  'to 490'

 L. 499       476  LOAD_FAST                'self'
              478  LOAD_ATTR                nparray
              480  LOAD_CONST               None
              482  LOAD_CONST               None
              484  BUILD_SLICE_2         2 
              486  BINARY_SUBSCR    
              488  STORE_FAST               'Carray'
            490_0  COME_FROM           472  '472'
            490_1  COME_FROM           462  '462'
            490_2  COME_FROM           372  '372'
            490_3  COME_FROM           362  '362'
            490_4  COME_FROM           268  '268'

Parse error at or near `COME_FROM_LOOP' instruction at offset 362_2

    def get_data(self, group='resol1', mode='onfile'):
        """
        loads and returns the FTICRdata attached to the self file
        same parameters as load()
        """
        self.load(group=group, mode=mode)
        return self.data

    def load(self, group='resol1', mode='onfile'):
        """
        loads the data into memory,
        set self.data as a FTICRData 

        group defines which group is loaded (default is resol1)
        mode defines how it is loaded in memory,
            "onfile" (default ) the data is kept on file and loaded only on demand.
                the capability of modifying the data is determined by the way the file was opened
                the data cannot be modified unless the file was opened with access='w' or 'rw'
            "memory" the data is copied to a memroy buffer and can be freely modified
                warning - may saturate the computer memory, there is no control
            if you want to load data into memory after having opened in 'onfile" mode, then do the following :
            h.load(mode="onfile")
            b = d.data.buffer[...]     # data are now copied into a new memory buffer b using ellipsis syntax
            d.data.buffer = b           # and b is used as the data buffer.
        """
        from .. import FTICR
        if self.debug > 0:
            print(group)
        else:
            hfgroup = getattr(self.hf.root, group)
            try:
                hbuf = hfgroup.data
            except:
                raise Exception('File seems to be corrupted, wrong resolution or not a genuine FTICR file.')

            if mode == 'onfile':
                self.data = FTICR.FTICRData(buffer=hbuf)
            else:
                if mode == 'memory':
                    self.data = FTICR.FTICRData(buffer=(hbuf[...]))
                else:
                    raise Exception("wrong mode, only 'onfile' and 'memory' allowed")
        if self.debug > 1:
            print(type(self.data.buffer))
        table = getattr(hfgroup, 'axes')
        values = table.read()
        fields = [i[0] for i in values.dtype.descr]
        for i in range(len(values)):
            if self.debug > 0:
                print('loading axis %d' % i)
            ax = FTICR.FTICRAxis()
            for j in range(len(values[i])):
                vv = values[i][j]
                if isinstance(vv, np.bytes_):
                    vv = vv.decode()
                if vv == 'None':
                    vv = None
                setattr(ax, fields[j], vv)
                if self.debug > 0:
                    print('  %s : %s' % (fields[j], vv))

            if self.correct0p9_0p91:
                if not math.isclose(ax.calibC, 0):
                    ax.calibB *= -1
            setattr(self.data, 'axis%d' % (i + 1), ax)

        self.data.adapt_size()
        try:
            self.data.params = self.retrieve_object('params')
        except:
            if self.debug > 0:
                print('WARNING: %s file does not have the params attribute' % self.fname)

        return self.data

    def get_info(self):
        """
        Retrieve info from self.nparray
        """
        info = {}
        info['Dim'] = len(self.nparray.shape)
        info['Sampling'] = 'Uniform'
        info['Dim1'] = self.nparray.shape[0]
        if info['Dim'] > 1:
            info['Dim2'] = self.nparray.shape[1]
            if info['Dim'] > 2:
                info['Dim3'] = self.nparray.shape[2]
        return info

    def axes_update(self, group='resol1', axis=2, infos=None):
        """routine called when you want to modify the information on a given axis
        group is the group name, default is resol1
        axis is the dimension we want to adjust
        infos is a dictionnary with al fields we want to adjust
        """
        for item in infos:
            self.table_updategroupaxisiteminfos[item]

    def table_update(self, group='resol1', axis=2, key='highmass', value=4000.0):
        """Microchangement in the wanted table"""
        for table in self.hf.walk_nodes('/' + group, 'Table'):
            table.modify_column((axis - 1), column=value, colname=key)

    def save(self, ser_file, group='resol1'):
        """
        save the ser_file to the HDF5 file
        """
        import array
        if sys.maxsize == 2147483647:
            flag = 'l'
        else:
            flag = 'i'
            chunks = self.determine_chunkshape()
        Carray = self.create_carray(('/' + group), 'data', (tables.Float64Atom()), (self.dims[0], self.dims[1]), chunk=chunks)
        with open(ser_file, 'rb') as (f):
            for i1 in xrange(int(self.dims[0])):
                tbuf = f.read(4 * int(self.dims[1]))
                abuf = np.array(array.array(flag, tbuf))
                Carray[i1, 0:int(self.dims[1])] = abuf[0:int(self.dims[1])]

    def save_fticrd(self):
        """
        save the FTICRData to the H5F file
        """
        if not self.data_valid:
            raise Exception('buffer data not set')
        self.position_array()

    def create_from_template(self, data, group='resol1'):
        """
        Take params from the empty FTICR data and put all the informations in the HDF5File
        creates an empty data, and attach it to data.buffer
        data is created in group, with default value 'resol1'
        """
        self.dim = data.dim
        self.create_tables()
        group_resol = self.create_group('/', group)
        table_axes = self.create_table(group_resol, 'axes', self.axis_table)
        infos = []
        self.dims = []
        for i in range(self.dim):
            ii = i + 1
            infos.append(data.axes(ii).__dict__)
            if self.debug > 0:
                print(infos)
            self.dims.append(infos[i]['size'])

        self.fill_table(table_axes, infos)
        self.data = None
        self.position_array('/' + group)
        hfgroup = getattr(self.hf.root, group)
        data.buffer = hfgroup.data
        self.data_valid = True
        data.hdf5file = self

    def create_HDF5_info(self):
        """
        Creates a HDF5 file, takes info as parameter
        """
        self.create_tables()
        self.position_array()

    def create_HDF5_nparray(self):
        """
        Creates a HDF5 file, takes nparray as parameters
        """
        self.info = self.get_info()
        self.create_tables()
        self.position_array()

    def flush(self):
        """
        flushes all nodes but does not close
        """
        if self.debug > 0:
            print('flushing ', self.fname)
        for node in self.hf.walk_nodes('/', 'Table'):
            node.flush()

        for node in self.hf.walk_nodes('/', 'Array'):
            node.flush()

    def close(self):
        """
        Closes HDF5File
        """
        if self.debug > 0:
            print('ABOUT TO CLOSE ', self.fname)
        self.hf.close()
        if self.debug > 0:
            print("IT's CLOSED ", self.fname)

    def create_group(self, where, name):
        """
        Create a group in the given hf_file
        """
        group = self.hf.create_group(where, name)
        return group

    def create_table(self, where, name, description):
        """
        Create a Table in the given hf_file at the given position with the right description
        """
        table = self.hf.create_table(where, name, description)
        return table

    def create_carray(self, where, name, data_type, shape, chunk=None):
        """
        Create a CArray in the given hf_file
        """
        if len(shape) == 2:
            if not chunk:
                chunk = determine_chunkshape(shape[0], shape[1])
        array = self.hf.create_carray(where, name, data_type, shape, chunkshape=chunk, filters=(self.filters))
        return array

    def determine_chunkshape(self, sizeF1=None, sizeF2=None):
        """
        Determine a good chunkshape according to the size of each axis
        """
        if self.info is not None:
            sizeF1 = self.info['Dim1']
            sizeF2 = self.info['Dim2']
        else:
            if sizeF1 is None:
                sizeF1 = self.dims[0]
                sizeF2 = self.dims[1]
        sz12 = float(sizeF2) / float(sizeF1)
        n2 = 1
        n1 = 1024
        while float(n2) / float(n1) < sz12 and n1 > 1:
            n1 = n1 / 2
            n2 = n2 * 2
            if self.debug > 0:
                print('si1 x si2 : %d %d   n1 x n2 : %d %d' % (float(sizeF1), float(sizeF2), n1, n2))

        return (
         n1, n2)

    def get_file_infos(self):
        """
        Read the generic_table and return the informations
        """
        infos = self.hf.root.generic_table.read()
        print('******************* \n %s is a %s file created by %s on %s with file version %s.\n HDF5 version is %s and API version is %s.\n Last modification has been made %s \n********************' % (self.fname, infos[0]['Method'], infos[0]['Owner'], infos[0]['Creation_Date'], infos[0]['File_Version'], infos[0]['HDF5_Version'], infos[0]['Version'], infos[0]['Last_Modification_Date']))


def update(fname, debug=1):
    """update so that the file is up to date"""
    hf = tables.open_file(fname, 'r')
    try:
        infos = hf.root.generic_table.read()
    except:
        raise Exception('The file %s does not seem to be a valid file' % fname)

    info = infos[0]
    fileversion = float(info['File_Version'])
    if debug > 0:
        print('File_Version', fileversion)
    hf.close()
    hf.close()
    if fileversion == float(__file_version__) or fileversion == 0.9:
        print('File is up to date, there is nothing to do')
    if fileversion < 0.6:
        raise Exception('The file %s is from version %s, which is too old to be updated, sorry' % (fname, fileversion))
    if fileversion < 0.7:
        print('updating from 0.6 to 0.7')
        up0p6_to_0p7(fname, debug=debug)
        fileversion = 0.7
    if fileversion < 0.8:
        print('updating from 0.7 to 0.8')
        up0p7_to_0p8(fname, debug=debug)
        fileversion = 0.8
    if fileversion < 0.9:
        print('updating from 0.8 to 0.9')
        up0p8_to_0p9(fname, debug=debug)
        fileversion = 0.9
        print('The file %s has been fully updated to %s' % (fname, __file_version__))


def up0p6_to_0p7(fname, debug=1):
    """docstring for up0p6_to_0p7
    Function that deals with changing HDF5 files created with file_version 0.6 to be read with 0.7
    It modifies 
    """
    import time
    print('modifying dtype of highmass')
    hf = tables.open_file(fname, 'r+')
    for table in hf.walk_nodes('/', 'Table'):
        try:
            table.description.highmass.type = 'float32'
        except:
            print(' no highmass field in this table')

    hf.root.generic_table.modify_column(0, column='0.7', colname='File_Version')
    hf.root.generic_table.modify_column(0, column=(time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime())), colname='Last_Modification_Date')
    hf.close()


def up0p7_to_0p8(fname, debug=1):
    """docstring for up0p7_to_0p8
    Function that deals with changing HDF5 files created with file_version 0.7 to be read with 0.8
    """
    hf = tables.open_file(fname, 'r+')
    description = ''
    for group in hf.iter_nodes('/', 'Group'):
        infos = []
        for table in hf.iter_nodes(group.axes, 'Table'):
            if table.name != 'generic_table':
                infos.append(table.read())
                description = table.description

        hf.remove_node(group, 'axes', True)
        table = hf.create_table(group, 'axes', description)
        for i in xrange(len(infos)):
            infos[i]['sampling'] = 'uniform'
            table.append(infos[i])

        table.flush()
        table.close()

    hf.root.generic_table.modify_column(0, column='0.8', colname='File_Version')
    hf.root.generic_table.modify_column(0, column=(time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime())), colname='Last_Modification_Date')
    if debug > 0:
        print('We have to gather all axes in one table')
    hf.close()


def up0p8_to_0p9(fname, debug=1):
    """
    Function that deals with changing HDF5 files created with file_version 0.8 to be read with 0.9 lib
    """
    hf = tables.open_file(fname, 'r+')
    if '/attached' not in hf:
        hf.create_group('/', 'attached', filters=tables.Filters(complevel=1, complib='zlib'))
        print("Added '/attached' entry")
    for group in hf.iter_nodes('/', 'Group'):
        print('GROUP', group._v_name)
        if group._v_name.startswith('resol'):
            axesv8 = getattr(group, 'axes')
            print(axesv8)
            newaxes = []
            for iax, ax in enumerate(axesv8):
                newax = {}
                sw = axesv8[iax]['specwidth']
                size = axesv8[iax]['size']
                left_point = axesv8[iax]['left_point']
                newax['left_point'] = 0
                newax['offsetfreq'] = left_point * sw / (size - 1 + left_point)
                newax['specwidth'] = sw - newax['offsetfreq']
                newax['calibA'] = axesv8[iax]['ref_mass'] * axesv8[iax]['ref_freq']
                newax['calibB'] = 0.0
                newax['calibC'] = 0.0
                newax['FTICR'] = 'FTICR'
                newax['highfreq'] = newax['specwidth']
                newax['lowfreq'] = newax['calibA'] / axesv8[iax]['highmass']
                for key in ('size', 'highmass', 'itype', 'sampling'):
                    newax[key] = axesv8[iax][key]

                newaxes.append(newax)

            hf.remove_node(group, 'axes', True)
            axtable = hf.create_table(group, 'axes', FTICR_AXISvp9)
            rows = axtable.row
            for ax in newaxes:
                for key in ax.keys():
                    rows[key] = ax[key]

                rows.append()

            axtable.flush()

    hf.root.generic_table.modify_column(0, column='0.9', colname='File_Version')
    hf.root.generic_table.modify_column(0, column=(time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime())), colname='Last_Modification_Date')
    print('file update succesful')
    hf.close()


class HDF5_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This one is called before running all the tests"""
        from ..Tests import filename, directory
        rootfiles = os.getcwd()
        print('Setting up tests')
        cls.TestFolder = directory()
        cls.DataFolder = filename('ubiquitine_2D_000002.d')
        cls.name_file1 = filename('test_file.msh5')
        cls.name_file2 = filename('test_file2.msh5')
        cls.name_chunk = filename('test_chunk.msh5')
        data_init = 10 * np.random.random((2048, 32768))
        threshold = data_init.std()
        data_init[abs(data_init) < threshold] = 0.0
        h5f = HDF5File((cls.name_file1), 'w', nparray=data_init, debug=1, compress=True)
        h5f.close()
        cls.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_get_data(self):
        """Test routine that opens a HDF5 file reading, gets the headers and the buffer"""
        self.announce()
        hdf5 = HDF5File(self.name_file1, 'r')
        hdf5.load()
        B = hdf5.data
        hdf5.close()

    def test_create_from_fticr(self):
        """Test routine that creates a HDF5 file according to a given FTICRData"""
        self.announce()
        from . import Apex as ap
        fticrdata = ap.Import_2D(self.DataFolder)
        h5f = HDF5File((self.name_file2), 'w', fticrd=fticrdata, debug=1, compress=True)
        h5f.close()

    def test_nparray_to_fticr(self):
        """Test routine that creates a HDF5 file according to a given nparray and returns the buffer (FTICRData)"""
        self.announce()
        data_init = 10 * np.random.random((2048, 65536))
        B = nparray_to_fticrd(self.name_file2, data_init)
        print(B.axis1.size)

    def test_axes_update(self):
        """Test routine that overloads the parameter from an axis"""
        from . import Apex as ap
        self.announce()
        import time
        d = HDF5File((self.name_file1), 'rw', debug=1)
        d.axes_update(axis=2, infos={'highmass':4200.0,  'itype':1})
        d.close()

    def _test_chunkshape(self):
        """Test routine that creates , processes Data according to chunkshapes"""
        self.announce()
        from time import time
        from .Apex import Import_2D
        t1 = time()
        d = Import_2D(self.DataFolder, self.name_chunk)
        print('---------------SETTINGS---------------------')
        print('CHUNK_CACHE_PREEMPT ', tables.parameters.CHUNK_CACHE_PREEMPT)
        print('CHUNK_CACHE_SIZE ', tables.parameters.CHUNK_CACHE_SIZE)
        print('METADATA_CACHE_SIZE ', tables.parameters.METADATA_CACHE_SIZE)
        print('NODE_CACHE_SLOTS ', tables.parameters.NODE_CACHE_SLOTS)
        print('---------------SETTINGS---------------------')
        print('import', time() - t1, 'secondes')
        t0 = time()
        t00 = t0
        d.rfft(axis=2)
        print('rfft2', time() - t0, 'secondes')
        t0 = time()
        d.rfft(axis=1)
        print('rfft1', time() - t0, 'secondes')
        t0 = time()
        d.modulus()
        print('modulus', time() - t0, 'secondes')
        print('calcul', time() - t00, 'secondes')

    def test_filenodes(self):
        """Test routines that work with filenodes"""
        self.announce()
        h5f = HDF5File((self.name_file1), 'r+', debug=1)
        obj = ['foo', {'bar': ('baz', None, 1.0, 2)}]
        h5f.store_internal_object(obj, h5name='test')
        name = 'scan.xml'
        fname = os.path.join(self.DataFolder, name)
        h5f.store_internal_file(fname, h5name=name)
        h5f.flush()
        h5f.close()
        h5f = HDF5File((self.name_file1), 'r', debug=1)
        objt = h5f.retrieve_object('test')
        self.assertEqual(objt[1]['bar'][2], 1.0)
        with self.assertRaises(Exception):
            objt2 = h5f.retrieve_object('foo')
        h5f = HDF5File(self.name_file1, 'r')
        F = h5f.open_internal_file(h5name=name)
        for i in range(17):
            l = F.readline()

        print('###', l.strip())
        self.assertEqual(l.strip(), b'<scan><count>15</count><minutes>0.5997</minutes><tic>2.37E7</tic><maxpeak>3.618E6</maxpeak></scan>')
        with self.assertRaises(Exception):
            G = h5f.open_internal_file(h5name='foo.bar')
        F.close()
        h5f.close()
        h5f.close()


def nparray_to_fticrd(name, nparray):
    """
    """
    h5f = HDF5File(name, 'w', None, nparray)
    h5f.get_file_infos()
    h5f.close()
    h5f2 = HDF5File(name, 'r')
    B = h5f2.get_data()
    h5f2.close()
    return B


def syntax(prgm):
    print('\n****** ERROR ******\nUsage:\n{0} Tests               runs self tests\n   or\n{0} update file_name    to update a old file to current\n'.format(prgm))
    sys.exit(1)


if __name__ == '__main__':
    argv = sys.argv
    try:
        action = argv[1]
    except:
        syntax(argv[0])
        sys.exit(0)

    if action == 'update':
        try:
            fname = argv[2]
        except:
            syntax(argv[0])

        update(fname, debug=1)
    else:
        if action == 'Tests':
            print('running tests')
            argv.pop()
            unittest.main()
        else:
            syntax(argv[0])
            sys.exit(1)