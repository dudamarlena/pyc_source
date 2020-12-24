# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/command/configuration.py
# Compiled at: 2018-12-10 09:28:20
# Size of source mod 2**32: 2173 bytes
"""The installation script for GeoPySpark.
Downloads the backend jar to the designated location and keeps a reference of where it was saved
to.
"""
import sys, os
from os import path
import argparse
from geopyspark.geopyspark_constants import JAR, CWD
JAR_URL = 'https://github.com/locationtech-labs/geopyspark/releases/download/v0.4.3/' + JAR
DEFAULT_JAR_PATH = path.join(CWD, 'jars')
CONF = path.join(CWD, 'command', 'geopyspark.conf')
parser = argparse.ArgumentParser(description='GeoPySpark Command Line Utility')
parser.set_defaults(func=lambda c, x: parser.print_help())
subparser = parser.add_subparsers(help='Commands')
installer_parser = subparser.add_parser('install-jar', help='Installs the jar to a given path')
installer_parser.add_argument('--path', '-p', metavar='INSTALL_PATH')
path_parser = subparser.add_parser('jar-path', help='Path to downloaded jar')
path_parser.add_argument('--absolute', '-a', action='store_true', help='Prints the absolute path of the jar')

def write_jar_path(jar_path):
    with open(CONF, 'w') as (f):
        f.write(jar_path)


def download_jar(jar_path):
    import subprocess
    jar_location = path.join(jar_path, JAR)
    write_jar_path(jar_location)
    subprocess.call(['curl', '-L', JAR_URL, '-o', jar_location])


def get_jar_path():
    default_jar_location = path.join(DEFAULT_JAR_PATH, JAR)
    if path.isfile(default_jar_location):
        return default_jar_location
    if path.isfile(CONF):
        with open(CONF, 'r') as (f):
            return f.read()
    else:
        raise Exception('The jar path has never been set.')


def parse_args():
    result = parser.parse_args()
    remaining = sys.argv[1:]
    if 'install-jar' in remaining:
        if result.path:
            download_jar(result.path)
        else:
            download_jar(DEFAULT_JAR_PATH)
    else:
        if 'jar-path' in remaining:
            if result.absolute:
                print(get_jar_path())
            else:
                jar_path = get_jar_path()
                rel_path = path.join(path.relpath(jar_path, os.getcwd()))
                print(rel_path)
        else:
            parser.print_help()


def main():
    parse_args()