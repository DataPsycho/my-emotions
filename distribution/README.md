# Package Distribution
This directory includes the distribution files for the recently build ml 
pipeline. The package can be installed in any server or micro systems to get
predictions manually when not using the provide api service.

Steps to build the `.whl` file:
- Clone the repo
- `cd` to distribution
- run `python setup.py bdist_wheel`
- a distribution wheel file will be generated in the dist directory
- `cd` to dist and 
- install the package by `pip install myemotion-0.0.1-py3-none-any.whl`