# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tabkit/scripts.py
# Compiled at: 2016-06-08 10:21:29
import sys, argparse
from itertools import islice, izip, izip_longest, tee, chain
from .awk import map_program, grp_program
from .header import Field, DataDesc, OrderField, parse_order
from .exception import TabkitException, decorate_exceptions
from .type import generic_type, narrowest_type
from .utils import Files, xsplit

def add_common_args(parser):
    parser.add_argument('-N', '--no-header', help="Don't output header", action='store_true')


def split_fields(string):
    return [ field.strip() for field in string.split(',') ]


@decorate_exceptions
def cat():
    parser = argparse.ArgumentParser(add_help=True, description='Concatenate FILE(s), or standard input, to standard output.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    add_common_args(parser)
    args = parser.parse_args()
    files = Files(args.files)
    data_desc = files.data_desc()
    if not args.no_header:
        sys.stdout.write('%s\n' % data_desc)
        sys.stdout.flush()
    files.call(['cat'])


@decorate_exceptions
def cut():
    parser = argparse.ArgumentParser(add_help=True, description='Print selected columns from each FILE to standard output.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-f', '--fields', help='Select only these fields')
    parser.add_argument('-r', '--remove', help='Remove these fields, keep the rest')
    add_common_args(parser)
    args = parser.parse_args()
    if not (args.fields or args.remove):
        TabkitException('You must specify list of fields')
    files = Files(args.files)
    data_desc = files.data_desc()
    if args.fields:
        fields = split_fields(args.fields)
    else:
        if args.remove:
            remove_fields = split_fields(args.remove)
            [ data_desc.index(field) for field in remove_fields ]
            fields = [ name for name in data_desc.field_names if name not in remove_fields ]
        field_indices = (data_desc.index(field) for field in fields)
        options = ['-f']
        options.append((',').join(str(index + 1) for index in field_indices))
        order = []
        for order_key in data_desc.order:
            if order_key.name not in fields:
                break
            order.append(order_key)

    data_desc = DataDesc(fields=[ f for f in data_desc if f.name in fields ], order=order)
    if not args.no_header:
        sys.stdout.write('%s\n' % data_desc)
        sys.stdout.flush()
    files.call(['cut'] + options)


@decorate_exceptions
def map():
    parser = argparse.ArgumentParser(add_help=True, description='Perform a map operation on all FILE(s)and write result to standard output.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-a', '--all', action='store_true', help='Add all fields to output (implied without -o option)')
    parser.add_argument('-o', '--output', action='append', help='Output fields', default=[])
    parser.add_argument('-f', '--filter', action='append', help='Filter expression')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose awk code')
    add_common_args(parser)
    args = parser.parse_args()
    files = Files(args.files)
    data_desc = files.data_desc()
    program, data_desc = map_program(data_desc, args.output, args.filter)
    if args.verbose:
        sys.stderr.write('%s\n' % program)
    if not args.no_header:
        sys.stdout.write('%s\n' % data_desc)
        sys.stdout.flush()
    files.call(['awk', '-F', '\t', '-v', 'OFS=\t', str(program)])


@decorate_exceptions
def group():
    parser = argparse.ArgumentParser(add_help=True, description='Perform a group operation on all FILE(s)and write result to standard output.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-g', '--group', action='append', help='Group fields', default=[])
    parser.add_argument('-o', '--output', action='append', help='Output fields', default=[])
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose awk code')
    add_common_args(parser)
    args = parser.parse_args()
    files = Files(args.files)
    data_desc = files.data_desc()
    if not args.group:
        args.group = [
         '_fake_implicit_group=1']
    if args.output:
        TabkitException('You must specify list of output field')
    program, data_desc = grp_program(data_desc, args.group, args.output)
    if args.verbose:
        sys.stderr.write('%s\n' % program)
    if not args.no_header:
        sys.stdout.write('%s\n' % data_desc)
        sys.stdout.flush()
    files.call(['awk', '-F', '\t', '-v', 'OFS=\t', str(program)])


def make_order(keys):
    for key in keys:
        for order in parse_order(key):
            yield OrderField(*order)


@decorate_exceptions
def sort():
    parser = argparse.ArgumentParser(add_help=True, description='Write sorted concatenation of all FILE(s) to standard output.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-k', '--keys', action='append', default=[], help='List sorting keys as field[:(str|num|general)][:desc]')
    add_common_args(parser)
    args = parser.parse_args()
    files = Files(args.files)
    data_desc = files.data_desc()
    order = list(make_order(args.keys or data_desc.field_names))
    data_desc = DataDesc(fields=data_desc.fields, order=order)
    options = []
    for order in data_desc.order:
        option = ('-k{0},{0}').format(data_desc.index(order.name) + 1)
        if order.type != 'str':
            option += order.type[0]
        if order.desc:
            option += 'r'
        options.append(option)

    if not args.no_header:
        sys.stdout.write('%s\n' % data_desc)
        sys.stdout.flush()
    files.call(['sort'] + options)


class add_set(argparse.Action):

    def __call__(self, parser, namespace, values, option_string):
        dest = getattr(namespace, self.dest)
        if not dest:
            setattr(namespace, self.dest, {values})
        else:
            dest.add(values)
            setattr(namespace, self.dest, dest)


@decorate_exceptions
def join--- This code section failed: ---

 L. 212         0  LOAD_GLOBAL           0  'argparse'
                3  LOAD_ATTR             1  'ArgumentParser'
                6  LOAD_CONST               'add_help'

 L. 213         9  LOAD_GLOBAL           2  'True'
               12  LOAD_CONST               'description'

 L. 214        15  LOAD_CONST               'Perform the join operation on LEFT_FILE and RIGHT_FILE and write result to standard output.'
               18  CALL_FUNCTION_512   512  None
               21  STORE_FAST            0  'parser'

 L. 217        24  LOAD_FAST             0  'parser'
               27  LOAD_ATTR             3  'add_argument'
               30  LOAD_CONST               'left'
               33  LOAD_CONST               'metavar'
               36  LOAD_CONST               'LEFT_FILE'
               39  LOAD_CONST               'type'
               42  LOAD_GLOBAL           0  'argparse'
               45  LOAD_ATTR             4  'FileType'
               48  LOAD_CONST               'r'
               51  CALL_FUNCTION_1       1  None
               54  CALL_FUNCTION_513   513  None
               57  POP_TOP          

 L. 218        58  LOAD_FAST             0  'parser'
               61  LOAD_ATTR             3  'add_argument'
               64  LOAD_CONST               'right'
               67  LOAD_CONST               'metavar'
               70  LOAD_CONST               'RIGHT_FILE'
               73  LOAD_CONST               'type'
               76  LOAD_GLOBAL           0  'argparse'
               79  LOAD_ATTR             4  'FileType'
               82  LOAD_CONST               'r'
               85  CALL_FUNCTION_1       1  None
               88  CALL_FUNCTION_513   513  None
               91  POP_TOP          

 L. 219        92  LOAD_FAST             0  'parser'
               95  LOAD_ATTR             3  'add_argument'
               98  LOAD_CONST               '-j'
              101  LOAD_CONST               '--join-key'
              104  LOAD_CONST               'metavar'
              107  LOAD_CONST               'FIELD'
              110  LOAD_CONST               'help'

 L. 220       113  LOAD_CONST               'Join on the FIELD of both LEFT_FILE and RIGHT_FILE'
              116  CALL_FUNCTION_514   514  None
              119  POP_TOP          

 L. 221       120  LOAD_FAST             0  'parser'
              123  LOAD_ATTR             3  'add_argument'
              126  LOAD_CONST               '-1'
              129  LOAD_CONST               '--left-key'
              132  LOAD_CONST               'metavar'
              135  LOAD_CONST               'FIELD'
              138  LOAD_CONST               'help'

 L. 222       141  LOAD_CONST               'Join on the FIELD of LEFT_FILE'
              144  CALL_FUNCTION_514   514  None
              147  POP_TOP          

 L. 223       148  LOAD_FAST             0  'parser'
              151  LOAD_ATTR             3  'add_argument'
              154  LOAD_CONST               '-2'
              157  LOAD_CONST               '--right-key'
              160  LOAD_CONST               'metavar'
              163  LOAD_CONST               'FIELD'
              166  LOAD_CONST               'help'

 L. 224       169  LOAD_CONST               'Join on the FIELD of RIGHT_FILE'
              172  CALL_FUNCTION_514   514  None
              175  POP_TOP          

 L. 225       176  LOAD_FAST             0  'parser'
              179  LOAD_ATTR             3  'add_argument'
              182  LOAD_CONST               '-a'
              185  LOAD_CONST               '--add-unpairable'
              188  LOAD_CONST               'metavar'

 L. 226       191  LOAD_CONST               'FILENO'
              194  LOAD_CONST               'type'
              197  LOAD_GLOBAL           5  'int'
              200  LOAD_CONST               'default'
              203  LOAD_GLOBAL           6  'set'
              206  CALL_FUNCTION_0       0  None
              209  LOAD_CONST               'choices'
              212  LOAD_CONST               1
              215  LOAD_CONST               2
              218  BUILD_SET_2           2 
              221  LOAD_CONST               'action'
              224  LOAD_GLOBAL           7  'add_set'
              227  LOAD_CONST               'help'

 L. 227       230  LOAD_CONST               'Add unpairable lines from FILENO'
              233  CALL_FUNCTION_1538  1538  None
              236  POP_TOP          

 L. 228       237  LOAD_FAST             0  'parser'
              240  LOAD_ATTR             3  'add_argument'
              243  LOAD_CONST               '-v'
              246  LOAD_CONST               '--only-unpairable'
              249  LOAD_CONST               'metavar'

 L. 229       252  LOAD_CONST               'FILENO'
              255  LOAD_CONST               'type'
              258  LOAD_GLOBAL           5  'int'
              261  LOAD_CONST               'default'
              264  LOAD_GLOBAL           6  'set'
              267  CALL_FUNCTION_0       0  None
              270  LOAD_CONST               'choices'
              273  LOAD_CONST               1
              276  LOAD_CONST               2
              279  BUILD_SET_2           2 
              282  LOAD_CONST               'action'
              285  LOAD_GLOBAL           7  'add_set'
              288  LOAD_CONST               'help'

 L. 230       291  LOAD_CONST               'Suppress all but unpairable lines from FILENO'
              294  CALL_FUNCTION_1538  1538  None
              297  POP_TOP          

 L. 231       298  LOAD_FAST             0  'parser'
              301  LOAD_ATTR             3  'add_argument'
              304  LOAD_CONST               '-e'
              307  LOAD_CONST               '--empty'
              310  LOAD_CONST               'metavar'
              313  LOAD_CONST               'NULL'
              316  LOAD_CONST               'help'

 L. 232       319  LOAD_CONST               'Fill unpairable fields with NULL (default is empty string)'
              322  CALL_FUNCTION_514   514  None
              325  POP_TOP          

 L. 234       326  LOAD_FAST             0  'parser'
              329  LOAD_ATTR             3  'add_argument'
              332  LOAD_CONST               '-o'
              335  LOAD_CONST               '--output'
              338  LOAD_CONST               'metavar'
              341  LOAD_CONST               'FILENO.FIELD, ...'
              344  LOAD_CONST               'help'

 L. 235       347  LOAD_CONST               'Specify output fields. FILENO is optional if FIELD is unambiguous.'
              350  CALL_FUNCTION_514   514  None
              353  POP_TOP          

 L. 236       354  LOAD_GLOBAL           8  'add_common_args'
              357  LOAD_FAST             0  'parser'
              360  CALL_FUNCTION_1       1  None
              363  POP_TOP          

 L. 237       364  LOAD_FAST             0  'parser'
              367  LOAD_ATTR             9  'parse_args'
              370  CALL_FUNCTION_0       0  None
              373  STORE_FAST            1  'args'

 L. 239       376  LOAD_FAST             1  'args'
              379  LOAD_ATTR            10  'left'
              382  LOAD_FAST             1  'args'
              385  LOAD_ATTR            11  'right'
              388  ROT_TWO          
              389  STORE_FAST            2  'left'
              392  STORE_FAST            3  'right'

 L. 240       395  LOAD_GLOBAL          12  'Files'
              398  LOAD_FAST             2  'left'
              401  LOAD_FAST             3  'right'
              404  BUILD_LIST_2          2 
              407  CALL_FUNCTION_1       1  None
              410  STORE_FAST            4  'files'

 L. 241       413  LOAD_GLOBAL          13  'list'
              416  LOAD_FAST             4  'files'
              419  LOAD_ATTR            14  'data_descs'
              422  CALL_FUNCTION_0       0  None
              425  CALL_FUNCTION_1       1  None
              428  UNPACK_SEQUENCE_2     2 
              431  STORE_FAST            5  'left_desc'
              434  STORE_FAST            6  'right_desc'

 L. 243       437  LOAD_FAST             1  'args'
              440  LOAD_ATTR            15  'join_key'
              443  JUMP_IF_TRUE_OR_POP   461  'to 461'
              446  LOAD_FAST             1  'args'
              449  LOAD_ATTR            16  'left_key'
              452  JUMP_IF_FALSE_OR_POP   461  'to 461'
              455  LOAD_FAST             1  'args'
              458  LOAD_ATTR            17  'right_key'
            461_0  COME_FROM           452  '452'
            461_1  COME_FROM           443  '443'
              461  POP_JUMP_IF_TRUE    479  'to 479'

 L. 244       464  LOAD_GLOBAL          18  'TabkitException'
              467  LOAD_CONST               'Specify join field through -j or -1, -2 options'
              470  CALL_FUNCTION_1       1  None
              473  RAISE_VARARGS_1       1  None
              476  JUMP_FORWARD          0  'to 479'
            479_0  COME_FROM           476  '476'

 L. 245       479  LOAD_FAST             1  'args'
              482  LOAD_ATTR            15  'join_key'
              485  DUP_TOP          
              486  STORE_FAST            7  'left_key'
              489  STORE_FAST            8  'right_key'

 L. 246       492  LOAD_FAST             1  'args'
              495  LOAD_ATTR            16  'left_key'
              498  POP_JUMP_IF_FALSE   513  'to 513'

 L. 247       501  LOAD_FAST             1  'args'
              504  LOAD_ATTR            16  'left_key'
              507  STORE_FAST            7  'left_key'
              510  JUMP_FORWARD          0  'to 513'
            513_0  COME_FROM           510  '510'

 L. 248       513  LOAD_FAST             1  'args'
              516  LOAD_ATTR            17  'right_key'
              519  POP_JUMP_IF_FALSE   534  'to 534'

 L. 249       522  LOAD_FAST             1  'args'
              525  LOAD_ATTR            17  'right_key'
              528  STORE_FAST            8  'right_key'
              531  JUMP_FORWARD          0  'to 534'
            534_0  COME_FROM           531  '531'

 L. 251       534  LOAD_FAST             1  'args'
              537  LOAD_ATTR            19  'add_unpairable'
              540  POP_JUMP_IF_FALSE   567  'to 567'
              543  LOAD_FAST             1  'args'
              546  LOAD_ATTR            20  'only_unpairable'
            549_0  COME_FROM           540  '540'
              549  POP_JUMP_IF_FALSE   567  'to 567'

 L. 252       552  LOAD_GLOBAL          18  'TabkitException'

 L. 253       555  LOAD_CONST               "-a does nothing in presence of -v. Are you sure about what you're trying to express?"
              558  CALL_FUNCTION_1       1  None
              561  RAISE_VARARGS_1       1  None
              564  JUMP_FORWARD          0  'to 567'
            567_0  COME_FROM           564  '564'

 L. 255       567  BUILD_LIST_0          0 
              570  STORE_FAST            9  'output'

 L. 256       573  BUILD_LIST_0          0 
              576  STORE_FAST           10  'output_desc'

 L. 257       579  BUILD_LIST_0          0 
              582  STORE_FAST           11  'output_order'

 L. 258       585  LOAD_CONST               None
              588  STORE_FAST           12  'generic_key'

 L. 259       591  LOAD_FAST             1  'args'
              594  LOAD_ATTR            20  'only_unpairable'
              597  UNARY_NOT        
              598  POP_JUMP_IF_TRUE    622  'to 622'
              601  LOAD_GLOBAL          22  'len'
              604  LOAD_FAST             1  'args'
              607  LOAD_ATTR            20  'only_unpairable'
              610  CALL_FUNCTION_1       1  None
              613  LOAD_CONST               2
              616  COMPARE_OP            2  ==
            619_0  COME_FROM           598  '598'
              619  POP_JUMP_IF_FALSE   817  'to 817'

 L. 260       622  LOAD_FAST             1  'args'
              625  LOAD_ATTR            19  'add_unpairable'
              628  LOAD_CONST               1
              631  BUILD_SET_1           1 
              634  COMPARE_OP            2  ==
              637  POP_JUMP_IF_FALSE   661  'to 661'

 L. 262       640  LOAD_FAST             5  'left_desc'
              643  LOAD_ATTR            23  'get_field'
              646  LOAD_FAST             7  'left_key'
              649  CALL_FUNCTION_1       1  None
              652  LOAD_ATTR            24  'type'
              655  STORE_FAST           13  'type_'
              658  JUMP_FORWARD        138  'to 799'

 L. 263       661  LOAD_FAST             1  'args'
              664  LOAD_ATTR            19  'add_unpairable'
              667  LOAD_CONST               2
              670  BUILD_SET_1           1 
              673  COMPARE_OP            2  ==
              676  POP_JUMP_IF_FALSE   700  'to 700'

 L. 265       679  LOAD_FAST             6  'right_desc'
              682  LOAD_ATTR            23  'get_field'
              685  LOAD_FAST             8  'right_key'
              688  CALL_FUNCTION_1       1  None
              691  LOAD_ATTR            24  'type'
              694  STORE_FAST           13  'type_'
              697  JUMP_FORWARD         99  'to 799'

 L. 266       700  LOAD_FAST             1  'args'
              703  LOAD_ATTR            19  'add_unpairable'
              706  POP_JUMP_IF_TRUE    718  'to 718'
              709  LOAD_FAST             1  'args'
              712  LOAD_ATTR            20  'only_unpairable'
            715_0  COME_FROM           706  '706'
              715  POP_JUMP_IF_FALSE   760  'to 760'

 L. 268       718  LOAD_GLOBAL          25  'generic_type'
              721  LOAD_FAST             5  'left_desc'
              724  LOAD_ATTR            23  'get_field'
              727  LOAD_FAST             7  'left_key'
              730  CALL_FUNCTION_1       1  None
              733  LOAD_ATTR            24  'type'

 L. 269       736  LOAD_FAST             6  'right_desc'
              739  LOAD_ATTR            23  'get_field'
              742  LOAD_FAST             8  'right_key'
              745  CALL_FUNCTION_1       1  None
              748  LOAD_ATTR            24  'type'
              751  CALL_FUNCTION_2       2  None
              754  STORE_FAST           13  'type_'
              757  JUMP_FORWARD         39  'to 799'

 L. 272       760  LOAD_GLOBAL          26  'narrowest_type'
              763  LOAD_FAST             5  'left_desc'
              766  LOAD_ATTR            23  'get_field'
              769  LOAD_FAST             7  'left_key'
              772  CALL_FUNCTION_1       1  None
              775  LOAD_ATTR            24  'type'

 L. 273       778  LOAD_FAST             6  'right_desc'
              781  LOAD_ATTR            23  'get_field'
              784  LOAD_FAST             8  'right_key'
              787  CALL_FUNCTION_1       1  None
              790  LOAD_ATTR            24  'type'
              793  CALL_FUNCTION_2       2  None
              796  STORE_FAST           13  'type_'
            799_0  COME_FROM           757  '757'
            799_1  COME_FROM           697  '697'
            799_2  COME_FROM           658  '658'

 L. 274       799  LOAD_GLOBAL          27  'Field'
              802  LOAD_FAST             7  'left_key'
              805  LOAD_FAST            13  'type_'
              808  CALL_FUNCTION_2       2  None
              811  STORE_FAST           12  'generic_key'
              814  JUMP_FORWARD          0  'to 817'
            817_0  COME_FROM           814  '814'

 L. 276       817  SETUP_LOOP          507  'to 1327'
              820  LOAD_CONST               1
              823  LOAD_FAST             2  'left'
              826  LOAD_FAST             7  'left_key'
              829  LOAD_FAST             5  'left_desc'
              832  BUILD_TUPLE_4         4 

 L. 277       835  LOAD_CONST               2
              838  LOAD_FAST             3  'right'
              841  LOAD_FAST             8  'right_key'
              844  LOAD_FAST             6  'right_desc'
              847  BUILD_TUPLE_4         4 
              850  BUILD_TUPLE_2         2 
              853  GET_ITER         
              854  FOR_ITER            469  'to 1326'
              857  UNPACK_SEQUENCE_4     4 
              860  STORE_FAST           14  'fileno'
              863  STORE_FAST           15  'file'
              866  STORE_FAST           16  'key'
              869  STORE_FAST           17  'desc'

 L. 278       872  LOAD_FAST            16  'key'
              875  LOAD_FAST            17  'desc'
              878  COMPARE_OP            7  not-in
              881  POP_JUMP_IF_FALSE   912  'to 912'

 L. 279       884  LOAD_GLOBAL          18  'TabkitException'
              887  LOAD_CONST               'No such field %r in file %r'
              890  LOAD_FAST            16  'key'
              893  LOAD_FAST            15  'file'
              896  LOAD_ATTR            28  'name'
              899  BUILD_TUPLE_2         2 
              902  BINARY_MODULO    
              903  CALL_FUNCTION_1       1  None
              906  RAISE_VARARGS_1       1  None
              909  JUMP_FORWARD          0  'to 912'
            912_0  COME_FROM           909  '909'

 L. 280       912  SETUP_EXCEPT         71  'to 986'

 L. 281       915  LOAD_FAST            17  'desc'
              918  LOAD_ATTR            29  'order'
              921  LOAD_ATTR            30  'pop'
              924  LOAD_CONST               0
              927  CALL_FUNCTION_1       1  None
              930  UNPACK_SEQUENCE_3     3 
              933  STORE_FAST           18  'field'
              936  STORE_FAST           19  'field_type'
              939  STORE_FAST           20  'order'

 L. 282       942  LOAD_FAST            18  'field'
              945  LOAD_FAST            16  'key'
              948  COMPARE_OP            2  ==
              951  JUMP_IF_FALSE_OR_POP   970  'to 970'
              954  LOAD_FAST            19  'field_type'
              957  LOAD_CONST               'str'
              960  COMPARE_OP            2  ==
              963  JUMP_IF_FALSE_OR_POP   970  'to 970'
              966  LOAD_FAST            20  'order'
              969  UNARY_NOT        
            970_0  COME_FROM           963  '963'
            970_1  COME_FROM           951  '951'
              970  POP_JUMP_IF_TRUE    982  'to 982'

 L. 283       973  LOAD_GLOBAL          31  'ValueError'
              976  RAISE_VARARGS_1       1  None
              979  JUMP_FORWARD          0  'to 982'
            982_0  COME_FROM           979  '979'
              982  POP_BLOCK        
              983  JUMP_FORWARD         48  'to 1034'
            986_0  COME_FROM           912  '912'

 L. 284       986  DUP_TOP          
              987  LOAD_GLOBAL          32  'IndexError'
              990  LOAD_GLOBAL          31  'ValueError'
              993  BUILD_TUPLE_2         2 
              996  COMPARE_OP           10  exception-match
              999  POP_JUMP_IF_FALSE  1033  'to 1033'
             1002  POP_TOP          
             1003  POP_TOP          
             1004  POP_TOP          

 L. 285      1005  LOAD_GLOBAL          18  'TabkitException'

 L. 286      1008  LOAD_CONST               'File %r must be sorted lexicographicaly ascending by the field %r'

 L. 287      1011  LOAD_FAST            15  'file'
             1014  LOAD_ATTR            28  'name'
             1017  LOAD_FAST            16  'key'
             1020  BUILD_TUPLE_2         2 
             1023  BINARY_MODULO    
             1024  CALL_FUNCTION_1       1  None
             1027  RAISE_VARARGS_1       1  None
             1030  JUMP_FORWARD          1  'to 1034'
             1033  END_FINALLY      
           1034_0  COME_FROM          1033  '1033'
           1034_1  COME_FROM           983  '983'

 L. 288      1034  LOAD_FAST             1  'args'
             1037  LOAD_ATTR            33  'output'
             1040  POP_JUMP_IF_TRUE    854  'to 854'

 L. 289      1043  LOAD_FAST             1  'args'
             1046  LOAD_ATTR            20  'only_unpairable'
             1049  POP_JUMP_IF_FALSE  1073  'to 1073'
             1052  LOAD_FAST            14  'fileno'
             1055  LOAD_FAST             1  'args'
             1058  LOAD_ATTR            20  'only_unpairable'
             1061  COMPARE_OP            7  not-in
           1064_0  COME_FROM          1049  '1049'
           1064_1  COME_FROM          1040  '1040'
             1064  POP_JUMP_IF_FALSE  1073  'to 1073'

 L. 290      1067  CONTINUE            854  'to 854'
             1070  JUMP_FORWARD          0  'to 1073'
           1073_0  COME_FROM          1070  '1070'

 L. 291      1073  SETUP_LOOP          247  'to 1323'
             1076  LOAD_GLOBAL          34  'enumerate'
             1079  LOAD_FAST            17  'desc'
             1082  LOAD_CONST               'start'
             1085  LOAD_CONST               1
             1088  CALL_FUNCTION_257   257  None
             1091  GET_ITER         
             1092  FOR_ITER            224  'to 1319'
             1095  UNPACK_SEQUENCE_2     2 
             1098  STORE_FAST           21  'fieldno'
             1101  STORE_FAST           18  'field'

 L. 292      1104  LOAD_FAST            18  'field'
             1107  LOAD_ATTR            28  'name'
             1110  LOAD_FAST            16  'key'
             1113  COMPARE_OP            2  ==
             1116  POP_JUMP_IF_FALSE  1237  'to 1237'

 L. 293      1119  LOAD_FAST            12  'generic_key'
             1122  POP_JUMP_IF_FALSE  1194  'to 1194'

 L. 294      1125  LOAD_FAST            15  'file'
             1128  LOAD_FAST             2  'left'
             1131  COMPARE_OP            2  ==
             1134  POP_JUMP_IF_FALSE  1092  'to 1092'

 L. 295      1137  LOAD_FAST             9  'output'
             1140  LOAD_ATTR            35  'append'
             1143  LOAD_CONST               '0'
             1146  CALL_FUNCTION_1       1  None
             1149  POP_TOP          

 L. 296      1150  LOAD_FAST            10  'output_desc'
             1153  LOAD_ATTR            35  'append'
             1156  LOAD_FAST            12  'generic_key'
             1159  CALL_FUNCTION_1       1  None
             1162  POP_TOP          

 L. 297      1163  LOAD_FAST            11  'output_order'
             1166  LOAD_ATTR            35  'append'
             1169  LOAD_GLOBAL          36  'OrderField'
             1172  LOAD_FAST            18  'field'
             1175  LOAD_ATTR            28  'name'
             1178  CALL_FUNCTION_1       1  None
             1181  CALL_FUNCTION_1       1  None
             1184  POP_TOP          
             1185  JUMP_BACK          1092  'to 1092'

 L. 298      1188  CONTINUE           1092  'to 1092'
             1191  JUMP_ABSOLUTE      1237  'to 1237'

 L. 299      1194  LOAD_FAST            14  'fileno'
             1197  LOAD_FAST             1  'args'
             1200  LOAD_ATTR            20  'only_unpairable'
             1203  COMPARE_OP            6  in
             1206  POP_JUMP_IF_FALSE  1237  'to 1237'

 L. 300      1209  LOAD_FAST            11  'output_order'
             1212  LOAD_ATTR            35  'append'
             1215  LOAD_GLOBAL          36  'OrderField'
             1218  LOAD_FAST            18  'field'
             1221  LOAD_ATTR            28  'name'
             1224  CALL_FUNCTION_1       1  None
             1227  CALL_FUNCTION_1       1  None
             1230  POP_TOP          
             1231  JUMP_ABSOLUTE      1237  'to 1237'
             1234  JUMP_FORWARD          0  'to 1237'
           1237_0  COME_FROM          1234  '1234'

 L. 302      1237  LOAD_FAST             9  'output'
             1240  LOAD_ATTR            35  'append'
             1243  LOAD_CONST               '%d.%d'
             1246  LOAD_FAST            14  'fileno'
             1249  LOAD_FAST            21  'fieldno'
             1252  BUILD_TUPLE_2         2 
             1255  BINARY_MODULO    
             1256  CALL_FUNCTION_1       1  None
             1259  POP_TOP          

 L. 303      1260  LOAD_FAST            18  'field'
             1263  LOAD_FAST            10  'output_desc'
             1266  COMPARE_OP            6  in
             1269  POP_JUMP_IF_FALSE  1303  'to 1303'

 L. 304      1272  LOAD_GLOBAL          18  'TabkitException'

 L. 305      1275  LOAD_CONST               'Duplicate field %r in file %r'
             1278  LOAD_FAST            18  'field'
             1281  LOAD_ATTR            28  'name'
             1284  LOAD_FAST            15  'file'
             1287  LOAD_ATTR            28  'name'
             1290  BUILD_TUPLE_2         2 
             1293  BINARY_MODULO    
             1294  CALL_FUNCTION_1       1  None
             1297  RAISE_VARARGS_1       1  None
             1300  JUMP_FORWARD          0  'to 1303'
           1303_0  COME_FROM          1300  '1300'

 L. 306      1303  LOAD_FAST            10  'output_desc'
             1306  LOAD_ATTR            35  'append'
             1309  LOAD_FAST            18  'field'
             1312  CALL_FUNCTION_1       1  None
             1315  POP_TOP          
             1316  JUMP_BACK          1092  'to 1092'
             1319  POP_BLOCK        
           1320_0  COME_FROM          1073  '1073'
             1320  JUMP_BACK           854  'to 854'
             1323  JUMP_BACK           854  'to 854'
             1326  POP_BLOCK        
           1327_0  COME_FROM           817  '817'

 L. 308      1327  LOAD_FAST             1  'args'
             1330  LOAD_ATTR            33  'output'
             1333  POP_JUMP_IF_FALSE  1725  'to 1725'

 L. 309      1336  SETUP_LOOP          386  'to 1725'
             1339  LOAD_GLOBAL          37  'split_fields'
             1342  LOAD_FAST             1  'args'
             1345  LOAD_ATTR            33  'output'
             1348  CALL_FUNCTION_1       1  None
             1351  GET_ITER         
             1352  FOR_ITER            366  'to 1721'
             1355  STORE_FAST           18  'field'

 L. 310      1358  LOAD_CONST               '.'
             1361  LOAD_FAST            18  'field'
             1364  COMPARE_OP            6  in
             1367  POP_JUMP_IF_FALSE  1579  'to 1579'

 L. 311      1370  LOAD_FAST            18  'field'
             1373  LOAD_ATTR            38  'split'
             1376  LOAD_CONST               '.'
             1379  LOAD_CONST               1
             1382  CALL_FUNCTION_2       2  None
             1385  UNPACK_SEQUENCE_2     2 
             1388  STORE_FAST           14  'fileno'
             1391  STORE_FAST           22  'field_name'

 L. 312      1394  SETUP_EXCEPT         37  'to 1434'

 L. 313      1397  LOAD_GLOBAL           5  'int'
             1400  LOAD_FAST            14  'fileno'
             1403  CALL_FUNCTION_1       1  None
             1406  STORE_FAST           14  'fileno'

 L. 314      1409  LOAD_FAST            14  'fileno'
             1412  LOAD_CONST               (1, 2)
             1415  COMPARE_OP            7  not-in
             1418  POP_JUMP_IF_FALSE  1430  'to 1430'

 L. 315      1421  LOAD_GLOBAL          31  'ValueError'
             1424  RAISE_VARARGS_1       1  None
             1427  JUMP_FORWARD          0  'to 1430'
           1430_0  COME_FROM          1427  '1427'
             1430  POP_BLOCK        
             1431  JUMP_FORWARD         33  'to 1467'
           1434_0  COME_FROM          1394  '1394'

 L. 316      1434  DUP_TOP          
             1435  LOAD_GLOBAL          31  'ValueError'
             1438  COMPARE_OP           10  exception-match
             1441  POP_JUMP_IF_FALSE  1466  'to 1466'
             1444  POP_TOP          
             1445  POP_TOP          
             1446  POP_TOP          

 L. 317      1447  LOAD_GLOBAL          18  'TabkitException'
             1450  LOAD_CONST               'Bad output field format %r'
             1453  LOAD_FAST            18  'field'
             1456  BINARY_MODULO    
             1457  CALL_FUNCTION_1       1  None
             1460  RAISE_VARARGS_1       1  None
             1463  JUMP_FORWARD          1  'to 1467'
             1466  END_FINALLY      
           1467_0  COME_FROM          1466  '1466'
           1467_1  COME_FROM          1431  '1431'

 L. 318      1467  LOAD_FAST             5  'left_desc'
             1470  LOAD_FAST             6  'right_desc'
             1473  BUILD_TUPLE_2         2 
             1476  LOAD_FAST            14  'fileno'
             1479  LOAD_CONST               1
             1482  BINARY_SUBTRACT  
             1483  BINARY_SUBSCR    
             1484  STORE_FAST           17  'desc'

 L. 319      1487  LOAD_FAST            22  'field_name'
             1490  LOAD_FAST            17  'desc'
             1493  COMPARE_OP            7  not-in
             1496  POP_JUMP_IF_FALSE  1518  'to 1518'

 L. 320      1499  LOAD_GLOBAL          18  'TabkitException'
             1502  LOAD_CONST               'Unknown output field %r'
             1505  LOAD_FAST            18  'field'
             1508  BINARY_MODULO    
             1509  CALL_FUNCTION_1       1  None
             1512  RAISE_VARARGS_1       1  None
             1515  JUMP_FORWARD          0  'to 1518'
           1518_0  COME_FROM          1515  '1515'

 L. 321      1518  LOAD_FAST             9  'output'
             1521  LOAD_ATTR            35  'append'
             1524  LOAD_CONST               '%d.%d'
             1527  LOAD_FAST            14  'fileno'
             1530  LOAD_FAST            17  'desc'
             1533  LOAD_ATTR            39  'index'
             1536  LOAD_FAST            22  'field_name'
             1539  CALL_FUNCTION_1       1  None
             1542  LOAD_CONST               1
             1545  BINARY_ADD       
             1546  BUILD_TUPLE_2         2 
             1549  BINARY_MODULO    
             1550  CALL_FUNCTION_1       1  None
             1553  POP_TOP          

 L. 322      1554  LOAD_FAST            10  'output_desc'
             1557  LOAD_ATTR            35  'append'
             1560  LOAD_FAST            17  'desc'
             1563  LOAD_ATTR            23  'get_field'
             1566  LOAD_FAST            22  'field_name'
             1569  CALL_FUNCTION_1       1  None
             1572  CALL_FUNCTION_1       1  None
             1575  POP_TOP          
             1576  JUMP_BACK          1352  'to 1352'

 L. 324      1579  LOAD_FAST            12  'generic_key'
             1582  POP_JUMP_IF_FALSE  1629  'to 1629'
             1585  LOAD_FAST            18  'field'
             1588  LOAD_FAST            12  'generic_key'
             1591  LOAD_ATTR            28  'name'
             1594  COMPARE_OP            2  ==
           1597_0  COME_FROM          1582  '1582'
             1597  POP_JUMP_IF_FALSE  1629  'to 1629'

 L. 325      1600  LOAD_FAST             9  'output'
             1603  LOAD_ATTR            35  'append'
             1606  LOAD_CONST               '0'
             1609  CALL_FUNCTION_1       1  None
             1612  POP_TOP          

 L. 326      1613  LOAD_FAST            10  'output_desc'
             1616  LOAD_ATTR            35  'append'
             1619  LOAD_FAST            12  'generic_key'
             1622  CALL_FUNCTION_1       1  None
             1625  POP_TOP          
             1626  JUMP_BACK          1352  'to 1352'

 L. 328      1629  LOAD_FAST            18  'field'
             1632  LOAD_FAST             5  'left_desc'
             1635  COMPARE_OP            6  in
             1638  POP_JUMP_IF_FALSE  1672  'to 1672'
             1641  LOAD_FAST            18  'field'
             1644  LOAD_FAST             6  'right_desc'
             1647  COMPARE_OP            6  in
           1650_0  COME_FROM          1638  '1638'
             1650  POP_JUMP_IF_FALSE  1672  'to 1672'

 L. 329      1653  LOAD_GLOBAL          18  'TabkitException'
             1656  LOAD_CONST               'Output field %r is ambiguous'
             1659  LOAD_FAST            18  'field'
             1662  BINARY_MODULO    
             1663  CALL_FUNCTION_1       1  None
             1666  RAISE_VARARGS_1       1  None
             1669  JUMP_FORWARD          0  'to 1672'
           1672_0  COME_FROM          1669  '1669'

 L. 330      1672  LOAD_FAST            18  'field'
             1675  LOAD_FAST             5  'left_desc'
             1678  COMPARE_OP            6  in
             1681  POP_JUMP_IF_FALSE  1687  'to 1687'

 L. 331      1684  CONTINUE           1352  'to 1352'

 L. 332      1687  LOAD_FAST            18  'field'
             1690  LOAD_FAST             6  'right_desc'
             1693  COMPARE_OP            6  in
             1696  POP_JUMP_IF_FALSE  1702  'to 1702'

 L. 333      1699  CONTINUE           1352  'to 1352'

 L. 335      1702  LOAD_GLOBAL          18  'TabkitException'
             1705  LOAD_CONST               'Unknown output field %r'
             1708  LOAD_FAST            18  'field'
             1711  BINARY_MODULO    
             1712  CALL_FUNCTION_1       1  None
             1715  RAISE_VARARGS_1       1  None
             1718  JUMP_BACK          1352  'to 1352'
             1721  POP_BLOCK        
           1722_0  COME_FROM          1336  '1336'
             1722  JUMP_FORWARD          0  'to 1725'
           1725_0  COME_FROM          1336  '1336'

 L. 337      1725  LOAD_SETCOMP             '<code_object <setcomp>>'
             1728  MAKE_FUNCTION_0       0  None
             1731  LOAD_FAST            10  'output_desc'
             1734  GET_ITER         
             1735  CALL_FUNCTION_1       1  None
             1738  STORE_DEREF           0  'output_field_names'

 L. 338      1741  LOAD_FAST            11  'output_order'
             1744  LOAD_ATTR            40  'extend'

 L. 339      1747  LOAD_CLOSURE          0  'output_field_names'
             1753  LOAD_GENEXPR             '<code_object <genexpr>>'
             1756  MAKE_CLOSURE_0        0  None
             1759  LOAD_GLOBAL          41  'chain'
             1762  LOAD_FAST             5  'left_desc'
             1765  LOAD_ATTR            29  'order'
             1768  LOAD_FAST             6  'right_desc'
             1771  LOAD_ATTR            29  'order'
             1774  CALL_FUNCTION_2       2  None
             1777  GET_ITER         
             1778  CALL_FUNCTION_1       1  None
             1781  CALL_FUNCTION_1       1  None
             1784  POP_TOP          

 L. 340      1785  LOAD_GLOBAL          42  'DataDesc'
             1788  LOAD_FAST            10  'output_desc'
             1791  LOAD_FAST            11  'output_order'
             1794  CALL_FUNCTION_2       2  None
             1797  STORE_FAST           10  'output_desc'

 L. 342      1800  LOAD_CONST               '-1'
             1803  LOAD_GLOBAL          43  'str'
             1806  LOAD_FAST             5  'left_desc'
             1809  LOAD_ATTR            39  'index'
             1812  LOAD_FAST             7  'left_key'
             1815  CALL_FUNCTION_1       1  None
             1818  LOAD_CONST               1
             1821  BINARY_ADD       
             1822  CALL_FUNCTION_1       1  None

 L. 343      1825  LOAD_CONST               '-2'
             1828  LOAD_GLOBAL          43  'str'
             1831  LOAD_FAST             6  'right_desc'
             1834  LOAD_ATTR            39  'index'
             1837  LOAD_FAST             8  'right_key'
             1840  CALL_FUNCTION_1       1  None
             1843  LOAD_CONST               1
             1846  BINARY_ADD       
             1847  CALL_FUNCTION_1       1  None
             1850  BUILD_LIST_4          4 
             1853  STORE_FAST           23  'options'

 L. 344      1856  SETUP_LOOP           42  'to 1901'
             1859  LOAD_FAST             1  'args'
             1862  LOAD_ATTR            19  'add_unpairable'
             1865  GET_ITER         
             1866  FOR_ITER             31  'to 1900'
             1869  STORE_FAST           14  'fileno'

 L. 345      1872  LOAD_FAST            23  'options'
             1875  LOAD_ATTR            40  'extend'
             1878  LOAD_CONST               '-a'
             1881  LOAD_GLOBAL          43  'str'
             1884  LOAD_FAST            14  'fileno'
             1887  CALL_FUNCTION_1       1  None
             1890  BUILD_LIST_2          2 
             1893  CALL_FUNCTION_1       1  None
             1896  POP_TOP          
             1897  JUMP_BACK          1866  'to 1866'
             1900  POP_BLOCK        
           1901_0  COME_FROM          1856  '1856'

 L. 346      1901  SETUP_LOOP           42  'to 1946'
             1904  LOAD_FAST             1  'args'
             1907  LOAD_ATTR            20  'only_unpairable'
             1910  GET_ITER         
             1911  FOR_ITER             31  'to 1945'
             1914  STORE_FAST           14  'fileno'

 L. 347      1917  LOAD_FAST            23  'options'
             1920  LOAD_ATTR            40  'extend'
             1923  LOAD_CONST               '-v'
             1926  LOAD_GLOBAL          43  'str'
             1929  LOAD_FAST            14  'fileno'
             1932  CALL_FUNCTION_1       1  None
             1935  BUILD_LIST_2          2 
             1938  CALL_FUNCTION_1       1  None
             1941  POP_TOP          
             1942  JUMP_BACK          1911  'to 1911'
             1945  POP_BLOCK        
           1946_0  COME_FROM          1901  '1901'

 L. 348      1946  LOAD_FAST             1  'args'
             1949  LOAD_ATTR            44  'empty'
             1952  POP_JUMP_IF_FALSE  1980  'to 1980'

 L. 349      1955  LOAD_FAST            23  'options'
             1958  LOAD_ATTR            40  'extend'
             1961  LOAD_CONST               '-e'
             1964  LOAD_FAST             1  'args'
             1967  LOAD_ATTR            44  'empty'
             1970  BUILD_LIST_2          2 
             1973  CALL_FUNCTION_1       1  None
             1976  POP_TOP          
             1977  JUMP_FORWARD          0  'to 1980'
           1980_0  COME_FROM          1977  '1977'

 L. 350      1980  LOAD_FAST            23  'options'
             1983  LOAD_ATTR            40  'extend'
             1986  LOAD_CONST               '-o'
             1989  LOAD_CONST               ','
             1992  LOAD_ATTR            45  'join'
             1995  LOAD_FAST             9  'output'
             1998  CALL_FUNCTION_1       1  None
             2001  BUILD_LIST_2          2 
             2004  CALL_FUNCTION_1       1  None
             2007  POP_TOP          

 L. 352      2008  LOAD_FAST             1  'args'
             2011  LOAD_ATTR            46  'no_header'
             2014  POP_JUMP_IF_TRUE   2053  'to 2053'

 L. 353      2017  LOAD_GLOBAL          47  'sys'
             2020  LOAD_ATTR            48  'stdout'
             2023  LOAD_ATTR            49  'write'
             2026  LOAD_CONST               '%s\n'
             2029  LOAD_FAST            10  'output_desc'
             2032  BINARY_MODULO    
             2033  CALL_FUNCTION_1       1  None
             2036  POP_TOP          

 L. 354      2037  LOAD_GLOBAL          47  'sys'
             2040  LOAD_ATTR            48  'stdout'
             2043  LOAD_ATTR            50  'flush'
             2046  CALL_FUNCTION_0       0  None
             2049  POP_TOP          
             2050  JUMP_FORWARD          0  'to 2053'
           2053_0  COME_FROM          2050  '2050'

 L. 356      2053  LOAD_FAST             4  'files'
             2056  LOAD_ATTR            51  'call'
             2059  LOAD_CONST               'join'
             2062  LOAD_CONST               '-t'
             2065  LOAD_CONST               '\t'
             2068  BUILD_LIST_3          3 
             2071  LOAD_FAST            23  'options'
             2074  BINARY_ADD       
             2075  CALL_FUNCTION_1       1  None
             2078  POP_TOP          
             2079  LOAD_CONST               None
             2082  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 1323


@decorate_exceptions
def pretty():
    parser = argparse.ArgumentParser(add_help=True, description='Output FILE(s) as human-readable pretty table.')
    parser.add_argument('files', metavar='FILE', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-n', default=100, help='Preread N rows to calculate column widths, default is 100')
    args = parser.parse_args()
    files = Files(args.files)
    data_desc = files.data_desc()
    preread, rows = tee((row.rstrip('\n') for row in files), 2)
    nfields = len(data_desc)
    split = lambda row: islice(xsplit(row), nfields)
    widths = [ len(str(f)) for f in data_desc ]
    for row in islice(preread, args.n):
        for i, value in enumerate(split(row)):
            widths[i] = max(widths[i], len(value))

    widths = [ w + 2 for w in widths ]
    print ('|').join((' %s ' % (f,)).ljust(w) for w, f in izip(widths, data_desc))
    print ('+').join('-' * w for w in widths)
    for row in rows:
        print ('|').join((' %s ' % (v or '')).ljust(w or 0) for w, v in izip_longest(widths, split(row)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        script = sys.argv.pop(1)
        sys.argv[0] = script
        globals()[script]()