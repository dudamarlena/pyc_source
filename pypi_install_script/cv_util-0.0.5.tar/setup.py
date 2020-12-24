from setuptools import setup, find_packages

setup(
    name='cv_util',
    version='0.0.5',
    maintainer='leoyejl',
    maintainer_email='jianglong.ye.leo@gmail.com',
    description='Utils for computer vision research.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tqdm',
        'trimesh',
        'torch',
        'torchvision'
    ],
    python_requires='>=3.6'
)

# install from source code: `pip install -e .` or `pip install .`
# distribute: `python setup.py sdist`
# upload: `twine upload -r pypi dist/*`
