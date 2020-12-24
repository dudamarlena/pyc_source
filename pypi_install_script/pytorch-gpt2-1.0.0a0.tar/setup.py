from setuptools import find_packages, setup

setup(
    name="pytorch-gpt2",
    version="1.0.0a0",
    install_requires=["torch>=1.3.0"],
    packages=find_packages(exclude=["tests"]),

    description="gpt2 implementation",
    author="Jeong Ukjae",
    author_email="jeongukjae@gmail.com",
    url="https://github.com/jeongukjae/pytorch-gpt2",
    python_requires=">=3.6, <3.8",
)
