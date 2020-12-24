# players_amp
### written in Phyton 3.8.1 by Strolch

from setuptools import setup

setup(
    name='players_amp',
    version='2.34',
    license='MIT',
    description='a little tool written in phyton to count all the active players on your AMP managed game server',
    author='Strolch',
    author_email='hello.circles@gmail.com',
    url="https://github.com/R0b95/player_amp",
    download_url='https://github.com/R0b95/players_amp/archive/2.0.tar.gz',
    keywords=['AMP', 'UserCount', 'ActiveUser', 'ActivePlayer'],
    packages=['players_amp', 'players_amp.api_functions'],
    entry_points="""
        [console_scripts] 
            players_amp = players_amp.main:main
            players_amp.debug = players_amp.debug:debug
            players_amp.setserver = players_amp.setserver:setserver
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
