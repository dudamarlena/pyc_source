# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\Documents\GitHub\fourMs\MGT-python\musicalgestures\_utils.py
# Compiled at: 2020-04-26 14:41:37
# Size of source mod 2**32: 11564 bytes


class MgProgressbar:
    __doc__ = "\n    Calls in a loop to create terminal progress bar.\n\n    Attributes\n    ----------\n    - total : int, optional\n\n        Default is 1000. Total iterations.\n    - time_limit : float, optional\n\n        Default is 0.1. The maximum refresh rate of the progressbar in seconds. \n    - prefix : str, optional\n\n        Default is 'Progress'. Prefix string.\n    - suffix : str, optional\n\n        Default is 'Complete'. Suffix string.\n    - decimals : int, optional\n\n        Default is 1. Positive number of decimals in percent complete.\n    - length : int, optional\n\n        Default is 40. Character length of bar.\n    - fill : str, optional\n\n        Default is '█'. Bar fill character.\n\n    Methods\n    -------\n    - progress(iteration : int)\n\n        Prints the progressbar according to `iteration` which is the \n        0-based step in the number of steps defined by `self.total`. At the \n        last step (where the progressbar shows 100%) `iteration` == `total` - 1. \n    "

    def __init__(self, total=100, time_limit=0.1, prefix='Progress', suffix='Complete', decimals=1, length=40, fill='█'):
        self.total = total - 1
        self.time_limit = time_limit
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.now = self.get_now()
        self.finished = False

    def get_now(self):
        from datetime import datetime
        return datetime.timestamp(datetime.now())

    def over_time_limit(self):
        callback_time = self.get_now()
        return callback_time - self.now >= self.time_limit

    def progress(self, iteration):
        if self.finished:
            return
        else:
            import sys
            capped_iteration = iteration if iteration <= self.total else self.total
            if iteration >= self.total:
                self.finished = True
                percent = ('{0:.' + str(self.decimals) + 'f}').format(100 * (capped_iteration / float(self.total)))
                filledLength = int(self.length * capped_iteration // self.total)
                bar = self.fill * filledLength + '-' * (self.length - filledLength)
                sys.stdout.flush()
                sys.stdout.write('\r%s |%s| %s%% %s' % (
                 self.prefix, bar, percent, self.suffix))
                print()
            else:
                if self.over_time_limit():
                    self.now = self.get_now()
                    percent = ('{0:.' + str(self.decimals) + 'f}').format(100 * (capped_iteration / float(self.total)))
                    filledLength = int(self.length * capped_iteration // self.total)
                    bar = self.fill * filledLength + '-' * (self.length - filledLength)
                    sys.stdout.flush()
                    sys.stdout.write('\r%s |%s| %s%% %s' % (
                     self.prefix, bar, percent, self.suffix))
                else:
                    return

    def __repr__(self):
        return 'MgProgressbar'


def scale_num(val, in_low, in_high, out_low, out_high):
    """
    Scales a number linearly.

    Parameters
    ----------
    - val : int or float

        The value to be scaled.
    - in_low : int or float

        Minimum of input range.
    - in_high : int or float

        Maximum of input range.
    - out_low : int or float

        Minimum of output range.
    - out_high : int or float

        Maximum of output range.

    Returns
    -------
    int or float

        The scaled number.
    """
    return (val - in_low) * (out_high - out_low) / (in_high - in_low) + out_low


def scale_array(array, out_low, out_high):
    """
    Scales an array linearly.

    Parameters
    ----------
    - array : arraylike

        The array to be scaled.
    - out_low : int or float

        Minimum of output range.
    - out_high : int or float

        Maximum of output range.

    Returns
    -------
    - arraylike

        The scaled array.
    """
    minimum, maximum = np.min(array), np.max(array)
    m = (out_high - out_low) / (maximum - minimum)
    b = out_low - m * minimum
    return m * array + b


def get_frame_planecount(frame):
    """
    Gets the planecount (color channel count) of a video frame.

    Parameters
    ----------
    - frame : numpy array

        A frame extracted by `cv2.VideoCapture().read()`.

    Returns
    -------
    - {3, 1}

        The planecount of the input frame.
    """
    import numpy as np
    if len(np.array(frame).shape) == 3:
        return 3
    return 1


def frame2ms(frame, fps):
    """
    Converts frames to milliseconds.

    Parameters
    ----------
    - frame : int

        The index of the frame to be converted to milliseconds.
    - fps : int

        Frames per second.

    Returns
    -------
    - int

        The rounded millisecond value of the input frame index.
    """
    return round(frame / fps * 1000)


class MgImage:
    __doc__ = '\n    Class for handling images in the Motion Gestures Toolbox.\n\n    Attributes\n    ----------\n    - filename : str\n\n        The path to the image file to be loaded.\n    '

    def __init__(self, filename):
        self.filename = filename
        import os
        self.of = os.path.splitext(self.filename)[0]
        self.fex = os.path.splitext(self.filename)[1]

    import musicalgestures._show as show

    def __repr__(self):
        return f"MgImage('{self.filename}')"


def convert_to_avi(filename):
    """
    Converts a video to one with .avi extension using ffmpeg.

    Parameters
    ----------
    - filename : str

        Path to the input video file.

    Outputs
    -------
    - `filename`.avi

        The converted video file.

    Returns
    -------
    - str

        The path to the output '.avi' file.
    """
    import os
    of = os.path.splitext(filename)[0]
    fex = os.path.splitext(filename)[1]
    cmds = ' '.join(['ffmpeg', '-i', filename, '-c:v',
     'mjpeg', '-q:v', '3', of + '.avi'])
    os.system(cmds)
    return of + '.avi'


def rotate_video(filename, angle):
    """
    Rotates a video by an `angle` using ffmpeg.

    Parameters
    ----------
    - filename : str

        The path to the input video.
    - angle : int or float

        The angle (in degrees) specifying the amount of rotation. Positive values rotate clockwise.

    Outputs
    -------
    - `filename`_rot.avi

        The rotated video file.

    Returns
    -------
    - str

        The path to the output (rotated) video file.
    """
    import os, math
    of = os.path.splitext(filename)[0]
    fex = os.path.splitext(filename)[1]
    if os.path.isfile(of + '_rot.avi'):
        os.remove(of + '_rot.avi')
    cmds = ' '.join(['ffmpeg', '-i', filename, '-c:v',
     'mjpeg', '-q:v', '3', '-vf', f"rotate={math.radians(angle)}", of + '_rot.avi'])
    os.system(cmds)
    return (of + '_rot', fex)


def convert_to_grayscale(filename):
    """
    Converts a video to grayscale using ffmpeg.

    Parameters
    ----------
    - filename : str

        Path to the video file to be converted to grayscale.

    Outputs
    -------
    - `filename`_gray.avi

    Returns
    -------
    - str

        The path to the output (grayscale) video file.
    """
    import os
    of = os.path.splitext(filename)[0]
    fex = os.path.splitext(filename)[1]
    cmds = ' '.join(['ffmpeg', '-i', filename, '-c:v', 'mjpeg', '-q:v', '3', '-vf',
     'hue=s=0', of + '_gray' + fex])
    os.system(cmds)
    return (of + '_gray', fex)


def extract_wav(filename):
    """
    Extracts audio from video into a .wav file via ffmpeg.

    Parameters
    ----------
    - filename : str

        Path to the video file from which the audio track shall be extracted.

    Outputs
    -------
    - `filename`.wav

    Returns
    -------
    - str

        The path to the output audio file.
    """
    import os
    of = os.path.splitext(filename)[0]
    fex = os.path.splitext(filename)[1]
    cmds = ' '.join(['ffmpeg', '-i', filename, '-acodec',
     'pcm_s16le', of + '.wav'])
    os.system(cmds)
    return of + '.wav'


def get_length(filename):
    """
    Gets the length (s) of a video using ffprobe.

    Parameters
    ----------
    - filename : str

        Path to the video file to be measured.

    Returns
    -------
    - float

        The length of the input video file in seconds.
    """
    import subprocess
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
     'default=noprint_wrappers=1:nokey=1', filename],
      stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
    return float(result.stdout)


def audio_dilate(filename, dilation_ratio=1):
    """
    Time-stretches or -shrinks (dilates) an audio file using ffmpeg.

    Parameters
    ----------
    - filename : str

        Path to the audio file to be dilated.
    - dilation_ratio : int or float, optional

        Default is 1. The source file's length divided by the resulting file's length.

    Outputs
    -------
    - `filename`_dilated.wav

    Returns
    -------
    - str

        The path to the output audio file.
    """
    import os
    of = os.path.splitext(filename)[0]
    fex = os.path.splitext(filename)[1]
    cmds = ' '.join(['ffmpeg', '-i', filename, '-codec:a', 'pcm_s16le',
     '-filter:a', 'atempo=' + str(dilation_ratio), of + '_dilated' + fex])
    os.system(cmds)
    return of + '_dilated' + fex


def embed_audio_in_video(source_audio, destination_video, dilation_ratio=1):
    """
    Embeds an audio file as the audio channel of a video file using ffmpeg.

    Parameters
    ----------
    - source_audio : str

        Path to the audio file to be embedded.

    - destination_video : str

        Path to the video file to embed the audio file in.

    Outputs
    -------
    - `destination_video` with the embedded audio file.
    """
    import os
    of = os.path.splitext(destination_video)[0]
    fex = os.path.splitext(destination_video)[1]
    if dilation_ratio != 1:
        audio_to_embed = audio_dilate(source_audio, dilation_ratio)
        dilated = True
    else:
        audio_to_embed = source_audio
        dilated = False
    cmds = ' '.join(['ffmpeg', '-i', destination_video, '-i', audio_to_embed, '-c:v',
     'copy', '-map', '0:v:0', '-map', '1:a:0', '-shortest', of + '_w_audio' + fex])
    os.system(cmds)
    if dilated:
        os.remove(audio_to_embed)
    os.remove(destination_video)
    os.rename(of + '_w_audio' + fex, destination_video)