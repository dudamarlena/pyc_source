from setuptools import setup, Extension
setup(
    name = 'applemusic',
    packages = ['applemusic'],
    version = '0.3',
    license = 'MIT',
    description = 'Apple music in python made easy - Play music with ease!',
    author = 'Thierry Popat',
    author_email = 'Thierry_popat@hotmail.com',
    url = 'https://github.com/Thierryonre/applemusic',
    download_url = 'https://github.com/Thierryonre/applemusic/archive/v0.3.tar.gz',
    keywords = ['apple', 'music', 'applemusic', 'player', 'selenium', 'automation'],
    install_requires=[
        'selenium',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Other Audience',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    long_description_content_type='text/markdown',
    long_description="""
    # applemusic
     Apple music in python made easy - Play music with ease!
     Please feel free to create pull requests, whether to fix a bug or implement a new feature.

    ## Features
    _Please keep in mind that this module is still in extreme-alpha._

    ### Current Features
    * Login to the apple music platform
    * Play songs
    * Resume and pause songs
    * Click the previous button
    * Shuffle songs

    ### Features to do
    * Differentiate the ability to click the previous button to previous song and restart song
    * Determine the country code via IP address
    * Only shuffle if not shuffled and vice versa
    * Allow user to change volume
    * Play playlists
    * Initiate all commands in one function
    * Allow sleep statements to be more easily changed for people with different internet speeds
    * Allow firefox and PhantomJS to be used

    ### Other things to do
    * Remove sleep statements to make it faster
    * Add documentation for variables dictionary
    * Add documentation to install module from source

    ## **Requirements**
    * Python 3.*
    * Selenium

    ## **Installation**
    ### **From PyPi**
    ```
    pip install applemusic
    ```

    ## **Usuage**
    To use the module, run the following commands:
    ```python
    from applemusic import AppleMusic
    AM = AppleMusic()
    AM.setupMethod()
    AM.setupVariables()
    AM.initiateWindow()
    AM.login("Johnny_applebottom@outlook.com", "password123")
    # <COMMAND> E.G. AM.playSong("Hello by Adele")
    ```

    Replace the line with <COMMAND> on it with some of the commands from below.
    The commands to be replaced are below and the above code is only to initiate the player so it only has to be used once,
     unless multiple songs are to be played synchronously.

    ## **Commands**
    | Command       | Parameters                      | What does it do?                                                                                                  |
    |---------------|---------------------------------|-------------------------------------------------------------------------------------------------------------------|
    | login         | Username/Email address Password | Logs into the apple music website. If 2FA is enabled, it will ask for the code sent to a validated iCloud device. |
    | playSong      | Song                            | Plays the song. The input is directly passed  into the apple music website.                                       |
    | resumeOrPause | NO PARAMETERS                   | Resumes or pauses the song regardless of its current state.                                                       |
    | previous      | NO PARAMETERS                   | Presses the previous button on the apple music website. Needs to be called twice to rewind a song.                |
    | forward       | NO PARAMETERS                   | Presses the forward button on the apple music website.                                                            |
    | shuffle       | NO PARAMETERS                   | Shuffles the order of the songs regardless of whether it was already shuffled or not.                             |

    ## **Notes**
    * Until the sleep statements are removed, the time for the script to execute will be longer than it should be.
    * However, selenium can just be slow. Speeds may vary due to your internet speed.
    * PhantomJS should make the script faster when I have implemented it.
    """,
)
