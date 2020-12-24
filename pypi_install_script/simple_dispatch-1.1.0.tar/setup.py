import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='simple_dispatch',
    version='1.1.0',
    author='Resilient Vitality',
    author_email='zprobst@resilientvitality.com',
    description='A library inspired by the Django Dispatch System for simple pub-sub interactions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/resilient-vitality/SimpleDispatch',
    packages=setuptools.find_packages(exclude=('tests', )),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
)
