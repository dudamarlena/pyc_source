from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_descriptions = fh.read()

s = setup(
    name="rx7",
    version="1.7.7",
    license="MIT",
    description="High API, Shortcut for most usefull functions, Special Features",
    url="http://rx7.ir",
    packages=find_packages(),
    install_requires=['colored'],
    python_requires = ">= 3.4",
    author="Ramin RX7",
    author_email="rawmin.rx@gmail.com",

    classifiers=['Programming Language :: Python :: 3'],
    long_description=long_descriptions,
    long_description_content_type="text/markdown",
    )
#,'pyautogui','PySimpleGUI'


