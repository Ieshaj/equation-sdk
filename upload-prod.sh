#!/bin/sh

echo "Uploading...."

python3 -m twine upload dist/equation-sdk-1.4.1.tar.gz -r pypi --verbose
