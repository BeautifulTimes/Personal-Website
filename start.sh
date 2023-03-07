#!/bin/bash

gunicorn -w 1 backend:app