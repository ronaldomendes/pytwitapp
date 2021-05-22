#!/usr/bin/env sh

#Login API
pip install -r requirements.txt
cd ./LoginAPI
python run.py &
cd ..
python run.py