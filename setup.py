# -*- coding: utf-8 -*-

# Import the setuptools module
import setuptools

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup parameters for the package
setuptools.setup(
    name='blazeqr', # The name of the package
    version='0.0.2', # The version number of the package
    keywords='qr qrcode blazing artistic animated gif colorized', # Keywords for the package
    description='Generator for blazing QR Codes. Including Common, Artistic and Animated QR Codes.', # A short description of the package
    long_description=long_description, # The contents of the README file
    long_description_content_type="text/markdown", # The type of the README file
    author='SirMghSBD', # The name of the package author
    author_email='sirmghsbd@gmail.com', # The email address of the package author
    url='https://github.com/sirmghsbd/blaze', # The URL of the package repository
    download_url='https://github.com/sirmghsbd/blaze', # The download URL of the package
    project_urls={
        "Bug Tracker": "https://github.com/sirmghsbd/blaze/issues", # The URL of the package issue tracker
    },
    install_requires=[
        'imageio >= 2.28.1', # The required version of the imageio package
        'numpy >= 1.24.3', # The required version of the numpy package
        'Pillow>=9.5.0' # The required version of the Pillow package
    ],
    packages=['blazeqr', 'blazeqr.qrlibs'], # The list of package directories to include
    license='GPLv3', # The license for the package
    classifiers=[
        'Programming Language :: Python :: 3', # The supported Python version
        'Operating System :: MacOS', # The supported operating systems
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)' # The license classification
    ],
    entry_points={
        'console_scripts': [
            'blazeqr=blazeqr.terminal:main', # The command-line script to create
        ],
    },
    python_requires=">=3", # The required Python version
)