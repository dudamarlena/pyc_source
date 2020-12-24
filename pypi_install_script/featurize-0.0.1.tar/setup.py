import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# 
# with open('requirements.txt') as f:
#     required = f.read().splitlines()
 

setuptools.setup(
    name='featurize',
    description='A framework which help people to build deep learning application.',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url="https://github.com/louis-she/featurize",
    author='louis',
    author_email='chenglu.she@gmail.com',
    keywords='pytorch minecraft',
    # install_requires=required,
    # entry_points={
    #     'console_scripts': ['minetorch=minetorch.cli:cli'],
    # }
)
