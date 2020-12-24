# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/qrcodes.py
# Compiled at: 2015-11-05 10:40:17
"""Utilities for working with QRCodes."""
import cStringIO, logging
try:
    import qrcode
except ImportError:
    qrcode = False
    logging.warn('Could not import Python qrcode module.')
    logging.debug("You'll need the qrcode Python module for this to work. On Debian-based systems, this should be in the python-qrcode package.")

def generateQR(bridgelines, imageFormat='JPEG', bridgeSchema=False):
    """Generate a QRCode for the client's bridge lines.

    :param str bridgelines: The Bridge Lines which we are distributing to the
        client.
    :param bool bridgeSchema: If ``True``, prepend ``'bridge://'`` to the
        beginning of each bridge line before QR encoding.
    :rtype: str or ``None``
    :returns: The generated QRCode, as a string.
    """
    logging.debug('Attempting to encode bridge lines into a QRCode...')
    if not bridgelines:
        return
    if not qrcode:
        logging.info('Not creating QRCode for bridgelines; no qrcode module.')
        return
    try:
        if bridgeSchema:
            schema = 'bridge://'
            prefixed = []
            for line in bridgelines.strip().split('\n'):
                prefixed.append(schema + line)

            bridgelines = ('\n').join(prefixed)
        logging.debug('QR encoding bridge lines: %s' % bridgelines)
        qr = qrcode.QRCode()
        qr.add_data(bridgelines)
        buf = cStringIO.StringIO()
        img = qr.make_image().resize([350, 350])
        img.save(buf, imageFormat)
        buf.seek(0)
        imgstr = buf.read()
        return imgstr
    except KeyError as error:
        logging.error(str(error))
        logging.debug("It seems python-imaging doesn't understand how to save in the %s format." % imageFormat)
    except Exception as error:
        logging.error('There was an error while attempting to generate the QRCode: %s' % str(error))