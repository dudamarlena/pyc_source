from setuptools import setup
import re

with open('bot.py', 'r') as file:
    local_version = re.findall("VERSION = '(.*?)'", file.read())

with open("README.md", "r") as f:
    long_description = f.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = 'discordgsm',
    version = local_version[0],
    license='MIT',
    description = 'Monitor your game servers on Discord',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'TatLead',
    url = 'https://github.com/DiscordGSM/DiscordGSM',
    download_url = f'https://github.com/DiscordGSM/DiscordGSM/archive/v{local_version[0]}.tar.gz',
    keywords = ["discordgsm", "query", "gameserver", "gameservers", "monitor", "dgsm", "game-servers", "discord", "gaming", "game"],
    install_requires = requirements,
    python_requires='>=3.5.3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)