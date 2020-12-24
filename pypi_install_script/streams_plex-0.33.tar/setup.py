# streams_plex
### written in Phyton 3.8.1 by Strolch

from setuptools import setup

setup(
    name='streams_plex',
    version='0.33',
    license='MIT',
    description='a little tool written in phyton to count all the active plex streams',
    author='Strolch',
    author_email='hello.circles@gmail.com',
    url="https://github.com/R0b95/streams_plex",
    download_url='https://github.com/R0b95/streams_plex/archive/0.2.tar.gz',
    keywords=['plex', 'StreamCount', 'ActiveUser', 'ActiveStreams'],
    packages=['streams_plex'],
    entry_points="""
        [console_scripts] 
            streams_plex = streams_plex.main:main
            streams_plex.debug = streams_plex.debug:debug
            streams_plex.setserver = streams_plex.setserver:setserver
        """,
    install_requires="""
        appdirs
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
