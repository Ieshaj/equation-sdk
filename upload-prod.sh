#!/bin/sh

echo "Uploading...."

python -m twine upload dist/*1.0.6*.* -r pypi --verbose
