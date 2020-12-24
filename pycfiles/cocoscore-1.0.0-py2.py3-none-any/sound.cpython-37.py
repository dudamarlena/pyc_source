# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\cocos\audio\SDL\sound.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 22344 bytes
__doc__ = "An abstract sound format decoding API.\n\nThe latest version of SDL_sound can be found at: http://icculus.org/SDL_sound/\n\nThe basic gist of SDL_sound is that you use an SDL_RWops to get sound data\ninto this library, and SDL_sound will take that data, in one of several\npopular formats, and decode it into raw waveform data in the format of\nyour choice. This gives you a nice abstraction for getting sound into your\ngame or application; just feed it to SDL_sound, and it will handle\ndecoding and converting, so you can just pass it to your SDL audio\ncallback (or whatever). Since it gets data from an SDL_RWops, you can get\nthe initial sound data from any number of sources: file, memory buffer,\nnetwork connection, etc.\n\nAs the name implies, this library depends on SDL: Simple Directmedia Layer,\nwhich is a powerful, free, and cross-platform multimedia library. It can\nbe found at http://www.libsdl.org/\n\nSupport is in place or planned for the following sound formats:\n- .WAV  (Microsoft WAVfile RIFF data, internal.)\n- .VOC  (Creative Labs' Voice format, internal.)\n- .MP3  (MPEG-1 Layer 3 support, via the SMPEG and mpglib libraries.)\n- .MID  (MIDI music converted to Waveform data, internal.)\n- .MOD  (MOD files, via MikMod and ModPlug.)\n- .OGG  (Ogg files, via Ogg Vorbis libraries.)\n- .SPX  (Speex files, via libspeex.)\n- .SHN  (Shorten files, internal.)\n- .RAW  (Raw sound data in any format, internal.)\n- .AU   (Sun's Audio format, internal.)\n- .AIFF (Audio Interchange format, internal.)\n- .FLAC (Lossless audio compression, via libFLAC.)\n"
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
import cocos.audio.SDL.array, cocos.audio.SDL.dll, cocos.audio.SDL.rwops, cocos.audio.SDL.version
SDL = cocos.audio.SDL
_dll = SDL.dll.SDL_DLL('SDL_sound', None, '1.2')

class Sound_Version(Structure):
    """Sound_Version"""
    _fields_ = [
     (
      'major', c_int),
     (
      'minor', c_int),
     (
      'patch', c_int)]

    def __repr__(self):
        return '%d.%d.%d' % (self.major, self.minor, self.patch)


_Sound_GetLinkedVersion = _dll.private_function('Sound_GetLinkedVersion',
  arg_types=[
 POINTER(Sound_Version)],
  return_type=None)

def Sound_GetLinkedVersion():
    """Get the version of the dynamically linked SDL_sound library

    :rtype: `Sound_Version`
    """
    version = Sound_Version()
    _Sound_GetLinkedVersion(byref(version))
    return version


_dll._version = SDL.dll._version_parts(Sound_GetLinkedVersion())

class Sound_AudioInfo(Structure):
    """Sound_AudioInfo"""
    _fields_ = [
     (
      'format', c_ushort),
     (
      'channels', c_ubyte),
     (
      'rate', c_uint)]


class Sound_DecoderInfo(Structure):
    """Sound_DecoderInfo"""
    _fields_ = [
     (
      '_extensions', POINTER(c_char_p)),
     (
      'description', c_char_p),
     (
      'author', c_char_p),
     (
      'url', c_char_p)]

    def __getattr__(self, name):
        if name == 'extensions':
            extensions = []
            ext_p = self._extensions
            i = 0
            while ext_p[i]:
                extensions.append(ext_p[i])
                i += 1

            return extensions
        raise AttributeError(name)


class Sound_Sample(Structure):
    """Sound_Sample"""
    _fields_ = [
     (
      'opaque', c_void_p),
     (
      '_decoder', POINTER(Sound_DecoderInfo)),
     (
      'desired', Sound_AudioInfo),
     (
      'actual', Sound_AudioInfo),
     (
      '_buffer', POINTER(c_ubyte)),
     (
      'buffer_size', c_uint),
     (
      'flags', c_int)]

    def __getattr__(self, name):
        if name == 'decoder':
            return self._decoder.contents
        if name == 'buffer':
            return SDL.array.SDL_array(self._buffer, self.buffer_size, c_ubyte)
        raise AttributeError(name)


Sound_Init = _dll.function('Sound_Init',
  'Initialize SDL_sound.\n\n    This must be called before any other SDL_sound function (except perhaps\n    `Sound_GetLinkedVersion`). You should call `SDL_Init` before calling\n    this.  `Sound_Init` will attempt to call ``SDL_Init(SDL_INIT_AUDIO)``,\n    just in case.  This is a safe behaviour, but it may not configure SDL\n    to your liking by itself.\n    ',
  args=[], arg_types=[], return_type=c_int,
  error_return=0)
Sound_Quit = _dll.function('Sound_Quit',
  'Shutdown SDL_sound.\n\n    This closes any SDL_RWops that were being used as sound sources, and\n    frees any resources in use by SDL_sound.\n\n    All Sound_Sample structures existing will become invalid.\n\n    Once successfully deinitialized, `Sound_Init` can be called again to\n    restart the subsystem. All default API states are restored at this\n    point.\n\n    You should call this before `SDL_Quit`. This will not call `SDL_Quit`\n    for you.\n    ',
  args=[], arg_types=[], return_type=c_int,
  error_return=0)
_Sound_AvailableDecoders = _dll.private_function('Sound_AvailableDecoders',
  arg_types=[], return_type=(POINTER(POINTER(Sound_DecoderInfo))))

def Sound_AvailableDecoders():
    """Get a list of sound formats supported by this version of SDL_sound.

    This is for informational purposes only. Note that the extension listed
    is merely convention: if we list "MP3", you can open an MPEG-1 Layer 3
    audio file with an extension of "XYZ", if you like. The file extensions
    are informational, and only required as a hint to choosing the correct
    decoder, since the sound data may not be coming from a file at all,
    thanks to the abstraction that an SDL_RWops provides.

    :rtype: list of `Sound_DecoderInfo`
    """
    decoders = []
    decoder_p = _Sound_AvailableDecoders()
    i = 0
    while decoder_p[i]:
        decoders.append(decoder_p[i].contents)
        i += 1

    return decoders


Sound_GetError = _dll.function('Sound_GetError',
  "Get the last SDL_sound error message.\n\n    This will be None if there's been no error since the last call to this\n    function.  Each thread has a unique error state associated with it, but\n    each time a new error message is set, it will overwrite the previous\n    one associated with that thread.  It is safe to call this function at\n    any time, even before `Sound_Init`.\n\n    :rtype: str\n    ",
  args=[], arg_types=[], return_type=c_char_p)
Sound_ClearError = _dll.function('Sound_ClearError',
  'Clear the current error message.\n\n    The next call to `Sound_GetError` after `Sound_ClearError` will return\n    None.\n    ',
  args=[], arg_types=[], return_type=None)
Sound_NewSample = _dll.function('Sound_NewSample',
  'Start decoding a new sound sample.\n\n    The data is read via an SDL_RWops structure, so it may be coming from\n    memory, disk, network stream, etc. The `ext` parameter is merely a hint\n    to determining the correct decoder; if you specify, for example, "mp3"\n    for an extension, and one of the decoders lists that as a handled\n    extension, then that decoder is given first shot at trying to claim the\n    data for decoding. If none of the extensions match (or the extension is\n    None), then every decoder examines the data to determine if it can\n    handle it, until one accepts it. In such a case your SDL_RWops will\n    need to be capable of rewinding to the start of the stream.\n\n    If no decoders can handle the data, an exception is raised.\n\n    Optionally, a desired audio format can be specified. If the incoming data\n    is in a different format, SDL_sound will convert it to the desired format\n    on the fly. Note that this can be an expensive operation, so it may be\n    wise to convert data before you need to play it back, if possible, or\n    make sure your data is initially in the format that you need it in.\n    If you don\'t want to convert the data, you can specify None for a desired\n    format. The incoming format of the data, preconversion, can be found\n    in the `Sound_Sample` structure.\n\n    Note that the raw sound data "decoder" needs you to specify both the\n    extension "RAW" and a "desired" format, or it will refuse to handle\n    the data. This is to prevent it from catching all formats unsupported\n    by the other decoders.\n\n    Finally, specify an initial buffer size; this is the number of bytes that\n    will be allocated to store each read from the sound buffer. The more you\n    can safely allocate, the more decoding can be done in one block, but the\n    more resources you have to use up, and the longer each decoding call will\n    take. Note that different data formats require more or less space to\n    store. This buffer can be resized via `Sound_SetBufferSize`.\n\n    The buffer size specified must be a multiple of the size of a single\n    sample point. So, if you want 16-bit, stereo samples, then your sample\n    point size is (2 channels   16 bits), or 32 bits per sample, which is four\n    bytes. In such a case, you could specify 128 or 132 bytes for a buffer,\n    but not 129, 130, or 131 (although in reality, you\'ll want to specify a\n    MUCH larger buffer).\n\n    When you are done with this `Sound_Sample` instance, you can dispose of\n    it via `Sound_FreeSample`.\n\n    You do not have to keep a reference to `rw` around. If this function\n    suceeds, it stores `rw` internally (and disposes of it during the call\n    to `Sound_FreeSample`). If this function fails, it will dispose of the\n    SDL_RWops for you.\n\n    :Parameters:\n        `rw` : `SDL_RWops`\n            SDL_RWops with sound data\n        `ext` : str\n            File extension normally associated with a data format.  Can\n            usually be None.\n        `desired` : `Sound_AudioInfo`\n            Format to convert sound data into.  Can usually be None if you\n            don\'t need conversion.\n        `bufferSize` : int\n            Size, in bytes, to allocate for the decoding buffer\n\n    :rtype: `Sound_Sample`\n    ',
  args=[
 'rw', 'ext', 'desired', 'bufferSize'],
  arg_types=[
 POINTER(SDL.rwops.SDL_RWops), c_char_p,
 POINTER(Sound_AudioInfo), c_uint],
  return_type=(POINTER(Sound_Sample)),
  dereference_return=True,
  require_return=True)
_Sound_NewSampleFromMem = _dll.private_function('Sound_NewSampleFromMem',
  arg_types=[
 POINTER(c_ubyte), c_uint, c_char_p,
 POINTER(Sound_AudioInfo), c_uint],
  return_type=(POINTER(Sound_Sample)),
  dereference_return=True,
  require_return=True,
  since=(9, 9, 9))

def Sound_NewSampleFromMem(data, ext, desired, bufferSize):
    """Start decoding a new sound sample from a buffer.

    This is identical to `Sound_NewSample`, but it creates an `SDL_RWops`
    for you from the buffer.

    :Parameters:
        `data` : `SDL_array` or sequence
            Buffer holding encoded byte sound data
        `ext` : str
            File extension normally associated with a data format.  Can
            usually be None.
        `desired` : `Sound_AudioInfo`
            Format to convert sound data into.  Can usually be None if you
            don't need conversion.
        `bufferSize` : int
            Size, in bytes, to allocate for the decoding buffer

    :rtype: `Sound_Sample`

    :since: Not yet released in SDL_sound
    """
    ref, data = SDL.array.to_ctypes(data, len(data), c_ubyte)
    return _Sound_NewSampleFromMem(data, len(data), ext, desired, bufferSize)


Sound_NewSampleFromFile = _dll.function('Sound_NewSampleFromFile',
  'Start decoding a new sound sample from a file on disk.\n\n    This is identical to `Sound_NewSample`, but it creates an `SDL_RWops\n    for you from the file located at `filename`.\n    ',
  args=[
 'filename', 'desired', 'bufferSize'],
  arg_types=[
 c_char_p, POINTER(Sound_AudioInfo), c_uint],
  return_type=(POINTER(Sound_Sample)),
  dereference_return=True,
  require_return=True)
Sound_FreeSample = _dll.function('Sound_FreeSample',
  'Dispose of a `Sound_Sample`.\n\n    This will also close/dispose of the `SDL_RWops` that was used at\n    creation time.  The `Sound_Sample` structure is invalid after this\n    call.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            The sound sample to delete.\n\n    ',
  args=[
 'sample'],
  arg_types=[
 POINTER(Sound_Sample)],
  return_type=None)
Sound_GetDuration = _dll.function('Sound_GetDuration',
  "Retrieve the total play time of a sample, in milliseconds.\n\n    Report total time length of sample, in milliseconds.  This is a fast\n    call.  Duration is calculated during `Sound_NewSample`, so this is just\n    an accessor into otherwise opaque data.\n\n    Note that not all formats can determine a total time, some can't\n    be exact without fully decoding the data, and thus will estimate the\n    duration. Many decoders will require the ability to seek in the data\n    stream to calculate this, so even if we can tell you how long an .ogg\n    file will be, the same data set may fail if it's, say, streamed over an\n    HTTP connection.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            Sample from which to retrieve duration information.\n\n    :rtype: int\n    :return: Sample length in milliseconds, or -1 if duration can't be\n        determined.\n\n    :since: Not yet released in SDL_sound\n    ",
  args=[
 'sample'],
  arg_types=[
 POINTER(Sound_Sample)],
  return_type=c_int,
  since=(9, 9, 9))
Sound_SetBufferSize = _dll.function('Sound_SetBufferSize',
  "Change the current buffer size for a sample.\n\n    If the buffer size could be changed, then the ``sample.buffer`` and\n    ``sample.buffer_size`` fields will reflect that. If they could not be\n    changed, then your original sample state is preserved. If the buffer is\n    shrinking, the data at the end of buffer is truncated. If the buffer is\n    growing, the contents of the new space at the end is undefined until you\n    decode more into it or initialize it yourself.\n\n    The buffer size specified must be a multiple of the size of a single\n    sample point. So, if you want 16-bit, stereo samples, then your sample\n    point size is (2 channels   16 bits), or 32 bits per sample, which is four\n    bytes. In such a case, you could specify 128 or 132 bytes for a buffer,\n    but not 129, 130, or 131 (although in reality, you'll want to specify a\n    MUCH larger buffer).\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            Sample to modify\n        `new_size` : int\n            The desired size, in bytes of the new buffer\n\n    ",
  args=[
 'sample', 'new_size'],
  arg_types=[
 POINTER(Sound_Sample), c_uint],
  return_type=c_int,
  error_return=0)
Sound_Decode = _dll.function('Sound_Decode',
  'Decode more of the sound data in a `Sound_Sample`.\n\n    It will decode at most sample->buffer_size bytes into ``sample.buffer``\n    in the desired format, and return the number of decoded bytes.\n\n    If ``sample.buffer_size`` bytes could not be decoded, then refer to\n    ``sample.flags`` to determine if this was an end-of-stream or error\n    condition.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            Do more decoding to this sample\n\n    :rtype: int\n    :return: number of bytes decoded into ``sample.buffer``\n    ',
  args=[
 'sample'],
  arg_types=[
 POINTER(Sound_Sample)],
  return_type=c_uint)
Sound_DecodeAll = _dll.function('Sound_DecodeAll',
  "Decode the remainder of the sound data in a `Sound_Sample`.\n\n    This will dynamically allocate memory for the entire remaining sample.\n    ``sample.buffer_size`` and ``sample.buffer`` will be updated to reflect\n    the new buffer.  Refer to ``sample.flags`` to determine if the\n    decoding finished due to an End-of-stream or error condition.\n\n    Be aware that sound data can take a large amount of memory, and that\n    this function may block for quite awhile while processing. Also note\n    that a streaming source (for example, from a SDL_RWops that is getting\n    fed from an Internet radio feed that doesn't end) may fill all available\n    memory before giving up...be sure to use this on finite sound sources\n    only.\n\n    When decoding the sample in its entirety, the work is done one buffer\n    at a time. That is, sound is decoded in ``sample.buffer_size`` blocks, and\n    appended to a continually-growing buffer until the decoding completes.\n    That means that this function will need enough RAM to hold\n    approximately ``sample.buffer_size`` bytes plus the complete decoded\n    sample at most. The larger your buffer size, the less overhead this\n    function needs, but beware the possibility of paging to disk. Best to\n    make this user-configurable if the sample isn't specific and small.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            Do all decoding for this sample.\n\n    :rtype: int\n    :return: number of bytes decoded into ``sample.buffer``\n    ",
  args=[
 'sample'],
  arg_types=[
 POINTER(Sound_Sample)],
  return_type=c_uint)
Sound_Rewind = _dll.function('Sound_Rewind',
  "Rewind a sample to the start.\n\n    Restart a sample at the start of its waveform data, as if newly\n    created with `Sound_NewSample`. If successful, the next call to\n    `Sound_Decode` will give audio data from the earliest point in the\n    stream.\n\n    Beware that this function will fail if the SDL_RWops that feeds the\n    decoder can not be rewound via it's seek method, but this can\n    theoretically be avoided by wrapping it in some sort of buffering\n    SDL_RWops.\n\n    This function will raise an exception if the RWops is not seekable, or\n    SDL_sound is not initialized.\n\n    If this function fails, the state of the sample is undefined, but it\n    is still safe to call `Sound_FreeSample` to dispose of it.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            The sample to rewind\n\n    ",
  args=[
 'sample'],
  arg_types=[
 POINTER(Sound_Sample)],
  return_type=c_int,
  error_return=0)
Sound_Seek = _dll.function('Sound_Seek',
  "Seek to a different point in a sample.\n\n    Reposition a sample's stream. If successful, the next call to\n    `Sound_Decode` or `Sound_DecodeAll` will give audio data from the\n    offset you specified.\n\n    The offset is specified in milliseconds from the start of the\n    sample.\n\n    Beware that this function can fail for several reasons. If the\n    SDL_RWops that feeds the decoder can not seek, this call will almost\n    certainly fail, but this can theoretically be avoided by wrapping it\n    in some sort of buffering SDL_RWops. Some decoders can never seek,\n    others can only seek with certain files. The decoders will set a flag\n    in the sample at creation time to help you determine this.\n\n    You should check ``sample.flags & SOUND_SAMPLEFLAG_CANSEEK``\n    before attempting. `Sound_Seek` reports failure immediately if this\n    flag isn't set. This function can still fail for other reasons if the\n    flag is set.\n\n    This function can be emulated in the application with `Sound_Rewind`\n    and predecoding a specific amount of the sample, but this can be\n    extremely inefficient. `Sound_Seek()` accelerates the seek on a\n    with decoder-specific code.\n\n    If this function fails, the sample should continue to function as if\n    this call was never made. If there was an unrecoverable error,\n    ``sample.flags & SOUND_SAMPLEFLAG_ERROR`` will be set, which your\n    regular decoding loop can pick up.\n\n    On success, ERROR, EOF, and EAGAIN are cleared from sample->flags.\n\n    :Parameters:\n        `sample` : `Sound_Sample`\n            The sample to seek\n        `ms` : int\n            The new position, in milliseconds, from the start of sample\n\n    ",
  args=[
 'sample', 'ms'],
  arg_types=[
 POINTER(Sound_Sample), c_uint],
  return_type=c_int,
  error_return=0)