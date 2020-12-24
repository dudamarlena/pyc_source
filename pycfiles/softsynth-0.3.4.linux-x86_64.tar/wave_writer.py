# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/wave_writer.py
# Compiled at: 2015-07-03 20:06:48
import wave, struct, sys

class WaveWriter(object):

    def __init__(self, options):
        self.options = options
        self.filename = options.get_output_file()
        self.also_output_to_stdout = options.write_wave_to_stdout
        self.open()

    def open(self):
        sys.stderr.write('Opening %s for writing\n' % self.filename)
        w = wave.open(self.filename, 'w')
        w.setnchannels(1)
        w.setsampwidth(self.options.byte_rate)
        w.setframerate(self.options.sample_rate)
        self.wave = w
        self.data = []

    def write_samples(self, elems):
        if elems is None:
            return False
        else:
            fmt = str(len(elems)) + self.options.struct_pack_format
            sample = struct.pack(fmt, *map(int, elems))
            if self.also_output_to_stdout:
                sys.stdout.write(sample)
                sys.stdout.flush()
            self.wave.writeframes(sample)
            return True

    def close(self):
        self.wave.close()
        sys.stderr.write('Written %s.' % self.filename)

    def output(self, synth):
        t = 0
        try:
            try:
                w = True
                while w:
                    samples = synth.get_samples_in_byte_rate(self.options.buffer_size, t)
                    w = self.write_samples(samples)
                    t += self.options.buffer_size

            except KeyboardInterrupt:
                pass

        finally:
            sys.stderr.write('Written %d samples.\n' % t)
            self.close()