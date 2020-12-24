from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='acenv',
    version='0.1.4',
    packages=['acenv', 'acenv.ex', 'acenv.engine', 'acenv.engine.pn', 'acenv.engine.rn'],
    url='',
    license='MIT',
    author='Andrea Viganò',
    author_email='vigano02aceproject@gmail.com',
    description='Algebraic Calculation Environment for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
