# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/david/flask_proj/polarishub_flask/polarishub_flask/server/myqrcode.py
# Compiled at: 2019-09-01 10:49:07
# Size of source mod 2**32: 1034 bytes
import qrcode, os
from polarishub_flask.server.parser import printv

def generateCode(url, filename='qrcode.png'):
    qr = qrcode.QRCode(version=1,
      error_correction=(qrcode.constants.ERROR_CORRECT_L),
      box_size=10,
      border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_name = os.path.join(os.getcwd(), 'temp', filename)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(qr_name)
    printv(qr_name)
    return (
     qr_name, '/' + qr_name[qr_name.find('temp'):].replace('\\', '/'))