# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fabric/contrib/xfiles/reader.py
# Compiled at: 2010-03-14 15:52:30
"""
:copyright: Copyright 2009 by Juha Mustonen, see AUTHORS.
:license: MIT, see LICENSE for details.
"""
import re
from fnmatch import fnmatch
import os, tempfile, shutil
from xml.etree import ElementTree
from fabric import api as fapi

class RXMLReader(object):
    """
  XMLReader for remote files, using
  Fabric

  .. code-block:: python

    from fabric.contrib.xfiles import reader
    rxr = reader.RXMLReader()
    rxr.open('/tmp/document.xml')
    rxr.query('/root/path/items')
    # do something with the result set
    rxr.close()

  """

    def __init__(self):
        super(RXMLReader, self).__init__()
        self.etree = None
        self.lpath = None
        return

    def open(self, rpath):
        """
    Reads the XML document from remote
    location and stores the parsed document
    into ``self.etree``

    rpath
      Path in server, to remote XML file
    returns
      Object itself
    """
        self.lpath = self._get(rpath)
        et = ElementTree.ElementTree()
        self.etree = et.parse(self.lpath)
        return self

    def query--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL           0  'False'
                3  STORE_FAST            2  'onlyroot'

 L.  67         6  LOAD_CONST               None
                9  STORE_FAST            3  'path'

 L.  68        12  LOAD_CONST               None
               15  STORE_FAST            4  'sel_name'

 L.  69        18  LOAD_CONST               None
               21  STORE_FAST            5  'sel_value'

 L.  70        24  LOAD_CONST               None
               27  STORE_FAST            6  'sel_text'

 L.  72        30  BUILD_LIST_0          0 
               33  STORE_FAST            7  'values'

 L.  73        36  LOAD_FAST             1  'query'
               39  LOAD_ATTR             2  'strip'
               42  CALL_FUNCTION_0       0  None
               45  STORE_FAST            1  'query'

 L.  77        48  LOAD_FAST             1  'query'
               51  LOAD_ATTR             3  'startswith'
               54  LOAD_CONST               '/'
               57  CALL_FUNCTION_1       1  None
               60  JUMP_IF_FALSE        88  'to 151'
             63_0  THEN                     152
               63  POP_TOP          

 L.  78        64  LOAD_FAST             1  'query'
               67  STORE_FAST            8  'org_query'

 L.  81        70  LOAD_FAST             1  'query'
               73  LOAD_ATTR             4  'rfind'
               76  LOAD_CONST               '/'
               79  CALL_FUNCTION_1       1  None
               82  LOAD_CONST               1
               85  COMPARE_OP            4  >
               88  JUMP_IF_FALSE        40  'to 131'
             91_0  THEN                     148
               91  POP_TOP          

 L.  82        92  LOAD_GLOBAL           5  're'
               95  LOAD_ATTR             6  'compile'
               98  LOAD_CONST               '^\\/\\w*\\/*'
              101  CALL_FUNCTION_1       1  None
              104  STORE_FAST            9  'rootx'

 L.  83       107  LOAD_FAST             9  'rootx'
              110  LOAD_ATTR             7  'sub'
              113  LOAD_CONST               ''
              116  LOAD_FAST             1  'query'
              119  LOAD_CONST               1
              122  CALL_FUNCTION_3       3  None
              125  STORE_FAST            1  'query'
              128  JUMP_ABSOLUTE       152  'to 152'
            131_0  COME_FROM            88  '88'
              131  POP_TOP          

 L.  87       132  LOAD_GLOBAL           8  'True'
              135  STORE_FAST            2  'onlyroot'

 L.  88       138  LOAD_FAST             1  'query'
              141  LOAD_CONST               1
              144  SLICE+1          
              145  STORE_FAST            1  'query'
              148  JUMP_FORWARD          1  'to 152'
            151_0  COME_FROM            60  '60'
              151  POP_TOP          
            152_0  COME_FROM           148  '148'

 L. 104       152  LOAD_GLOBAL           5  're'
              155  LOAD_ATTR             9  'VERBOSE'
              158  LOAD_GLOBAL           5  're'
              161  LOAD_ATTR            10  'UNICODE'
              164  BINARY_OR        
              165  LOAD_GLOBAL           5  're'
              168  LOAD_ATTR            11  'IGNORECASE'
              171  BINARY_OR        
              172  STORE_FAST           10  'rflags'

 L. 107       175  LOAD_GLOBAL           5  're'
              178  LOAD_ATTR             6  'compile'
              181  LOAD_CONST               '(?P<path>(\\w|\\/)+)(\\[@?(?P<name>(\\w|\\*|-|\\?)+)(=(?P<value>.*(?=\\])))?\\])?(=(?P<text>.*))?'
              184  LOAD_FAST            10  'rflags'
              187  CALL_FUNCTION_2       2  None
              190  STORE_FAST           11  'atrx'

 L. 110       193  LOAD_FAST            11  'atrx'
              196  LOAD_ATTR            12  'search'
              199  LOAD_FAST             1  'query'
              202  CALL_FUNCTION_1       1  None
              205  STORE_FAST           12  'm'

 L. 111       208  LOAD_FAST            12  'm'
              211  JUMP_IF_FALSE        88  'to 302'
            214_0  THEN                     303
              214  POP_TOP          

 L. 112       215  LOAD_FAST            12  'm'
              218  LOAD_ATTR            13  'groupdict'
              221  CALL_FUNCTION_0       0  None
              224  STORE_FAST           13  'gd'

 L. 113       227  LOAD_FAST            13  'gd'
              230  LOAD_ATTR            14  'get'
              233  LOAD_CONST               'path'
              236  LOAD_CONST               None
              239  CALL_FUNCTION_2       2  None
              242  STORE_FAST            3  'path'

 L. 114       245  LOAD_FAST            13  'gd'
              248  LOAD_ATTR            14  'get'
              251  LOAD_CONST               'name'
              254  LOAD_CONST               None
              257  CALL_FUNCTION_2       2  None
              260  STORE_FAST            4  'sel_name'

 L. 115       263  LOAD_FAST            13  'gd'
              266  LOAD_ATTR            14  'get'
              269  LOAD_CONST               'value'
              272  LOAD_CONST               None
              275  CALL_FUNCTION_2       2  None
              278  STORE_FAST            5  'sel_value'

 L. 116       281  LOAD_FAST            13  'gd'
              284  LOAD_ATTR            14  'get'
              287  LOAD_CONST               'text'
              290  LOAD_CONST               None
              293  CALL_FUNCTION_2       2  None
              296  STORE_FAST            6  'sel_text'
              299  JUMP_FORWARD          1  'to 303'
            302_0  COME_FROM           211  '211'
              302  POP_TOP          
            303_0  COME_FROM           299  '299'

 L. 118       303  LOAD_FAST             3  'path'
              306  JUMP_IF_TRUE         16  'to 325'
            309_0  THEN                     326
              309  POP_TOP          

 L. 119       310  LOAD_GLOBAL          15  'Exception'
              313  LOAD_CONST               'Regexp matching failed, check the format'
              316  CALL_FUNCTION_1       1  None
              319  RAISE_VARARGS_1       1  None
              322  JUMP_FORWARD          1  'to 326'
            325_0  COME_FROM           306  '306'
              325  POP_TOP          
            326_0  COME_FROM           322  '322'

 L. 124       326  LOAD_FAST             0  'self'
              329  LOAD_ATTR            16  'etree'
              332  LOAD_CONST               None
              335  COMPARE_OP            9  is-not
              338  JUMP_IF_FALSE       297  'to 638'
              341  POP_TOP          

 L. 127       342  LOAD_FAST             0  'self'
              345  LOAD_ATTR            16  'etree'
              348  LOAD_ATTR            17  'findall'
              351  LOAD_FAST             3  'path'
              354  CALL_FUNCTION_1       1  None
              357  STORE_FAST           14  'elems'

 L. 131       360  LOAD_FAST             2  'onlyroot'
              363  JUMP_IF_FALSE        19  'to 385'
            366_0  THEN                     386
              366  POP_TOP          

 L. 132       367  LOAD_FAST             0  'self'
              370  LOAD_ATTR            16  'etree'
              373  LOAD_ATTR            18  'getiterator'
              376  CALL_FUNCTION_0       0  None
              379  STORE_FAST           14  'elems'
              382  JUMP_FORWARD          1  'to 386'
            385_0  COME_FROM           363  '363'
              385  POP_TOP          
            386_0  COME_FROM           382  '382'

 L. 134       386  SETUP_LOOP          250  'to 639'
              389  LOAD_FAST            14  'elems'
              392  GET_ITER         
              393  FOR_ITER            238  'to 634'
              396  STORE_FAST           15  'elem'

 L. 136       399  LOAD_FAST             6  'sel_text'
              402  JUMP_IF_FALSE        28  'to 433'
            405_0  THEN                     434
              405  POP_TOP          

 L. 138       406  LOAD_GLOBAL          19  'fnmatch'
              409  LOAD_FAST            15  'elem'
              412  LOAD_ATTR            20  'text'
              415  LOAD_FAST             6  'sel_text'
              418  CALL_FUNCTION_2       2  None
              421  JUMP_IF_TRUE          5  'to 429'
            424_0  THEN                     430
              424  POP_TOP          

 L. 139       425  BREAK_LOOP       
              426  JUMP_ABSOLUTE       434  'to 434'
            429_0  COME_FROM           421  '421'
              429  POP_TOP          
              430  JUMP_FORWARD          1  'to 434'
            433_0  COME_FROM           402  '402'
              433  POP_TOP          
            434_0  COME_FROM           430  '430'

 L. 143       434  LOAD_FAST             4  'sel_name'
              437  JUMP_IF_FALSE       177  'to 617'
              440  POP_TOP          

 L. 145       441  BUILD_LIST_0          0 
              444  DUP_TOP          
              445  STORE_FAST           16  '_[1]'
              448  LOAD_FAST            15  'elem'
              451  LOAD_ATTR            21  'keys'
              454  CALL_FUNCTION_0       0  None
              457  GET_ITER         
              458  FOR_ITER             33  'to 494'
              461  STORE_FAST           17  'k'
              464  LOAD_GLOBAL          19  'fnmatch'
              467  LOAD_FAST            17  'k'
              470  LOAD_FAST             4  'sel_name'
              473  CALL_FUNCTION_2       2  None
              476  JUMP_IF_FALSE        11  'to 490'
              479  POP_TOP          
              480  LOAD_FAST            16  '_[1]'
              483  LOAD_FAST             4  'sel_name'
              486  LIST_APPEND      
              487  JUMP_BACK           458  'to 458'
            490_0  COME_FROM           476  '476'
              490  POP_TOP          
              491  JUMP_BACK           458  'to 458'
              494  DELETE_FAST          16  '_[1]'
              497  JUMP_IF_FALSE       113  'to 613'
              500  POP_TOP          

 L. 147       501  LOAD_FAST             5  'sel_value'
              504  JUMP_IF_FALSE        89  'to 596'
              507  POP_TOP          

 L. 151       508  SETUP_LOOP           99  'to 610'
              511  LOAD_FAST            15  'elem'
              514  LOAD_ATTR            21  'keys'
              517  CALL_FUNCTION_0       0  None
              520  GET_ITER         
              521  FOR_ITER             68  'to 592'
              524  STORE_FAST           18  'attr'

 L. 152       527  LOAD_GLOBAL          19  'fnmatch'
              530  LOAD_FAST            18  'attr'
              533  LOAD_FAST             4  'sel_name'
              536  CALL_FUNCTION_2       2  None
              539  JUMP_IF_FALSE        46  'to 588'
              542  POP_TOP          

 L. 153       543  LOAD_GLOBAL          19  'fnmatch'
              546  LOAD_FAST            15  'elem'
              549  LOAD_ATTR            14  'get'
              552  LOAD_FAST            18  'attr'
              555  CALL_FUNCTION_1       1  None
              558  LOAD_FAST             5  'sel_value'
              561  CALL_FUNCTION_2       2  None
              564  JUMP_IF_FALSE        17  'to 584'
              567  POP_TOP          

 L. 154       568  LOAD_FAST             7  'values'
              571  LOAD_ATTR            22  'append'
              574  LOAD_FAST            15  'elem'
              577  CALL_FUNCTION_1       1  None
              580  POP_TOP          
              581  JUMP_ABSOLUTE       589  'to 589'
            584_0  COME_FROM           564  '564'
              584  POP_TOP          
              585  JUMP_BACK           521  'to 521'
            588_0  COME_FROM           539  '539'
              588  POP_TOP          
              589  JUMP_BACK           521  'to 521'
              592  POP_BLOCK        
              593  JUMP_ABSOLUTE       614  'to 614'
            596_0  COME_FROM           504  '504'
              596  POP_TOP          

 L. 158       597  LOAD_FAST             7  'values'
              600  LOAD_ATTR            22  'append'
              603  LOAD_FAST            15  'elem'
              606  CALL_FUNCTION_1       1  None
              609  POP_TOP          
            610_0  COME_FROM           508  '508'
              610  JUMP_ABSOLUTE       631  'to 631'
            613_0  COME_FROM           497  '497'
              613  POP_TOP          
              614  JUMP_BACK           393  'to 393'
            617_0  COME_FROM           437  '437'
              617  POP_TOP          

 L. 162       618  LOAD_FAST             7  'values'
              621  LOAD_ATTR            22  'append'
              624  LOAD_FAST            15  'elem'
              627  CALL_FUNCTION_1       1  None
              630  POP_TOP          
              631  JUMP_BACK           393  'to 393'
              634  POP_BLOCK        
              635  JUMP_FORWARD          1  'to 639'
            638_0  COME_FROM           338  '338'
              638  POP_TOP          
            639_0  COME_FROM           386  '386'

 L. 164       639  LOAD_FAST             7  'values'
              642  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 610

    def close(self):
        """
    Closes the reader.
    Deletes the local, temporary XML document
    """
        if self.lpath:
            os.remove(self.lpath)

    def _get(self, rpath):
        """
    Retrieves the remote file based on given
    remotepath ``rpath`` to local, temporary location.

    .. NOTE:: The temp file needs to be removed manually

    rpath
      Path to XML file in remote server
    returns
      Absolute path to local, temporary file
    """
        (fd, lpath) = tempfile.mkstemp(suffix='xfiles')
        if not fapi.env.host_string or fapi.env.host_string.lower() in ('localhost',
                                                                        '127.0.0.1'):
            shutil.copy(os.path.abspath(rpath), lpath)
        else:
            fapi.get(rpath, lpath)
        if len(set(fapi.env.hosts)) > 1:
            lpath = '%s.%s' % (lpath, fapi.env.host_string)
        return lpath