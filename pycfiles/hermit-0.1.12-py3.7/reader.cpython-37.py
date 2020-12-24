# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/qrcode/reader.py
# Compiled at: 2019-06-07 02:02:02
# Size of source mod 2**32: 2041 bytes
from typing import Optional
from pyzbar import pyzbar
import asyncio, cv2
from hermit.errors import InvalidSignatureRequest
from .format import decode_qr_code_data
from .utils import window_is_open

def read_qr_code() -> Optional[str]:
    task = _capture_qr_code_async()
    return asyncio.get_event_loop().run_until_complete(task)


async def _capture_qr_code_async() -> Optional[str]:
    capture = _start_camera()
    preview_dimensions = (640, 480)
    decoded_data = None
    encoded_data = None
    window_name = 'Signature Request QR Code Scanner'
    cv2.namedWindow(window_name)
    while window_is_open(window_name):
        ret, frame = capture.read()
        frame = cv2.resize(frame, preview_dimensions)
        for qrcode in pyzbar.decode(frame):
            x, y, w, h = qrcode.rect
            cv2.rectangle(frame, (
             x, y), (
             x + w, y + h), (0, 0, 255), 2)
            encoded_data = qrcode.data
            try:
                decoded_data = decode_qr_code_data(encoded_data)
            except InvalidSignatureRequest as e:
                try:
                    print('Invalid signature request: {}'.format(str(e)))
                finally:
                    e = None
                    del e

            if decoded_data is not None:
                break

        mirror = cv2.flip(frame, 1)
        cv2.imshow(window_name, mirror)
        if decoded_data:
            break
        await asyncio.sleep(0.01)

    capture.release()
    cv2.destroyWindow(window_name)
    return decoded_data


def _start_camera() -> cv2.VideoCapture:
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError('Cannot open webcam')
    return capture