from setuptools import setup, find_packages

setup(
    name='todarithgen',
    version='1.0.3',
    description='A math problem generator designed for the todarith database',
    url='https://github.com/lukew3/todarithgen',
    author='Luke Weiler',
    author_email='lukew25073@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mdutils',
    ],
    entry_points={
	   'console_scripts': [
            'todarithgen=todarithgen.generator:main'
	   ],
    },
)
