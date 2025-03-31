#!/bin/bash
if ! command -v python3 &> /dev/null
then
    echo "Python3 not installed. Try again"
    exit 1
fi

# Rulează main.py
python3 main.py
