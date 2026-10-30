#!/bin/bash

cd "/mnt/c/retail-data engineeering-pipeline" || exit 1

source "$HOME/venvs/retail-pipeline/bin/activate"

python SRC/load_data.py

if [ $? -ne 0 ]; then
    echo "Pipeline failed. Check logs/pipeline.log"
    exit 1
fi

echo "Pipeline completed successfully."
