#!/bin/bash

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Create source distribution
python setup.py sdist bdist_wheel

# Output created files
echo "Created distribution files:"
ls -l dist/

echo "To install the package, run:"
echo "pip install dist/*.whl"
