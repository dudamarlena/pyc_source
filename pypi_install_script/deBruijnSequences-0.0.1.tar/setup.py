from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='deBruijnSequences',
    version='0.0.1',
    packages=['deBruijnSequence'],
    url='https://github.com/emteeoh/deBruijn-Sequences',
    license='AGPL',
    author='Richard Betel',
    author_email='emteeoh@gmail.com',
    description='generate and decode binary debruin sequences of arbitrary length',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
'''
run python setup.py sdist upload to send this module to pypi. Don't forget to update version first!
'''
