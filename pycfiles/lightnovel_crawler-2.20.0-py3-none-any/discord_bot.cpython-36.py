# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/bots/discord/discord_bot.py
# Compiled at: 2020-03-23 10:55:22
# Size of source mod 2**32: 3225 bytes
import asyncio, logging, os, queue, re, shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import discord
from ...binders import available_formats
from ...core.app import App
from ...sources import crawler_list
from ...utils.uploader import upload
from .config import signal
from .message_handler import MessageHandler
logger = logging.getLogger('DISCORD_BOT')

class DiscordBot(discord.Client):
    handlers = {}

    def start_bot(self):
        self.run(os.getenv('DISCORD_TOKEN'))

    async def on_ready(self):
        print('Discord bot in online!')
        activity = discord.Activity(name=('🔥%slncrawl🔥' % signal), type=(discord.ActivityType.watching))
        await self.change_presence(activity=activity, status=(discord.Status.online))

    async def on_message(self, message):
        self.cleanup_handlers()
        if message.author == self.user:
            return
        if message.author.bot:
            return
        try:
            if message.content == signal + 'lncrawl':
                uid = message.author.id
                if uid in self.handlers:
                    self.handlers[uid].destroy()
                await self.handle_message(message)
            else:
                if isinstance(message.channel, discord.abc.PrivateChannel):
                    await self.handle_message(message)
        except Exception:
            logger.exception('Something went wrong processing message')

    async def send_public_text(self, message, text):
        async with message.channel.typing():
            await message.channel.send(text)

    async def handle_message(self, message):
        if self.is_closed():
            return
        try:
            uid = str(message.author.id)
            logger.info('Processing message from %s', message.author.name)
            if uid not in self.handlers:
                self.handlers[uid] = MessageHandler(self)
                await message.author.send('-' * 25 + '\n' + 'Hello %s\n' % message.author.name + '-' * 25 + '\n')
                logger.info('New handler for %s', message.author.name)
            self.handlers[uid].process(message)
        except Exception as err:
            logger.exception('While handling this message: %s', message)

    async def cleanup_handlers(self):
        try:
            cur_time = datetime.now()
            for uid, handler in self.handlers.items():
                last_time = getattr(handler, 'last_activity', cur_time)
                if (cur_time - last_time).days > 1:
                    handler.destroy()

        except Exception:
            logger.exception('Failed to cleanup handlers')