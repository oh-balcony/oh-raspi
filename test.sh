#!/usr/bin/env bash

set -e

BASEDIR=$(dirname "$0")

echo "Killing the oh-raspi process."
killall python3 || echo "Could not kill process. Probably was not running."

echo "Starting in testing mode:"
python3 -i "$BASEDIR/test.py"

echo "Starting the oh-raspi process again:"
"$BASEDIR/start.sh"
