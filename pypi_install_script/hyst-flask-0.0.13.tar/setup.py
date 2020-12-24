import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hyst-flask',
    version='0.0.13',
    author='Léo Richard',
    author_email='leo-externe.richard@edf.fr',
    description='Un package pour connecter une application Flask à l\'HydroStore.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://si-devops-gitlab.edf.fr/dih-dpih-sci/hydrostore/libs/hyst-flask',
    install_requires=[
        'flask>=1.1.0',
        'requests>=2.23.0',
        'pyjwt>=1.7.1',
        'cryptography==2.9',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
)
