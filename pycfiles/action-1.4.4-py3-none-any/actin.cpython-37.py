# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jgsilva/Astrophysics/Packages/ACTIN/actin/actin.py
# Compiled at: 2019-07-08 17:09:37
# Size of source mod 2**32: 12264 bytes
from __future__ import print_function
from __future__ import division
import sys, os, glob, time, datetime, numpy as np
import astropy.io.fits as pyfits
import argparse, pkg_resources, appdirs
path = os.path.dirname(os.path.realpath(__file__))
actin_files_dir = os.path.join(path, 'actin_files')
sys.path.append(actin_files_dir)
import ac_settings as ac_set, ac_config, ac_read_data, ac_get_win, ac_calc_ind, ac_save, ac_plot_time as ac_plot, ac_tools
from matplotlib import pylab as plt
ac_set.init()
config_file = os.path.join(path, 'config_lines.txt')
version_file = os.path.join(path, 'VERSION')
version = ac_set.preamble(version_file)

def actin_file(file, calc_index=None, rv_in=None, config_file=config_file, save_output=False, ln_plts=False, obj_name=None, targ_list=None, del_out=False, frac=True):
    """
    Runs ACTIN for one fits file.
    Accepts files of types: 'S2D', 'S1D', 'e2ds', 's1d', 's1d_*_rv', 'ADP', and 'rdb'.
    Recognizes fits files from HARPS, HARPS-N and ESPRESSO instruments.
    """
    print()
    print('--------------------')
    print('EXECUTING ACTIN_FILE')
    print('--------------------')
    if type(file) is list:
        file = file[0]
    tel, instr = ac_tools.get_instr(file)
    if instr == False:
        pass
    else:
        if instr in ac_set.instr:
            pass
        else:
            msg = "*** ERROR:\nUnrecognized instrument. ACTIN only accepts HARPS, HARPS-N or ESPRESSO. To read from a different instrument convert data to rdb file with the headers: 'obj', 'obs_date', 'bjd', 'wave', 'flux', 'error_pixel' (optional)."
            sys.exit(msg)
        if targ_list:
            check = ac_tools.check_targ(file, targets=targ_list)
            if check is True:
                pass
            elif check is False:
                return
        if calc_index:
            sel_lines = ac_config.read_conf(config_file, calc_index)
        else:
            data = ac_read_data.read_data(file, rv_in=rv_in, obj_name=obj_name)
            if not data:
                return
            if save_output is not False:
                if data['file_type'] != 'rdb':
                    dupl = ac_save.check_duplicate(data['obj'], data['obs_date'], data['instr'], data['file_type'], save_output)
                    if dupl is True:
                        return
                else:
                    if calc_index:
                        test = ac_calc_ind.check_lines(data['wave'], sel_lines)
                        if not test:
                            print('*** ACTION: Ignoring measurement.')
                            return
                        sel_lines = ac_calc_ind.calc_flux_lines(data, sel_lines, ln_plts=ln_plts, frac=frac)
                        index = ac_calc_ind.calc_ind(sel_lines)
                    index = calc_index or None
                    sel_lines = None
                if save_output is not False:
                    rdb_file = ac_save.save_data(data, index, out_dir=save_output)
            else:
                rdb_file = None
        info = {}
        info['config_file'] = config_file
        info['file_type'] = data['file_type']
        info['version'] = version
        info['source_path'] = os.path.split(file)[0]
        info['tel'] = data['tel']
        info['instr'] = data['instr']
        info['obj'] = data['obj']
        options = {}
        options['frac'] = frac
        output = {}
        output['data'] = data
        output['index'] = index
        output['sel_lines'] = sel_lines
        output['info'] = info
        output['options'] = options
        output['rdb_file'] = rdb_file
        return output


def actin--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL              print
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 147         6  LOAD_GLOBAL              print
                8  LOAD_STR                 '----------------'
               10  CALL_FUNCTION_1       1  ''
               12  POP_TOP          

 L. 148        14  LOAD_GLOBAL              print
               16  LOAD_STR                 ' STARTING ACTIN '
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 149        22  LOAD_GLOBAL              print
               24  LOAD_STR                 '----------------'
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L. 151        30  LOAD_GLOBAL              time
               32  LOAD_METHOD              time
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'start_time'

 L. 154        38  LOAD_FAST                'config_file'
               40  LOAD_CONST               None
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 155        46  LOAD_GLOBAL              get_config
               48  CALL_FUNCTION_0       0  ''
               50  STORE_FAST               'cfg_file'
               52  JUMP_FORWARD         58  'to 58'
             54_0  COME_FROM            44  '44'

 L. 157        54  LOAD_FAST                'config_file'
               56  STORE_FAST               'cfg_file'
             58_0  COME_FROM            52  '52'

 L. 158        58  LOAD_GLOBAL              print
               60  CALL_FUNCTION_0       0  ''
               62  POP_TOP          

 L. 159        64  LOAD_GLOBAL              print
               66  LOAD_STR                 'Using spectral lines from configuration file:'
               68  CALL_FUNCTION_1       1  ''
               70  POP_TOP          

 L. 160        72  LOAD_GLOBAL              print
               74  LOAD_FAST                'cfg_file'
               76  CALL_FUNCTION_1       1  ''
               78  POP_TOP          

 L. 164        80  LOAD_FAST                'test'
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L. 165        84  LOAD_GLOBAL              ac_tools
               86  LOAD_METHOD              test_actin
               88  LOAD_FAST                'test'
               90  LOAD_GLOBAL              path
               92  LOAD_FAST                'calc_index'
               94  CALL_METHOD_3         3  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'calc_index'
              100  STORE_FAST               'files'
            102_0  COME_FROM            82  '82'

 L. 167       102  LOAD_FAST                'files'
              104  POP_JUMP_IF_TRUE    114  'to 114'

 L. 168       106  LOAD_GLOBAL              sys
              108  LOAD_METHOD              exit
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          
            114_0  COME_FROM           104  '104'

 L. 171       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'files'
              118  LOAD_GLOBAL              str
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_FALSE   130  'to 130'

 L. 171       124  LOAD_FAST                'files'
              126  BUILD_LIST_1          1 
              128  STORE_FAST               'files'
            130_0  COME_FROM           122  '122'

 L. 173       130  LOAD_FAST                'rv_in'
              132  LOAD_CONST               None
              134  COMPARE_OP               is
              136  POP_JUMP_IF_FALSE   154  'to 154'

 L. 174       138  LOAD_FAST                'rv_in'
              140  BUILD_LIST_1          1 
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'files'
              146  CALL_FUNCTION_1       1  ''
              148  BINARY_MULTIPLY  
              150  STORE_FAST               'rv_in'
              152  JUMP_FORWARD        178  'to 178'
            154_0  COME_FROM           136  '136'

 L. 175       154  LOAD_GLOBAL              type
              156  LOAD_FAST                'rv_in'
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_GLOBAL              list
              162  COMPARE_OP               is-not
              164  POP_JUMP_IF_FALSE   178  'to 178'

 L. 176       166  LOAD_GLOBAL              float
              168  LOAD_FAST                'rv_in'
              170  CALL_FUNCTION_1       1  ''
              172  BUILD_LIST_1          1 
              174  STORE_FAST               'rv_in'
              176  JUMP_FORWARD        178  'to 178'
            178_0  COME_FROM           176  '176'
            178_1  COME_FROM           164  '164'
            178_2  COME_FROM           152  '152'

 L. 180       178  LOAD_GLOBAL              ac_tools
              180  LOAD_METHOD              check_files
              182  LOAD_FAST                'files'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 183       188  LOAD_FAST                'del_out'
          190_192  POP_JUMP_IF_FALSE   416  'to 416'

 L. 184       194  LOAD_GLOBAL              print
              196  CALL_FUNCTION_0       0  ''
              198  POP_TOP          

 L. 185       200  LOAD_GLOBAL              print
              202  LOAD_STR                 'Executing ac_tools.remove_output:'
              204  CALL_FUNCTION_1       1  ''
              206  POP_TOP          

 L. 186       208  LOAD_GLOBAL              print
              210  LOAD_STR                 'Searching output files to delete...'
              212  CALL_FUNCTION_1       1  ''
              214  POP_TOP          

 L. 188       216  LOAD_FAST                'obj_name'
          218_220  POP_JUMP_IF_FALSE   344  'to 344'

 L. 189       222  SETUP_LOOP          416  'to 416'
              224  LOAD_FAST                'files'
              226  GET_ITER         
            228_0  COME_FROM           304  '304'
              228  FOR_ITER            340  'to 340'
              230  STORE_FAST               'f'

 L. 190       232  LOAD_GLOBAL              ac_tools
              234  LOAD_METHOD              get_instr
              236  LOAD_FAST                'f'
              238  CALL_METHOD_1         1  ''
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               '_'
              244  STORE_FAST               'instr'

 L. 191       246  LOAD_GLOBAL              ac_tools
              248  LOAD_METHOD              get_file_type
              250  LOAD_FAST                'f'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'file_type'

 L. 192       256  LOAD_GLOBAL              isinstance
              258  LOAD_FAST                'obj_name'
              260  LOAD_GLOBAL              str
              262  CALL_FUNCTION_2       2  ''
          264_266  POP_JUMP_IF_FALSE   290  'to 290'

 L. 193       268  LOAD_FAST                'obj_name'
              270  STORE_FAST               'star_name'

 L. 194       272  LOAD_GLOBAL              ac_tools
              274  LOAD_METHOD              remove_output2
              276  LOAD_FAST                'star_name'
              278  LOAD_FAST                'instr'
              280  LOAD_FAST                'file_type'
              282  LOAD_FAST                'save_output'
              284  CALL_METHOD_4         4  ''
              286  POP_TOP          
              288  JUMP_BACK           228  'to 228'
            290_0  COME_FROM           264  '264'

 L. 195       290  LOAD_GLOBAL              isinstance
              292  LOAD_FAST                'obj_name'
              294  LOAD_GLOBAL              list
              296  LOAD_GLOBAL              np
              298  LOAD_ATTR                ndarray
              300  BUILD_TUPLE_2         2 
              302  CALL_FUNCTION_2       2  ''
              304  POP_JUMP_IF_FALSE   228  'to 228'

 L. 196       306  SETUP_LOOP          338  'to 338'
              308  LOAD_FAST                'obj_name'
              310  GET_ITER         
              312  FOR_ITER            336  'to 336'
              314  STORE_FAST               'star_name'

 L. 197       316  LOAD_GLOBAL              ac_tools
              318  LOAD_METHOD              remove_output2
              320  LOAD_FAST                'star_name'
              322  LOAD_FAST                'instr'
              324  LOAD_FAST                'file_type'
              326  LOAD_FAST                'save_output'
              328  CALL_METHOD_4         4  ''
              330  POP_TOP          
          332_334  JUMP_BACK           312  'to 312'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      306  '306'
              338  JUMP_BACK           228  'to 228'
              340  POP_BLOCK        
              342  JUMP_FORWARD        416  'to 416'
            344_0  COME_FROM           218  '218'

 L. 198       344  LOAD_FAST                'obj_name'
          346_348  POP_JUMP_IF_TRUE    416  'to 416'

 L. 199       350  SETUP_LOOP          416  'to 416'
              352  LOAD_FAST                'files'
              354  GET_ITER         
              356  FOR_ITER            414  'to 414'
              358  STORE_FAST               'f'

 L. 200       360  LOAD_GLOBAL              ac_tools
              362  LOAD_METHOD              get_target
              364  LOAD_FAST                'f'
              366  CALL_METHOD_1         1  ''
              368  STORE_FAST               'star_name'

 L. 201       370  LOAD_GLOBAL              ac_tools
              372  LOAD_METHOD              get_instr
              374  LOAD_FAST                'f'
              376  CALL_METHOD_1         1  ''
              378  UNPACK_SEQUENCE_2     2 
              380  STORE_FAST               '_'
              382  STORE_FAST               'instr'

 L. 202       384  LOAD_GLOBAL              ac_tools
              386  LOAD_METHOD              get_file_type
              388  LOAD_FAST                'f'
              390  CALL_METHOD_1         1  ''
              392  STORE_FAST               'file_type'

 L. 203       394  LOAD_GLOBAL              ac_tools
              396  LOAD_METHOD              remove_output2
              398  LOAD_FAST                'star_name'
              400  LOAD_FAST                'instr'
              402  LOAD_FAST                'file_type'
              404  LOAD_FAST                'save_output'
              406  CALL_METHOD_4         4  ''
              408  POP_TOP          
          410_412  JUMP_BACK           356  'to 356'
              414  POP_BLOCK        
            416_0  COME_FROM_LOOP      350  '350'
            416_1  COME_FROM           346  '346'
            416_2  COME_FROM           342  '342'
            416_3  COME_FROM_LOOP      222  '222'
            416_4  COME_FROM           190  '190'

 L. 206       416  LOAD_FAST                'ln_plts'
              418  LOAD_STR                 'same'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   430  'to 430'

 L. 207       426  LOAD_FAST                'save_output'
              428  STORE_FAST               'ln_plts'
            430_0  COME_FROM           422  '422'

 L. 209       430  LOAD_GLOBAL              len
              432  LOAD_FAST                'files'
              434  CALL_FUNCTION_1       1  ''
              436  STORE_FAST               'total_files'

 L. 212       438  LOAD_GLOBAL              ac_tools
              440  LOAD_METHOD              files_by_star_and_ftype
              442  LOAD_FAST                'files'
              444  CALL_METHOD_1         1  ''
              446  STORE_FAST               'files_list'

 L. 214       448  LOAD_CONST               0
              450  STORE_FAST               'n_files_t'

 L. 216   452_454  SETUP_LOOP          720  'to 720'
              456  LOAD_GLOBAL              range
              458  LOAD_GLOBAL              len
              460  LOAD_FAST                'files_list'
              462  CALL_FUNCTION_1       1  ''
              464  CALL_FUNCTION_1       1  ''
              466  GET_ITER         
              468  FOR_ITER            718  'to 718'
              470  STORE_FAST               'k'

 L. 218       472  SETUP_LOOP          714  'to 714'
              474  LOAD_GLOBAL              range
              476  LOAD_GLOBAL              len
              478  LOAD_FAST                'files_list'
              480  LOAD_FAST                'k'
              482  BINARY_SUBSCR    
              484  CALL_FUNCTION_1       1  ''
              486  CALL_FUNCTION_1       1  ''
              488  GET_ITER         
            490_0  COME_FROM           592  '592'
              490  FOR_ITER            712  'to 712'
              492  STORE_FAST               'i'

 L. 219       494  LOAD_CONST               0
              496  STORE_FAST               'n_files'

 L. 221       498  SETUP_LOOP          590  'to 590'
              500  LOAD_GLOBAL              range
              502  LOAD_GLOBAL              len
              504  LOAD_FAST                'files_list'
              506  LOAD_FAST                'k'
              508  BINARY_SUBSCR    
              510  LOAD_FAST                'i'
              512  BINARY_SUBSCR    
              514  CALL_FUNCTION_1       1  ''
              516  CALL_FUNCTION_1       1  ''
              518  GET_ITER         
              520  FOR_ITER            588  'to 588'
              522  STORE_FAST               'j'

 L. 222       524  LOAD_FAST                'n_files'
              526  LOAD_CONST               1
              528  INPLACE_ADD      
              530  STORE_FAST               'n_files'

 L. 223       532  LOAD_FAST                'n_files_t'
              534  LOAD_CONST               1
              536  INPLACE_ADD      
              538  STORE_FAST               'n_files_t'

 L. 225       540  LOAD_GLOBAL              actin_file
              542  LOAD_FAST                'files_list'
              544  LOAD_FAST                'k'
              546  BINARY_SUBSCR    
              548  LOAD_FAST                'i'
              550  BINARY_SUBSCR    
              552  LOAD_FAST                'j'
              554  BINARY_SUBSCR    

 L. 226       556  LOAD_FAST                'calc_index'

 L. 227       558  LOAD_FAST                'rv_in'
              560  LOAD_FAST                'j'
              562  BINARY_SUBSCR    

 L. 228       564  LOAD_FAST                'cfg_file'

 L. 229       566  LOAD_FAST                'save_output'

 L. 230       568  LOAD_FAST                'ln_plts'

 L. 231       570  LOAD_FAST                'obj_name'

 L. 232       572  LOAD_FAST                'targ_list'

 L. 233       574  LOAD_FAST                'del_out'

 L. 234       576  LOAD_FAST                'frac'
              578  LOAD_CONST               ('rv_in', 'config_file', 'save_output', 'ln_plts', 'obj_name', 'targ_list', 'del_out', 'frac')
              580  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
              582  STORE_FAST               'output'
          584_586  JUMP_BACK           520  'to 520'
              588  POP_BLOCK        
            590_0  COME_FROM_LOOP      498  '498'

 L. 237       590  LOAD_FAST                'output'
          592_594  POP_JUMP_IF_FALSE   490  'to 490'

 L. 239       596  LOAD_FAST                'output'
              598  LOAD_STR                 'sel_lines'
              600  BINARY_SUBSCR    
              602  STORE_FAST               'sel_lines'

 L. 240       604  LOAD_FAST                'output'
              606  LOAD_STR                 'info'
              608  BINARY_SUBSCR    
              610  STORE_FAST               'info'

 L. 241       612  LOAD_FAST                'output'
              614  LOAD_STR                 'options'
              616  BINARY_SUBSCR    
              618  STORE_FAST               'options'

 L. 242       620  LOAD_FAST                'output'
              622  LOAD_STR                 'rdb_file'
              624  BINARY_SUBSCR    
              626  STORE_FAST               'rdb_file'

 L. 245       628  LOAD_GLOBAL              ac_save
              630  LOAD_ATTR                save_log
              632  LOAD_FAST                'info'
              634  LOAD_FAST                'options'
              636  LOAD_FAST                'n_files'
              638  LOAD_FAST                'save_output'
              640  LOAD_CONST               ('out_dir',)
              642  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              644  POP_TOP          

 L. 246       646  LOAD_GLOBAL              ac_save
              648  LOAD_ATTR                save_line_info
              650  LOAD_FAST                'info'
              652  LOAD_FAST                'sel_lines'
              654  LOAD_FAST                'save_output'
              656  LOAD_CONST               ('out_dir',)
              658  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              660  POP_TOP          

 L. 248       662  LOAD_FAST                'save_plots'
          664_666  POP_JUMP_IF_FALSE   708  'to 708'

 L. 250       668  LOAD_GLOBAL              ac_plot
              670  LOAD_ATTR                plt_time
              672  LOAD_FAST                'info'
              674  LOAD_FAST                'save_output'
              676  LOAD_CONST               False
              678  LOAD_CONST               True
              680  LOAD_CONST               ('out_dir', 'rmv_flgs', 'save_plt')
              682  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              684  POP_TOP          

 L. 251       686  LOAD_GLOBAL              ac_plot
              688  LOAD_ATTR                plt_time_mlty
              690  LOAD_FAST                'info'
              692  LOAD_FAST                'save_output'
              694  LOAD_CONST               False
              696  LOAD_CONST               True
              698  LOAD_FAST                'calc_index'
              700  LOAD_CONST               ('out_dir', 'rmv_flgs', 'save_plt', 'hdrs')
              702  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              704  POP_TOP          
              706  JUMP_BACK           490  'to 490'
            708_0  COME_FROM           664  '664'

 L. 252   708_710  JUMP_BACK           490  'to 490'
              712  POP_BLOCK        
            714_0  COME_FROM_LOOP      472  '472'
          714_716  JUMP_BACK           468  'to 468'
              718  POP_BLOCK        
            720_0  COME_FROM_LOOP      452  '452'

 L. 254       720  LOAD_FAST                'n_files_t'
              722  LOAD_FAST                'total_files'
              724  COMPARE_OP               !=
          726_728  POP_JUMP_IF_FALSE   764  'to 764'

 L. 255       730  LOAD_GLOBAL              print
              732  CALL_FUNCTION_0       0  ''
              734  POP_TOP          

 L. 256       736  LOAD_GLOBAL              print
              738  LOAD_STR                 '*** ERROR: Number of ACTIN calls different than number of files.'
              740  CALL_FUNCTION_1       1  ''
              742  POP_TOP          

 L. 257       744  LOAD_GLOBAL              print
              746  LOAD_STR                 'n_files_t:'
              748  LOAD_FAST                'n_files_t'
              750  CALL_FUNCTION_2       2  ''
              752  POP_TOP          

 L. 258       754  LOAD_GLOBAL              print
              756  LOAD_STR                 'total_files:'
              758  LOAD_FAST                'total_files'
              760  CALL_FUNCTION_2       2  ''
              762  POP_TOP          
            764_0  COME_FROM           726  '726'

 L. 260       764  LOAD_GLOBAL              time
              766  LOAD_METHOD              time
              768  CALL_METHOD_0         0  ''
              770  LOAD_FAST                'start_time'
              772  BINARY_SUBTRACT  
              774  LOAD_CONST               60
              776  BINARY_TRUE_DIVIDE
              778  STORE_FAST               'elapsed_time'

 L. 263       780  LOAD_GLOBAL              print
              782  LOAD_STR                 '\n---------------------------------'
              784  CALL_FUNCTION_1       1  ''
              786  POP_TOP          

 L. 264       788  LOAD_GLOBAL              print
              790  LOAD_STR                 'Fractional pixels:\t{}'
              792  LOAD_METHOD              format
              794  LOAD_FAST                'frac'
              796  CALL_METHOD_1         1  ''
              798  CALL_FUNCTION_1       1  ''
              800  POP_TOP          

 L. 265       802  LOAD_GLOBAL              print
              804  LOAD_STR                 'Files analysed:\t\t{}'
              806  LOAD_METHOD              format
              808  LOAD_FAST                'total_files'
              810  CALL_METHOD_1         1  ''
              812  CALL_FUNCTION_1       1  ''
              814  POP_TOP          

 L. 266       816  LOAD_GLOBAL              print
              818  LOAD_STR                 'Save output:\t\t{}'
              820  LOAD_METHOD              format
              822  LOAD_FAST                'save_output'
              824  CALL_METHOD_1         1  ''
              826  CALL_FUNCTION_1       1  ''
              828  POP_TOP          

 L. 267       830  LOAD_GLOBAL              print
              832  LOAD_STR                 'Elapsed time:\t\t{:.4f} min'
              834  LOAD_METHOD              format
              836  LOAD_FAST                'elapsed_time'
              838  CALL_METHOD_1         1  ''
              840  CALL_FUNCTION_1       1  ''
              842  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 840


def get_config():
    """
    Check for existence of ACTIN folder and config file and creates them if not present. Returns the path to the config file.
    """
    cfg_dir = appdirs.user_config_dir('ACTIN')
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)
    cfg_file = os.path.join(cfg_dir, 'config_lines.txt')
    if not os.path.isfile(cfg_file):
        create_user_config(cfg_file)
    return cfg_file


def create_user_config(cfg_file):
    """
    Create the user's config file
    """
    from shutil import copyfile
    src = pkg_resources.resource_stream(__name__, 'config_lines.txt')
    copyfilesrc.namecfg_file


def main():
    """
    Main function, call actin function with arguments from terminal.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', '-f', help='Read file(s)', nargs='+')
    parser.add_argument('--calc_index', '-i', help="Index id to calculate as designated by 'ind_id' in config_index.txt.", nargs='+', default=None)
    parser.add_argument('--rv_in', '-rv', help='RV value to calibrate wavelength. If False (default) try to read RV from CCF file.', nargs='+', default=None, type=float)
    parser.add_argument('--config_file', '-cf', help='Path to config_file, or False (default) read config file from standard directory.', default=None)
    parser.add_argument('--save_output', '-s', help='Path to output directory of data table, or False (default).', default=False)
    parser.add_argument('--ln_plts', '-lp', help="Path to directory to save line plots. If 'same' saves line plots to same directory of data output. If 'show' only shows the plots. If 'False' (default) does not save or show line plots", default=False)
    parser.add_argument('--obj_name', '-obj', help='Give target a name that overides the one from the fits files.', default=None)
    parser.add_argument('--targ_list', '-tl', help='Give a list of stars to select from fits files.', nargs='+', default=None)
    parser.add_argument('--del_out', '-del', help='Delete output data file if True.', default=False, type=(lambda x: str(x).lower() == 'true'))
    parser.add_argument('--test', '-t', help='Tests actin using the provided fits files in the "test_files" directory. Options are "e2ds", "s1d", and "adp"', default=False)
    parser.add_argument('--frac', '-frc', help='Turns fractional pixel on (True, default) or off (False).', default=True, type=(lambda x: str(x).lower() == 'true'))
    parser.add_argument('--save_plots', '-sp', help="If True saves time-series and multi-plots to same directory as 'save_output'.", default=False, type=(lambda x: str(x).lower() == 'true'))
    args = parser.parse_args()
    actin(files=(args.files), calc_index=(args.calc_index),
      rv_in=(args.rv_in),
      config_file=(args.config_file),
      save_output=(args.save_output),
      ln_plts=(args.ln_plts),
      obj_name=(args.obj_name),
      targ_list=(args.targ_list),
      del_out=(args.del_out),
      test=(args.test),
      frac=(args.frac),
      save_plots=(args.save_plots))


if __name__ == '__main__':
    main()