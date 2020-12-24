from pathlib import Path

from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="reportme",
    version="0.3.2",
    description="Report generator for THG",
    author="thg",
    author_email="isidentical@gmail.com",
    packages=["reportme"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
