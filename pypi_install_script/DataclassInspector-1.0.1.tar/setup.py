import io
from setuptools import setup, find_packages

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="DataclassInspector",
    version="1.0.1",
    url="https://github.com/DamlaAltun/DataclassInspector",
    license="MIT",
    author="Damla Altun",
    author_email="initalize.damla@gmail.com",
    maintainer="Damla Altun",
    maintainer_email="initalize.damla@gmail.com",
    description="See the generated code of dataclasses with reassembling bytecode, formatting static templates and tons of magic.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=['black', 'uncompyle6'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
)
