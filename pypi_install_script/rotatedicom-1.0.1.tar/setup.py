import setuptools
setuptools.setup(
    name = "rotatedicom",
    version = "1.0.1",
    packages = ["rotatedicom"],
    
    author="Dibya Raj Ghosh", 
    author_email="dibyaraj11@gmail.com", 
    maintainer="Dibya", 
    maintainer_email="dibyaraj11@gmail.com", 
    description="It will rotate image by a specific angle provided by user",
    long_description="""
    Input-Dicom image
    Output-Dicom image
    It will rotate image by a specific angle provided by user
    This function will accept 3 mandatory parameter- source folder, destination folder, 
    rotation-angle(positive  value means -anticlowise and negative value means clockwise rotation)

    """, 

    license="MIT"
    )