# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/lv_we/data/codes/tools_lib/cpmd_cube_tools/release/cpmd_cube_tools/main.py
# Compiled at: 2020-04-23 10:52:59
# Size of source mod 2**32: 3225 bytes
from cpmd_cube_tools.api import *

def main():
    parser = argparse.ArgumentParser(description=('A python library and tool to read in and manipulate Gaussian/CPMD cube files. \nThis code allows you to:\nRead and write cube files\nPerform VDD analysis\nVersion:' + str(version)), formatter_class=RawTextHelpFormatter)
    parser.add_argument('Files', help='Cube files used in program', nargs='+')
    parser.add_argument('-g', '--geom', help='Geometry file from CPMD run')
    parser.add_argument('-mol', '--molecule', help='atom list (atom0,atom1,..., or *.txt file, or mol, or mol,atomid) of a molecule for electronic density integration')
    parser.add_argument('-inp', '--inpfile', help='cpmd input file for atoms index selection')
    parser.add_argument('-vdd', '--dovdd', help='yes/no')
    parser.add_argument('-net', '--netcharge', help='Net charge of the selected atoms', nargs=1, type=float)
    parser.add_argument('-a', '--add', help='Add two or more cube files together', action='store_true')
    parser.add_argument('-s', '--subtract', help='Subtract two or more cube files together', action='store_true')
    parser.add_argument('-t', '--translate', help='Translate a cube file. Requires a translation vector as an argument.', nargs=3, type=float)
    if len(argv) <= 1:
        print('No enough input ....')
        parser.print_help()
        exit()
    else:
        args = parser.parse_args()
        print(args)
        if args.dovdd != None:
            if args.geom != None and args.inpfile != None:
                if args.dovdd.lower() == 'yes':
                    print('Ready to perform vdd analysis')
                    if args.Files:
                        cube2vdd(args.Files[0], args.geom, args.inpfile)
                    else:
                        print('No cube file is provided.')
            else:
                print('If you want to do vdd, please add option flage: -vdd yes')
        else:
            if args.geom != None:
                print('Correct corrdinates information in cube file with ', args.geom)
                if args.Files:
                    correct_cube(args.Files[0], args.geom)
                else:
                    print('No cube file is provided.')
        if args.molecule != None:
            print('Atom list of molecule in consider is ', args.molecule)
            if args.molecule.split(',')[0] == 'mol':
                if args.inpfile:
                    print('Using ', args.inpfile, ' in electrons integration')
            else:
                print('No inpfile information supplied!')
                exit()
        else:
            print('Have you checked the input atom list carefully?', args.molecule)
    if args.netcharge == None:
        print('No netcharge of the considered region? Setup net charge as 0.')
        args.netcharge = [0]
    else:
        if args.add:
            if len(args.Files) >= 2:
                add_cubes(args.Files)
            else:
                print('Error: To use the add function, two or more cube files need to be specified.')
        if args.subtract:
            if len(args.Files) >= 2:
                diff_cubes(args.Files)
            else:
                print('Error: To use the subtract function, two or more cube files need to be specified.')
    if args.translate:
        if args.Files:
            translate_cubes(args.Files, args.translate)