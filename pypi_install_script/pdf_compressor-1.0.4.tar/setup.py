import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thomas Dewitte",
    author_email="thomasdewittecontact@gmail.com",

    name='pdf_compressor',
    version='1.0.4',
    license="MIT",
    url='https://github.com/dewittethomas/pdf-compressor',
    python_requires='>= 3.5',
    
    description='An engine to compress pdf files to one pdf file, the process to compress the files takes maximum one minute',
    long_description=README,
    long_description_content_type="text/markdown",

    package_dir={"pdf_compressor": "pdf_compressor"},
    install_requires=["Pillow>=7.0.0", "pdf2jpg>=1.0", "img2pdf>=0.3.3"],
    
    packages=setuptools.find_packages(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)