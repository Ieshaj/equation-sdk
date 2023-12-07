#!/bin/sh

echo "Uploading...."

python -m twine upload dist/*1.0.7*.* -r pypi --verbose
