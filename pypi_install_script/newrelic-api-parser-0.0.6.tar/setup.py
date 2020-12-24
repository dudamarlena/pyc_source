import setuptools

setuptools.setup(
    name="newrelic-api-parser",
    package=['newrelic-api-parser'],
    version="0.0.6",
    author="Bharat Sinha",
    author_email="bharat.sinha.2307@gmail.com",
    description="A plug-n-play package to start using new relic APIs for data gathering",
    url="https://github.com/Bharat23/newrelic-api-parser",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords = ['new relic api', 'insights', 'new relic'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
    ],
    install_requires=[
          'requests',
      ],
    python_requires='>=3.6',
)
