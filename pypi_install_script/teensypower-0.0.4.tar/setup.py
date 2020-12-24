from setuptools import setup, find_packages
import versioneer
requirements = ['teensytoany',]
test_requirements = ['pytest',]
setup(
    author = "Jaehee Park",
    author_email = "jaehee@ramonaoptics.com",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description = "teensy controlled power switch",
    install_requires = requirements,
    test_require = test_requirements,
    name = "teensypower",
    packages=find_packages(include=['teensypower']),
    python_requires='>=3.6',
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    LICENSE='BSD license',
)
