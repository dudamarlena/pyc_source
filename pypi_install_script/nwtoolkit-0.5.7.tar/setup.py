import setuptools
from nwtoolkit.__version__ import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nwtoolkit", # Replace with your own username
    version=version,
    author="RSA Security",
    author_email="sean.drzewiecki@rsa.com",
    description="Toolkit for administration of RSA Netwitness Installations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nwps.gitlab.io/nwtoolkit/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['nwtoolkit=nwtoolkit.__main__:main']
    },
    install_requires=[
        'colorama',
        'cmd2',
        'paramiko',
        'click',
        'jinja2'
    ],
)