# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/libsixel/__init__.py
# Compiled at: 2018-06-07 08:23:33
from ctypes import cdll, c_void_p, c_int, c_byte, c_char_p, POINTER, byref, CFUNCTYPE, string_at
from ctypes.util import find_library
SIXEL_OK = 0
SIXEL_FALSE = 4096
SIXEL_RUNTIME_ERROR = SIXEL_FALSE | 256
SIXEL_LOGIC_ERROR = SIXEL_FALSE | 512
SIXEL_FEATURE_ERROR = SIXEL_FALSE | 768
SIXEL_LIBC_ERROR = SIXEL_FALSE | 1024
SIXEL_CURL_ERROR = SIXEL_FALSE | 1280
SIXEL_JPEG_ERROR = SIXEL_FALSE | 1536
SIXEL_PNG_ERROR = SIXEL_FALSE | 1792
SIXEL_GDK_ERROR = SIXEL_FALSE | 2048
SIXEL_GD_ERROR = SIXEL_FALSE | 2304
SIXEL_STBI_ERROR = SIXEL_FALSE | 2560
SIXEL_STBIW_ERROR = SIXEL_FALSE | 2816
SIXEL_INTERRUPTED = SIXEL_OK | 1
SIXEL_BAD_ALLOCATION = SIXEL_RUNTIME_ERROR | 1
SIXEL_BAD_ARGUMENT = SIXEL_RUNTIME_ERROR | 2
SIXEL_BAD_INPUT = SIXEL_RUNTIME_ERROR | 3
SIXEL_NOT_IMPLEMENTED = SIXEL_FEATURE_ERROR | 1

def SIXEL_SUCCEEDED(status):
    return status & 4096 == 0


def SIXEL_FAILED(status):
    return status & 4096 != 0


SIXEL_LARGE_AUTO = 0
SIXEL_LARGE_NORM = 1
SIXEL_LARGE_LUM = 2
SIXEL_REP_AUTO = 0
SIXEL_REP_CENTER_BOX = 1
SIXEL_REP_AVERAGE_COLORS = 2
SIXEL_REP_AVERAGE_PIXELS = 3
SIXEL_DIFFUSE_AUTO = 0
SIXEL_DIFFUSE_NONE = 1
SIXEL_DIFFUSE_ATKINSON = 2
SIXEL_DIFFUSE_FS = 3
SIXEL_DIFFUSE_JAJUNI = 4
SIXEL_DIFFUSE_STUCKI = 5
SIXEL_DIFFUSE_BURKES = 6
SIXEL_DIFFUSE_A_DITHER = 7
SIXEL_DIFFUSE_X_DITHER = 8
SIXEL_QUALITY_AUTO = 0
SIXEL_QUALITY_HIGH = 1
SIXEL_QUALITY_LOW = 2
SIXEL_QUALITY_FULL = 3
SIXEL_QUALITY_HIGHCOLOR = 4
SIXEL_BUILTIN_MONO_DARK = 0
SIXEL_BUILTIN_MONO_LIGHT = 1
SIXEL_BUILTIN_XTERM16 = 2
SIXEL_BUILTIN_XTERM256 = 3
SIXEL_BUILTIN_VT340_MONO = 4
SIXEL_BUILTIN_VT340_COLOR = 5
SIXEL_BUILTIN_G1 = 6
SIXEL_BUILTIN_G2 = 7
SIXEL_BUILTIN_G4 = 8
SIXEL_BUILTIN_G8 = 9
SIXEL_FORMATTYPE_COLOR = 0
SIXEL_FORMATTYPE_GRAYSCALE = 64
SIXEL_FORMATTYPE_PALETTE = 128
SIXEL_PIXELFORMAT_RGB555 = SIXEL_FORMATTYPE_COLOR | 1
SIXEL_PIXELFORMAT_RGB565 = SIXEL_FORMATTYPE_COLOR | 2
SIXEL_PIXELFORMAT_RGB888 = SIXEL_FORMATTYPE_COLOR | 3
SIXEL_PIXELFORMAT_BGR555 = SIXEL_FORMATTYPE_COLOR | 4
SIXEL_PIXELFORMAT_BGR565 = SIXEL_FORMATTYPE_COLOR | 5
SIXEL_PIXELFORMAT_BGR888 = SIXEL_FORMATTYPE_COLOR | 6
SIXEL_PIXELFORMAT_ARGB8888 = SIXEL_FORMATTYPE_COLOR | 16
SIXEL_PIXELFORMAT_RGBA8888 = SIXEL_FORMATTYPE_COLOR | 17
SIXEL_PIXELFORMAT_ABGR8888 = SIXEL_FORMATTYPE_COLOR | 18
SIXEL_PIXELFORMAT_BGRA8888 = SIXEL_FORMATTYPE_COLOR | 19
SIXEL_PIXELFORMAT_G1 = SIXEL_FORMATTYPE_GRAYSCALE | 0
SIXEL_PIXELFORMAT_G2 = SIXEL_FORMATTYPE_GRAYSCALE | 1
SIXEL_PIXELFORMAT_G4 = SIXEL_FORMATTYPE_GRAYSCALE | 2
SIXEL_PIXELFORMAT_G8 = SIXEL_FORMATTYPE_GRAYSCALE | 3
SIXEL_PIXELFORMAT_AG88 = SIXEL_FORMATTYPE_GRAYSCALE | 19
SIXEL_PIXELFORMAT_GA88 = SIXEL_FORMATTYPE_GRAYSCALE | 35
SIXEL_PIXELFORMAT_PAL1 = SIXEL_FORMATTYPE_PALETTE | 0
SIXEL_PIXELFORMAT_PAL2 = SIXEL_FORMATTYPE_PALETTE | 1
SIXEL_PIXELFORMAT_PAL4 = SIXEL_FORMATTYPE_PALETTE | 2
SIXEL_PIXELFORMAT_PAL8 = SIXEL_FORMATTYPE_PALETTE | 3
SIXEL_PALETTETYPE_AUTO = 0
SIXEL_PALETTETYPE_HLS = 1
SIXEL_PALETTETYPE_RGB = 2
SIXEL_ENCODEPOLICY_AUTO = 0
SIXEL_ENCODEPOLICY_FAST = 1
SIXEL_ENCODEPOLICY_SIZE = 2
SIXEL_RES_NEAREST = 0
SIXEL_RES_GAUSSIAN = 1
SIXEL_RES_HANNING = 2
SIXEL_RES_HAMMING = 3
SIXEL_RES_BILINEAR = 4
SIXEL_RES_WELSH = 5
SIXEL_RES_BICUBIC = 6
SIXEL_RES_LANCZOS2 = 7
SIXEL_RES_LANCZOS3 = 8
SIXEL_RES_LANCZOS4 = 9
SIXEL_FORMAT_GIF = 0
SIXEL_FORMAT_PNG = 1
SIXEL_FORMAT_BMP = 2
SIXEL_FORMAT_JPG = 3
SIXEL_FORMAT_TGA = 4
SIXEL_FORMAT_WBMP = 5
SIXEL_FORMAT_TIFF = 6
SIXEL_FORMAT_SIXEL = 7
SIXEL_FORMAT_PNM = 8
SIXEL_FORMAT_GD2 = 9
SIXEL_FORMAT_PSD = 10
SIXEL_FORMAT_HDR = 11
SIXEL_LOOP_AUTO = 0
SIXEL_LOOP_FORCE = 1
SIXEL_LOOP_DISABLE = 2
SIXEL_OPTFLAG_INPUT = 'i'
SIXEL_OPTFLAG_OUTPUT = 'o'
SIXEL_OPTFLAG_OUTFILE = 'o'
SIXEL_OPTFLAG_7BIT_MODE = '7'
SIXEL_OPTFLAG_8BIT_MODE = '8'
SIXEL_OPTFLAG_COLORS = 'p'
SIXEL_OPTFLAG_MAPFILE = 'm'
SIXEL_OPTFLAG_MONOCHROME = 'e'
SIXEL_OPTFLAG_INSECURE = 'k'
SIXEL_OPTFLAG_INVERT = 'i'
SIXEL_OPTFLAG_HIGH_COLOR = 'I'
SIXEL_OPTFLAG_USE_MACRO = 'u'
SIXEL_OPTFLAG_MACRO_NUMBER = 'n'
SIXEL_OPTFLAG_COMPLEXION_SCORE = 'C'
SIXEL_OPTFLAG_IGNORE_DELAY = 'g'
SIXEL_OPTFLAG_STATIC = 'S'
SIXEL_OPTFLAG_DIFFUSION = 'd'
SIXEL_OPTFLAG_FIND_LARGEST = 'f'
SIXEL_OPTFLAG_SELECT_COLOR = 's'
SIXEL_OPTFLAG_CROP = 'c'
SIXEL_OPTFLAG_WIDTH = 'w'
SIXEL_OPTFLAG_HEIGHT = 'h'
SIXEL_OPTFLAG_RESAMPLING = 'r'
SIXEL_OPTFLAG_QUALITY = 'q'
SIXEL_OPTFLAG_LOOPMODE = 'l'
SIXEL_OPTFLAG_PALETTE_TYPE = 't'
SIXEL_OPTFLAG_BUILTIN_PALETTE = 'b'
SIXEL_OPTFLAG_ENCODE_POLICY = 'E'
SIXEL_OPTFLAG_BGCOLOR = 'B'
SIXEL_OPTFLAG_PENETRATE = 'P'
SIXEL_OPTFLAG_PIPE_MODE = 'D'
SIXEL_OPTFLAG_VERBOSE = 'v'
SIXEL_OPTFLAG_VERSION = 'V'
SIXEL_OPTFLAG_HELP = 'H'
if not find_library('sixel'):
    raise ImportError('libsixel not found.')
_sixel = cdll.LoadLibrary(find_library('sixel'))

def sixel_helper_format_error(status):
    _sixel.sixel_helper_format_error.restype = c_char_p
    _sixel.sixel_helper_format_error.argtypes = [c_int]
    return _sixel.sixel_helper_format_error(status)


def sixel_helper_compute_depth(pixelformat):
    _sixel.sixel_helper_compute_depth.restype = c_int
    _sixel.sixel_encoder_encode.argtypes = [c_int]
    return _sixel.sixel_helper_compute_depth(pixelformat)


def sixel_output_new(fn_write, priv=None, allocator=c_void_p(None)):

    def _fn_write_local(data, size, priv_from_c):
        fn_write(string_at(data, size), priv)
        return size

    sixel_write_function = CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
    _sixel.sixel_output_new.restype = c_int
    _sixel.sixel_output_new.argtypes = [POINTER(c_void_p), sixel_write_function, c_void_p, c_void_p]
    output = c_void_p(None)
    _fn_write = sixel_write_function(_fn_write_local)
    _fn_write.restype = c_int
    _fn_write.argtypes = [sixel_write_function, c_void_p, c_void_p]
    status = _sixel.sixel_output_new(byref(output), _fn_write, c_void_p(None), allocator)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)
    output.__fn_write = _fn_write
    return output


def sixel_output_ref(output):
    _sixel.sixel_output_ref.restype = None
    _sixel.sixel_output_ref.argtypes = [c_void_p]
    _sixel.sixel_output_ref(output)
    return


def sixel_output_unref(output):
    _sixel.sixel_output_unref.restype = None
    _sixel.sixel_output_unref.argtypes = [c_void_p]
    _sixel.sixel_output_unref(output)
    output.__fn_write = None
    return


def sixel_output_get_8bit_availability(output):
    _sixel.sixel_output_get_8bit_availability.restype = None
    _sixel.sixel_output_get_8bit_availability.argtypes = [c_void_p]
    _sixel.sixel_output_get_8bit_availability(output)
    return


def sixel_output_set_8bit_availability(output):
    _sixel.sixel_output_set_8bit_availability.restype = None
    _sixel.sixel_output_set_8bit_availability.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_8bit_availability(output)
    return


def sixel_output_set_gri_arg_limit(output):
    _sixel.sixel_output_set_gri_arg_limit.restype = None
    _sixel.sixel_output_set_gri_arg_limit.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_gri_arg_limit(output)
    return


def sixel_output_set_penetrate_multiplexer(output):
    _sixel.sixel_output_set_penetrate_multiplexer.restype = None
    _sixel.sixel_output_set_penetrate_multiplexer.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_penetrate_multiplexer(output)
    return


def sixel_output_set_skip_dcs_envelope(output):
    _sixel.sixel_output_set_skip_dcs_envelope.restype = None
    _sixel.sixel_output_set_skip_dcs_envelope.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_skip_dcs_envelope(output)
    return


def sixel_output_set_palette_type(output):
    _sixel.sixel_output_set_palette_type.restype = None
    _sixel.sixel_output_set_palette_type.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_palette_type(output)
    return


def sixel_output_set_encode_policy(output):
    _sixel.sixel_output_set_encode_policy.restype = None
    _sixel.sixel_output_set_encode_policy.argtypes = [c_void_p, c_int]
    _sixel.sixel_output_set_encode_policy(output)
    return


def sixel_dither_new(ncolors, allocator=None):
    _sixel.sixel_dither_new.restype = c_int
    _sixel.sixel_dither_new.argtypes = [POINTER(c_void_p), c_int, c_void_p]
    dither = c_void_p(None)
    status = _sixel.sixel_dither_new(byref(dither), ncolors, allocator)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)
    return dither


def sixel_dither_get(builtin_dither):
    _sixel.sixel_dither_get.restype = c_void_p
    _sixel.sixel_dither_get.argtypes = [c_int]
    return _sixel.sixel_dither_get(builtin_dither)


def sixel_dither_destroy(dither):
    _sixel.sixel_dither_destroy.restype = None
    _sixel.sixel_dither_destroy.argtypes = [c_void_p]
    return _sixel.sixel_dither_destroy(dither)


def sixel_dither_ref(dither):
    _sixel.sixel_dither_ref.restype = None
    _sixel.sixel_dither_ref.argtypes = [c_void_p]
    return _sixel.sixel_dither_ref(dither)


def sixel_dither_unref(dither):
    _sixel.sixel_dither_unref.restype = None
    _sixel.sixel_dither_unref.argtypes = [c_void_p]
    return _sixel.sixel_dither_unref(dither)


def sixel_dither_initialize(dither, data, width, height, pixelformat, method_for_largest=SIXEL_LARGE_AUTO, method_for_rep=SIXEL_REP_AUTO, quality_mode=SIXEL_QUALITY_AUTO):
    _sixel.sixel_dither_initialize.restype = c_int
    _sixel.sixel_dither_initialize.argtypes = [c_void_p, c_char_p, c_int, c_int, c_int,
     c_int, c_int, c_int]
    status = _sixel.sixel_dither_initialize(dither, data, width, height, pixelformat, method_for_largest, method_for_rep, quality_mode)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)


def sixel_dither_set_diffusion_type(dither, method_for_diffuse):
    _sixel.sixel_dither_set_diffusion_type.restype = None
    _sixel.sixel_dither_set_diffusion_type.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_diffusion_type(dither, method_for_diffuse)
    return


def sixel_dither_get_num_of_palette_colors(dither):
    _sixel.sixel_dither_get_num_of_palette_colors.restype = c_int
    _sixel.sixel_dither_get_num_of_palette_colors.argtypes = [c_void_p]
    return _sixel.sixel_dither_get_num_of_palette_colors(dither)


def sixel_dither_get_num_of_histogram_colors(dither):
    _sixel.sixel_dither_get_num_of_histogram_colors.restype = c_int
    _sixel.sixel_dither_get_num_of_histogram_colors.argtypes = [c_void_p]
    return _sixel.sixel_dither_get_num_of_histogram_colors(dither)


def sixel_dither_get_palette(dither):
    _sixel.sixel_dither_get_palette.restype = c_char_p
    _sixel.sixel_dither_get_palette.argtypes = [c_void_p]
    cpalette = _sixel.sixel_dither_get_palette(dither)
    return [ ord(c) for c in cpalette ]


def sixel_dither_set_palette(dither, palette):
    _sixel.sixel_dither_set_palette.restype = None
    _sixel.sixel_dither_set_palette.argtypes = [c_void_p, c_char_p]
    cpalette = ('').join(map(chr, palette))
    _sixel.sixel_dither_set_palette(dither, cpalette)
    return


def sixel_dither_set_complexion_score(dither, score):
    _sixel.sixel_dither_set_complexion_score.restype = None
    _sixel.sixel_dither_set_complexion_score.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_complexion_score(dither, score)
    return


def sixel_dither_set_body_only(dither, bodyonly):
    _sixel.sixel_dither_set_body_only.restype = None
    _sixel.sixel_dither_set_body_only.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_body_only(dither, bodyonly)
    return


def sixel_dither_set_optimize_palette(dither, do_opt):
    _sixel.sixel_dither_set_optimize_palette.restype = None
    _sixel.sixel_dither_set_optimize_palette.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_optimize_palette(dither, do_opt)
    return


def sixel_dither_set_pixelformat(dither, pixelformat):
    _sixel.sixel_dither_set_pixelformat.restype = None
    _sixel.sixel_dither_set_pixelformat.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_pixelformat(dither, pixelformat)
    return


def sixel_dither_set_transparent(dither, transparent):
    _sixel.sixel_dither_set_transparent.restype = None
    _sixel.sixel_dither_set_transparent.argtypes = [c_void_p, c_int]
    _sixel.sixel_dither_set_transparent(dither, transparent)
    return


def sixel_encode(pixels, width, height, depth, dither, output):
    _sixel.sixel_encode.restype = c_int
    _sixel.sixel_encode.argtypes = [c_char_p, c_int, c_int, c_int, c_void_p, c_void_p]
    return _sixel.sixel_encode(pixels, width, height, depth, dither, output)


def sixel_encoder_new(allocator=c_void_p(None)):
    _sixel.sixel_encoder_new.restype = c_int
    _sixel.sixel_encoder_new.argtypes = [POINTER(c_void_p), c_void_p]
    encoder = c_void_p(None)
    status = _sixel.sixel_encoder_new(byref(encoder), allocator)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)
    return encoder


def sixel_encoder_ref(encoder):
    _sixel.sixel_encoder_ref.restype = None
    _sixel.sixel_encoder_ref.argtypes = [c_void_p]
    _sixel.sixel_encoder_ref(encoder)
    return


def sixel_encoder_unref(encoder):
    _sixel.sixel_encoder_unref.restype = None
    _sixel.sixel_encoder_unref.argtypes = [c_void_p]
    _sixel.sixel_encoder_unref(encoder)
    return


def sixel_encoder_setopt(encoder, flag, arg=None):
    _sixel.sixel_encoder_setopt.restype = c_int
    _sixel.sixel_encoder_setopt.argtypes = [c_void_p, c_int, c_char_p]
    flag = ord(flag)
    if arg:
        arg = str(arg).encode('utf-8')
    status = _sixel.sixel_encoder_setopt(encoder, flag, arg)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)


def sixel_encoder_encode(encoder, filename):
    import locale
    language, encoding = locale.getdefaultlocale()
    _sixel.sixel_encoder_encode.restype = c_int
    _sixel.sixel_encoder_encode.argtypes = [c_void_p, c_char_p]
    status = _sixel.sixel_encoder_encode(encoder, filename.encode(encoding))
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)


def sixel_encoder_encode_bytes(encoder, buf, width, height, pixelformat, palette):
    depth = sixel_helper_compute_depth(pixelformat)
    if depth <= 0:
        raise ValueError('invalid pixelformat value : %d' % pixelformat)
    if len(buf) < width * height * depth:
        raise ValueError('buf.len is too short : %d < %d * %d * %d' % (buf.len, width, height, depth))
    if not hasattr(buf, 'readonly') or buf.readonly:
        cbuf = c_void_p.from_buffer_copy(buf)
    else:
        cbuf = c_void_p.from_buffer(buf)
    if palette:
        cpalettelen = len(palette)
        cpalette = (c_byte * cpalettelen)(*palette)
    else:
        cpalettelen = None
        cpalette = None
    _sixel.sixel_encoder_encode_bytes.restype = c_int
    _sixel.sixel_encoder_encode.argtypes = [c_void_p, c_void_p, c_int, c_int, c_int, c_void_p, c_int]
    status = _sixel.sixel_encoder_encode_bytes(encoder, buf, width, height, pixelformat, cpalette, cpalettelen)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)
    return


def sixel_decoder_new(allocator=c_void_p(None)):
    _sixel.sixel_decoder_new.restype = c_int
    _sixel.sixel_decoder_new.argtypes = [POINTER(c_void_p), c_void_p]
    decoder = c_void_p(None)
    status = _sixel.sixel_decoder_new(byref(decoder), c_void_p(None))
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)
    return decoder


def sixel_decoder_ref(decoder):
    _sixel.sixel_decoder_ref.restype = None
    _sixel.sixel_decoder_ref.argtypes = [c_void_p]
    _sixel.sixel_decoder_ref(decoder)
    return


def sixel_decoder_unref(decoder):
    _sixel.sixel_decoder_unref.restype = None
    _sixel.sixel_decoder_unref.argtypes = [c_void_p]
    _sixel.sixel_decoder_unref(decoder)
    return


def sixel_decoder_setopt(decoder, flag, arg=None):
    _sixel.sixel_decoder_setopt.restype = c_int
    _sixel.sixel_decoder_setopt.argtypes = [c_void_p, c_int, c_char_p]
    flag = ord(flag)
    if arg:
        arg = str(arg).encode('utf-8')
    status = _sixel.sixel_decoder_setopt(decoder, flag, arg)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)


def sixel_decoder_decode(decoder, infile=None):
    _sixel.sixel_decoder_decode.restype = c_int
    _sixel.sixel_decoder_decode.argtypes = [c_void_p]
    if infile:
        sixel_decoder_setopt(decoder, SIXEL_OPTFLAG_INPUT, infile)
    status = _sixel.sixel_decoder_decode(decoder)
    if SIXEL_FAILED(status):
        message = sixel_helper_format_error(status)
        raise RuntimeError(message)