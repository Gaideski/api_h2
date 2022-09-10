#!/bin/bash

while true;do
    /usr/bin/supervisord &
    python movies_api/rest_api/app.py
    done