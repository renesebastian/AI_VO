#!/bin/bash

# Check if file argument is provided
if [ $# -eq 0 ]; then
    echo "❌ Please provide a markdown file from the input directory"
    echo "Usage: ./convert.sh filename.md"
    echo "Example: ./convert.sh test.md"
    exit 1
fi

# Run the Docker command
docker run -it --rm -v "$(pwd):/app" lbl-volabs python app.py "input/$1"