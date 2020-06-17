#/bin/bash

rm -rf ./package
pip3 install --target ./package py-etherscan-api
cd package
zip -r9 ${OLDPWD}/function.zip .
cd ..
zip -g function.zip etherscan_api.py
