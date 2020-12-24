# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/media_types/video/transcoders.py
# Compiled at: 2016-03-29 15:18:39
# Size of source mod 2**32: 16040 bytes
from __future__ import division, print_function
import os, sys, logging, multiprocessing
from mediagoblin.media_types.tools import discover
from mediagoblin.tools.translate import lazy_pass_to_ugettext as _
old_argv = sys.argv
sys.argv = []
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
Gst.init(None)
from gi.repository import GstPbutils
sys.argv = old_argv
import struct
try:
    from PIL import Image
except ImportError:
    import Image

_log = logging.getLogger(__name__)
CPU_COUNT = 2
try:
    CPU_COUNT = multiprocessing.cpu_count()
except NotImplementedError:
    _log.warning('multiprocessing.cpu_count not implemented')

os.putenv('GST_DEBUG_DUMP_DOT_DIR', '/tmp')

def capture_thumb(video_path, dest_path, width=None, height=None, percent=0.5):

    def pad_added(element, pad, connect_to):
        """This is a callback to dynamically add element to pipeline"""
        caps = pad.query_caps(None)
        name = caps.to_string()
        _log.debug('on_pad_added: {0}'.format(name))
        if name.startswith('video'):
            if not connect_to.is_linked():
                pad.link(connect_to)

    pipeline = Gst.Pipeline()
    uridecodebin = Gst.ElementFactory.make('uridecodebin', None)
    uridecodebin.set_property('uri', 'file://{0}'.format(video_path))
    videoconvert = Gst.ElementFactory.make('videoconvert', None)
    uridecodebin.connect('pad-added', pad_added, videoconvert.get_static_pad('sink'))
    videoscale = Gst.ElementFactory.make('videoscale', None)
    caps_struct = Gst.Structure.new_empty('video/x-raw')
    caps_struct.set_value('pixel-aspect-ratio', Gst.Fraction(1, 1))
    caps_struct.set_value('format', 'RGB')
    if height:
        caps_struct.set_value('height', height)
    if width:
        caps_struct.set_value('width', width)
    caps = Gst.Caps.new_empty()
    caps.append_structure(caps_struct)
    appsink = Gst.ElementFactory.make('appsink', None)
    appsink.set_property('caps', caps)
    elements = [
     uridecodebin, videoconvert, videoscale, appsink]
    for e in elements:
        pipeline.add(e)

    videoconvert.link(videoscale)
    videoscale.link(appsink)
    pipeline.set_state(Gst.State.PAUSED)
    state = pipeline.get_state(Gst.SECOND * 3)
    if state[0] != Gst.StateChangeReturn.SUCCESS:
        _log.warning('state change failed, {0}'.format(state))
        return
    success, duration = pipeline.query_duration(Gst.Format.TIME)
    if not success:
        _log.warning('query_duration failed')
        return
    seek_to = int(duration * int(percent * 100) / 100)
    _log.debug('Seeking to {0} of {1}'.format(float(seek_to) / Gst.SECOND, float(duration) / Gst.SECOND))
    seek = pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, seek_to)
    if not seek:
        _log.warning('seek failed')
        return
    sample = appsink.emit('pull-preroll')
    if not sample:
        _log.warning('could not get sample')
        return
    caps = sample.get_caps()
    if not caps:
        _log.warning('could not get snapshot format')
        return
    structure = caps.get_structure(0)
    success, width = structure.get_int('width')
    success, height = structure.get_int('height')
    buffer = sample.get_buffer()
    im = Image.frombytes('RGB', (width, height), buffer.extract_dup(0, buffer.get_size()))
    im.save(dest_path)
    _log.info('thumbnail saved to {0}'.format(dest_path))
    pipeline.set_state(Gst.State.NULL)


class VideoTranscoder(object):
    __doc__ = '\n    Video transcoder\n\n    Transcodes the SRC video file to a VP8 WebM video file at DST\n\n     - Produces a WebM vp8 and vorbis video file.\n    '

    def __init__(self):
        _log.info('Initializing VideoTranscoder...')
        self.progress_percentage = None
        self.loop = GObject.MainLoop()

    def transcode(self, src, dst, **kwargs):
        """
        Transcode a video file into a 'medium'-sized version.
        """
        self.source_path = src
        self.destination_path = dst
        self.destination_dimensions = kwargs.get('dimensions', (640, 640))
        self.vp8_quality = kwargs.get('vp8_quality', 8)
        self.vp8_threads = kwargs.get('vp8_threads', CPU_COUNT - 1)
        if self.vp8_threads == 0:
            self.vp8_threads = CPU_COUNT
        self.vorbis_quality = kwargs.get('vorbis_quality', 0.3)
        self._progress_callback = kwargs.get('progress_callback') or None
        if not type(self.destination_dimensions) == tuple:
            raise Exception('dimensions must be tuple: (width, height)')
        self._setup_pipeline()
        self.data = discover(self.source_path)
        self._link_elements()
        self._VideoTranscoder__setup_videoscale_capsfilter()
        self.pipeline.set_state(Gst.State.PLAYING)
        _log.info('Transcoding...')
        _log.debug('Initializing MainLoop()')
        self.loop.run()

    def _setup_pipeline(self):
        _log.debug('Setting up transcoding pipeline')
        self.pipeline = Gst.Pipeline.new('VideoTranscoderPipeline')
        self.filesrc = Gst.ElementFactory.make('filesrc', 'filesrc')
        self.filesrc.set_property('location', self.source_path)
        self.pipeline.add(self.filesrc)
        self.decoder = Gst.ElementFactory.make('decodebin', 'decoder')
        self.decoder.connect('pad-added', self._on_dynamic_pad)
        self.pipeline.add(self.decoder)
        self.videoqueue = Gst.ElementFactory.make('queue', 'videoqueue')
        self.pipeline.add(self.videoqueue)
        self.videorate = Gst.ElementFactory.make('videorate', 'videorate')
        self.pipeline.add(self.videorate)
        self.videoconvert = Gst.ElementFactory.make('videoconvert', 'videoconvert')
        self.pipeline.add(self.videoconvert)
        self.videoscale = Gst.ElementFactory.make('videoscale', 'videoscale')
        self.pipeline.add(self.videoscale)
        self.capsfilter = Gst.ElementFactory.make('capsfilter', 'capsfilter')
        self.pipeline.add(self.capsfilter)
        self.vp8enc = Gst.ElementFactory.make('vp8enc', 'vp8enc')
        self.vp8enc.set_property('threads', self.vp8_threads)
        self.pipeline.add(self.vp8enc)
        self.audioqueue = Gst.ElementFactory.make('queue', 'audioqueue')
        self.pipeline.add(self.audioqueue)
        self.audiorate = Gst.ElementFactory.make('audiorate', 'audiorate')
        self.audiorate.set_property('tolerance', 80000000)
        self.pipeline.add(self.audiorate)
        self.audioconvert = Gst.ElementFactory.make('audioconvert', 'audioconvert')
        self.pipeline.add(self.audioconvert)
        self.audiocapsfilter = Gst.ElementFactory.make('capsfilter', 'audiocapsfilter')
        audiocaps = Gst.Caps.new_empty()
        audiocaps_struct = Gst.Structure.new_empty('audio/x-raw')
        audiocaps.append_structure(audiocaps_struct)
        self.audiocapsfilter.set_property('caps', audiocaps)
        self.pipeline.add(self.audiocapsfilter)
        self.vorbisenc = Gst.ElementFactory.make('vorbisenc', 'vorbisenc')
        self.vorbisenc.set_property('quality', self.vorbis_quality)
        self.pipeline.add(self.vorbisenc)
        self.webmmux = Gst.ElementFactory.make('webmmux', 'webmmux')
        self.pipeline.add(self.webmmux)
        self.filesink = Gst.ElementFactory.make('filesink', 'filesink')
        self.filesink.set_property('location', self.destination_path)
        self.pipeline.add(self.filesink)
        self.progressreport = Gst.ElementFactory.make('progressreport', 'progressreport')
        self.progressreport.set_property('update-freq', 1)
        self.progressreport.set_property('silent', True)
        self.pipeline.add(self.progressreport)

    def _link_elements(self):
        """
        Link all the elements

        This code depends on data from the discoverer and is called
        from __discovered
        """
        _log.debug('linking elements')
        self.filesrc.link(self.decoder)
        self.videoqueue.link(self.videorate)
        self.videorate.link(self.videoconvert)
        self.videoconvert.link(self.videoscale)
        self.videoscale.link(self.capsfilter)
        self.capsfilter.link(self.vp8enc)
        self.vp8enc.link(self.webmmux)
        if self.data.get_audio_streams():
            self.audioqueue.link(self.audiorate)
            self.audiorate.link(self.audioconvert)
            self.audioconvert.link(self.audiocapsfilter)
            self.audiocapsfilter.link(self.vorbisenc)
            self.vorbisenc.link(self.webmmux)
        self.webmmux.link(self.progressreport)
        self.progressreport.link(self.filesink)
        self._setup_bus()

    def _on_dynamic_pad(self, dbin, pad):
        """
        Callback called when ``decodebin`` has a pad that we can connect to
        """
        if self.videorate.get_static_pad('sink').get_pad_template().get_caps().intersect(pad.query_caps()).is_empty():
            _log.debug('linking audio to the pad dynamically')
            pad.link(self.audioqueue.get_static_pad('sink'))
        else:
            _log.debug('linking video to the pad dynamically')
            pad.link(self.videoqueue.get_static_pad('sink'))

    def _setup_bus(self):
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self._on_message)

    def __setup_videoscale_capsfilter(self):
        """
        Sets up the output format (width, height) for the video
        """
        caps_struct = Gst.Structure.new_empty('video/x-raw')
        caps_struct.set_value('pixel-aspect-ratio', Gst.Fraction(1, 1))
        caps_struct.set_value('framerate', Gst.Fraction(30, 1))
        video_info = self.data.get_video_streams()[0]
        if video_info.get_height() > video_info.get_width():
            caps_struct.set_value('height', self.destination_dimensions[1])
        else:
            caps_struct.set_value('width', self.destination_dimensions[0])
        caps = Gst.Caps.new_empty()
        caps.append_structure(caps_struct)
        self.capsfilter.set_property('caps', caps)

    def _on_message(self, bus, message):
        _log.debug((bus, message, message.type))
        if message.type == Gst.MessageType.EOS:
            self.dst_data = discover(self.destination_path)
            self._VideoTranscoder__stop()
            _log.info('Done')
        else:
            if message.type == Gst.MessageType.ELEMENT:
                if message.has_name('progress'):
                    structure = message.get_structure()
                    success, percent = structure.get_int('percent')
                    if self.progress_percentage != percent:
                        if success:
                            self.progress_percentage = percent
                            if self._progress_callback:
                                self._progress_callback(percent)
                            _log.info('{percent}% done...'.format(percent=percent))
            elif message.type == Gst.MessageType.ERROR:
                _log.error('Got error: {0}'.format(message.parse_error()))
                self.dst_data = None
                self._VideoTranscoder__stop()

    def __stop(self):
        _log.debug(self.loop)
        if hasattr(self, 'pipeline'):
            self.pipeline.set_state(Gst.State.NULL)
        GObject.idle_add(self._VideoTranscoder__stop_mainloop)

    def __stop_mainloop(self):
        """
        Wrapper for GObject.MainLoop.quit()

        This wrapper makes us able to see if self.loop.quit has been called
        """
        _log.info('Terminating MainLoop')
        self.loop.quit()


if __name__ == '__main__':
    os.nice(19)
    from optparse import OptionParser
    parser = OptionParser(usage='%prog [-v] -a [ video | thumbnail | discover ] SRC [ DEST ]')
    parser.add_option('-a', '--action', dest='action', help='One of "video", "discover" or "thumbnail"')
    parser.add_option('-v', dest='verbose', action='store_true', help='Output debug information')
    parser.add_option('-q', dest='quiet', action='store_true', help='Dear program, please be quiet unless *error*')
    parser.add_option('-w', '--width', type=int, default=180)
    options, args = parser.parse_args()
    if options.verbose:
        _log.setLevel(logging.DEBUG)
else:
    _log.setLevel(logging.INFO)
if options.quiet:
    _log.setLevel(logging.ERROR)
_log.debug(args)
if not len(args) == 2:
    if not options.action == 'discover':
        parser.print_help()
        sys.exit()
transcoder = VideoTranscoder()
if options.action == 'thumbnail':
    args.append(options.width)
    VideoThumbnailerMarkII(*args)
else:
    if options.action == 'video':

        def cb(data):
            print("I'm a callback!")


        transcoder.transcode(*args, progress_callback=cb)
    elif options.action == 'discover':
        print(transcoder.discover(*args))