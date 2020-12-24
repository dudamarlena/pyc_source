import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

_INSTALL_REQUIRES = [
    'beautifulsoup4>=4.8.2',
]

setuptools.setup(
    name='lite-linter',
    version='0.1.3',
    author="Jan Faracik",
    author_email="",
    description="Linting for LITE",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/uktrade/lite-linter",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'lint = linter.lint:main',
        ],
    },
    install_requires=_INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
