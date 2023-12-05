#!/bin/sh

echo "Uploading...."

python -m twine upload dist/*1.0.5*.* -r pypi --verbose
