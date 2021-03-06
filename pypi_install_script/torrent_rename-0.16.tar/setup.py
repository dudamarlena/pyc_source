import io
import re
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

setup(
    name="torrent_rename",
    version=version,
    url="https://github.com/licface/torrent_rename",
    project_urls={
        "Documentation": "https://github.com/licface/torrent_rename",
        "Code": "https://github.com/licface/torrent_rename",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="print objects with colored with less info",
    long_description=readme,
    packages=["torrent_rename"],
    install_requires=[
        'make_colors>=3.12',
        'make_colors_tc',
        'colorama',
        'termcolor',
        'configset',
        'cmdw',
        'configparser',
        'pydebugger'
    ],
    entry_points = {
         "console_scripts": [
             "torrent_rename = torrent_rename.torrent_rename_script:usage",
         ]
    },
    data_files=['__version__.py', 'README.rst', 'LICENSE.rst'],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
