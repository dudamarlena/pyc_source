import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ffsendclient',
    version='1.2.1',
    author='Alexei Doudkine',
    author_email='alexei@volkis.com.au',
    description='A library for interfacing with Firefox Send <https://send.firefox.com/> or your own instance of it.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/skorov/ffsendclient",
    install_requires=[
        'requests',
        'pycryptodome',
        'websockets'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
 )
