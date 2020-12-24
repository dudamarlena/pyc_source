from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='Fortnite-API-com',
    packages=['FortniteAPI'],
    version='0.0.5',
    license='MIT',
    description='Simple python wrapper for https://fortniteapi.com/',
    author='KarkaLT',
    author_email='karoliscd@gmail.com',
    url='https://fortniteapi.com/',
    keywords=['fortnite', 'stats', 'statistics', 'game'],
    install_requires=['requests==2.21.0'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
