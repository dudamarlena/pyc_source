from setuptools import setup

setup(
    name='fondberg-spotipy',
    version='2.4.5-dev2',
    description='Forked for later release simple client for the Spotify Web API',
    author="@fondberg",
    author_email="niklas.fondberg@gmail.com",
    url='http://spotipy.readthedocs.org/',
    install_requires=[
        'requests>=2.3.0',
        'six>=1.10.0',
    ],
    download_url= 'https://github.com/fondberg/spotipy/tarball/2.4.5-dev2',
    license='LICENSE.txt',
    packages=['spotipy'])
