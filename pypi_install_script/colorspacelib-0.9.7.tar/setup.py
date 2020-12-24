import pathlib
from setuptools import setup

ROOT=pathlib.Path(__file__).parent
README = (ROOT/'README.md').read_text()

setup(
    name="colorspacelib",
    version='0.9.7',
    author='Fredrick Pwol',
    author_email='fredpwol@gmail.com',
    url='https://github.com/Fredpwol/colorspacelib.git',
    description='A Python color library That easier to work with',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['colorspacelib'],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

)