import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='polymicro',
    version='0.2.0',
    author='Resilient Vitality',
    author_email='zprobst@resilientvitality.com',
    description='PolyMicro is a Model Based Rest API system written around PynamoDD and Marshmallow for flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/resilient-vitality/PolyMicro',
    packages=setuptools.find_packages(exclude=('tests', 'example')),
    install_requires=[
        'pynamodb>=4.0.0',
        'marshmallow>=3.0.0',
        'flask>=1.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
)
