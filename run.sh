#!/bin/bash
cd /${WebRoot}/
gunicorn -w 4 -b 0.0.0.0:8000 run:app 

