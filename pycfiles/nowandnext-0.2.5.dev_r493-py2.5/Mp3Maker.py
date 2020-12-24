# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/Mp3Maker.py
# Compiled at: 2009-05-11 19:02:39
import urllib, sys, datetime, logging, cStringIO, os, socket
log = logging.getLogger(__name__)

class RecordingError(Exception):
    """
    Something bad happened during recording.
    """
    pass


class Mp3Maker:
    """
    A class of utilities to record from shoutcast & icecast streams to local files on the hard disk.
    """
    BUFFERSIZE = 65535
    MAX_BUFFERSIZE = BUFFERSIZE * 16

    @classmethod
    def applyTag(cls, file):
        mp3 = ID3v2(file)
        mp3.version
        for frame in mp3.frames:
            print frame.fid

    @classmethod
    def RecordMp3(cls, url, duration, outfile):
        """
        Record the output of a shoutcast stream for a period of time.
        @param url: The complete shoutcast URL where the stream can be obtained.
        @type url: str
        @param duration: The duration to record for.
        @type duration: datetime.timedelta
        @param out_filepath: A file to write to
        @type out_filepath: file-like object
        """
        assert type(url) == str, 'Url should be a string'
        assert url.startswith('http'), 'Url needs to start wtith http'
        assert type(duration) == datetime.timedelta
        assert duration > datetime.timedelta()
        starttime = datetime.datetime.now()
        endtime = starttime + duration
        mp3data = urllib.urlopen(url)
        memorybuffer = cStringIO.StringIO()
        try:
            while datetime.datetime.now() < endtime:
                try:
                    memorybuffer.write(mp3data.read(cls.BUFFERSIZE))
                except socket.error, se:
                    raise RecordingError('Error during recording %s' % repr(se))

                if len(memorybuffer.getvalue()) >= cls.MAX_BUFFERSIZE:
                    bufferout.write(memorybuffer.getvalue())
                    memorybuffer.truncate(0)

        finally:
            lastData = memorybuffer.getvalue()
            bufferout.write(lastData)

    def __init__(self, secs, out_filename):
        pass


if __name__ == '__main__':
    import tempfile
    logging.basicConfig()
    bufferout = tempfile.NamedTemporaryFile(suffix='.mp3')
    result = Mp3Maker.RecordMp3(url='http://icecast.commedia.org.uk:8000/resonance_hi.mp3', duration=datetime.timedelta(seconds=10), outfile='/home/james/jt.mp3')
    outfile = bufferout
    log.warn('Sample file saved to %s' % bufferout.name)
    log.warn('actually finished ')
    bufferout.close()