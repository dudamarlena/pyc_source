from setuptools import setup

setup(
    author="Nikita Sivakov",
    author_email="cryptomaniac.512@gmail.com",
    description="Library for generating static API",
    install_requires=['PyYAML'],
    keywords="static api generator",
    license="MIT",
    long_description_markdown_filename='README.md',
    name="static_api_generator",
    packages=["static_api_generator"],
    setup_requires=['setuptools-markdown'],
    url="https://github.com/cryptomaniac512/python-static-api-generator",
    version="0.0.2",
)
