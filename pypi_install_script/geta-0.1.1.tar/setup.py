import setuptools
from distutils.util import convert_path

# The following "version in one place soltuiion" was found here:
# https://stackoverflow.com/a/24517154
main_ns = {}
ver_path = convert_path('geta/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geta",
    version=main_ns['__version__'],
    author="Shea Newton",
    author_email="shnewto@gmail.com",
    description="geta, for when you need to \"get a\" random thing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shnewto/geta",
    download_url="https://github.com/shnewto/geta/archive/" +
        main_ns['__version__'] + ".tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[
        'docopt',
        'names',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'geta = geta.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
