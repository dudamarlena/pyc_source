# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libray/iso.py
# Compiled at: 2019-07-07 13:37:44
# Size of source mod 2**32: 4860 bytes
import sys
from tqdm import tqdm
from Crypto.Cipher import AES
try:
    from libray import core
    from libray import ird
except ImportError:
    import core, ird

class ISO:
    __doc__ = 'Class for handling PS3 .iso files\n  \n  Attributes:\n  size: Size of .iso in bytes\n  number_of_regions: Number of regions in the .iso\n  regions: List with info of every region\n  game_id: PS3 game id\n  ird: IRD object (see ird.py)\n  disc_key: data1 from .ird, encrypted\n  '
    NUM_INFO_BYTES = 4

    def __init__(self, args):
        """ISO constructor using args from argparse"""
        self.size = core.size(args.iso)
        if not self.size:
            core.error('looks like ISO file/mount is empty?')
        with open(args.iso, 'rb') as (input_iso):
            self.number_of_regions = core.to_int(input_iso.read(self.NUM_INFO_BYTES))
            unused_bytes = input_iso.read(self.NUM_INFO_BYTES)
            self.regions = self.read_regions(input_iso, args.iso)
            input_iso.seek(core.SECTOR)
            playstation = input_iso.read(16)
            self.game_id = input_iso.read(16).decode('utf8').strip()
        if args.verbose:
            self.print_info()
        if not args.ird:
            core.warning('No IRD file specified, downloading required file')
            args.ird = core.ird_by_game_id(self.game_id)
        self.ird = ird.IRD(args)
        if self.ird.region_count != len(self.regions) - 1:
            core.error('Corrupt ISO. Expected %s regions, found %s regions' % (self.ird.region_count, len(self.regions) - 1))
        if self.regions[(-1)]['start'] > self.size:
            core.error('Corrupt ISO. Expected filesize larger than %.2f GiB, actual size is %.2f GiB' % (self.regions[(-1)]['start'] / 1073741824, self.size / 1073741824))
        cipher = AES.new(core.ISO_SECRET, AES.MODE_CBC, core.ISO_IV)
        self.disc_key = cipher.encrypt(self.ird.data1)

    def decrypt(self, args):
        """Decrypt self using args from argparse"""
        print('Decrypting with disc key: %s' % self.disc_key.hex())
        with open(args.iso, 'rb') as (input_iso):
            with open(args.output, 'wb') as (output_iso):
                pbar = tqdm(total=(self.size // 2048 - 4))
                for i, region in enumerate(self.regions):
                    input_iso.seek(region['start'])
                    if not region['enc']:
                        while input_iso.tell() < region['end']:
                            data = input_iso.read(core.SECTOR)
                            if not data:
                                core.warning('Trying to read past the end of the file')
                                break
                            pbar.update(1)
                            output_iso.write(data)

                        continue
                    else:
                        while input_iso.tell() < region['end']:
                            num = input_iso.tell() // 2048
                            iv = bytearray([0 for i in range(0, 16)])
                            for j in range(0, 16):
                                iv[16 - j - 1] = num & 255
                                num >>= 8

                            data = input_iso.read(core.SECTOR)
                            if not data:
                                core.warning('Trying to read past the end of the file')
                                break
                            pbar.update(1)
                            cipher = AES.new(self.disc_key, AES.MODE_CBC, bytes(iv))
                            decrypted = cipher.decrypt(data)
                            output_iso.write(decrypted)

                    pbar.close()

    def read_regions(self, input_iso, filename):
        """List with information (start, end, whether it's encrypted) for every region"""
        regions = []
        encrypted = False
        for i in range(0, self.number_of_regions * 2):
            regions.append({'start':core.to_int(input_iso.read(self.NUM_INFO_BYTES)) * core.SECTOR, 
             'end':core.to_int(input_iso.read(self.NUM_INFO_BYTES)) * core.SECTOR, 
             'enc':encrypted})
            input_iso.seek(input_iso.tell() - self.NUM_INFO_BYTES)
            encrypted = not encrypted

        regions[(-1)]['end'] = self.size
        return regions

    def print_info(self):
        """Print some info about the ISO"""
        print('Info from ISO:')
        print('Regions: %s (%s)' % (self.number_of_regions, self.number_of_regions * 2))
        for i, region in enumerate(self.regions):
            print(i, region)