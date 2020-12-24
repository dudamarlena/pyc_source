from setuptools import setup


REQUIREMENTS = [
    'astropy', 'matplotlib', 'numpy', 'scipy'
]


def readme():
    """
    This function just return the content of README.md
    """
    with open('README.md') as f:
        return f.read()


setup(
    name='pyoptica',
    version='0.3',
    description='Tools to apply light propagation algorithms',
    long_description_content_type='text/markdown',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='fourier_optics light_propagation ',
    url='https://gitlab.com/pyoptica',
    author='Maciej Grochowicz, Michal Miler',
    author_email='pyoptica@protonmail.com',
    license='MIT License',
    packages=['pyoptica', 'pyoptica.optical_elements', 'pyoptica.imaging'],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
)
