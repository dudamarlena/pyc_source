# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FBpyGIF/fb.py
# Compiled at: 2017-09-05 07:56:56
# Size of source mod 2**32: 11337 bytes
FBIOGET_VSCREENINFO = 17920
FBIOPUT_VSCREENINFO = 17921
FBIOGET_FSCREENINFO = 17922
FBIOGETCMAP = 17924
FBIOPUTCMAP = 17925
FBIOPAN_DISPLAY = 17926
FBIOGET_CON2FBMAP = 17935
FBIOPUT_CON2FBMAP = 17936
FBIOBLANK = 17937
FBIO_ALLOC = 17939
FBIO_FREE = 17940
FBIOGET_GLYPH = 17941
FBIOGET_HWCINFO = 17942
FBIOPUT_MODEINFO = 17943
FBIOGET_DISPINFO = 17944
FB_TYPE_PACKED_PIXELS = 0
FB_TYPE_PLANES = 1
FB_TYPE_INTERLEAVED_PLANES = 2
FB_TYPE_TEXT = 3
FB_TYPE_VGA_PLANES = 4
FB_TYPE_FOURCC = 5
FB_AUX_TEXT_MDA = 0
FB_AUX_TEXT_CGA = 1
FB_AUX_TEXT_S3_MMIO = 2
FB_AUX_TEXT_MGA_STEP16 = 3
FB_AUX_TEXT_MGA_STEP8 = 4
FB_AUX_TEXT_SVGA_GROUP = 8
FB_AUX_TEXT_SVGA_MASK = 7
FB_AUX_TEXT_SVGA_STEP2 = 8
FB_AUX_TEXT_SVGA_STEP4 = 9
FB_AUX_TEXT_SVGA_STEP8 = 10
FB_AUX_TEXT_SVGA_STEP16 = 11
FB_AUX_TEXT_SVGA_LAST = 15
FB_AUX_VGA_PLANES_VGA4 = 0
FB_AUX_VGA_PLANES_CFB4 = 1
FB_AUX_VGA_PLANES_CFB8 = 2
FB_VISUAL_MONO01 = 0
FB_VISUAL_MONO10 = 1
FB_VISUAL_TRUECOLOR = 2
FB_VISUAL_PSEUDOCOLOR = 3
FB_VISUAL_DIRECTCOLOR = 4
FB_VISUAL_STATIC_PSEUDOCOLOR = 5
FB_VISUAL_FOURCC = 6
FB_ACCEL_NONE = 0
FB_ACCEL_ATARIBLITT = 1
FB_ACCEL_AMIGABLITT = 2
FB_ACCEL_S3_TRIO64 = 3
FB_ACCEL_NCR_77C32BLT = 4
FB_ACCEL_S3_VIRGE = 5
FB_ACCEL_ATI_MACH64GX = 6
FB_ACCEL_DEC_TGA = 7
FB_ACCEL_ATI_MACH64CT = 8
FB_ACCEL_ATI_MACH64VT = 9
FB_ACCEL_ATI_MACH64GT = 10
FB_ACCEL_SUN_CREATOR = 11
FB_ACCEL_SUN_CGSIX = 12
FB_ACCEL_SUN_LEO = 13
FB_ACCEL_IMS_TWINTURBO = 14
FB_ACCEL_3DLABS_PERMEDIA2 = 15
FB_ACCEL_MATROX_MGA2064W = 16
FB_ACCEL_MATROX_MGA1064SG = 17
FB_ACCEL_MATROX_MGA2164W = 18
FB_ACCEL_MATROX_MGA2164W_AGP = 19
FB_ACCEL_MATROX_MGAG100 = 20
FB_ACCEL_MATROX_MGAG200 = 21
FB_ACCEL_SUN_CG14 = 22
FB_ACCEL_SUN_BWTWO = 23
FB_ACCEL_SUN_CGTHREE = 24
FB_ACCEL_SUN_TCX = 25
FB_ACCEL_MATROX_MGAG400 = 26
FB_ACCEL_NV3 = 27
FB_ACCEL_NV4 = 28
FB_ACCEL_NV5 = 29
FB_ACCEL_CT_6555x = 30
FB_ACCEL_3DFX_BANSHEE = 31
FB_ACCEL_ATI_RAGE128 = 32
FB_ACCEL_IGS_CYBER2000 = 33
FB_ACCEL_IGS_CYBER2010 = 34
FB_ACCEL_IGS_CYBER5000 = 35
FB_ACCEL_SIS_GLAMOUR = 36
FB_ACCEL_3DLABS_PERMEDIA3 = 37
FB_ACCEL_ATI_RADEON = 38
FB_ACCEL_I810 = 39
FB_ACCEL_SIS_GLAMOUR_2 = 40
FB_ACCEL_SIS_XABRE = 41
FB_ACCEL_I830 = 42
FB_ACCEL_NV_10 = 43
FB_ACCEL_NV_20 = 44
FB_ACCEL_NV_30 = 45
FB_ACCEL_NV_40 = 46
FB_ACCEL_XGI_VOLARI_V = 47
FB_ACCEL_XGI_VOLARI_Z = 48
FB_ACCEL_OMAP1610 = 49
FB_ACCEL_TRIDENT_TGUI = 50
FB_ACCEL_TRIDENT_3DIMAGE = 51
FB_ACCEL_TRIDENT_BLADE3D = 52
FB_ACCEL_TRIDENT_BLADEXP = 53
FB_ACCEL_CIRRUS_ALPINE = 53
FB_ACCEL_NEOMAGIC_NM2070 = 90
FB_ACCEL_NEOMAGIC_NM2090 = 91
FB_ACCEL_NEOMAGIC_NM2093 = 92
FB_ACCEL_NEOMAGIC_NM2097 = 93
FB_ACCEL_NEOMAGIC_NM2160 = 94
FB_ACCEL_NEOMAGIC_NM2200 = 95
FB_ACCEL_NEOMAGIC_NM2230 = 96
FB_ACCEL_NEOMAGIC_NM2360 = 97
FB_ACCEL_NEOMAGIC_NM2380 = 98
FB_ACCEL_PXA3XX = 99
FB_ACCEL_SAVAGE4 = 128
FB_ACCEL_SAVAGE3D = 129
FB_ACCEL_SAVAGE3D_MV = 130
FB_ACCEL_SAVAGE2000 = 131
FB_ACCEL_SAVAGE_MX_MV = 132
FB_ACCEL_SAVAGE_MX = 133
FB_ACCEL_SAVAGE_IX_MV = 134
FB_ACCEL_SAVAGE_IX = 135
FB_ACCEL_PROSAVAGE_PM = 136
FB_ACCEL_PROSAVAGE_KM = 137
FB_ACCEL_S3TWISTER_P = 138
FB_ACCEL_S3TWISTER_K = 139
FB_ACCEL_SUPERSAVAGE = 140
FB_ACCEL_PROSAVAGE_DDR = 141
FB_ACCEL_PROSAVAGE_DDRK = 142
FB_ACCEL_PUV3_UNIGFX = 160
from PIL.Image import ANTIALIAS
from mmap import mmap
from fcntl import ioctl
import struct
mm = None
bpp, w, h = (0, 0, 0)
bytepp = 0
vx, vy, vw, vh = (0, 0, 0, 0)
vi, fi = (None, None)
_fb_cmap = 'IIPPPP'
RGB = False
_verbose = False
msize_kb = 0

def report_fb(i=0, layer=0):
    with open('/dev/fb' + str(i), 'r+b') as (f):
        vi = ioctl(f, FBIOGET_VSCREENINFO, bytes(160))
        vi = list(struct.unpack('I' * 40, vi))
        print(vi)
        ffm = 'ccccccccccccccccL' + 'IIII' + 'HHH' + 'ILIIHHH'
        fic = struct.calcsize(ffm)
        fi = struct.unpack(ffm, ioctl(f, FBIOGET_FSCREENINFO, bytes(fic)))
        print(fi)


def ready_fb(_bpp=None, i=0, layer=0, _win=None):
    global RGB
    global bpp
    global bytepp
    global fi
    global h
    global mm
    global msize_kb
    global vh
    global vi
    global vw
    global vx
    global vy
    global w
    if mm and bpp == _bpp:
        return (
         mm, w, h, bpp)
    with open('/dev/fb' + str(i), 'r+b') as (f):
        vi = ioctl(f, FBIOGET_VSCREENINFO, bytes(160))
        vi = list(struct.unpack('I' * 40, vi))
        bpp = vi[6]
        bytepp = bpp // 8
        if _bpp:
            vi[6] = _bpp
            try:
                vi = ioctl(f, FBIOPUT_VSCREENINFO, struct.pack(('I' * 40), *vi))
                vi = struct.unpack('I' * 40, vi)
                bpp = vi[6]
                bytepp = bpp // 8
            except:
                pass

        if vi[8] == 0:
            RGB = True
        ffm = 'ccccccccccccccccL' + 'IIII' + 'HHH' + 'ILIIHHH'
        fic = struct.calcsize(ffm)
        fi = struct.unpack(ffm, ioctl(f, FBIOGET_FSCREENINFO, bytes(fic)))
        msize = fi[17]
        ll, start = fi[-7:-5]
        w, h = ll // bytepp, vi[1]
        if _win and len(_win) == 4:
            vx, vy, vw, vh = _win
            if vw == 'w':
                vw = w
            if vh == 'h':
                vh = h
            vx, vy, vw, vh = map(int, (vx, vy, vw, vh))
            if vx >= w:
                vx = 0
            if vy >= h:
                vy = 0
            if vx > w:
                vw = w - vx
            else:
                vw -= vx
            if vy > h:
                vh = h - vy
            else:
                vh -= vy
        else:
            vx, vy, vw, vh = (
             0, 0, w, h)
        msize_kb = vw * vh * bytepp // 1024
        mm = mmap(f.fileno(), msize, offset=start)
        return (mm, w, h, bpp)


def magick(fpath):
    """ Use ImageMagick to convert to BGR """
    from subprocess import check_output, PIPE
    try:
        if b'ImageMagick' not in check_output('convert'):
            return
    except FileNotFoundError:
        return

    p = run(['convert', '-verbose', '-coalesce', '-resize', '%dx%d' % (vw, vh), fpath, ('bgr' if bpp < 32 else 'bgra') + ':-'], stdout=PIPE, stderr=PIPE, bufsize=0)
    p, m = p.stdout, p.stderr
    from re import findall
    m = len(findall(b'gif\\[([0-9]+)\\]', m))
    if not m:
        return p
    r = []
    s = len(p) // m
    for i in range(m):
        r.append(p[s * i:s * (i + 1)])

    return r


def fill_scr(r, g, b):
    if bpp == 32:
        seed = struct.pack('BBBB', b, g, r, 255)
    else:
        if bpp == 24:
            seed = struct.pack('BBB', b, g, r)
        elif bpp == 16:
            seed = struct.pack('H', r >> 3 << 11 | g >> 2 << 5 | b >> 3)
    mm.seek(0)
    show_img(seed * vw * vh)


def fill_scr_ani(event=None, delay=0.03333333333333333):
    """ R - G - B transition animation, 30fps delay = 1/30 sec by default """
    from time import sleep
    while not event or not event.is_set():
        for i in range(256):
            if event and event.is_set():
                event.clear()
                return
            fill_scr(i, 255 - i, 255)
            sleep(delay)

        for i in range(256):
            if event and event.is_set():
                event.clear()
                return
            fill_scr(255, i, 255 - i)
            sleep(delay)

        for i in range(256):
            if event and event.is_set():
                event.clear()
                return
            fill_scr(255 - i, 255, i)
            sleep(delay)


def black_scr():
    fill_scr(0, 0, 0)


def white_scr():
    fill_scr(255, 255, 255)


def mmseekto(x, y):
    mm.seek((x + y * w) * bytepp)


def dot(x, y, r, g, b):
    mmseekto(x, y)
    mm.write(struct.pack('BBB', *((r, g, b) if RGB else (b, g, r))))


def get_pixel(x, y):
    mmseekto(x, y)
    return mm.read(bytepp)


def ready_img(fpath, resize=True):
    from PIL import Image
    im = Image.open(fpath)
    if resize:
        return im.resize((vw, vh), ANTIALIAS)
    return im


def _888_to_565(bt):
    b = b''
    for i in range(0, len(bt), 3):
        b += int.to_bytes(bt[i] >> 3 << 11 | bt[(i + 1)] >> 2 << 5 | bt[(i + 2)] >> 3, 2, 'little')

    return b


def numpy_888_565(bt):
    import numpy as np
    arr = np.fromstring(bt, dtype=np.uint32)
    return ((16252928 & arr) >> 8 | (64512 & arr) >> 5 | (248 & arr) >> 3).astype(np.uint16).tostring()


def show_img(img):
    if type(img) is not bytes:
        if (RGB or bpp) == 24:
            img = img.tobytes('raw', 'BGR')
        else:
            img = img.convert('RGBA').tobytes('raw', 'BGRA')
            if bpp == 16:
                img = numpy_888_565(img)
    else:
        if bpp == 24:
            img = img.tobytes()
        else:
            img = img.convert('RGBA').tobytes()
            if bpp == 16:
                img = numpy_888_565(img)
            from io import BytesIO
            b = BytesIO(img)
            s = vw * bytepp
            for y in range(vh):
                mmseekto(vx, vy + y)
                mm.write(b.read(s))


def _ready_gif(cut):
    dur = 1
    if cut.info.get('duration'):
        dur = cut.info['duration'] / 1000
    cut = cut.convert('RGBA' if bpp == 32 else 'RGB').resize((vw, vh), ANTIALIAS)
    if not RGB:
        return (cut.tobytes('raw', 'BGRA' if bpp == 32 else 'BGR'), dur)
    return (
     cut.tobytes(), dur)


def ready_gif(gif, preview=False):
    from PIL import ImageSequence
    imgs = []
    fm = ''
    for l in open('/proc/meminfo'):
        if l.startswith('MemFree:'):
            fm = int(l.split()[1])
            break

    frame_limit = fm // msize_kb
    for img in ImageSequence.Iterator(gif):
        imgs.append(_ready_gif(img))
        if preview:
            preview = False
            show_img(imgs[0][0])
        if len(imgs) >= frame_limit:
            if _verbose:
                print('This file is too big to play. Limited to play only %d frames.' % frame_limit)
            break

    return imgs


def gif_loop(gif, event=None, force_loop=False, preview=False):
    from threading import Thread, Event, Timer
    from itertools import cycle
    imgs = ready_gif(gif, preview)
    if event is None:
        event = Event()
    for i in range(force_loop if type(force_loop) is int else 1):
        for img, dur in cycle(imgs) if force_loop is True else imgs:
            if event and event.is_set():
                return
            Timer(dur, lambda e: event.set(), [event]).start()
            show_img(img)
            event.wait()
            event.clear()


if __name__ == '__main__':
    print("This is a pure Python library file. If you want to use as stand-alone, use 'main.py' instead.")
    exit(1)