import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name="Calculator-demo",
        version='0.0.1',
        author='Liu tian',
        author_email='the163163163@163.com',
        description='This is just a demo package for learning to publish a package on PyPI.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/TianshangLiu/calc-demo',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],

        )
