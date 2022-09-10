#!/bin/bash

while true;do
    /usr/sbin/sshd -D &
    python movies_api/rest_api/app.py
    done