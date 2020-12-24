from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oauthGDN",
    version="1.0.3",
    author="asepherb",
    author_email="asep.herbasuki@gramedia.digital",
    description="add missing folder in gdn",
    long_description=long_description,
    license='MIT',
    url="",
    packages=[
        'gdn',
        'gdn.backends',
        'gdn.pipeline',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
