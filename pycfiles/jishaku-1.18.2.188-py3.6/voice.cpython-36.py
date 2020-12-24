# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/voice.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 2174 bytes
"""
jishaku.voice
~~~~~~~~~~~~~

Voice-related functions and classes.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import discord.opus, discord.voice_client
from discord.ext import commands
try:
    import youtube_dl
except ImportError:
    youtube_dl = None

async def vc_check(ctx: commands.Context):
    """
    Check for whether VC is available in this bot.
    """
    if not discord.voice_client.has_nacl:
        return await ctx.send('Voice cannot be used because PyNaCl is not loaded.')
    else:
        if discord.opus.is_loaded() or hasattr(discord.opus, '_load_default'):
            if not discord.opus._load_default():
                return await ctx.send('Voice cannot be used because libopus is not loaded and attempting to load the default failed.')
        else:
            return await ctx.send('Voice cannot be used because libopus is not loaded.')


async def connected_check(ctx: commands.Context):
    """
    Check whether we are connected to VC in this guild.
    """
    voice = ctx.guild.voice_client
    if not voice or not voice.is_connected():
        return await ctx.send('Not connected to a voice channel in this guild.')


async def playing_check(ctx: commands.Context):
    """
    Checks whether we are playing audio in VC in this guild.

    This doubles up as a connection check.
    """
    check = await connected_check(ctx)
    if check:
        return check
    if not ctx.guild.voice_client.is_playing():
        return await ctx.send('The voice client in this guild is not playing anything.')


BASIC_OPTS = {'format':'webm[abr>0]/bestaudio/best', 
 'prefer_ffmpeg':True, 
 'quiet':True}

class BasicYouTubeDLSource(discord.FFmpegPCMAudio):
    __doc__ = '\n    Basic audio source for youtube_dl-compatible URLs.\n    '

    def __init__(self, url, download=False):
        ytdl = youtube_dl.YoutubeDL(BASIC_OPTS)
        info = ytdl.extract_info(url, download=download)
        super().__init__(info['url'])