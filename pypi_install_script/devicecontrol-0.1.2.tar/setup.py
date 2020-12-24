import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

package_name = "devicecontrol"

setuptools.setup(
    name=package_name,
    version=version,
    author="Foo Bar",
    author_email="foo@bar.com",
    description="A package to interact with device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://pypi.apple.com/simple/{package_name}",
    # packages=setuptools.find_packages(),
    package_dir={'devicecontrol': 'source'},
    python_requires='>=3.7',
)
