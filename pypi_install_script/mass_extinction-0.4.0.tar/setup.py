'''
Mass Extinction in Evolutionary Algorithms
Author: Kaelan Engholdt
Version: 02/11/2020

Setup file for the mass_extinction package.

'''

from setuptools import setup


# a shorter version of the README.txt that serves as a basic description of the package
long_description = "Mass Extinction in Evolutionary Algorithms\nAuthor: Kaelan Engholdt\nVersion: 02/11/2020\n" \
                   "\nA biologically inspired mass extinction class for use in evolutionary algorithms. Contains " \
                   "adjustable parameters for extinction events and methods of repopulation. This package is designed" \
                   " to be integrated into an evolutionary algorithm. Due to the problem-specific nature of " \
                   "evolutionary algorithms, minor parts of this package must be finished by the user.\n\nIf used and" \
                   " tuned correctly, extinction can be a powerful tool in evolutionary algorithms. This simple " \
                   "package attempts to provide a basis upon which users can integrate extinction events into their " \
                   "evolutionary algorithms, maintain population diversity, improve the overall fitness of their " \
                   "population, and attempt to overcome " \
                   "sub-optimal peaks within the search space of their particular problem.\n\n" \
                   "Includes support for integration with evolutionary algorithms that make use of the " \
                   "Distributed Evolutionary Algorithms in Python (DEAP) library, which is a framework for writing " \
                   "evolutionary algorithms. This package is not affiliated with DEAP, but offers support for " \
                   "evolutionary algorithms using that library.\n\n\nCompatibility\n" \
                   "----------\nThe package is OS independent, and can be run on either Python 2 or Python 3.\n\n\n" \
                   "Requirements\n----------\nRequirements:\n - A population based evolutionary algorithm.\n" \
                   " - The parent population must be sorted by fitness and stored in a list.\n - Following" \
                   " and completing all TODO comments.\n\n\nContents\n----------\nThe package consists of the " \
                   "following files:\n - mass_extinction.py: Contains the main Extinction class.\n - ext_params.py:" \
                   " Contains all of the adjustable parameters for the Extinction class.\n - ext_types.py: Contains" \
                   " numerous extinction parameter sets for testing.\n\n\nDesign\n----------\n" \
                   "This package has been specifically designed to be integrated and interlaced with an " \
                   "evolutionary algorithm. Due to the problem-specific nature of evolutionary algorithms, " \
                   "some of this package must be finished by the user.\n\nThis package features the following:" \
                   "\n\nA multitude of completely adjustable parameters that affect how both extinction and " \
                   "repopulation operate.\nTwo methods of extinction:\n - Instant Extinction\n - Gradual " \
                   "Extinction\nThree types of extinction that can be used separately or in conjunction " \
                   "with one another:\n - Interval Extinction\n - Probabilistic Extinction\n - " \
                   "Fitness Extinction\nTwo methods of repopulation:\n - Instant Repopulation\n - Gradual " \
                   "Repopulation\nThree types of repopulation that can be used separately or " \
                   "in conjunction with one another:\n - Repopulation using elite members.\n - Repopulation " \
                   "using surviving members.\n - Repopulation using random members.\nTesting of up to 324 " \
                   "parameter sets generated from permutations of user-defined parameters.\nAll parameters can be " \
                   "saved and later called upon to revert back to a previous version of extinction/repopulation." \
                   "\n\nFurther information can be found in the README.txt."

# define setup
setup(
    name = "mass_extinction",
    version = "0.4.0",
    author = "Kaelan Engholdt",
    author_email = "engholdt8911@uwlax.edu",
    description = ("Mass extinction class for evolutionary algorithms."),
    keywords = "extinction evolutionary genetic algorithm",
    url = "https://bitbucket.org/Trench58/mass_extinction/src/master/",
    packages = ["mass_extinction"],
    package_data = {"" : ["README.txt"]},
    long_description = long_description,
    long_description_content_type = "text/plain",
    classifiers = ["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering :: Artificial Intelligence",
                   "Topic :: Scientific/Engineering :: Artificial Life"]
)
