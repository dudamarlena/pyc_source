# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/converter.py
# Compiled at: 2020-03-14 09:27:30
# Size of source mod 2**32: 3789 bytes
import pathlib, subprocess
from zimscraperlib.logging import nicer_args_join
from zimscraperlib.imaging import resize_image
from .constants import logger

def hook_youtube_dl_ffmpeg(video_format, low_quality, data):
    """ youtube-dl hook to convert video at end of download

        - if low_quality was request
        - if received format is not requested one """
    if data.get('status') != 'finished':
        return
    src_path = pathlib.Path(data['filename'])
    post_process_video(video_dir=(src_path.parent),
      video_id=(src_path.stem),
      video_format=video_format,
      low_quality=low_quality)


def post_process_video(video_dir, video_id, video_format, low_quality):
    """ apply custom post-processing to downloaded video

        - resize thumbnail
        - recompress video if incorrect video_format or low_quality requested """
    files = [p for p in video_dir.iterdir() if p.stem == 'video' if p.suffix != '.jpg']
    if len(files) == 0:
        logger.error(f"Video file missing in {video_dir} for {video_id}")
        logger.debug(list(video_dir.iterdir()))
        raise FileNotFoundError(f"Missing video file in {video_dir}")
    if len(files) > 1:
        logger.warning(f"Multiple video file candidates for {video_id} in {video_dir}. Picking {files[0]} out of {files}")
    src_path = files[0]
    resize_image((src_path.parent.joinpath('video.jpg')),
      width=480, height=270, method='cover')
    if not low_quality:
        if src_path.suffix[1:] == video_format:
            return
    dst_path = src_path.parent.joinpath(f"video.{video_format}")
    recompress_video(src_path, dst_path, video_format, low_quality)


def recompress_video(src_path, dst_path, video_format, low_quality):
    """ re-encode a video file in-place (via a temp file) for format and quality """
    tmp_path = src_path.parent.joinpath(f"video.tmp.{video_format}")
    video_codecs = {'mp4':'h264', 
     'webm':'libvpx'}
    audio_codecs = {'mp4':'aac',  'webm':'libvorbis'}
    params = {'mp4':['-movflags', '+faststart'],  'webm':[]}
    args = [
     'ffmpeg', '-y', '-i', f"file:{src_path}"]
    if low_quality:
        args += [
         '-codec:v',
         video_codecs[video_format],
         '-quality',
         'best',
         '-cpu-used',
         '0',
         '-b:v',
         '300k',
         '-qmin',
         '30',
         '-qmax',
         '42',
         '-maxrate',
         '300k',
         '-bufsize',
         '1000k',
         '-threads',
         '8',
         '-vf',
         "scale='480:trunc(ow/a/2)*2'",
         '-codec:a',
         audio_codecs[video_format],
         '-b:a',
         '128k']
    else:
        args += [
         '-codec:v',
         video_codecs[video_format],
         '-quality',
         'best',
         '-cpu-used',
         '0',
         '-bufsize',
         '1000k',
         '-threads',
         '8',
         '-codec:a',
         audio_codecs[video_format]]
    args += params[video_format]
    args += [f"file:{tmp_path}"]
    logger.info(f"recompress {src_path} -> {dst_path} video_format={video_format!r} low_quality={low_quality!r}")
    logger.debug(nicer_args_join(args))
    ffmpeg = subprocess.run(args)
    ffmpeg.check_returncode()
    src_path.unlink()
    tmp_path.replace(dst_path)