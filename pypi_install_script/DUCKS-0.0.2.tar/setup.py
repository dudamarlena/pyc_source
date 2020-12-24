import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "DUCKS",
    version = "0.0.2",
    author = "Jn Brq",
    author_email = "juan.baruque@gmail.com",
    description = "It just prints random ducks",
    long_description = read('README'),
    license = "0BSD",
    keywords = "ducks test example",
    url = "http://pixelrobot.net",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts': [
            'ducks=DUCKS.ducks:run',
        ],
    },
)
