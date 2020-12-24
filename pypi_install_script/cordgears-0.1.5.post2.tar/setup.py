from setuptools import setup, find_packages

setup(
    name="cordgears",
    author="Jacob J\u0083ger",
    maintainer="Jacob J\u0083ger",
    version="0.1.5-2",
    description="A simple discord bot engine",
    packages=find_packages(),
    install_requires=["discord.py", "async_timeout"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities"
    ]
)
