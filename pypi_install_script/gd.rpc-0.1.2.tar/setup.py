from pathlib import Path
import re

from setuptools import setup

root = Path(__file__).parent

init = (root / "gdrpc.py").read_text("utf-8")

result = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', init, re.MULTILINE)

if result is None:
    raise RuntimeError("Failed to find version.")

version = result.group(1)

readme = (root / "README.rst").read_text("utf-8")


setup(
    name="gd.rpc",
    author="NeKitDS",
    author_email="gdpy13@gmail.com",
    url="https://github.com/NeKitDS/gd.rpc",
    project_urls={"Issue tracker": "https://github.com/NeKitDS/gd.rpc/issues",},
    version=version,
    py_modules=["gdrpc"],
    license="MIT",
    description="Geometry Dash Discord Rich Presence",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    entry_points={"run": ["gd.rpc = gdrpc:run"]},
)
