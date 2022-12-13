#!/bin/bash
python3 -m venv venv
source venv/bin/activate
apt install python3-pip
pip3 install -r requirements.txt
chmod a+x main.py
./main.py
