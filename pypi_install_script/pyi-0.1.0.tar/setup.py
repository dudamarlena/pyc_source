try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="pyi",
    version="0.1.0",
    description='',
    long_description=readme,
    author="Johan Andersson",
    author_email="Grokzen@gmail.com",
    maintainer='Johan Andersson',
    maintainer_email='Grokzen@gmail.com',
    license='MIT',
    packages=['pyi'],
    scripts=['scripts/pyi'],
    url='http://github.com/grokzen/pyi',
    install_requires=[
        'docopt==0.6.2',
        'requests',
    ],
    classifiers=(
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    )
)
