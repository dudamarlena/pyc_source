from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="embark",
    version="0.1.1",
    author="Naresh Nagabushan",
    description="Deep Learning code starter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Naresh1318/embark",
    license="MIT",
    packages=["embark"],
    zip_safe=True,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "embark = embark.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "wheel"
    ],
    python_requires=">=3.5",
)
