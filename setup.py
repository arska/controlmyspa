"""
controlmyspa python module manifest
"""
from os.path import abspath, dirname, join
from setuptools import setup


def read_file(filename):
    """Get the contents of a file"""
    here = abspath(dirname(__file__))
    with open(join(here, filename), encoding="utf-8") as file:
        return file.read()


setup(
    name="controlmyspa",
    version_config={"dirty_template": "{tag}"},
    description="Get metrics and control Balboa Controlmyspa whirlpool",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=["controlmyspa"],
    package_dir={"controlmyspa": "."},
    keywords=["Balboa", "Controlmyspa", "Whirlpool", "API"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/arska/controlmyspa",
    author="Aarno Aukia",
    author_email="aarno@aukia.com",
    license="MIT",
    python_requires=">=3.5",
    extras_require={"dev": ["tox"]},
    install_requires=["requests>=2"],
    setup_requires=["setuptools-git-versioning"],
)
