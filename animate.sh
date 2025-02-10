#!/bin/bash

# Animation Script for Running shader2png_a.py

# Check if correct arguments are passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <GLSL_FILE> <RESOLUTION> <TOTAL_FRAMES>"
    echo "Example: $0 mega.glsl 3840x2160 100"
    exit 1
fi

# Arguments
GLSL_FILE="$1"          # GLSL file to use
RESOLUTION="$2"         # Resolution (e.g., 3840x2160)
TOTAL_FRAMES="$3"       # Total number of frames to render

# Check if the GLSL file exists
if [ ! -f "$GLSL_FILE" ]; then
    echo "Error: File '$GLSL_FILE' not found!"
    exit 1
fi

# Loop to generate frames
for FRAME_NUM in $(seq 1 $TOTAL_FRAMES); do
    echo "Rendering frame $FRAME_NUM of $TOTAL_FRAMES..."
    python3 shader2png_a.py "$RESOLUTION" "$GLSL_FILE" "$FRAME_NUM"

    # Check if the Python script failed
    if [ $? -ne 0 ]; then
        echo "Error: Frame $FRAME_NUM failed to render. Exiting."
        exit 1
    fi
done

echo "All $TOTAL_FRAMES frames rendered successfully."
