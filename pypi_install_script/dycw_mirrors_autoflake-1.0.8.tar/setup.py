from pathlib import Path

from setuptools import find_packages
from setuptools import setup

from versioneer import get_cmdclass
from versioneer import get_version


author = "Derek Wan"
author_email = "d.wan@icloud.com"
with open(Path(__file__).resolve().parent.joinpath("README.md")) as fh:
    long_description = fh.read()


setup(
    # metadata
    name="dycw_mirrors_autoflake",
    version=get_version(),
    url="https://github.com/dycw/mirrors-autoflake/",
    download_url="https://pypi.org/project/dycw-mirrors-autoflake/",
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    license="MIT",
    description="A mirror of the autoflake package for pre-commit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # options
    zip_safe=False,
    install_requires=["autoflake"],
    python_requires=">=3.7",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    options={"bdist_wheel": {"universal": "1"}},
    # versioneer
    cmdclass=get_cmdclass(),
)
