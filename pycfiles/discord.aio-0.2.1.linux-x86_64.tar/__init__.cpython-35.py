# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/__init__.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 1112 bytes
"""
discord.aio is an asynchronous Discord API wrapper for python 3.6+
"""
from .client import DiscordBot
from .channel import Channel, ChannelMessage, Attachment, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo
from .emoji import Emoji
from .user import User, UserConnection
from .guild import Guild, GuildEmbed, GuildMember, Integration, IntegrationAccount
from .role import Role
from .http import HTTPHandler
from .websocket import DiscordWebsocket
from .webhook import Webhook
from .invite import Invite, InviteMetadata
from .enums import ChannelTypes, ExplicitContentFilterLevel, MessageActivityTypes, MessageNotificationLevel, MFALevel, VerificationLevel
from .exceptions import WebSocketCreationError, AuthorizationError, EventTypeError, UnhandledEndpointStatusError
from .base import DiscordObject
from .voice import VoiceRegion, VoiceState
from .activity import Activity, ActivityAssets, ActivityParty, ActivityTimestamps
from .constants import DISCORD_API_URL, DISCORD_CDN
from .version import __version__
__author__ = 'Ryozuki'
__license__ = 'MIT'