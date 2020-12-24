from setuptools import setup

setup(
        name='tts',    # This is the name of your PyPI-package.
        keywords='tts text-to-speech',
        version='1.1',
        description='A simple text to speech engine for mac',
        long_description=open('README.txt').read(),
        scripts=['tts.py']                  # The name of your scipt, and also the command you'll be using for calling it
)