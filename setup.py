# Import the setuptools module
import setuptools

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup parameters for the package
setuptools.setup(
    name='blazeqr',
    version='0.0.1',
    keywords='qr qrcode blazing artistic animated gif colorized',
    description='Generator for blazing QR Codes. Including Common, Artistic and Animated QR Codes.', # A short description of the package
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='SirMghSBD', 
    author_email='sirmghsbd@gmail.com',
    url='https://github.com/sirmghsbd/blaze',
    download_url='https://github.com/sirmghsbd/blaze',
    project_urls={
        "Bug Tracker": "https://github.com/sirmghsbd/blaze/issues",
    },
    install_requires=[
        'imageio >= 2.28.1',
        'numpy >= 1.24.3',
        'Pillow>=9.5.0' 
    ],
    packages=['blazeqr', 'blazeqr.qrlibs'],
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS', 
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    entry_points={
        'console_scripts': [
            'blazeqr=blazeqr.terminal:main',
        ],
    },
    python_requires=">=3",
)