from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyddblapi',
    packages=['ddblapi'],
    version='0.0.3',
    description='The official Python wrapper of Divine Discord Bot List',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DivineDiscordBotList/ddblAPI.py',
    author='Sworder71',
    author_email='divinediscordbots@gmail.com',
    license='Apache-2.0',
    keywords=['python3', 'ddbl', 'api'],
    install_requires=['aiohttp']
)