#!/bin/bash

cd ../blog && git pull origin master
cd ../gblog && .env/bin/python update.py
