# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_threads/ffprobe_parser.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 15160 bytes
import subprocess, platform, re

class FFProbe(object):
    __doc__ = '\n    FFProbe wraps the ffprobe command and pulls the data into\n    an object form:\n\n    `data = FFProbe(FFPROBE_URL, filename_url, parse=True,\n                    pretty=True, select=None, entries=None,\n                    show_format=True, show_streams=True, writer=None)`\n\n   The `parse` argument defines the parser\'s behavior; `parse=True` get\n   an automatically parsed output with four list-type sections while the\n   `select`, `entries`,` writer` arguments will be ignored; `parse=False`\n   you get a customized output characterized by the arguments you define.\n\n    ---------------------\n    USE with `parse=True`:\n    ---------------------\n\n        After referencing the above class, use a convenient way to handle\n        possible exceptions, example:\n\n            if data.ERROR():\n                print ("Some Error:  %s" % (data.error))\n                return\n            else:\n                print (data.video_stream())\n                print (data.audio_stream())\n                print (data.subtitle_stream())\n                print (data.data_format())\n\n            format_dict = dict()\n            for line in data.data_format():\n                for items in line:\n                    if \'=\' in items:\n                        k, v = items.split(\'=\')\n                        k, v = k.strip(), v.strip()\n                        data_format[k] = v\n            print (data_format)\n\n    ----------------------\n    USE with `parse=False`:\n    ----------------------\n\n        Get simple output data:\n        -----------------------\n\n            `data = FFProbe(FFPROBE_URL,\n                            filename_url,\n                            parse=False,\n                            writer=\'xml\')\n                            )`\n\n            After referencing the above class, use a convenient way to handle\n            possible exceptions, example:\n\n                if data.ERROR():\n                    print ("Some Error:  %s" % (data.error))\n                    return\n\n            then, get your custom output:\n\n                print(data.custom_output())\n\n        To get a kind of output:\n        ------------------------\n\n             A example entry of a first audio streams section\n\n            `data = FFProbe(FFPROBE_URL,\n                            filename_url,\n                            parse=False,\n                            pretty=True,\n                            select=\'a:0\',\n                            entries=\'stream=code_type\',\n                            show_format=False,\n                            show_streams=False,\n                            writer=\'compact=nk=1:p=0\'\n                            )`\n\n            After referencing the above class, use a convenient way to handle\n            possible exceptions, example:\n\n                if data.ERROR():\n                    print ("Some Error:  %s" % (data.error))\n                    return\n\n            then, get your custom output:\n\n                print(data.custom_output().strip())\n\n            The `entries` arg is the key to search some entry on sections\n\n                entries=\'stream=codec_type,codec_name,bits_per_sample\'\n                entries=\'format=duration\'\n\n            The `select` arg is the key to select a specified section\n\n                select=\'\' # select all sections\n                select=\'v\' # select all video sections\n                select=\'v:0\' # select first video section\n\n            The `writer` arg alias:\n\n                writer=\'default=nw=1:nk=1\'\n                writer=\'default=noprint_wrappers=1:nokey=1\'\n\n                available writers name are:\n\n                `default`, `compact`, `csv`, `flat`, `ini`, `json` and `xml`\n\n                Options are list of key=value pairs, separated by ":"\n\n                See `man ffprobe`\n\n    ------------------------------------------------\n    [i] This class was partially inspired to:\n    ------------------------------------------------\n        <https://github.com/simonh10/ffprobe/blob/master/ffprobe/ffprobe.py>\n\n    '

    def __init__(self, FFPROBE_URL, filename, parse=True, pretty=True, select=None, entries=None, show_format=True, show_streams=True, writer=None):
        """
        -------------------
        Parameters meaning:
        -------------------
            FFPROBE_URL     command name by $PATH defined or a binary url
            filename_url    a pathname appropriately quoted
            parse           defines the output mode
            show_format     show format informations
            show_streams    show all streams information
            select          select which section to show (''= all sections)
            entries         get one or more entries
            pretty          get human values or machine values
            writer          define a format of printing output

        --------------------------------------------------
        [?] to know the meaning of the above options, see:
        --------------------------------------------------
            <http://trac.ffmpeg.org/wiki/FFprobeTips>
            <https://slhck.info/ffmpeg-encoding-course/#/46>

        -------------------------------------------------------------------
        The ffprobe command has stdout and stderr (unlike ffmpeg and ffplay)
        which allows me to initialize separate attributes also for errors
        """
        self.error = False
        self.mediastreams = []
        self.mediaformat = []
        self.video = []
        self.audio = []
        self._format = []
        self.subtitle = []
        self.writer = None
        self.datalines = []
        pretty = '-pretty' if pretty is True else 'no_pretty'
        show_format = '-show_format' if show_format is True else ''
        show_streams = '-show_streams' if show_streams is True else ''
        select = '-select_streams %s' % select if select else ''
        entries = '-show_entries %s' % entries if entries else ''
        writer = '-of %s' % writer if writer else '-of default'
        if parse:
            cmnd = '%s -i "%s" -v error %s %s %s -print_format default' % (
             FFPROBE_URL,
             filename,
             pretty,
             show_format,
             show_streams)
        else:
            cmnd = '%s -i "%s" -v error %s %s %s %s %s %s' % (FFPROBE_URL,
             filename,
             pretty,
             select,
             entries,
             show_format,
             show_streams,
             writer)
        if not platform.system() == 'Windows':
            import shlex
            cmnd = shlex.split(cmnd)
            info = None
        else:
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            p = subprocess.Popen(cmnd, stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE),
              universal_newlines=True,
              startupinfo=info)
            output, error = p.communicate()
        except (OSError, FileNotFoundError) as e:
            try:
                self.error = e
                return
            finally:
                e = None
                del e

        if p.returncode:
            self.error = error
        elif parse:
            self.parser(output)
        else:
            self.writer = output

    def parser(self, output):
        r"""
        Indexes the catalogs [STREAM\] and [FORMAT\] given by
        the default output of FFprobe
        """
        probing = output.split('\n')
        for s in probing:
            if re.match('\\[STREAM\\]', s):
                self.datalines = []
            elif re.match('\\[\\/STREAM\\]', s):
                self.mediastreams.append(self.datalines)
                self.datalines = []
            else:
                self.datalines.append(s)

        for f in probing:
            if re.match('\\[FORMAT\\]', f):
                self.datalines = []
            elif re.match('\\[\\/FORMAT\\]', f):
                self.mediaformat.append(self.datalines)
                self.datalines = []
            else:
                self.datalines.append(f)

    def video_stream(self):
        """
        Return a metadata list for video stream. If there is not
        data video return a empty list
        """
        for datastream in self.mediastreams:
            if 'codec_type=video' in datastream:
                self.video.append(datastream)

        return self.video

    def audio_stream(self):
        """
        Return a metadata list for audio stream. If there is not
        data audio return a empty list
        """
        for datastream in self.mediastreams:
            if 'codec_type=audio' in datastream:
                self.audio.append(datastream)

        return self.audio

    def subtitle_stream(self):
        """
        Return a metadata list for subtitle stream. If there is not
        data subtitle return a empty list
        """
        for datastream in self.mediastreams:
            if 'codec_type=subtitle' in datastream:
                self.subtitle.append(datastream)

        return self.subtitle

    def data_format(self):
        """
        Return a metadata list for data format. If there is not
        data format return a empty list
        """
        for dataformat in self.mediaformat:
            self._format.append(dataformat)

        return self._format

    def get_audio_codec_name(self):
        """
        Return title and list of possible audio codec name and
        tag language into a video with one or more audio streams.
        If not audio stream in video return None.
        This method is useful for exemple to saving audio content as
        audio track.
        """
        astream = self.audio_stream()
        audio_lang = []
        acod = ''
        lang = 'unknown'
        indx = ''
        srate = ''
        bits = ''
        chan = ''
        bitr = ''
        if astream == []:
            print('No AUDIO stream metadata found')
            return (None, None)
        n = len(astream)
        for a in range(n):
            key, value = astream[a][0].strip().split('=')
            for b in astream[a]:
                key, value = b.strip().split('=')
                if 'codec_name' in key:
                    acod = value
                if 'stream_tags' in key:
                    lang = value
                if 'TAG:language' in key:
                    lang = value
                if 'index' in key:
                    indx = value
                if key == 'sample_rate':
                    srate = value
                if key == 'bits_per_sample':
                    bits = value
                if key == 'channel_layout':
                    chan = value
                if key == 'bit_rate':
                    bitr = value

            audio_lang.append('index: %s | codec: %s | language: %s | sampe rate: %s | bit: %s | channels: %s | bit rate: %s' % (
             indx, acod, lang,
             srate, bits, chan,
             bitr))

        video_list = self.data_format()
        for t in video_list[0]:
            if 'filename=' in t:
                vtitle = t.split('=')[1]
                break
            else:
                vtitle = 'Title unknown'

        return (
         audio_lang, vtitle)

    def custom_output(self):
        """
        Print output defined by writer argument. To use this feature
        you must specify parse=False, example:

        `data = FFProbe(filename_url,
                        FFPROBE_URL,
                        parse=False,
                        writer='json')`

        Then, to get output data call this method:

        output = data.custom_output()

        Valid writers are: `default`, `json`, `compact`, `csv`, `flat`,
        `ini` and `xml` .
        """
        return self.writer

    def ERROR(self):
        """
        check for errors on stderr of the ffprobe command. It also
        handles the IOError exception. You can use this interface
        before using all other methods of this class.
        """
        if self.error:
            return self.error