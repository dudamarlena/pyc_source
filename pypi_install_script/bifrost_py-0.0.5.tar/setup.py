import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setuptools.setup(
    name='bifrost_py',
    version='0.0.5',
    author="Ignacio Althabe",
    author_email="nacho.althabe@gmail.com ",
    description="Wallets based on SALT instead of Nonce.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.riaquest.com/nacho/bifrost",
    packages=['bifrost_py'],
    package_data = {
        'bifrost_py': ['**/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
