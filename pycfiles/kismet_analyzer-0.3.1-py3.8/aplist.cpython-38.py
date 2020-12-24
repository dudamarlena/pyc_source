# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kismetanalyzer/aplist.py
# Compiled at: 2020-02-07 16:56:45
# Size of source mod 2**32: 7990 bytes
from __future__ import print_function
import argparse, json, sqlite3, sys
from fastkml import kml, styles
from pygeoif import geometry
from kismetanalyzer.model import AccessPoint
from kismetanalyzer.util import does_ssid_matches

def get_description(ap):
    """
    This fuction is used to create the description string for the device.
    
    :param ap: instance of kismetanalzer.model.AccessPoint class
    
    :return: A string which can be used as description for the device
    :rtype string
    """
    clients = '\n'.join(ap.client_map)
    desc = 'MAC: {0}\nEncryption: {1}\nFrequency: {2}\nChannel: {3}\nManufacturer: {4}\n\nClients:\n{5}'
    description = desc.format(ap.mac, ap.encryption, ap.frequency, ap.channel, ap.manufacturer, clients)
    return description


def get_networkcolor(encryption):
    """
    This fuction is used to get color for a network which will be added 
    to a KML-File.s
    
    :param encryption: encryption string 
    
    :return: Color to use for the network
    :rtype simplekml.Color
    """
    if 'WPA' in encryption:
        return 'ff008000'
    if 'WEP' in encryption:
        return 'ff00a5ff'
    if 'Open' in encryption:
        return 'ff0000ff'
    return 'ff00ffff'


def export_csv(filename, devices, delimiter=';'):
    """
    Export found devices to a CSV file. The filename prefix and the list 
    of devices is required. The delimiter is optional.
    
    :param filename: Prefix for the filename. The extention "csv" will be added
    :param devices: list of devices. Each device must be a tuple with 
                    the followin format (lon, lat, mac, title, encryption, description )
    :param delimiter: Delimiter to use for separation of columns (optional)
    """
    import csv
    num_plotted = 0
    outfile = '{0}.csv'.format(filename)
    with open(outfile, mode='w') as (csv_file):
        w = csv.writer(csv_file, delimiter=delimiter, quotechar='"', quoting=(csv.QUOTE_MINIMAL))
        w.writerow(['MAC-Address', 'SSID', 'Encryption', 'Frequency', 'Channel', 'Manufacturer'])
        for dev in devices:
            w.writerow([dev.mac, dev.ssid, dev.encryption, dev.frequency, dev.channel, dev.manufacturer])
            num_plotted = num_plotted + 1

    print('Exported {} devices to {}'.format(num_plotted, outfile))


def export_kml(filename, title, devices):
    """
    Export found devices to a KML file which can be imported to Googleearth.
    The filename prefix and the list of devices is required.

    :param filename: Prefix for the filename. The extention "kml" will be added
    :param title: name which will be added to kml file
    :param devices: list of devices. Each device must be a tuple in the following format (lon, lat, mac, title, encryption, description )
   """
    num_plotted = 0
    outfile = '{0}.kml'.format(filename)
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    doc = kml.Document(ns, 'docid', title, '')
    k.append(doc)
    for dev in devices:
        icon_style = styles.IconStyle(ns=ns, color=(get_networkcolor(dev.encryption)))
        style = styles.Style(ns=ns, styles=[icon_style])
        desc = get_description(dev)
        p = kml.Placemark(name=(dev.ssid), description=desc, styles=[style])
        p.geometry = geometry.Point(dev.location.lon, dev.location.lat, dev.location.alt)
        doc.append(p)
        num_plotted = num_plotted + 1
    else:
        with open(outfile, 'w') as (f):
            s = str(k.to_string(prettyprint=True))
            f.write(s)
        print('Exported {} devices to {}'.format(num_plotted, outfile))


def gen_aplist--- This code section failed: ---

 L. 124         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_STR                 'List access points discovered by kismet.'
                6  LOAD_CONST               ('description',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L. 125        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '--in'
               18  LOAD_STR                 'store'
               20  LOAD_STR                 'infile'
               22  LOAD_CONST               True
               24  LOAD_STR                 'Input file (.kismet)'
               26  LOAD_CONST               ('action', 'dest', 'required', 'help')
               28  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               30  POP_TOP          

 L. 126        32  LOAD_FAST                'parser'
               34  LOAD_ATTR                add_argument
               36  LOAD_STR                 '--out'
               38  LOAD_STR                 'store'
               40  LOAD_STR                 'outfile'
               42  LOAD_STR                 'Output filename (optional)'
               44  LOAD_CONST               ('action', 'dest', 'help')
               46  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               48  POP_TOP          

 L. 127        50  LOAD_FAST                'parser'
               52  LOAD_ATTR                add_argument
               54  LOAD_STR                 '--title'
               56  LOAD_STR                 'store'
               58  LOAD_STR                 'title'
               60  LOAD_STR                 'Kismet'
               62  LOAD_STR                 'Title embedded in KML file'
               64  LOAD_CONST               ('action', 'dest', 'default', 'help')
               66  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               68  POP_TOP          

 L. 128        70  LOAD_FAST                'parser'
               72  LOAD_ATTR                add_argument
               74  LOAD_STR                 '--ssid'
               76  LOAD_STR                 'store'
               78  LOAD_STR                 'ssid'
               80  LOAD_STR                 'Only plot networks which match the SSID (or SSID regex)'
               82  LOAD_CONST               ('action', 'dest', 'help')
               84  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               86  POP_TOP          

 L. 129        88  LOAD_FAST                'parser'
               90  LOAD_ATTR                add_argument
               92  LOAD_STR                 '--exclude-ssid'
               94  LOAD_STR                 'store'
               96  LOAD_STR                 'excludessid'
               98  LOAD_STR                 'Exclude networks which match the SSID (or SSID regex)'
              100  LOAD_CONST               ('action', 'dest', 'help')
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  POP_TOP          

 L. 130       106  LOAD_FAST                'parser'
              108  LOAD_ATTR                add_argument
              110  LOAD_STR                 '--strongest-point'
              112  LOAD_STR                 'store_true'
              114  LOAD_STR                 'strongest'
              116  LOAD_CONST               False
              118  LOAD_STR                 'Plot points based on strongest signal'
              120  LOAD_CONST               ('action', 'dest', 'default', 'help')
              122  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              124  POP_TOP          

 L. 131       126  LOAD_FAST                'parser'
              128  LOAD_ATTR                add_argument
              130  LOAD_STR                 '--encryption'
              132  LOAD_STR                 'store'
              134  LOAD_STR                 'encryption'
              136  LOAD_CONST               None
              138  LOAD_STR                 'Show only networks with given encryption type'
              140  LOAD_CONST               ('action', 'dest', 'default', 'help')
              142  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              144  POP_TOP          

 L. 132       146  LOAD_FAST                'parser'
              148  LOAD_ATTR                add_argument
              150  LOAD_STR                 '--csv'
              152  LOAD_STR                 'store_true'
              154  LOAD_STR                 'csv'
              156  LOAD_CONST               False
              158  LOAD_STR                 'Export results to csv'
              160  LOAD_CONST               ('action', 'dest', 'default', 'help')
              162  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              164  POP_TOP          

 L. 133       166  LOAD_FAST                'parser'
              168  LOAD_ATTR                add_argument
              170  LOAD_STR                 '--kml'
              172  LOAD_STR                 'store_true'
              174  LOAD_STR                 'kml'
              176  LOAD_CONST               False
              178  LOAD_STR                 'Export results to kml'
              180  LOAD_CONST               ('action', 'dest', 'default', 'help')
              182  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              184  POP_TOP          

 L. 134       186  LOAD_FAST                'parser'
              188  LOAD_ATTR                add_argument
              190  LOAD_STR                 '--verbose'
              192  LOAD_STR                 'store_true'
              194  LOAD_STR                 'verbose'
              196  LOAD_CONST               False
              198  LOAD_STR                 'Print MAC, SSID, encryption type to stdout'
              200  LOAD_CONST               ('action', 'dest', 'default', 'help')
              202  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              204  POP_TOP          

 L. 135       206  LOAD_FAST                'parser'
              208  LOAD_METHOD              parse_args
              210  CALL_METHOD_0         0  ''
              212  STORE_FAST               'parameters'

 L. 139       214  LOAD_FAST                'parameters'
              216  LOAD_ATTR                outfile
              218  LOAD_CONST               None
              220  COMPARE_OP               is
          222_224  POP_JUMP_IF_FALSE   266  'to 266'

 L. 140       226  LOAD_FAST                'parameters'
              228  LOAD_ATTR                infile
              230  LOAD_METHOD              endswith
              232  LOAD_STR                 '.kismet'
              234  CALL_METHOD_1         1  ''
          236_238  POP_JUMP_IF_FALSE   258  'to 258'

 L. 141       240  LOAD_FAST                'parameters'
              242  LOAD_ATTR                infile
              244  LOAD_CONST               None
              246  LOAD_CONST               -7
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  LOAD_FAST                'parameters'
              254  STORE_ATTR               outfile
              256  JUMP_FORWARD        266  'to 266'
            258_0  COME_FROM           236  '236'

 L. 143       258  LOAD_FAST                'parameters'
              260  LOAD_ATTR                infile
              262  LOAD_FAST                'parameters'
              264  STORE_ATTR               outfile
            266_0  COME_FROM           256  '256'
            266_1  COME_FROM           222  '222'

 L. 145       266  SETUP_FINALLY       284  'to 284'

 L. 146       268  LOAD_GLOBAL              sqlite3
              270  LOAD_METHOD              connect
              272  LOAD_FAST                'parameters'
              274  LOAD_ATTR                infile
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'db'
              280  POP_BLOCK        
              282  JUMP_FORWARD        344  'to 344'
            284_0  COME_FROM_FINALLY   266  '266'

 L. 147       284  DUP_TOP          
              286  LOAD_GLOBAL              Exception
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   342  'to 342'
              294  POP_TOP          
              296  STORE_FAST               'e'
              298  POP_TOP          
              300  SETUP_FINALLY       330  'to 330'

 L. 148       302  LOAD_GLOBAL              print
              304  LOAD_STR                 'Failed to open kismet logfile: {0}'
              306  LOAD_METHOD              format
              308  LOAD_FAST                'e'
              310  CALL_METHOD_1         1  ''
              312  CALL_FUNCTION_1       1  ''
              314  POP_TOP          

 L. 149       316  LOAD_GLOBAL              sys
              318  LOAD_METHOD              exit
              320  LOAD_CONST               1
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
              326  POP_BLOCK        
              328  BEGIN_FINALLY    
            330_0  COME_FROM_FINALLY   300  '300'
              330  LOAD_CONST               None
              332  STORE_FAST               'e'
              334  DELETE_FAST              'e'
              336  END_FINALLY      
              338  POP_EXCEPT       
              340  JUMP_FORWARD        344  'to 344'
            342_0  COME_FROM           290  '290'
              342  END_FINALLY      
            344_0  COME_FROM           340  '340'
            344_1  COME_FROM           282  '282'

 L. 151       344  SETUP_FINALLY       372  'to 372'

 L. 152       346  LOAD_STR                 "SELECT * FROM devices where type='Wi-Fi AP'; "
              348  STORE_FAST               'sql'

 L. 153       350  LOAD_FAST                'db'
              352  LOAD_METHOD              cursor
              354  CALL_METHOD_0         0  ''
              356  STORE_FAST               'c'

 L. 154       358  LOAD_FAST                'c'
              360  LOAD_METHOD              execute
              362  LOAD_FAST                'sql'
              364  CALL_METHOD_1         1  ''
              366  STORE_FAST               'sql_result'
              368  POP_BLOCK        
              370  JUMP_FORWARD        400  'to 400'
            372_0  COME_FROM_FINALLY   344  '344'

 L. 155       372  POP_TOP          
              374  POP_TOP          
              376  POP_TOP          

 L. 156       378  LOAD_GLOBAL              print
              380  LOAD_STR                 'Failed to extract data from database'
              382  CALL_FUNCTION_1       1  ''
              384  POP_TOP          

 L. 157       386  LOAD_GLOBAL              sys
              388  LOAD_METHOD              exit
              390  CALL_METHOD_0         0  ''
              392  POP_TOP          
              394  POP_EXCEPT       
              396  JUMP_FORWARD        400  'to 400'
              398  END_FINALLY      
            400_0  COME_FROM           396  '396'
            400_1  COME_FROM           370  '370'

 L. 160       400  BUILD_LIST_0          0 
              402  STORE_FAST               'devs'

 L. 162       404  LOAD_FAST                'sql_result'
              406  GET_ITER         
              408  FOR_ITER            634  'to 634'
              410  STORE_FAST               'row'

 L. 163       412  SETUP_FINALLY       584  'to 584'

 L. 166       414  LOAD_GLOBAL              json
              416  LOAD_METHOD              loads
              418  LOAD_FAST                'row'
              420  LOAD_CONST               14
              422  BINARY_SUBSCR    
              424  CALL_METHOD_1         1  ''
              426  STORE_FAST               'dev'

 L. 170       428  LOAD_FAST                'parameters'
              430  LOAD_ATTR                strongest
              432  STORE_FAST               'strongest'

 L. 171       434  LOAD_GLOBAL              AccessPoint
              436  LOAD_METHOD              from_json
              438  LOAD_FAST                'dev'
              440  LOAD_FAST                'strongest'
              442  CALL_METHOD_2         2  ''
              444  STORE_FAST               'ap'

 L. 175       446  LOAD_FAST                'parameters'
              448  LOAD_ATTR                ssid
              450  LOAD_CONST               None
              452  COMPARE_OP               is-not
          454_456  POP_JUMP_IF_FALSE   478  'to 478'

 L. 176       458  LOAD_GLOBAL              does_ssid_matches
              460  LOAD_FAST                'dev'
              462  LOAD_FAST                'parameters'
              464  LOAD_ATTR                ssid
              466  CALL_FUNCTION_2       2  ''
          468_470  POP_JUMP_IF_TRUE    478  'to 478'

 L. 178       472  POP_BLOCK        
          474_476  JUMP_BACK           408  'to 408'
            478_0  COME_FROM           468  '468'
            478_1  COME_FROM           454  '454'

 L. 183       478  LOAD_FAST                'parameters'
              480  LOAD_ATTR                excludessid
              482  LOAD_CONST               None
              484  COMPARE_OP               is-not
          486_488  POP_JUMP_IF_FALSE   510  'to 510'

 L. 184       490  LOAD_GLOBAL              does_ssid_matches
              492  LOAD_FAST                'dev'
              494  LOAD_FAST                'parameters'
              496  LOAD_ATTR                excludessid
              498  CALL_FUNCTION_2       2  ''
          500_502  POP_JUMP_IF_FALSE   510  'to 510'

 L. 186       504  POP_BLOCK        
          506_508  JUMP_BACK           408  'to 408'
            510_0  COME_FROM           500  '500'
            510_1  COME_FROM           486  '486'

 L. 190       510  LOAD_FAST                'parameters'
              512  LOAD_ATTR                encryption
          514_516  POP_JUMP_IF_FALSE   538  'to 538'

 L. 191       518  LOAD_FAST                'parameters'
              520  LOAD_ATTR                encryption
              522  LOAD_FAST                'ap'
              524  LOAD_ATTR                encryption
              526  COMPARE_OP               not-in
          528_530  POP_JUMP_IF_FALSE   538  'to 538'

 L. 192       532  POP_BLOCK        
          534_536  JUMP_BACK           408  'to 408'
            538_0  COME_FROM           528  '528'
            538_1  COME_FROM           514  '514'

 L. 195       538  LOAD_FAST                'parameters'
              540  LOAD_ATTR                verbose
          542_544  POP_JUMP_IF_FALSE   570  'to 570'

 L. 196       546  LOAD_GLOBAL              print
              548  LOAD_STR                 '{:20s}{:20s}{:40s}'
              550  LOAD_METHOD              format
              552  LOAD_FAST                'ap'
              554  LOAD_ATTR                mac
              556  LOAD_FAST                'ap'
              558  LOAD_ATTR                encryption
              560  LOAD_FAST                'ap'
              562  LOAD_ATTR                ssid
              564  CALL_METHOD_3         3  ''
              566  CALL_FUNCTION_1       1  ''
              568  POP_TOP          
            570_0  COME_FROM           542  '542'

 L. 198       570  LOAD_FAST                'devs'
              572  LOAD_METHOD              append
              574  LOAD_FAST                'ap'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
              580  POP_BLOCK        
              582  JUMP_BACK           408  'to 408'
            584_0  COME_FROM_FINALLY   412  '412'

 L. 200       584  DUP_TOP          
              586  LOAD_GLOBAL              Exception
              588  COMPARE_OP               exception-match
          590_592  POP_JUMP_IF_FALSE   628  'to 628'
              594  POP_TOP          
              596  STORE_FAST               'e'
              598  POP_TOP          
              600  SETUP_FINALLY       616  'to 616'

 L. 201       602  POP_BLOCK        
              604  POP_EXCEPT       
              606  CALL_FINALLY        616  'to 616'
          608_610  JUMP_BACK           408  'to 408'
              612  POP_BLOCK        
              614  BEGIN_FINALLY    
            616_0  COME_FROM           606  '606'
            616_1  COME_FROM_FINALLY   600  '600'
              616  LOAD_CONST               None
              618  STORE_FAST               'e'
              620  DELETE_FAST              'e'
              622  END_FINALLY      
              624  POP_EXCEPT       
              626  JUMP_BACK           408  'to 408'
            628_0  COME_FROM           590  '590'
              628  END_FINALLY      
          630_632  JUMP_BACK           408  'to 408'

 L. 204       634  LOAD_FAST                'parameters'
              636  LOAD_ATTR                csv
          638_640  POP_JUMP_IF_FALSE   654  'to 654'

 L. 205       642  LOAD_GLOBAL              export_csv
              644  LOAD_FAST                'parameters'
              646  LOAD_ATTR                outfile
              648  LOAD_FAST                'devs'
              650  CALL_FUNCTION_2       2  ''
              652  POP_TOP          
            654_0  COME_FROM           638  '638'

 L. 207       654  LOAD_FAST                'parameters'
              656  LOAD_ATTR                kml
          658_660  POP_JUMP_IF_FALSE   678  'to 678'

 L. 208       662  LOAD_GLOBAL              export_kml
              664  LOAD_FAST                'parameters'
              666  LOAD_ATTR                outfile
              668  LOAD_FAST                'parameters'
              670  LOAD_ATTR                title
              672  LOAD_FAST                'devs'
              674  CALL_FUNCTION_3       3  ''
              676  POP_TOP          
            678_0  COME_FROM           658  '658'

Parse error at or near `JUMP_BACK' instruction at offset 474_476