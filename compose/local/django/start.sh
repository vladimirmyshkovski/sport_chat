#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


python manage.py migrate
python manage.py runserver 0.0.0.0:8000 #runserver_plus 0.0.0.0:8000
