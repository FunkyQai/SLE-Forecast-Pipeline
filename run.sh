#!/bin/bash

# Run the application
echo "Running the end-to-end pipeline with the following arguments: $@"
python src/main.py "$@"

