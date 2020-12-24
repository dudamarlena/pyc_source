# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/qrscanner.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 4877 bytes
import os, sys, ctypes
if sys.platform == 'darwin':
    name = 'libzbar.dylib'
else:
    if sys.platform in ('windows', 'win32'):
        name = 'libzbar-0.dll'
    else:
        name = 'libzbar.so.0'
try:
    libzbar = ctypes.cdll.LoadLibrary(name)
except BaseException:
    libzbar = None

def scan_barcode_ctypes(device='', timeout=-1, display=True, threaded=False, try_again=True):
    if libzbar is None:
        raise RuntimeError('Cannot start QR scanner; zbar not available.')
    else:
        libzbar.zbar_symbol_get_data.restype = ctypes.c_char_p
        libzbar.zbar_processor_create.restype = ctypes.POINTER(ctypes.c_int)
        libzbar.zbar_processor_get_results.restype = ctypes.POINTER(ctypes.c_int)
        libzbar.zbar_symbol_set_first_symbol.restype = ctypes.POINTER(ctypes.c_int)
        proc = libzbar.zbar_processor_create(threaded)
        libzbar.zbar_processor_request_size(proc, 640, 480)
        if libzbar.zbar_processor_init(proc, device.encode('utf-8'), display) != 0:
            if try_again:
                return scan_barcode(device, timeout, display, threaded, try_again=False)
            raise RuntimeError('Can not start QR scanner; initialization failed.')
        else:
            libzbar.zbar_processor_set_visible(proc)
            if libzbar.zbar_process_one(proc, timeout):
                symbols = libzbar.zbar_processor_get_results(proc)
            else:
                symbols = None
        libzbar.zbar_processor_destroy(proc)
        if symbols is None:
            return
        return libzbar.zbar_symbol_set_get_size(symbols) or None
    symbol = libzbar.zbar_symbol_set_first_symbol(symbols)
    data = libzbar.zbar_symbol_get_data(symbol)
    return data.decode('utf8')


def scan_barcode_osx(*args_ignored, **kwargs_ignored):
    import subprocess
    root_ec_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
    prog = root_ec_dir + '/' + 'contrib/osx/CalinsQRReader/build/Release/CalinsQRReader.app/Contents/MacOS/CalinsQRReader'
    if not os.path.exists(prog):
        raise RuntimeError('Cannot start QR scanner; helper app not found.')
    data = ''
    try:
        with subprocess.Popen([prog], stdout=(subprocess.PIPE)) as (p):
            data = p.stdout.read().decode('utf-8').strip()
        return data
    except OSError as e:
        try:
            raise RuntimeError('Cannot start camera helper app; {}'.format(e.strerror))
        finally:
            e = None
            del e


scan_barcode = scan_barcode_osx if sys.platform == 'darwin' else scan_barcode_ctypes

def _find_system_cameras():
    device_root = '/sys/class/video4linux'
    devices = {}
    if os.path.exists(device_root):
        for device in os.listdir(device_root):
            path = os.path.join(device_root, device, 'name')
            try:
                with open(path, encoding='utf-8') as (f):
                    name = f.read()
            except Exception:
                continue

            name = name.strip('\n')
            devices[name] = os.path.join('/dev', device)

    return devices


if __name__ == '__main__':
    print(scan_barcode())