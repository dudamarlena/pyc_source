from setuptools import setup

setup(
    name="vectorspector",
    version="0.1",
    author="D. I. Cortes",
    description='Library for plotting vector fields, based on Matplotlib quiver',
    url='https://github.com/davidcortesortuno/vectorspector',
    install_requires=[
        'matplotlib', 'scipy'
    ],
    packages=['vectorspector', 'vectorspector.readers'],
    # scripts=['bin/nb_cat'],
    license='BSD3',
    # package_data={
    #     'tests':['Makefile']
    #     }
)
