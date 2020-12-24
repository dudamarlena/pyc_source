# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kayleevc/recognizer.py
# Compiled at: 2016-04-30 21:58:23
# Size of source mod 2**32: 2000 bytes
import os.path, sys, gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)

class Recognizer(GObject.GObject):
    __gsignals__ = {'finished': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                  (
                   GObject.TYPE_STRING,))}

    def __init__(self, config):
        GObject.GObject.__init__(self)
        self.commands = {}
        src = config.options.microphone
        if src:
            audio_src = 'alsasrc device="hw:{0},0"'.format(src)
        else:
            audio_src = 'autoaudiosrc'
        cmd = audio_src + ' ! audioconvert' + ' ! audioresample' + ' ! pocketsphinx lm=' + config.lang_file + ' dict=' + config.dic_file + ' ! appsink sync=false'
        try:
            self.pipeline = Gst.parse_launch(cmd)
        except Exception as e:
            print(e.message)
            print('You may need to install gstreamer1.0-pocketsphinx')
            raise e

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.result)

    def listen(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def pause(self):
        self.pipeline.set_state(Gst.State.PAUSED)

    def result(self, bus, msg):
        msg_struct = msg.get_structure()
        msgtype = msg_struct.get_name()
        if msgtype != 'pocketsphinx':
            return
        command = msg_struct.get_string('hypothesis')
        if command != '' and msg_struct.get_boolean('final')[1]:
            self.emit('finished', command)