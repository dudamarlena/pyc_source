import setuptools

setuptools.setup(
    name="custom_format",
    version="1.0.2",
    author="AndyHsueh",
    author_email="syt156321@gmail.com",
    description="A custom format for optional html form",
    packages=["custom_format"],
    python_requires='>=3.6',
    license="MIT",
    install_requires=["behave", "yattag"],
    download_url="https://github.com/andy8927/custom_format/archive/1.0.2.tar.gz"
)
