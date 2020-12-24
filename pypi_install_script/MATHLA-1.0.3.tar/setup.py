import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MATHLA",
    version="1.0.3",
    author="yiliny",
    author_email="yiliny@neocura.net",
    description="MATHLA: A Binding Affinity Prediction Tool",
    long_description=long_description,
    license='MIT License',
    long_description_content_type="text/markdown",
    url="https://github.com/MATHLAtools/MATHLA",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'numpy',
          'pandas',
          'tqdm',
          'torch==0.4.1'
      ],
    entry_points={
        'console_scripts': [
            'MATHLA=MATHLA:MATHLA.main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    zip_safe=True
)