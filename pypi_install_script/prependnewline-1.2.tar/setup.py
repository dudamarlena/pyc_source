from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prependnewline',
    version='1.2',
    py_modules=['prependnewline'],
    author="Ayobami Adewale",
    author_email="ayblaq@gmail.com",
    keywords="markdown prepend list with newline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ayblaq/prependnewline",
    install_requires = ['markdown>=2.5','setuptools'],
    license='MIT License',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)