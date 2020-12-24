from pathlib import Path

from setuptools import find_packages, setup

name = "conast"
current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=f"{name}",
    version="0.1.0a0",
    packages=find_packages(),
    url="https://github.com/thg-consulting/conast",
    author="thg",
    description="ConAST is an AST extension that allows consistency between python versions (Py38+).",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
