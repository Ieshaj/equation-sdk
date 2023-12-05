#!/bin/sh

echo "Uploading...."

python -m twine upload dist/*1.0.3*.* -r pypi --verbose
