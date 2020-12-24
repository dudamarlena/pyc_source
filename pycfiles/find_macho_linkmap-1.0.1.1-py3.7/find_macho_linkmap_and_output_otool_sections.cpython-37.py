# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/find-macho-linkmap/find_macho_linkmap_and_output_otool_sections.py
# Compiled at: 2019-02-15 00:37:25
# Size of source mod 2**32: 6076 bytes
import os, sys, getopt
from enum import Enum, unique
import subprocess
sys.path.append(os.path.abspath(os.path.curdir))
from utils import *

def main(argv):
    global buildmode
    try:
        opts, args = getopt.getopt(argv, 'm:i:n:o:', ['buildmode', 'inputpath', 'productname', 'outputpath'])
    except getopt.GetoptError:
        print('xxx.py [-m <debug/release>] -i <path> -n <name> -o <path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-m', '--buildmode'):
            buildmode = BuildMode.debug.value if arg.lower() == BuildMode.debug.value else BuildMode.release.value

    __do_exec()


@unique
class BuildMode(Enum):
    release = 'release'
    debug = 'debug'


buildmode = BuildMode.debug.value
inputpath = ''
outputpath = ''
productname = ''

def __do_exec():
    global inputpath
    global outputpath
    global productname
    PrintWithColor.black('')
    if len(productname) <= 0:
        PrintWithColor.red(f"product name is not a valid name: {productname}")
        return
    if not os.path.isdir(inputpath):
        PrintWithColor.red(f"input path is not a valid dir: {inputpath}")
        return
    if not os.path.isdir(outputpath):
        PrintWithColor.red(f"output path is not a valid dir: {outputpath}")
        return
    src_macho_path = ''
    src_linkmap_path = ''
    exclude_folders = {
     f"{productname}.app.dsym"}
    exclude_buildmode = BuildMode.debug.value if buildmode == BuildMode.release.value else BuildMode.release.value
    exclude_folders |= {f"{buildmode}-{x}" for x in {'watchsimulator', 'watchos', 'iphonesimulator'}}
    exclude_folders |= {f"{exclude_buildmode}-{x}" for x in {'watchsimulator', 'iphoneos', 'watchos', 'iphonesimulator'}}
    for root, dirs, files in os.walk(inputpath):
        mdirs = dirs.copy()
        for name in mdirs:
            if name.lower() in exclude_folders:
                dirs.remove(name)

        for file in files:
            if file == (f"{productname}"):
                src_macho_path = os.path.join(root, file)
                PrintWithColor.yellow(f"find MachO file: {src_macho_path}")

    if not os.path.isfile(src_macho_path):
        PrintWithColor.red('MachO file not found.')
        return
    if not os.path.isfile(src_linkmap_path):
        PrintWithColor.red('Linkmap file not found.')
        return
    dest_dir1 = os.path.join(outputpath, '物料')
    if not os.path.exists(dest_dir1):
        os.makedirs(dest_dir1)
    dest_dir2 = os.path.join(outputpath, 'otool')
    if not os.path.exists(dest_dir2):
        os.makedirs(dest_dir2)
    if not os.path.isdir(dest_dir1):
        PrintWithColor.red(f"not a valid dir: {dest_dir1}")
        return
    if not os.path.isdir(dest_dir2):
        PrintWithColor.red(f"not a valid dir: {dest_dir2}")
        return
    dest_macho_path = os.path.join(dest_dir1, productname)
    dest_linkmap_path = os.path.join(dest_dir1, f"{productname}-LinkMap-normal-arm64.txt")
    dest_classlist_path = os.path.join(dest_dir2, 'objc_classlist.txt')
    dest_classrefs_path = os.path.join(dest_dir2, 'objc_classrefs.txt')
    PrintWithColor.yellow(f"copying macho to: {dest_macho_path}")
    os.system(f"cp {src_macho_path} {dest_macho_path}")
    PrintWithColor.yellow(f"encoding utf8 linkmap to: {dest_linkmap_path}")
    src_linkmap_encoding = 'MAC'
    os.system(f"iconv -f {src_linkmap_encoding} -t UTF-8 {src_linkmap_path} | cat > {dest_linkmap_path}")
    PrintWithColor.yellow(f"extracting _objc_classlist to: {dest_classlist_path}")
    objc_classlist_bytes = subprocess.check_output(f"otool -arch arm64 -s __DATA __objc_classlist {dest_macho_path}", shell=True)
    objc_classlist_output = str(objc_classlist_bytes, encoding='utf-8')
    with open(dest_classlist_path, 'w+', encoding='utf-8') as (fo):
        fo.write(objc_classlist_output)
    PrintWithColor.yellow(f"extracting _objc_classrefs to: {dest_classrefs_path}")
    objc_classrefs_bytes = subprocess.check_output(f"otool -arch arm64 -s __DATA __objc_classrefs {dest_macho_path}", shell=True)
    objc_classrefs_output = str(objc_classrefs_bytes, encoding='utf-8')
    with open(dest_classrefs_path, 'w+', encoding='utf-8') as (fo):
        fo.write(objc_classrefs_output)
    PrintWithColor.blue('--- end ---')


if __name__ == '__main__':
    main(sys.argv[1:])