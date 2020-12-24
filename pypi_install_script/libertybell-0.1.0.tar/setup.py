from pathlib import Path

from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="libertybell",
    version="0.1.0",
    author="thg",
    py_modules=["libertybell"],
    description="A static object tracer",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
