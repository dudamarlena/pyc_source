from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    zip_safe=False,
    name="wom",
    version="1.1.4",
    description="the 'words of meaning' toolkit library",
    url="https://github.com/wordsofmeaning/wom",
    author="Sam J. Walls",
    author_email="sam@s-w.io",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "corpgen = wom.corpgen.__main__:main"
        ]
    },
)