#!/bin/bash

rm -rf env
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd env/lib/python3.5/site-packages/
zip -r9 ../../../../AWS-Lambda-Python.zip *
cd ../../../..

zip -g AWS-Lambda-Python.zip *.py

aws s3 cp AWS-Lambda-Python.zip \
    s3://ly-lambda-tmp
aws lambda update-function-code --function-name ly-dydbtest \
    --s3-bucket ly-lambda-tmp\
    --s3-key AWS-Lambda-Python.zip