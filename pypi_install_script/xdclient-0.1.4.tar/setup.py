from os import path
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xdclient",
    version="0.1.4",

    author="Chen Jiaxing",
    author_email="jxchen@withfield.tech",

    packages=['xdclient'],

    install_requires=[
        'requests==2.22.0',
        'requests-toolbelt==0.9.1'],
    description="X-Developer Command Line Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=2.7.6',

    license="MIT",
    keywords=['X-Developer', 'git', 'client', 'git log analysis'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    url="https://x-developer.cn",
)
