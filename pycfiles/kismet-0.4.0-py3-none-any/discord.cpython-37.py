# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/github/kismet-py/kismet/chatbot/discord.py
# Compiled at: 2019-07-19 22:52:54
# Size of source mod 2**32: 1065 bytes
from os import getenv
from discord import Client
from kismet.core import process_markdown
token = getenv('DISCORD_TOKEN', '')
clientid = getenv('DISCORD_CLIENTID', '0')
permissions = getenv('DISCORD_PERMISSIONS', '1116800')
oauth2_template = 'https://discordapp.com/oauth2/authorize?scope=bot&client_id=%s&permissions=%s'
oauth2_url = oauth2_template % (clientid, permissions)
print('Use the following URL to invite:')
print(oauth2_url)
client = Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content
    if client.user in message.mentions:
        content = content.replace('<@' + str(client.user.id) + '>', 'kismet')
    response = process_markdown(content, '{0.author.mention}'.format(message))
    if response:
        await message.channel.send(response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(token)