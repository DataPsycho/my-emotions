from setuptools import setup, find_packages
from modelboy.pkg_version import __version__

setup(
    name="myemotion",
    packages=find_packages(),
    description="Light weight ml model pipeline for Text Scoring",
    long_description=open("README.md").read(),
    author="data psycho",
    author_email="mr.data.psycho@gmail.com",
    version=__version__,
    license="MIT open source",
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy",
        "spacy",
        "joblib"
    ],
    dependency_links=[],
    platforms=["any"],
    zip_safe=False
)

