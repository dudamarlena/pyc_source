
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-throttling-py",
    version="0.1.1",
    author="Meng yangyang",
    author_email="mengyy_linux@163.com",
    description="Django throttling",
    long_description=long_description,
    url="https://github.com/hotbaby/django-throttling-py",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["django>=1.8.18"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
