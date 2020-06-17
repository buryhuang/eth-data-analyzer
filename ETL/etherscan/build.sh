#/bin/bash

rm -f ./function.zip
rm -rf ./package
pip3 install --target ./package py-etherscan-api requests boto3
cd package
zip -r9 ${OLDPWD}/function.zip .
cd ..
zip -g function.zip lambda_function.py api_key.json
