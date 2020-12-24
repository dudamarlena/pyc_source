# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gopro2gpx/gpmf.py
# Compiled at: 2020-04-24 06:26:35
# Size of source mod 2**32: 3413 bytes
import os, array, sys, struct
from gopro2gpx.config import Config
from .ffmpegtools import FFMpegTools
from .klvdata import KLVData

class Parser:

    def __init__(self, config: Config):
        self.config = config
        self.ffmtools = FFMpegTools(self.config)
        self.verbose = config.verbose
        self.file = config.input_file
        self.outputfile = config.output_file

    def readFromMP4(self):
        """read data the metadata track from video. Requires FFMPEG wrapper.
           -vv creates a dump file with the  binary data called dump_track.bin
        """
        if not os.path.exists(self.file):
            raise FileNotFoundError("Can't open %s" % self.file)
        track_number, lineinfo = self.ffmtools.getMetadataTrack(self.file)
        if not track_number:
            raise Exception("File %s doesn't have any metadata" % self.file)
        if self.verbose:
            print('Working on file %s track %s (%s)' % (self.file, track_number, lineinfo))
        metadata_raw = self.ffmtools.getMetadata(track_number, self.file)
        if self.verbose == 2:
            print('Creating output file for binary data (fromMP4): %s' % self.outputfile)
            f = open('%s.bin' % self.outputfile, 'wb')
            f.write(metadata_raw)
            f.close()
        metadata = self.parseStream(metadata_raw)
        return metadata

    def readFromBinary(self):
        """read data from binary file, instead extract the metadata track from video. Useful for quick development
           -vv creates a dump file with the  binary data called dump_binary.bin
        """
        if not os.path.exists(self.file):
            raise FileNotFoundError("Can't open %s" % self.file)
        if self.verbose:
            print('Reading binary file %s' % self.file)
        fd = open(self.file, 'rb')
        data = fd.read()
        fd.close()
        if self.verbose == 2:
            print('Creating output file for binary data (from binary): %s' % self.outputfile)
            f = open('%s.bin' % self.outputfile, 'wb')
            f.write(data)
            f.close()
        metadata = self.parseStream(data)
        return metadata

    def parseStream(self, data_raw):
        """
        main code that reads the points
        """
        data = array.array('b')
        data.fromstring(data_raw)
        offset = 0
        klvlist = []
        while offset < len(data):
            klv = KLVData(data, offset)
            if not klv.skip():
                klvlist.append(klv)
                if self.verbose == 3:
                    print(klv)
            offset += 8
            if klv.type != 0:
                offset += klv.padded_length

        return klvlist