from setuptools import setup, find_packages

setup(
    name='ol-commons-models-dev',
    packages=find_packages(),  # this must be the same as the name above
    version='1.2.2',
    description='Paquete conteniente objetos reutilizables para los microservicios de OLYMPUS',
    author='Jean Pier Barbieri Rios',
    author_email='jean.barbieri1996@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
    ], install_requires=['sqlalchemy', 'flask_sqlalchemy']
)
