# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/database.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 11576 bytes
__doc__ = '\nThis module contains classes, functions, and methods for reading input files\nand assembling database entries for use by pyEQL.\n\nBy default, pyEQL searches all files in the /database subdirectory for parameters.\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
import logging
from pyEQL.logging_system import Unique
import pyEQL.parameter as pm
import os
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Paramsdb:
    """Paramsdb"""

    def __init__(self):
        self.parameters_database = {}
        self.database_dir = [
         os.path.dirname(__file__) + '/database']

    def add_path(self, path):
        """
        Add a user-defined directory to the database search path
        """
        self.database_dir.append(path)

    def list_path(self):
        """
        List all search paths for database files
        """
        for path in self.database_dir:
            print(path)

    def search_parameters--- This code section failed: ---

 L.  84         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         pyEQL.chemical_formula
                6  IMPORT_FROM              chemical_formula
                8  STORE_FAST               'chem'
               10  POP_TOP          

 L.  88        12  LOAD_FAST                'formula'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                parameters_database
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.  89     22_24  JUMP_FORWARD        564  'to 564'
             26_0  COME_FROM            20  '20'

 L.  92        26  LOAD_GLOBAL              set
               28  CALL_FUNCTION_0       0  ''
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                parameters_database
               34  LOAD_FAST                'formula'
               36  STORE_SUBSCR     

 L.  95        38  LOAD_FAST                'self'
               40  LOAD_ATTR                database_dir
               42  GET_ITER         
            44_46  FOR_ITER            564  'to 564'
               48  STORE_FAST               'directory'

 L.  96        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              listdir
               54  LOAD_FAST                'directory'
               56  CALL_METHOD_1         1  ''
               58  GET_ITER         
             60_0  COME_FROM            86  '86'
            60_62  FOR_ITER            562  'to 562'
               64  STORE_FAST               'file'

 L.  98        66  LOAD_CONST               0
               68  STORE_FAST               'line_num'

 L. 101        70  LOAD_FAST                'file'
               72  LOAD_STR                 'template.tsv'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    80  'to 80'

 L. 102        78  JUMP_BACK            60  'to 60'
             80_0  COME_FROM            76  '76'

 L. 105        80  LOAD_STR                 '.tsv'
               82  LOAD_FAST                'file'
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE    60  'to 60'

 L. 108        88  LOAD_GLOBAL              open
               90  LOAD_FAST                'directory'
               92  LOAD_STR                 '/'
               94  BINARY_ADD       
               96  LOAD_FAST                'file'
               98  BINARY_ADD       
              100  LOAD_STR                 'r'
              102  CALL_FUNCTION_2       2  ''
              104  STORE_FAST               'current_file'

 L. 111   106_108  SETUP_FINALLY       516  'to 516'

 L. 112       110  LOAD_FAST                'current_file'
              112  GET_ITER         
          114_116  FOR_ITER            512  'to 512'
              118  STORE_FAST               'line'

 L. 114       120  LOAD_FAST                'line_num'
              122  LOAD_CONST               1
              124  INPLACE_ADD      
              126  STORE_FAST               'line_num'

 L. 116   128_130  SETUP_FINALLY       466  'to 466'

 L. 119       132  LOAD_STR                 'Name'
              134  LOAD_FAST                'line'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   156  'to 156'

 L. 120       140  LOAD_GLOBAL              _parse_line
              142  LOAD_FAST                'line'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_CONST               1
              148  BINARY_SUBSCR    
              150  STORE_FAST               'param_name'
          152_154  JUMP_FORWARD        462  'to 462'
            156_0  COME_FROM           138  '138'

 L. 122       156  LOAD_STR                 'Description'
              158  LOAD_FAST                'line'
              160  COMPARE_OP               in
              162  POP_JUMP_IF_FALSE   180  'to 180'

 L. 123       164  LOAD_GLOBAL              _parse_line
              166  LOAD_FAST                'line'
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  STORE_FAST               'param_desc'
          176_178  JUMP_FORWARD        462  'to 462'
            180_0  COME_FROM           162  '162'

 L. 125       180  LOAD_STR                 'Unit'
              182  LOAD_FAST                'line'
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 126       188  LOAD_GLOBAL              _parse_line
              190  LOAD_FAST                'line'
              192  CALL_FUNCTION_1       1  ''
              194  LOAD_CONST               1
              196  BINARY_SUBSCR    
              198  STORE_FAST               'param_unit'
          200_202  JUMP_FORWARD        462  'to 462'
            204_0  COME_FROM           186  '186'

 L. 128       204  LOAD_STR                 'Reference'
              206  LOAD_FAST                'line'
              208  COMPARE_OP               in
              210  POP_JUMP_IF_FALSE   226  'to 226'

 L. 129       212  LOAD_GLOBAL              _parse_line
              214  LOAD_FAST                'line'
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_CONST               1
              220  BINARY_SUBSCR    
              222  STORE_FAST               'param_ref'
              224  JUMP_FORWARD        462  'to 462'
            226_0  COME_FROM           210  '210'

 L. 131       226  LOAD_STR                 'Temperature'
              228  LOAD_FAST                'line'
              230  COMPARE_OP               in
              232  POP_JUMP_IF_FALSE   248  'to 248'

 L. 132       234  LOAD_GLOBAL              _parse_line
              236  LOAD_FAST                'line'
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  STORE_FAST               'param_temp'
              246  JUMP_FORWARD        462  'to 462'
            248_0  COME_FROM           232  '232'

 L. 134       248  LOAD_STR                 'Pressure'
              250  LOAD_FAST                'line'
              252  COMPARE_OP               in
          254_256  POP_JUMP_IF_FALSE   272  'to 272'

 L. 135       258  LOAD_GLOBAL              _parse_line
              260  LOAD_FAST                'line'
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_CONST               1
              266  BINARY_SUBSCR    
              268  STORE_FAST               'param_press'
              270  JUMP_FORWARD        462  'to 462'
            272_0  COME_FROM           254  '254'

 L. 137       272  LOAD_STR                 'Ionic Strength'
              274  LOAD_FAST                'line'
              276  COMPARE_OP               in
          278_280  POP_JUMP_IF_FALSE   296  'to 296'

 L. 138       282  LOAD_GLOBAL              _parse_line
              284  LOAD_FAST                'line'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_CONST               1
              290  BINARY_SUBSCR    
              292  STORE_FAST               'param_ionic'
              294  JUMP_FORWARD        462  'to 462'
            296_0  COME_FROM           278  '278'

 L. 140       296  LOAD_STR                 'Comment'
              298  LOAD_FAST                'line'
              300  COMPARE_OP               in
          302_304  POP_JUMP_IF_FALSE   320  'to 320'

 L. 141       306  LOAD_GLOBAL              _parse_line
              308  LOAD_FAST                'line'
              310  CALL_FUNCTION_1       1  ''
              312  LOAD_CONST               1
              314  BINARY_SUBSCR    
              316  STORE_FAST               'param_comment'
              318  JUMP_FORWARD        462  'to 462'
            320_0  COME_FROM           302  '302'

 L. 148       320  LOAD_FAST                'chem'
              322  LOAD_METHOD              is_valid_formula
              324  LOAD_GLOBAL              _parse_line
              326  LOAD_FAST                'line'
              328  CALL_FUNCTION_1       1  ''
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
              334  CALL_METHOD_1         1  ''
          336_338  POP_JUMP_IF_FALSE   462  'to 462'

 L. 149       340  LOAD_FAST                'chem'
              342  LOAD_METHOD              hill_order
              344  LOAD_FAST                'formula'
              346  CALL_METHOD_1         1  ''
              348  LOAD_FAST                'chem'
              350  LOAD_METHOD              hill_order

 L. 150       352  LOAD_GLOBAL              _parse_line
              354  LOAD_FAST                'line'
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_CONST               0
              360  BINARY_SUBSCR    

 L. 149       362  CALL_METHOD_1         1  ''
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   462  'to 462'

 L. 154       370  LOAD_GLOBAL              len
              372  LOAD_GLOBAL              _parse_line
              374  LOAD_FAST                'line'
              376  CALL_FUNCTION_1       1  ''
              378  CALL_FUNCTION_1       1  ''
              380  LOAD_CONST               2
              382  COMPARE_OP               >
          384_386  POP_JUMP_IF_FALSE   406  'to 406'

 L. 155       388  LOAD_GLOBAL              _parse_line
              390  LOAD_FAST                'line'
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_CONST               1
              396  LOAD_CONST               None
              398  BUILD_SLICE_2         2 
              400  BINARY_SUBSCR    
              402  STORE_FAST               'param_value'
              404  JUMP_FORWARD        418  'to 418'
            406_0  COME_FROM           384  '384'

 L. 157       406  LOAD_GLOBAL              _parse_line
              408  LOAD_FAST                'line'
              410  CALL_FUNCTION_1       1  ''
              412  LOAD_CONST               1
              414  BINARY_SUBSCR    
              416  STORE_FAST               'param_value'
            418_0  COME_FROM           404  '404'

 L. 160       418  LOAD_GLOBAL              pm
              420  LOAD_ATTR                Parameter

 L. 161       422  LOAD_FAST                'param_name'

 L. 162       424  LOAD_FAST                'param_value'

 L. 163       426  LOAD_FAST                'param_unit'

 L. 164       428  LOAD_FAST                'param_ref'

 L. 165       430  LOAD_FAST                'param_press'

 L. 166       432  LOAD_FAST                'param_temp'

 L. 167       434  LOAD_FAST                'param_ionic'

 L. 168       436  LOAD_FAST                'param_desc'

 L. 169       438  LOAD_FAST                'param_comment'

 L. 160       440  LOAD_CONST               ('reference', 'pressure', 'temperature', 'ionic_strength', 'description', 'comment')
              442  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              444  STORE_FAST               'parameter'

 L. 173       446  LOAD_FAST                'self'
              448  LOAD_ATTR                parameters_database
              450  LOAD_FAST                'formula'
              452  BINARY_SUBSCR    
              454  LOAD_METHOD              add

 L. 174       456  LOAD_FAST                'parameter'

 L. 173       458  CALL_METHOD_1         1  ''
              460  POP_TOP          
            462_0  COME_FROM           366  '366'
            462_1  COME_FROM           336  '336'
            462_2  COME_FROM           318  '318'
            462_3  COME_FROM           294  '294'
            462_4  COME_FROM           270  '270'
            462_5  COME_FROM           246  '246'
            462_6  COME_FROM           224  '224'
            462_7  COME_FROM           200  '200'
            462_8  COME_FROM           176  '176'
            462_9  COME_FROM           152  '152'
              462  POP_BLOCK        
              464  JUMP_BACK           114  'to 114'
            466_0  COME_FROM_FINALLY   128  '128'

 L. 177       466  DUP_TOP          
              468  LOAD_GLOBAL              ValueError
              470  COMPARE_OP               exception-match
          472_474  POP_JUMP_IF_FALSE   508  'to 508'
              476  POP_TOP          
              478  POP_TOP          
              480  POP_TOP          

 L. 178       482  LOAD_GLOBAL              logger
              484  LOAD_METHOD              warning

 L. 179       486  LOAD_STR                 'Error encountered when reading line %s in %s'

 L. 180       488  LOAD_FAST                'line_num'
              490  LOAD_FAST                'file'
              492  BUILD_TUPLE_2         2 

 L. 179       494  BINARY_MODULO    

 L. 178       496  CALL_METHOD_1         1  ''
              498  POP_TOP          

 L. 182       500  POP_EXCEPT       
              502  JUMP_BACK           114  'to 114'
              504  POP_EXCEPT       
              506  JUMP_BACK           114  'to 114'
            508_0  COME_FROM           472  '472'
              508  END_FINALLY      
              510  JUMP_BACK           114  'to 114'
              512  POP_BLOCK        
              514  JUMP_FORWARD        552  'to 552'
            516_0  COME_FROM_FINALLY   106  '106'

 L. 185       516  DUP_TOP          
              518  LOAD_GLOBAL              UnicodeDecodeError
              520  COMPARE_OP               exception-match
          522_524  POP_JUMP_IF_FALSE   550  'to 550'
              526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          

 L. 186       532  LOAD_GLOBAL              logger
              534  LOAD_METHOD              warning

 L. 187       536  LOAD_STR                 'Invalid character found when reading %s. File skipped.'

 L. 188       538  LOAD_FAST                'file'

 L. 187       540  BINARY_MODULO    

 L. 186       542  CALL_METHOD_1         1  ''
              544  POP_TOP          
              546  POP_EXCEPT       
              548  JUMP_FORWARD        552  'to 552'
            550_0  COME_FROM           522  '522'
              550  END_FINALLY      
            552_0  COME_FROM           548  '548'
            552_1  COME_FROM           514  '514'

 L. 191       552  LOAD_FAST                'current_file'
              554  LOAD_METHOD              close
              556  CALL_METHOD_0         0  ''
              558  POP_TOP          
              560  JUMP_BACK            60  'to 60'
              562  JUMP_BACK            44  'to 44'
            564_0  COME_FROM            22  '22'

Parse error at or near `POP_EXCEPT' instruction at offset 504

    def has_parameter--- This code section failed: ---

 L. 199         0  LOAD_FAST                'self'
                2  LOAD_METHOD              has_species
                4  LOAD_FAST                'formula'
                6  CALL_METHOD_1         1  ''
                8  LOAD_CONST               False
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 200        14  LOAD_FAST                'self'
               16  LOAD_METHOD              search_parameters
               18  LOAD_FAST                'formula'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
             24_0  COME_FROM            12  '12'

 L. 202        24  LOAD_CONST               False
               26  STORE_FAST               'found'

 L. 204        28  SETUP_FINALLY        72  'to 72'

 L. 205        30  LOAD_FAST                'self'
               32  LOAD_ATTR                parameters_database
               34  LOAD_FAST                'formula'
               36  BINARY_SUBSCR    
               38  GET_ITER         
             40_0  COME_FROM            54  '54'
               40  FOR_ITER             66  'to 66'
               42  STORE_FAST               'item'

 L. 206        44  LOAD_FAST                'item'
               46  LOAD_METHOD              get_name
               48  CALL_METHOD_0         0  ''
               50  LOAD_FAST                'name'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    40  'to 40'

 L. 207        56  LOAD_CONST               True
               58  STORE_FAST               'found'
               60  CONTINUE             40  'to 40'

 L. 209        62  CONTINUE             40  'to 40'
               64  JUMP_BACK            40  'to 40'

 L. 211        66  LOAD_FAST                'found'
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    28  '28'

 L. 213        72  DUP_TOP          
               74  LOAD_GLOBAL              KeyError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   106  'to 106'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 214        86  LOAD_GLOBAL              logger
               88  LOAD_METHOD              error
               90  LOAD_STR                 'Species %s not found in database'
               92  LOAD_FAST                'formula'
               94  BINARY_MODULO    
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 215       100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            78  '78'
              106  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 68

    def get_parameter--- This code section failed: ---

 L. 221         0  LOAD_CONST               False
                2  STORE_FAST               'found'

 L. 223         4  SETUP_FINALLY        74  'to 74'

 L. 224         6  LOAD_FAST                'self'
                8  LOAD_ATTR                parameters_database
               10  LOAD_FAST                'formula'
               12  BINARY_SUBSCR    
               14  GET_ITER         
             16_0  COME_FROM            30  '30'
               16  FOR_ITER             48  'to 48'
               18  STORE_FAST               'item'

 L. 225        20  LOAD_FAST                'item'
               22  LOAD_METHOD              get_name
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'name'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    16  'to 16'

 L. 226        32  LOAD_CONST               True
               34  STORE_FAST               'found'

 L. 227        36  LOAD_FAST                'item'
               38  ROT_TWO          
               40  POP_TOP          
               42  POP_BLOCK        
               44  RETURN_VALUE     
               46  JUMP_BACK            16  'to 16'

 L. 229        48  LOAD_FAST                'found'
               50  POP_JUMP_IF_TRUE     70  'to 70'

 L. 230        52  LOAD_GLOBAL              logger
               54  LOAD_METHOD              error

 L. 231        56  LOAD_STR                 'Parameter %s for species %s not found in database'

 L. 232        58  LOAD_FAST                'name'
               60  LOAD_FAST                'formula'
               62  BUILD_TUPLE_2         2 

 L. 231        64  BINARY_MODULO    

 L. 230        66  CALL_METHOD_1         1  ''
               68  POP_TOP          
             70_0  COME_FROM            50  '50'
               70  POP_BLOCK        
               72  JUMP_FORWARD        110  'to 110'
             74_0  COME_FROM_FINALLY     4  '4'

 L. 235        74  DUP_TOP          
               76  LOAD_GLOBAL              KeyError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   108  'to 108'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 236        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              error
               92  LOAD_STR                 'Species %s not found in database'
               94  LOAD_FAST                'formula'
               96  BINARY_MODULO    
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 237       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            80  '80'
              108  END_FINALLY      
            110_0  COME_FROM            72  '72'

Parse error at or near `POP_BLOCK' instruction at offset 42

    def add_parameter(self, formula, parameter):
        """
        Add a parameter to the database
        """
        self.parameters_database[formula].add(parameter)

    def has_species(self, formula):
        """
        Boolean test to determine whether a species is present in the database
        """
        if formula in self.parameters_database:
            return True
        return False

    def print_database(self, solute=None):
        """ Function to generate a human-friendly summary of all the database parameters
        that are actually used in the simulation

        Parameters
        ----------
        solute : str, optional
                The chemical formula for a species. If this argument of supplied, the output
                will contain only the database entries for this species. Otherwise,
                all database entries will be printed.

        """
        if solute is not None:
            try:
                key = solute
                print('Parameters for species %s:' % key)
                print('--------------------------\n')
                for item in self.parameters_database[key]:
                    print(item)

            except KeyError:
                print('Species %s not found in database.' % solute)

        else:
            for key in self.parameters_database.keys():
                print('Parameters for species %s:' % key)
                print('--------------------------\n')
                for item in self.parameters_database[key]:
                    print(item)


def _parse_line(line):
    """
    Function to parse lines in a tab-seprated value file format.

    This function accepts a string (a line read from a tab-separated
    input file). It removes the newline character and splits the string
    at each tab stop, returning a list of the remaining substrings in which each
    list entry corresponds to the contents of one cell in the file.

    """
    line = line.replace('\n', '')
    str_list = line.split('\t')
    return str_list