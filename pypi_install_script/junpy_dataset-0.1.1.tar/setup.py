from setuptools import setup, find_packages

#==============================================================================

setup(
    #----------------------------------
    # JunPy information

    name='junpy_dataset',
    description='JunPy-dataset is a collection of data used in JunPy tests and examples.',
    url='https://labstt.phy.ncu.edu.tw/junpy',
    license='GPL',

    #----------------------------------
    # package information

    packages=find_packages(),
    python_requires='~=3.6',
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: C++',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],

    #----------------------------------
    # contact information

    author='Bao-Huei Huang',
    author_email='lise811020@gmail.com',
)

#==============================================================================
