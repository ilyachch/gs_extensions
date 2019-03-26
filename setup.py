import setuptools


def get_version():
    with open("VERSION", "r") as fh:
        version = fh.read()
    return version


def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setuptools.setup(
    # Common data
    name="gs_extensions",
    version=get_version(),
    author="Ilya Chichak",
    author_email="ilyachch@gmail.com",
    description="CLI tool to manage gnome shell extensions",
    # Meta
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/ilyachch/gs_extensions",
    # Technical data
    python_requires=">=3.4",
    packages=setuptools.find_packages(exclude=['tests*', ]),
    install_requires=[
        "requests",
    ],
    extras_require={
        'dev': [
            'twine',
            'wheel',
            'setuptools',
            'bumpversion',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
    entry_points={
        'console_scripts': ['gs_extensions=gs_extensions.app:main'],
    }
)
