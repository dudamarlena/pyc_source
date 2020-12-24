import setuptools

pkg_name = "spikeforest_widgets"

setuptools.setup(
    name=pkg_name,
    version="0.1.1",
    author="Jeremy Magland",
    description="Widgets for visualizing a SpikeForest analysis",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'simplejson',
        'spikeextractors',
        'scipy'
        ],
    scripts=[
        'bin/sf-view-recording',
        'bin/sf-view-timeseries'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)