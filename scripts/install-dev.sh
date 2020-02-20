#!/bin/bash
# This script will setup a development copy of 911maps in the current directory.
git clone https://github.com/gavinrozzi/911maps
cd 911maps
virtualenv env
source env/bin/activate
pip3 install -r nineoneonemaps/requirements.txt
cd nineoneonemaps
./manage.py createsuperuser
./manage.py migrate