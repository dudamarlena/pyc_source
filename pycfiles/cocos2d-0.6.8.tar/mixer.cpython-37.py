# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\audio\SDL\mixer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 38050 bytes
"""A simple multi-channel audio mixer.

It supports 8 channels of 16 bit stereo audio, plus a single channel
of music, mixed by MidMod MOD, Timidity MIDI or SMPEG MP3 libraries.

The mixer can currently load Microsoft WAVE files and Creative Labs VOC
files as audio samples, and can load MIDI files via Timidity and the
following music formats via MikMod: MOD, S3M, IT, XM.  It can load Ogg
Vorbis streams as music if built with the Ogg Vorbis libraries, and finally
it can load MP3 music using the SMPEG library.

The process of mixing MIDI files to wave output is very CPU intensive, so
if playing regular WAVE files sounds great, but playing MIDI files sounds
choppy, try using 8-bit audio, mono audio, or lower frequencies.

:note: The music stream does not resample to the required audio rate.  You
    must call `Mix_OpenAudio` with the sampling rate of your music track.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
import cocos.compat
from . import dll
from . import version
from . import array
from . import rwops
_dll = dll.SDL_DLL('SDL_mixer', 'Mix_Linked_Version', '1.2')
Mix_Linked_Version = _dll.function('Mix_Linked_Version',
  'Get the version of the dynamically linked SDL_mixer library.\n    ',
  args=[], arg_types=[], return_type=(POINTER(version.SDL_version)),
  dereference_return=True,
  require_return=True)

class Mix_Chunk(Structure):
    __doc__ = 'Internal format for an audio chunk.\n\n    :Ivariables:\n        `allocated` : int\n            Undocumented.\n        `abuf` : `SDL_array`\n            Buffer of audio data\n        `alen` : int\n            Length of audio buffer\n        `volume` : int\n            Per-sample volume, in range [0, 128]\n\n    '
    _fields_ = [('allocated', c_int),
     (
      '_abuf', POINTER(c_ubyte)),
     (
      'alen', c_uint),
     (
      'volume', c_ubyte)]

    def __getattr__(self, attr):
        if attr == 'abuf':
            return array.SDL_array(self._abuf, self.alen, c_ubyte)
        raise AttributeError(attr)


_Mix_Music = c_void_p
Mix_OpenAudio = _dll.function('Mix_OpenAudio',
  'Open the mixer with a certain audio format.\n\n    :Parameters:\n        `frequency` : int\n            Samples per second.  Typical values are 22050, 44100, 44800.\n        `format` : int\n            Audio format; one of AUDIO_U8, AUDIO_S8, AUDIO_U16LSB,\n            AUDIO_S16LSB, AUDIO_U16MSB or AUDIO_S16MSB\n        `channels` : int\n            Either 1 for monophonic or 2 for stereo.\n        `chunksize` : int\n            Size of the audio buffer.  Typical values are 4096, 8192.\n\n    ',
  args=[
 'frequency', 'format', 'channels', 'chunksize'],
  arg_types=[
 c_int, c_ushort, c_int, c_int],
  return_type=c_int,
  error_return=(-1))
Mix_AllocateChannels = _dll.function('Mix_AllocateChannels',
  'Dynamically change the number of channels managed by the mixer.\n\n    If decreasing the number of channels, the upper channels\n    are stopped.\n\n    :Parameters:\n     - `numchans`: int\n\n    :rtype: int\n    :return: the new number of allocated channels.\n    ',
  args=[
 'numchans'],
  arg_types=[
 c_int],
  return_type=c_int)
_Mix_QuerySpec = _dll.private_function('Mix_QuerySpec',
  arg_types=[
 POINTER(c_int), POINTER(c_ushort), POINTER(c_int)],
  return_type=c_int)

def Mix_QuerySpec():
    """Find out what the actual audio device parameters are.

    The function returns a tuple giving each parameter value.  The first
    value is 1 if the audio has been opened, 0 otherwise.

    :rtype: (int, int, int, int)
    :return: (opened, frequency, format, channels)
    """
    frequency, format, channels = c_int(), c_ushort(), c_int()
    opened = _Mix_QuerySpec(byref(frequency), byref(format), byref(channels))
    return (opened, frequency.value, format.value, channels.value)


Mix_LoadWAV_RW = _dll.function('Mix_LoadWAV_RW',
  'Load a WAV, RIFF, AIFF, OGG or VOC file from a RWops source.\n\n\n\n    :rtype: `Mix_Chunk`\n    ',
  args=[
 'src', 'freesrc'],
  arg_types=[
 POINTER(rwops.SDL_RWops), c_int],
  return_type=(POINTER(Mix_Chunk)),
  dereference_return=True,
  require_return=True)

def Mix_LoadWAV(file):
    """Load a WAV, RIFF, AIFF, OGG or VOC file.

    :Parameters:
        `file` : string
            Filename to load.

    :rtype: `Mix_Chunk`
    """
    filename = cocos.compat.asciibytes(file)
    return Mix_LoadWAV_RW(rwops.SDL_RWFromFile(filename, b'rb'), 1)


Mix_LoadMUS = _dll.function('Mix_LoadMUS',
  'Load a WAV, MID, OGG, MP3 or MOD file.\n\n    :Parameters:\n        `file` : string\n            Filename to load.\n\n    :rtype: ``Mix_Music``\n    ',
  args=[
 'file'],
  arg_types=[
 c_char_p],
  return_type=_Mix_Music,
  require_return=True)
Mix_LoadMUS_RW = _dll.function('Mix_LoadMUS_RW',
  'Load a MID, OGG, MP3 or MOD file from a RWops source.\n\n    :Parameters:\n        `src` : `SDL_RWops`\n            Readable RWops to load from.\n        `freesrc` : `int`\n            If non-zero, the source will be closed after loading.\n\n    :rtype: ``Mix_Music``\n    ',
  args=[
 'file'],
  arg_types=[
 c_char_p],
  return_type=_Mix_Music,
  require_return=True)
_Mix_QuickLoad_WAV = _dll.private_function('Mix_QuickLoad_WAV',
  arg_types=[
 POINTER(c_ubyte)],
  return_type=(POINTER(Mix_Chunk)),
  dereference_return=True,
  require_return=True)

def Mix_QuickLoad_WAV(mem):
    """Load a wave file of the mixer format from a sequence or SDL_array.

    :Parameters:
     - `mem`: sequence or `SDL_array`

    :rtype: `Mix_Chunk`
    """
    ref, mem = array.to_ctypes(mem, len(mem), c_ubyte)
    return _Mix_QuickLoad_WAV(mem)


_Mix_QuickLoad_RAW = _dll.private_function('Mix_QuickLoad_RAW',
  arg_types=[
 POINTER(c_ubyte), c_uint],
  return_type=(POINTER(Mix_Chunk)),
  dereference_return=True,
  require_return=True)

def Mix_QuickLoad_RAW(mem):
    """Load raw audio data of the mixer format from a sequence or SDL_array.

    :Parameters:
     - `mem`: sequence or `SDL_array`

    :rtype: `Mix_Chunk`
    """
    l = len(mem)
    ref, mem = SDL.array.to_ctypes(mem, len(mem), c_ubyte)
    return _Mix_QuickLoad_RAW(mem, l)


Mix_FreeChunk = _dll.function('Mix_FreeChunk',
  'Free an audio chunk previously loaded.\n\n    :Parameters:\n     - `chunk`: `Mix_Chunk`\n\n    ',
  args=[
 'chunk'],
  arg_types=[
 POINTER(Mix_Chunk)],
  return_type=None)
Mix_FreeMusic = _dll.function('Mix_FreeMusic',
  'Free a music chunk previously loaded.\n\n    :Parameters:\n     - `music`: ``Mix_Music``\n\n    ',
  args=[
 'music'],
  arg_types=[
 _Mix_Music],
  return_type=None)
Mix_GetMusicType = _dll.function('Mix_GetMusicType',
  'Get the music format of a mixer music.\n\n    Returns the format of the currently playing music if `music` is None.\n\n    :Parameters:\n     - `music`: ``Mix_Music``\n\n    :rtype: int\n    :return: one of `MUS_NONE`, `MUS_CMD`, `MUS_WAV`, `MUS_MOD`, `MUS_MID`,\n        `MUS_OGG` or `MUS_MP3`\n    ',
  args=[
 'music'],
  arg_types=[
 _Mix_Music],
  return_type=c_int)
_Mix_FilterFunc = CFUNCTYPE(None, c_void_p, POINTER(c_ubyte), c_int)

def _make_filter(func, udata):
    if func:

        def f(ignored, stream, len):
            if len < 0:
                return
            stream = array.SDL_array(stream, len, c_ubyte)
            func(udata, stream)

        return _Mix_FilterFunc(f)
    return _Mix_FilterFunc()


_Mix_SetPostMix = _dll.private_function('Mix_SetPostMix',
  arg_types=[
 _Mix_FilterFunc, c_void_p],
  return_type=None)
_mix_postmix_ref = None

def Mix_SetPostMix(mix_func, udata):
    """Set a function that is called after all mixing is performed.

    This can be used to provide real-time visual display of the audio
    stream or add a custom mixer filter for the stream data.

    :Parameters
        `mix_func` : function
            The function must have the signature
            (stream: `SDL_array`, udata: any) -> None.  The first argument
            is the array of audio data that may be modified in place.
            `udata` is the value passed in this function.
        `udata` : any
            A variable that is passed to the `mix_func` function each
            call.

    """
    global _mix_postmix_ref
    _mix_postmix_ref = _make_filter(mix_func, udata)
    _Mix_SetPostMix(_mix_postmix_ref, None)


_Mix_HookMusic = _dll.private_function('Mix_HookMusic',
  arg_types=[
 _Mix_FilterFunc, c_void_p],
  return_type=None)
_hookmusic_ref = None

def Mix_HookMusic(mix_func, udata):
    """Add your own music player or additional mixer function.

    If `mix_func` is None, the default music player is re-enabled.

    :Parameters
        `mix_func` : function
            The function must have the signature
            (stream: `SDL_array`, udata: any) -> None.  The first argument
            is the array of audio data that may be modified in place.
            `udata` is the value passed in this function.
        `udata` : any
            A variable that is passed to the `mix_func` function each
            call.

    """
    global _hookmusic_ref
    _hookmusic_ref = _make_filter(mix_func, udata)
    _Mix_HookMusic(_hookmusic_ref, None)


_Mix_HookMusicFinishedFunc = CFUNCTYPE(None)
_Mix_HookMusicFinished = _dll.private_function('Mix_HookMusicFinished',
  arg_types=[
 _Mix_HookMusicFinishedFunc],
  return_type=None)

def Mix_HookMusicFinished(music_finished):
    """Add your own callback when the music has finished playing.

    This callback is only called if the music finishes naturally.

    :Parameters:
        `music_finished` : function
            The callback takes no arguments and returns no value.

    """
    if music_finished:
        _Mix_HookMusicFinished(_Mix_HookMusicFinishedFunc(music_finished))
    else:
        _Mix_HookMusicFinished(_Mix_HookMusicFinishedFunc())


_Mix_ChannelFinishedFunc = CFUNCTYPE(None, c_int)
_Mix_ChannelFinished = _dll.private_function('Mix_ChannelFinished',
  arg_types=[
 _Mix_ChannelFinishedFunc],
  return_type=None)
_channelfinished_ref = None

def Mix_ChannelFinished(channel_finished):
    """Add your own callback when a channel has finished playing.

    The callback may be called from the mixer's audio callback or it
    could be called as a result of `Mix_HaltChannel`, etc.

    Do not call `SDL_LockAudio` from this callback; you will either be
    inside the audio callback, or SDL_mixer will explicitly lock the
    audio before calling your callback.

    :Parameters:
        `channel_finished` : function
            The function takes the channel number as its only argument,
            and returns None.  Pass None here to disable the callback.

    """
    global _channelfinished_ref
    if channel_finished:
        _channelfinished_ref = _Mix_ChannelFinishedFunc(channel_finished)
    else:
        _channelfinished_ref = _Mix_ChannelFinishedFunc()
    _Mix_ChannelFinished(_channelfinished_ref)


_Mix_EffectFunc = CFUNCTYPE(None, c_int, POINTER(c_ubyte), c_int, c_void_p)

def _make_Mix_EffectFunc(func, udata):
    if func:

        def f(chan, stream, len, ignored):
            stream = array.SDL_array(stream, len, c_ubyte)
            func(chan, stream, udata)

        return _Mix_EffectFunc(f)
    return _Mix_EffectFunc()


_Mix_EffectDoneFunc = CFUNCTYPE(None, c_int, c_void_p)

def _make_Mix_EffectDoneFunc(func, udata):
    if func:

        def f(chan, ignored):
            func(chan, udata)

        return _MixEffectDoneFunc(f)
    return _MixEffectDoneFunc()


_Mix_RegisterEffect = _dll.private_function('Mix_RegisterEffect',
  arg_types=[
 c_int, _Mix_EffectFunc, _Mix_EffectDoneFunc, c_void_p],
  return_type=c_int,
  error_return=0)
_effect_func_refs = []

def Mix_RegisterEffect(chan, f, d, arg):
    """Register a special effect function.

    At mixing time, the channel data is copied into a buffer and passed
    through each registered effect function.  After it passes through all
    the functions, it is mixed into the final output stream. The copy to
    buffer is performed once, then each effect function performs on the
    output of the previous effect. Understand that this extra copy to a
    buffer is not performed if there are no effects registered for a given
    chunk, which saves CPU cycles, and any given effect will be extra
    cycles, too, so it is crucial that your code run fast. Also note that
    the data that your function is given is in the format of the sound
    device, and not the format you gave to `Mix_OpenAudio`, although they
    may in reality be the same. This is an unfortunate but necessary speed
    concern. Use `Mix_QuerySpec` to determine if you can handle the data
    before you register your effect, and take appropriate actions.

    You may also specify a callback (`d`) that is called when the channel
    finishes playing. This gives you a more fine-grained control than
    `Mix_ChannelFinished`, in case you need to free effect-specific
    resources, etc. If you don't need this, you can specify None.

    You may set the callbacks before or after calling `Mix_PlayChannel`.

    Things like `Mix_SetPanning` are just internal special effect
    functions, so if you are using that, you've already incurred the
    overhead of a copy to a separate buffer, and that these effects will be
    in the queue with any functions you've registered. The list of
    registered effects for a channel is reset when a chunk finishes
    playing, so you need to explicitly set them with each call to
    ``Mix_PlayChannel*``.

    You may also register a special effect function that is to be run after
    final mixing occurs. The rules for these callbacks are identical to
    those in `Mix_RegisterEffect`, but they are run after all the channels
    and the music have been mixed into a single stream, whereas
    channel-specific effects run on a given channel before any other mixing
    occurs. These global effect callbacks are call "posteffects".
    Posteffects only have their `d` function called when they are
    unregistered (since the main output stream is never "done" in the same
    sense as a channel).  You must unregister them manually when you've had
    enough. Your callback will be told that the channel being mixed is
    (`MIX_CHANNEL_POST`) if the processing is considered a posteffect.

    After all these effects have finished processing, the callback
    registered through `Mix_SetPostMix` runs, and then the stream goes to
    the audio device.

    Do not call `SDL_LockAudio` from your callback function.

    :Parameters:
        `chan` : int
            Channel to set effect on, or `MIX_CHANNEL_POST` for postmix.
        `f` : function
            Callback function for effect.  Must have the signature
            (channel: int, stream: `SDL_array`, udata: any) -> None;
            where channel is the channel being affected, stream contains
            the audio data and udata is the user variable passed in to
            this function.
        `d` : function
            Callback function for when the effect is done.  The function
            must have the signature (channel: int, udata: any) -> None.
        `arg` : any
            User data passed to both callbacks.

    """
    f = _make_MixEffectFunc(f, arg)
    d = _make_MixEffectDoneFunc(d, arg)
    _effect_func_refs.append(f)
    _effect_func_refs.append(d)
    _Mix_RegisterEffect(chan, f, d, arg)


Mix_UnregisterAllEffects = _dll.function('Mix_UnregisterAllEffects',
  "Unregister all effects for a channel.\n\n    You may not need to call this explicitly, unless you need to stop all\n    effects from processing in the middle of a chunk's playback. Note that\n    this will also shut off some internal effect processing, since\n    `Mix_SetPanning` and others may use this API under the hood. This is\n    called internally when a channel completes playback.\n\n    Posteffects are never implicitly unregistered as they are for channels,\n    but they may be explicitly unregistered through this function by\n    specifying `MIX_CHANNEL_POST` for a channel.\n\n    :Parameters:\n     - `channel`: int\n\n    ",
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=c_int,
  error_return=0)
Mix_SetPanning = _dll.function('Mix_SetPanning',
  "Set the panning of a channel.\n\n    The left and right channels are specified as integers between 0 and\n    255, quietest to loudest, respectively.\n\n    Technically, this is just individual volume control for a sample with\n    two (stereo) channels, so it can be used for more than just panning.\n    If you want real panning, call it like this::\n\n        Mix_SetPanning(channel, left, 255 - left)\n\n    Setting (channel) to `MIX_CHANNEL_POST` registers this as a posteffect, and\n    the panning will be done to the final mixed stream before passing it on\n    to the audio device.\n\n    This uses the `Mix_RegisterEffect` API internally, and returns without\n    registering the effect function if the audio device is not configured\n    for stereo output. Setting both (left) and (right) to 255 causes this\n    effect to be unregistered, since that is the data's normal state.\n\n    :Parameters:\n     - `channel`: int\n     - `left`: int\n     - `right`: int\n\n    ",
  args=[
 'channel', 'left', 'right'],
  arg_types=[
 c_int, c_ubyte, c_ubyte],
  return_type=c_int,
  error_return=0)
Mix_SetPosition = _dll.function('Mix_SetPosition',
  'Set the position of a channel.\n\n    `angle` is an integer from 0 to 360, that specifies the location of the\n    sound in relation to the listener. `angle` will be reduced as neccesary\n    (540 becomes 180 degrees, -100 becomes 260).  Angle 0 is due north, and\n    rotates clockwise as the value increases.  For efficiency, the\n    precision of this effect may be limited (angles 1 through 7 might all\n    produce the same effect, 8 through 15 are equal, etc).  `distance` is\n    an integer between 0 and 255 that specifies the space between the sound\n    and the listener. The larger the number, the further away the sound is.\n    Using 255 does not guarantee that the channel will be culled from the\n    mixing process or be completely silent. For efficiency, the precision\n    of this effect may be limited (distance 0 through 5 might all produce\n    the same effect, 6 through 10 are equal, etc). Setting `angle` and\n    `distance` to 0 unregisters this effect, since the data would be\n    unchanged.\n\n    If you need more precise positional audio, consider using OpenAL for\n    spatialized effects instead of SDL_mixer. This is only meant to be a\n    basic effect for simple "3D" games.\n\n    If the audio device is configured for mono output, then you won\'t get\n    any effectiveness from the angle; however, distance attenuation on the\n    channel will still occur. While this effect will function with stereo\n    voices, it makes more sense to use voices with only one channel of\n    sound, so when they are mixed through this effect, the positioning will\n    sound correct. You can convert them to mono through SDL before giving\n    them to the mixer in the first place if you like.\n\n    Setting `channel` to `MIX_CHANNEL_POST` registers this as a posteffect,\n    and the positioning will be done to the final mixed stream before\n    passing it on to the audio device.\n\n    This is a convenience wrapper over `Mix_SetDistance` and\n    `Mix_SetPanning`.\n\n    :Parameters:\n     - `channel`: int\n     - `angle`: int\n     - `distance`: int\n\n    ',
  args=[
 'channel', 'angle', 'distance'],
  arg_types=[
 c_int, c_short, c_ubyte],
  return_type=c_int,
  error_return=0)
Mix_SetDistance = _dll.function('Mix_SetDistance',
  'Set the "distance" of a channel.\n\n    `distance` is an integer from 0 to 255 that specifies the location of\n    the sound in relation to the listener.  Distance 0 is overlapping the\n    listener, and 255 is as far away as possible A distance of 255 does not\n    guarantee silence; in such a case, you might want to try changing the\n    chunk\'s volume, or just cull the sample from the mixing process with\n    `Mix_HaltChannel`.\n\n    For efficiency, the precision of this effect may be limited (distances\n    1 through 7 might all produce the same effect, 8 through 15 are equal,\n    etc).  `distance` is an integer between 0 and 255 that specifies the\n    space between the sound and the listener. The larger the number, the\n    further away the sound is.\n\n    Setting `distance` to 0 unregisters this effect, since the data would\n    be unchanged.\n\n    If you need more precise positional audio, consider using OpenAL for\n    spatialized effects instead of SDL_mixer. This is only meant to be a\n    basic effect for simple "3D" games.\n\n    Setting `channel` to `MIX_CHANNEL_POST` registers this as a posteffect,\n    and the distance attenuation will be done to the final mixed stream\n    before passing it on to the audio device.\n\n    This uses the `Mix_RegisterEffect` API internally.\n\n    :Parameters:\n     - `channel`: int\n     - `distance`: distance\n\n    ',
  args=[
 'channel', 'distance'],
  arg_types=[
 c_int, c_ubyte],
  return_type=c_int,
  error_return=0)
Mix_SetReverseStereo = _dll.function('Mix_SetReverseStereo',
  "Causes a channel to reverse its stereo.\n\n    This is handy if the user has his or her speakers hooked up backwards,\n    or you would like to have a minor bit of psychedelia in your sound\n    code.  Calling this function with `flip` set to non-zero reverses the\n    chunks's usual channels. If `flip` is zero, the effect is unregistered.\n\n    This uses the `Mix_RegisterEffect` API internally, and thus is probably\n    more CPU intensive than having the user just plug in his speakers\n    correctly.  `Mix_SetReverseStereo` returns without registering the\n    effect function if the audio device is not configured for stereo\n    output.\n\n    If you specify `MIX_CHANNEL_POST` for `channel`, then this the effect\n    is used on the final mixed stream before sending it on to the audio\n    device (a posteffect).\n\n    :Parameters:\n     - `channel`: int\n     - `flip`: int\n\n    ",
  args=[
 'channel', 'flip'],
  arg_types=[
 c_int, c_int],
  return_type=c_int,
  error_return=0)
Mix_ReserveChannels = _dll.function('Mix_ReserveChannels',
  'Reserve the first channels (0 to n-1) for the application.\n\n    If reserved, a channel will not be allocated dynamically to a sample\n    if requested with one of the ``Mix_Play*`` functions.\n\n    :Parameters:\n     - `num`: int\n\n    :rtype: int\n    :return: the number of reserved channels\n    ',
  args=[
 'num'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_GroupChannel = _dll.function('Mix_GroupChannel',
  'Assing a channel to a group.\n\n    A tag can be assigned to several mixer channels, to form groups\n    of channels.  If `tag` is -1, the tag is removed (actually -1 is the\n    tag used to represent the group of all the channels).\n\n    :Parameters:\n     - `channel`: int\n     - `tag`: int\n\n    ',
  args=[
 'channel', 'tag'],
  arg_types=[
 c_int, c_int],
  return_type=c_int,
  error_return=0)
Mix_GroupChannels = _dll.function('Mix_GroupChannels',
  'Assign several consecutive channels to a group.\n\n    A tag can be assigned to several mixer channels, to form groups\n    of channels.  If `tag` is -1, the tag is removed (actually -1 is the\n    tag used to represent the group of all the channels).\n\n    :Parameters:\n     - `channel_from`: int\n     - `channel_to`: int\n     - `tag`: int\n\n    ',
  args=[
 'channel_from', 'channel_to', 'tag'],
  arg_types=[
 c_int, c_int, c_int],
  return_type=c_int,
  error_return=0)
Mix_GroupAvailable = _dll.function('Mix_GroupAvailable',
  'Find the first available channel in a group of channels.\n\n    :Parameters:\n     - `tag`: int\n\n    :rtype: int\n    :return: a channel, or -1 if none are available.\n    ',
  args=[
 'tag'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_GroupCount = _dll.function('Mix_GroupCount',
  'Get the number of channels in a group.\n\n    If `tag` is -1, returns the total number of channels.\n\n    :Parameters:\n     - `tag`: int\n\n    :rtype: int\n    ',
  args=[
 'tag'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_GroupOldest = _dll.function('Mix_GroupOldest',
  'Find the "oldest" sample playing in a group of channels.\n\n    :Parameters:\n     - `tag`: int\n\n    :rtype: int\n    ',
  args=[
 'tag'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_GroupNewer = _dll.function('Mix_GroupNewer',
  'Find the "most recent" (i.e., last) sample playing in a group of\n    channels.\n\n    :Parameters:\n     - `tag`: int\n\n    :rtype: int\n    ',
  args=[
 'tag'],
  arg_types=[
 c_int],
  return_type=c_int)

def Mix_PlayChannel(channel, chunk, loops):
    """Play an audio chunk on a specific channel.

    :Parameters:
        `channel` : int
            If -1, play on the first free channel.
        `chunk` : `Mix_Chunk`
            Chunk to play
        `loops` : int
            If greater than zero, the number of times to play the sound;
            if -1, loop infinitely.

    :rtype: int
    :return: the channel that was used to play the sound.
    """
    return Mix_PlayChannelTimed(channel, chunk, loops, -1)


Mix_PlayChannelTimed = _dll.function('Mix_PlayChannelTimed',
  'Play an audio chunk on a specific channel for a specified amount of\n    time.\n\n    :Parameters:\n        `channel` : int\n            If -1, play on the first free channel.\n        `chunk` : `Mix_Chunk`\n            Chunk to play\n        `loops` : int\n            If greater than zero, the number of times to play the sound;\n            if -1, loop infinitely.\n        `ticks` : int\n            Maximum number of milliseconds to play sound for.\n\n    :rtype: int\n    :return: the channel that was used to play the sound.\n    ',
  args=[
 'channel', 'chunk', 'loops', 'ticks'],
  arg_types=[
 c_int, POINTER(Mix_Chunk), c_int, c_int],
  return_type=c_int)
Mix_PlayMusic = _dll.function('Mix_PlayMusic',
  'Play a music chunk.\n\n    :Parameters:\n        `music` : ``Mix_Music``\n            Chunk to play\n        `loops` : int\n            If greater than zero, the number of times to play the sound;\n            if -1, loop infinitely.\n    ',
  args=[
 'music', 'loops'],
  arg_types=[
 _Mix_Music, c_int],
  return_type=c_int,
  error_return=(-1))
Mix_FadeInMusic = _dll.function('Mix_FadeInMusic',
  'Fade in music over a period of time.\n\n    :Parameters:\n        `music` : ``Mix_Music``\n            Chunk to play\n        `loops` : int\n            If greater than zero, the number of times to play the sound;\n            if -1, loop infinitely.\n        `ms` : int\n            Number of milliseconds to fade up over.\n    ',
  args=[
 'music', 'loops', 'ms'],
  arg_types=[
 _Mix_Music, c_int, c_int],
  return_type=c_int,
  error_return=(-1))
Mix_FadeInMusicPos = _dll.function('Mix_FadeInMusicPos',
  'Fade in music at an offset over a period of time.\n\n    :Parameters:\n        `music` : ``Mix_Music``\n            Chunk to play\n        `loops` : int\n            If greater than zero, the number of times to play the sound;\n            if -1, loop infinitely.\n        `ms` : int\n            Number of milliseconds to fade up over.\n        `position` : float\n            Position within music to start at.  Currently implemented\n            only for MOD, OGG and MP3.\n\n    :see: Mix_SetMusicPosition\n    ',
  args=[
 'music', 'loops', 'ms', 'position'],
  arg_types=[
 _Mix_Music, c_int, c_int, c_double],
  return_type=c_int,
  error_return=(-1))

def Mix_FadeInChannel(channel, chunk, loops, ms):
    """Fade in a channel.

    :Parameters:
        `channel` : int
            If -1, play on the first free channel.
        `chunk` : `Mix_Chunk`
            Chunk to play
        `loops` : int
            If greater than zero, the number of times to play the sound;
            if -1, loop infinitely.
        `ms` : int
            Number of milliseconds to fade up over.
    """
    Mix_FadeInChannelTimed(channel, chunk, loops, -1)


Mix_FadeInChannelTimed = _dll.function('Mix_FadeInChannelTimed',
  'Fade in a channel and play for a specified amount of time.\n\n    :Parameters:\n        `channel` : int\n            If -1, play on the first free channel.\n        `chunk` : `Mix_Chunk`\n            Chunk to play\n        `loops` : int\n            If greater than zero, the number of times to play the sound;\n            if -1, loop infinitely.\n        `ms` : int\n            Number of milliseconds to fade up over.\n        `ticks` : int\n            Maximum number of milliseconds to play sound for.\n    ',
  args=[
 'channel', 'music', 'loops', 'ms', 'ticks'],
  arg_types=[
 c_int, _Mix_Music, c_int, c_int, c_int],
  return_type=c_int,
  error_return=(-1))
Mix_Volume = _dll.function('Mix_Volume',
  'Set the volume in the range of 0-128 of a specific channel.\n\n    :Parameters:\n        `channel` : int\n            If -1, set the volume for all channels\n        `volume` : int\n            Volume to set, in the range 0-128, or -1 to just return the\n            current volume.\n\n    :rtype: int\n    :return: the original volume.\n    ',
  args=[
 'channel', 'volume'],
  arg_types=[
 c_int, c_int],
  return_type=c_int)
Mix_VolumeChunk = _dll.function('Mix_VolumeChunk',
  'Set the volume in the range of 0-128 of a chunk.\n\n    :Parameters:\n        `chunk` : `Mix_Chunk`\n            Chunk to set volume.\n        `volume` : int\n            Volume to set, in the range 0-128, or -1 to just return the\n            current volume.\n\n    :rtype: int\n    :return: the original volume.\n    ',
  args=[
 'chunk', 'volume'],
  arg_types=[
 POINTER(Mix_Chunk), c_int],
  return_type=c_int)
Mix_VolumeMusic = _dll.function('Mix_VolumeMusic',
  'Set the volume in the range of 0-128 of the music.\n\n    :Parameters:\n        `volume` : int\n            Volume to set, in the range 0-128, or -1 to just return the\n            current volume.\n\n    :rtype: int\n    :return: the original volume.\n    ',
  args=[
 'volume'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_HaltChannel = _dll.function('Mix_HaltChannel',
  'Halt playing of a particular channel.\n\n    :Parameters:\n     - `channel`: int\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=None)
Mix_HaltGroup = _dll.function('Mix_HaltGroup',
  'Halt playing of a particular group.\n\n    :Parameters:\n     - `tag`: int\n    ',
  args=[
 'tag'],
  arg_types=[
 c_int],
  return_type=None)
Mix_HaltMusic = _dll.function('Mix_HaltMusic',
  'Halt playing music.\n    ',
  args=[], arg_types=[], return_type=None)
Mix_ExpireChannel = _dll.function('Mix_ExpireChannel',
  'Change the expiration delay for a particular channel.\n\n    The sample will stop playing afte the `ticks` milliseconds have\n    elapsed, or remove the expiration if `ticks` is -1.\n\n    :Parameters:\n     - `channel`: int\n     - `ticks`: int\n\n    :rtype: int\n    :return: the number of channels affected.\n    ',
  args=[
 'channel', 'ticks'],
  arg_types=[
 c_int, c_int],
  return_type=c_int)
Mix_FadeOutChannel = _dll.function('Mix_FadeOutChannel',
  "Halt a channel, fading it out progressively until it's silent.\n\n    The `ms` parameter indicates the number of milliseconds the fading\n    will take.\n\n    :Parameters:\n     - `channel`: int\n     - `ms`: int\n    ",
  args=[
 'channel', 'ms'],
  arg_types=[
 c_int, c_int],
  return_type=None)
Mix_FadeOutGroup = _dll.function('Mix_FadeOutGroup',
  "Halt a group, fading it out progressively until it's silent.\n\n    The `ms` parameter indicates the number of milliseconds the fading\n    will take.\n\n    :Parameters:\n     - `tag`: int\n     - `ms`: int\n    ",
  args=[
 'tag', 'ms'],
  arg_types=[
 c_int, c_int],
  return_type=None)
Mix_FadeOutMusic = _dll.function('Mix_FadeOutMusic',
  "Halt playing music, fading it out progressively until it's silent.\n\n    The `ms` parameter indicates the number of milliseconds the fading\n    will take.\n\n    :Parameters:\n     - `ms`: int\n    ",
  args=[
 'ms'],
  arg_types=[
 c_int],
  return_type=None)
Mix_FadingMusic = _dll.function('Mix_FadingMusic',
  'Query the fading status of the music.\n\n    :rtype: int\n    :return: one of MIX_NO_FADING, MIX_FADING_OUT, MIX_FADING_IN.\n    ',
  args=[], arg_types=[], return_type=c_int)
Mix_FadingChannel = _dll.function('Mix_FadingChannel',
  'Query the fading status of a channel.\n\n    :Parameters:\n     - `channel`: int\n\n    :rtype: int\n    :return: one of MIX_NO_FADING, MIX_FADING_OUT, MIX_FADING_IN.\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_Pause = _dll.function('Mix_Pause',
  'Pause a particular channel.\n\n    :Parameters:\n     - `channel`: int\n\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=None)
Mix_Resume = _dll.function('Mix_Resume',
  'Resume a particular channel.\n\n    :Parameters:\n     - `channel`: int\n\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=None)
Mix_Paused = _dll.function('Mix_Paused',
  'Query if a channel is paused.\n\n    :Parameters:\n     - `channel`: int\n\n    :rtype: int\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_PauseMusic = _dll.function('Mix_PauseMusic',
  'Pause the music stream.\n    ',
  args=[], arg_types=[], return_type=None)
Mix_ResumeMusic = _dll.function('Mix_ResumeMusic',
  'Resume the music stream.\n    ',
  args=[], arg_types=[], return_type=None)
Mix_RewindMusic = _dll.function('Mix_RewindMusic',
  'Rewind the music stream.\n    ',
  args=[], arg_types=[], return_type=None)
Mix_PausedMusic = _dll.function('Mix_PausedMusic',
  'Query if the music stream is paused.\n\n    :rtype: int\n    ',
  args=[], arg_types=[], return_type=c_int)
Mix_SetMusicPosition = _dll.function('Mix_SetMusicPosition',
  'Set the current position in the music stream.\n\n    For MOD files the position represents the pattern order number;\n    for OGG and MP3 files the position is in seconds.  Currently no other\n    music file formats support positioning.\n\n    :Parameters:\n     - `position`: float\n\n    ',
  args=[
 'position'],
  arg_types=[
 c_double],
  return_type=c_int,
  error_return=(-1))
Mix_Playing = _dll.function('Mix_Playing',
  'Query the status of a specific channel.\n\n    :Parameters:\n     - `channel`: int\n\n    :rtype: int\n    :return: the number of queried channels that are playing.\n    ',
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=c_int)
Mix_PlayingMusic = _dll.function('Mix_PlayingMusic',
  'Query the status of the music stream.\n\n    :rtype: int\n    :return: 1 if music is playing, 0 otherwise.\n    ',
  args=[], arg_types=[], return_type=c_int)
Mix_SetMusicCMD = _dll.function('Mix_SetMusicCMD',
  'Set the external music playback command.\n\n    Any currently playing music will stop.\n\n    :Parameters:\n     - `command`: string\n\n    ',
  args=[
 'command'],
  arg_types=[
 c_char_p],
  return_type=c_int,
  error_return=(-1))
Mix_SetSynchroValue = _dll.function('Mix_SetSynchroValue',
  'Set the synchro value for a MOD music stream.\n\n    :Parameters:\n     - `value`: int\n\n    ',
  args=[
 'value'],
  arg_types=[
 c_int],
  return_type=c_int,
  error_return=(-1))
Mix_GetSynchroValue = _dll.function('Mix_GetSynchroValue',
  'Get the synchro value for a MOD music stream.\n\n    :rtype: int\n    ',
  args=[], arg_types=[], return_type=c_int)
Mix_GetChunk = _dll.function('Mix_GetChunk',
  "Get the chunk currently associated with a mixer channel.\n\n    Returns None if the channel is invalid or if there's no chunk associated.\n\n    :Parameters:\n     - `channel`: int\n\n    :rtype: `Mix_Chunk`\n    ",
  args=[
 'channel'],
  arg_types=[
 c_int],
  return_type=(POINTER(Mix_Chunk)),
  dereference_return=True)
Mix_CloseAudio = _dll.function('Mix_CloseAudio',
  'Close the mixer, halting all playing audio.\n\n    ',
  args=[], arg_types=[], return_type=None)