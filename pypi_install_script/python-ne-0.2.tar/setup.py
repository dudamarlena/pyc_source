from distutils.core import setup

setup(
    name='python-ne',
    packages=['python_ne', 'python_ne/core', 'python_ne/extra', 'python_ne/utils', 'python_ne/core/model_adapters',
              'python_ne/core/ga', 'python_ne/core/neural_network', 'python_ne/extra/env_adapters', ],
    version='0.2',
    license='MIT',
    description='A neuroevolution library for python',
    author='Matheus Zickuhr',
    author_email='matheuszickuhr97@gmail.com',
    url='https://github.com/MatheusZickuhr/python-ne',
    keywords=['neuroevolution', 'neat', 'ne', 'ann', 'deep-learning'],
    install_requires=['numpy', 'tqdm'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
