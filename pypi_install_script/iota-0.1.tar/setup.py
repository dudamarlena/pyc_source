from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='iota',
    version='0.1',
    rust_extensions=[
        RustExtension('iota._helloworld', 'Cargo.toml', binding=Binding.PyO3)
    ],
    packages=['iota'],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False)
