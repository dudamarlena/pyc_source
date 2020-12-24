from setuptools import setup, find_packages
import pydnevnikruapi


setup(
    name="pydnevnikruapi",
    version=pydnevnikruapi.__version__,
    url="https://github.com/kesha1225/DnevnikRuAPI",
    author="kesha1225",
    packages=find_packages(),
    description="simple wrapper for dnevnik.ru API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=["requests", "aiohttp"],
)
