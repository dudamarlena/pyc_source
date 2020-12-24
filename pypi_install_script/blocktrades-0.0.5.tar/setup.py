# blocktrades
import blocktrades

# python
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=blocktrades.__name__,
    version = blocktrades.__version__,
    packages = ["blocktrades", "blocktrades_base"],
    description = blocktrades.__description__,
    author = blocktrades.__author__,
    author_email = blocktrades.__author_email__,
    url = blocktrades.__url__,
    python_requires='>=3.5.0',
    py_modules=["requests"],
    long_description=read('README.md'),
    include_package_data = True,
    install_requires = ["requests"],
    keywords = ["blocktrades","blocktrades api", "blocktrades python"],
    license = "MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
