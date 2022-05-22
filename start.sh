#!/bin/bash
git pull
gunicorn -w 1 backend:app