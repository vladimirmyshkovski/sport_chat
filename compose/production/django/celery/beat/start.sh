#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A sport_chat.taskapp beat -l INFO
