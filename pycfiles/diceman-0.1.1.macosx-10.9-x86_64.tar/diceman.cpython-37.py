# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/diceman/diceman.py
# Compiled at: 2019-10-31 16:29:22
# Size of source mod 2**32: 1474 bytes
import discord, logging, os, re, roll
client = discord.Client()
re_str = '(?P<num>\\d+)[Dd]{1}(?P<sides>\\d+) (?P<qualifiers>[0-9\\+\\- ]*)'
re_str: str
regex = re.compile(re_str)
regex: str

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!d') or message.content.startswith('!diceman'):
        await message.channel.send('Hello!')


def get_secrets(file: str='secret.txt') -> str:
    """
    Reads the secrets file for the discord client
    """
    secret = ''
    try:
        with open(file, 'r') as (s_file):
            secret = s_file.readline()
        return secret
    except FileNotFoundError:
        logging.error('diceman.py:get_secrets - Secrets file can not be found or you do not have permissions to read it')
        exit(1)


def main():
    token = ''
    try:
        token = os.environ['DICEMAN_TOKEN']
    except KeyError:
        logging.warning('diceman.py:__main__ - DICEMAN_TOKEN environment variable not set')

    if token != '':
        client.run(token)
    else:
        client.run(get_secrets())


if __name__ == '__main__':
    main()