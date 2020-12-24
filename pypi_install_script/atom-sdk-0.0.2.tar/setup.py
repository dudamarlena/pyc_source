from setuptools import setup

setup(
    name="atom-sdk",
    version="0.0.2",
    description="Atom Python SDK",
    url="https://pypi.org/project/atom-sdk",
    maintainer="Supremind Atom",
    maintainer_email="atom@supremind.com",
    packages=['atom', 'atom.interceptors', 'atom.github.com.envoyproxy.protoc_gen_validate.validate'],
    install_requires=[
        "grpcio"
    ],
)
