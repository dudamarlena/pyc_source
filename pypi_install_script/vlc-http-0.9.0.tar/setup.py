from setuptools import setup

setup(
    name='vlc-http',
    version='0.9.0',
    packages=['vlchttp'],
    install_requires=['requests'],
    url='https://www.github.com/dylhack/vlc-http',
    license='BSD-2-Clause',
    author='dylhack',
    author_email='dylhack@librem.one',
    description='An HTTP client for VLC\'s HTTP server.'
)
