# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libray/core.py
# Compiled at: 2019-07-07 13:23:49
# Size of source mod 2**32: 3592 bytes
import os, sys, stat, shutil, requests
from bs4 import BeautifulSoup
try:
    from libray import iso
except ImportError:
    import iso

SECTOR = 2048
ALL_IRD_NET_LOC = 'http://jonnysp.bplaced.net/data.php'
GET_IRD_NET_LOC = 'http://jonnysp.bplaced.net/ird/'

def to_int(data, byteorder='big'):
    """Convert bytes to integer"""
    if isinstance(data, bytes):
        return int.from_bytes(data, byteorder)


def to_bytes(data):
    """Convert a string of HEX to bytes"""
    if isinstance(data, str):
        return bytes(bytearray.fromhex(data))


ISO_SECRET = to_bytes('380bcf0b53455b3c7817ab4fa3ba90ed')
ISO_IV = to_bytes('69474772af6fdab342743aefaa186287')

def size(path):
    """Get size of a file or block device in bytes"""
    pathstat = os.stat(path)
    if stat.S_ISBLK(pathstat.st_mode):
        return open(path, 'rb').seek(0, os.SEEK_END)
    return pathstat.st_size


def read_seven_bit_encoded_int(fileobj, order):
    """Read an Int32, 7 bits at a time."""
    count = 0
    shift = 0
    byte = -1
    while byte & 128 != 0 or byte == -1:
        if shift == 35:
            raise ValueError
        byte = to_int(fileobj.read(1), order)
        count |= (byte & 127) << shift
        shift += 7

    return count


def error(msg):
    """Print fatal error message and terminate"""
    print('ERROR: %s' % msg)
    sys.exit(1)


def warning(msg):
    """Print a warning message"""
    print('WARNING: %s. Continuing regardless' % msg)


def download_ird(ird_name):
    """Download an .ird from GET_IRD_NET_LOC"""
    ird_link = GET_IRD_NET_LOC + ird_name
    r = requests.get(ird_link, stream=True)
    with open(ird_name, 'wb') as (ird_file):
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, ird_file)


def ird_by_game_id(game_id):
    """Using a game_id, download the responding .ird from ALL_IRD_NET_LOC"""
    gameid = game_id.replace('-', '')
    r = requests.get(ALL_IRD_NET_LOC, headers={'User-Agent': 'Anonymous (You)'}, timeout=5)
    soup = BeautifulSoup(r.text, 'html.parser')
    ird_name = False
    for elem in soup.find_all('a'):
        url = elem.get('href').split('/')[(-1)].replace('\\"', '')
        if gameid in url:
            ird_name = url

    if not ird_name:
        error("Unable to download IRD, couldn't find link")
    download_ird(ird_name)
    return ird_name


def decrypt(args):
    """Try to decrypt a given .iso using relevant .ird using args from argparse
  
  If no .ird is given this will try to automatically download an .ird file with the encryption/decryption key for the given game .iso
  """
    input_iso = iso.ISO(args)
    input_iso.decrypt(args)