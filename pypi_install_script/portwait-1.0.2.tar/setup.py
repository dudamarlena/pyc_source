from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'portwait',
    scripts=['bin/portwait'],
    version = '1.0.2',
    description = 'CLI tool for waiting on ports to open',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'KJ',
    author_email = 'jdotpy@users.noreply.github.com',
    url = 'https://github.com/jdotpy/portwait',
    download_url = 'https://github.com/jdotpy/portwait/tarball/master',
    keywords = ['tools'],
    classifiers = [],
)
