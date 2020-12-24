import distutils
import os
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()


class PTHBasedInstaller(install):
    def initialize_options(self):
        super().initialize_options()
        contents = "import sys; exec({!r})\n".format(
            self.read_pth("hackybee.pth")
        )
        self.extra_path = (self.distribution.metadata.name, contents)

    def read_pth(self, path):
        with open(path) as f:
            content = f.read()
        return content

    def finalize_options(self):
        super().finalize_options()

        install_suffix = Path(self.install_lib).relative_to(
            self.install_libbase
        )
        if str(install_suffix) == self.extra_path[1]:
            self.install_lib = self.install_libbase


setup(
    name="tigerthebee",
    version="0.1.3",
    description="Beefore plugin for Inspector Tiger",
    author="thg",
    author_email="isidentical@gmail.com",
    url="https://github.com/thg-consulting/tigerthebee",
    py_modules=["tigerthebee"],
    cmdclass={"install": PTHBasedInstaller},
    intall_requires=["inspectortiger"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
