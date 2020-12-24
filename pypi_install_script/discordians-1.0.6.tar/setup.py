from setuptools import setup, find_packages
long_description = open("README.rst").read()
setup(
    name="discordians",
    version="1.0.6",
    description="The official Python wrapper for the Discordians API.",
    url="https://github.com/TheDiscordians/discordians.py",
    author="NightShade256",
    author_email="nightshade1024@yandex.com",
    license="MIT",
    keywords="Discordians Python Wrapper",
    packages=find_packages(exclude=["docs"]),
    install_requires=["aiohttp>=3.3.0,<3.4.0"],
    long_description=long_description
)
