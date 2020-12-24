from setuptools import setup

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name='adcom',
    version='1.3',
    packages=[''],
    url='https://github.com/KvaksMan/adcom',
    license='Apache 2.0',
    author='KvaksManYT',
    author_email='kvaksman225@gmail.com',
    description='The additional commands to Python!',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
