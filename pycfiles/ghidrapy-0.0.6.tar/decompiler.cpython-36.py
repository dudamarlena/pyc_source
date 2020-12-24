# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Git\assembly-code\JARV1S-Ghidra\pywrap\ghidrapy\decompiler.py
# Compiled at: 2019-12-11 22:33:27
# Size of source mod 2**32: 1515 bytes
from ghidrapy.dependencies import install_jdk_if_needed
from ghidrapy.dependencies import install_jar_if_needed
import os
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from shutil import rmtree
import sys, json, errno
NULL_FILE = open(os.devnull, 'w')
home = os.path.join(str(Path.home()), '.jarv1s-ghidra')
jar = install_jar_if_needed(home)
java = install_jdk_if_needed(home)

def process(file, json_suffix='.asm.json', project_suffix='.ghidra', decompile=False, load=False):
    json_file = file + json_suffix
    project_dir = file + project_suffix
    json_file = os.path.abspath(json_file)
    project_dir = os.path.abspath(project_dir)
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    else:
        cmd = [
         java, '-jar', jar, file, json_file,
         project_dir, str(decompile).lower()]
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        out, _ = p.communicate()
        if os.path.exists(json_file):
            if load:
                with open(json_file) as (of):
                    json_file = json.load(of)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), json_file)
    return (
     json_file, out)


def cleanup(file, project_only=True, json_suffix='.asm.json', project_suffix='.ghidra'):
    json_file = file + json_suffix
    project_dir = file + project_suffix
    rmtree(project_dir)
    if not project_only:
        os.remove(json_file)