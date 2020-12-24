from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='amocrm_pywrapper',
    packages=['amocrm_pywrapper'],
    version='0.1',
    license='MIT',
    author='Nikita Yugov',
    author_email='nikitosnikn@yandex.ru',
    description='Python API Wrapper for AmoCRM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NikitosnikN/amocrm_pywrapper',
    download_url='https://github.com/NikitosnikN/amocrm_pywrapper/archive/0.1.0.tar.gz',
    keywords=[
        'amocrm',
        'api',
        'wrapper'
    ],
    install_requires=[
        'httpx (~=0.11.1)',
    ],
    classifiers=[
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7',
)
