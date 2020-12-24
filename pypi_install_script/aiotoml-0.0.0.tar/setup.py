import setuptools


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r") as req_file:
    dependeces = [
        pack for pack in req_file.read().split('\n')
    ]

setuptools.setup(
    name="aiotoml",
    version="0.0.0",
    author="Kurbatov Yan",
    author_email="deknowny@gmail.com",
    description="Works with TOML in the async style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rhinik/aiotoml",
    packages=setuptools.find_packages(),
    license="Apache=2.0",
    install_requires=dependeces,
    keywords='aio async toml',
    python_requires='>=3.8',
)
