# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/zlibutil.py
# Compiled at: 2018-01-06 14:43:43
"""
Making your zlib experience that much nicer!

Most importantly, this offers protection from "zlib bomb" attacks, where the
original data was maximally compressable, and a naive use of zlib would
consume all of your RAM while trying to decompress it.
"""
import exceptions, string, zlib
from humanreadable import hr
from pyutil.assertutil import precondition

class DecompressError(exceptions.StandardError, zlib.error):
    pass


class UnsafeDecompressError(DecompressError):
    pass


class TooBigError(DecompressError):
    pass


class ZlibError(DecompressError):
    pass


MINMAXMEM = 76 * 1024 + 264192 + 2063 - 1

def decompress(zbuf, maxlen=65 * 1048576, maxmem=65 * 1048576):
    """
    Decompress zbuf so that it decompresses to <= maxlen bytes, while using
    <= maxmem memory, or else raise an exception.  If zbuf contains
    uncompressed data an exception will be raised.

   This function guards against memory allocation attacks.

    @param maxlen the resulting text must not be greater than this
    @param maxmem the execution of this function must not use more than this
        amount of memory in bytes;  The higher this number is (optimally
        1032 * maxlen, or even greater), the faster this function can
        complete.  (Actually I don't fully understand the workings of zlib, so
        this function might use a *little* more than this memory, but not a
        lot more.)  (Also, this function will raise an exception if the amount
        of memory required even *approaches* maxmem.  Another reason to make
        it large.)  (Hence the default value which would seem to be
        exceedingly large until you realize that it means you can decompress
        64 KB chunks of compressiontext at a bite.)
    """
    assert isinstance(maxlen, (int, long)) and maxlen > 0, 'maxlen is required to be a real maxlen, geez!'
    assert isinstance(maxmem, (int, long)) and maxmem > 0, 'maxmem is required to be a real maxmem, geez!'
    assert maxlen <= maxmem, 'maxlen is required to be <= maxmem.  All data that is included in the return value is counted against maxmem as well as against maxlen, so it is impossible to return a result bigger than maxmem, even if maxlen is bigger than maxmem.  See decompress_to_spool() if you want to spool a large text out while limiting the amount of memory used during the process.'
    lenzbuf = len(zbuf)
    offset = 0
    decomplen = 0
    availmem = maxmem - 76 * 1024
    availmem = availmem / 2
    decompstrlist = []
    decomp = zlib.decompressobj()
    while offset < lenzbuf:
        lencompbite = availmem / 1032
        if lencompbite < 128:
            raise UnsafeDecompressError, 'used up roughly maxmem memory. maxmem: %s, len(zbuf): %s, offset: %s, decomplen: %s, lencompbite: %s' % tuple(map(hr, [maxmem, len(zbuf), offset, decomplen, lencompbite]))
        try:
            if offset == 0 and lencompbite >= lenzbuf:
                tmpstr = decomp.decompress(zbuf)
            else:
                tmpstr = decomp.decompress(zbuf[offset:offset + lencompbite])
        except zlib.error as le:
            raise ZlibError, (offset, lencompbite, decomplen, hr(le))

        lentmpstr = len(tmpstr)
        decomplen = decomplen + lentmpstr
        if decomplen > maxlen:
            raise TooBigError, 'length of resulting data > maxlen. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s' % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
        availmem = availmem - lentmpstr
        offset = offset + lencompbite
        decompstrlist.append(tmpstr)
        tmpstr = ''

    try:
        tmpstr = decomp.flush()
    except zlib.error as le:
        raise ZlibError, (offset, lencompbite, decomplen, le)

    lentmpstr = len(tmpstr)
    decomplen = decomplen + lentmpstr
    if decomplen > maxlen:
        raise TooBigError, 'length of resulting data > maxlen. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s' % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
    availmem = availmem - lentmpstr
    offset = offset + lencompbite
    if lentmpstr > 0:
        decompstrlist.append(tmpstr)
        tmpstr = ''
    if len(decompstrlist) > 0:
        return string.join(decompstrlist, '')
    else:
        return decompstrlist[0]


def decompress_to_fileobj(zbuf, fileobj, maxlen=65 * 1048576, maxmem=65 * 1048576):
    """
    Decompress zbuf so that it decompresses to <= maxlen bytes, while using
    <= maxmem memory, or else raise an exception.  If zbuf contains
    uncompressed data an exception will be raised.

    This function guards against memory allocation attacks.

    Note that this assumes that data written to fileobj still occupies memory,
    so such data counts against maxmem as well as against maxlen.

    @param maxlen the resulting text must not be greater than this
    @param maxmem the execution of this function must not use more than this
        amount of memory in bytes;  The higher this number is (optimally
        1032 * maxlen, or even greater), the faster this function can
        complete.  (Actually I don't fully understand the workings of zlib, so
        this function might use a *little* more than this memory, but not a
        lot more.)  (Also, this function will raise an exception if the amount
        of memory required even *approaches* maxmem.  Another reason to make
        it large.)  (Hence the default value which would seem to be
        exceedingly large until you realize that it means you can decompress
        64 KB chunks of compressiontext at a bite.)
    @param fileobj a file object to which the decompressed text will be written
    """
    precondition(hasattr(fileobj, 'write') and callable(fileobj.write), 'fileobj is required to have a write() method.', fileobj=fileobj)
    precondition(isinstance(maxlen, (int, long)) and maxlen > 0, 'maxlen is required to be a real maxlen, geez!', maxlen=maxlen)
    precondition(isinstance(maxmem, (int, long)) and maxmem > 0, 'maxmem is required to be a real maxmem, geez!', maxmem=maxmem)
    precondition(maxlen <= maxmem, 'maxlen is required to be <= maxmem.  All data that is written out to fileobj is counted against maxmem as well as against maxlen, so it is impossible to return a result bigger than maxmem, even if maxlen is bigger than maxmem.  See decompress_to_spool() if you want to spool a large text out while limiting the amount of memory used during the process.', maxlen=maxlen, maxmem=maxmem)
    lenzbuf = len(zbuf)
    offset = 0
    decomplen = 0
    availmem = maxmem - 76 * 1024
    decomp = zlib.decompressobj()
    while offset < lenzbuf:
        lencompbite = availmem / 1032
        if lencompbite < 128:
            raise UnsafeDecompressError, 'used up roughly maxmem memory. maxmem: %s, len(zbuf): %s, offset: %s, decomplen: %s' % tuple(map(hr, [maxmem, len(zbuf), offset, decomplen]))
        try:
            if offset == 0 and lencompbite >= lenzbuf:
                tmpstr = decomp.decompress(zbuf)
            else:
                tmpstr = decomp.decompress(zbuf[offset:offset + lencompbite])
        except zlib.error as le:
            raise ZlibError, (offset, lencompbite, decomplen, le)

        lentmpstr = len(tmpstr)
        decomplen = decomplen + lentmpstr
        if decomplen > maxlen:
            raise TooBigError, 'length of resulting data > maxlen. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s' % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
        availmem = availmem - lentmpstr
        offset = offset + lencompbite
        fileobj.write(tmpstr)
        tmpstr = ''

    try:
        tmpstr = decomp.flush()
    except zlib.error as le:
        raise ZlibError, (offset, lencompbite, decomplen, le)

    lentmpstr = len(tmpstr)
    decomplen = decomplen + lentmpstr
    if decomplen > maxlen:
        raise TooBigError, 'length of resulting data > maxlen. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s' % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
    availmem = availmem - lentmpstr
    offset = offset + lencompbite
    fileobj.write(tmpstr)
    tmpstr = ''


def decompress_to_spool(zbuf, fileobj, maxlen=65 * 1048576, maxmem=65 * 1048576):
    """
    Decompress zbuf so that it decompresses to <= maxlen bytes, while using
    <= maxmem memory, or else raise an exception.  If zbuf contains
    uncompressed data an exception will be raised.

    This function guards against memory allocation attacks.

    Note that this assumes that data written to fileobj does *not* continue to
    occupy memory, so such data doesn't count against maxmem, although of
    course it still counts against maxlen.

    @param maxlen the resulting text must not be greater than this
    @param maxmem the execution of this function must not use more than this
        amount of memory in bytes;  The higher this number is (optimally
        1032 * maxlen, or even greater), the faster this function can
        complete.  (Actually I don't fully understand the workings of zlib, so
        this function might use a *little* more than this memory, but not a
        lot more.)  (Also, this function will raise an exception if the amount
        of memory required even *approaches* maxmem.  Another reason to make
        it large.)  (Hence the default value which would seem to be
        exceedingly large until you realize that it means you can decompress
        64 KB chunks of compressiontext at a bite.)
    @param fileobj the decompressed text will be written to it
    """
    precondition(hasattr(fileobj, 'write') and callable(fileobj.write), 'fileobj is required to have a write() method.', fileobj=fileobj)
    precondition(isinstance(maxlen, (int, long)) and maxlen > 0, 'maxlen is required to be a real maxlen, geez!', maxlen=maxlen)
    precondition(isinstance(maxmem, (int, long)) and maxmem > 0, 'maxmem is required to be a real maxmem, geez!', maxmem=maxmem)
    tmpstr = ''
    lenzbuf = len(zbuf)
    offset = 0
    decomplen = 0
    availmem = maxmem - 76 * 1024
    decomp = zlib.decompressobj()
    while offset < lenzbuf:
        lencompbite = availmem / 1032
        if lencompbite < 128:
            raise UnsafeDecompressError, "used up roughly `maxmem' memory. maxmem: %s, len(zbuf): %s, offset: %s, decomplen: %s" % tuple(map(hr, [maxmem, len(zbuf), offset, decomplen]))
        try:
            if offset == 0 and lencompbite >= lenzbuf:
                tmpstr = decomp.decompress(zbuf)
            else:
                tmpstr = decomp.decompress(zbuf[offset:offset + lencompbite])
        except zlib.error as le:
            raise ZlibError, (offset, lencompbite, decomplen, le)

        lentmpstr = len(tmpstr)
        decomplen = decomplen + lentmpstr
        if decomplen > maxlen:
            raise TooBigError, "length of resulting data > `maxlen'. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s" % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
        offset = offset + lencompbite
        fileobj.write(tmpstr)
        tmpstr = ''

    try:
        tmpstr = decomp.flush()
    except zlib.error as le:
        raise ZlibError, (offset, lencompbite, decomplen, le)

    lentmpstr = len(tmpstr)
    decomplen = decomplen + lentmpstr
    if decomplen > maxlen:
        raise TooBigError, "length of resulting data > `maxlen'. maxlen: %s, len(zbuf): %s, offset: %s, decomplen: %s" % tuple(map(hr, [maxlen, len(zbuf), offset, decomplen]))
    offset = offset + lencompbite
    fileobj.write(tmpstr)
    tmpstr = ''