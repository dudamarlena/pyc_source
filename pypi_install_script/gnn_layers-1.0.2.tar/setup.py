import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="gnn_layers",
    description="Some custom GNN layers for PyTorch Geometric",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="v1.0.2",
    packages=["gnn_layers"],
    python_requires=">=3",
    url="https://github.com/shobrook/custom-gnn-layers",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    # classifiers=[],
    install_requires=["torch", "torch_geometric"],
    keywords=["gnn", "graph-neural-network", "convolution", "pooling", "pytorch", "graph"],
    license="MIT"
)
