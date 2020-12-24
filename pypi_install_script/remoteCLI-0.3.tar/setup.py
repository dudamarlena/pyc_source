from setuptools import setup, find_packages

setup(
    name='remoteCLI',
    version=0.3,
    python_requires='>=3.4.0',
    description=(
        '对 socket 简单的封装'
    ),
    long_description=open('remoteCLI/README.md').read(),
    long_description_content_type="text/markdown",
    author='rmb122',
    author_email='pypi@rmb122.com',
    license='GPLv3.0',
    packages=find_packages(),
    platforms=["all"],
    keywords=['remote', 'ctf'],
    url='https://github.com/rmb122/remoteCLI',
)
