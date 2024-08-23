#!/bin/bash
set -euo pipefail

BASE_DIR="/path/to/NII/dataset"

process_directory() {
    SUB_DIR="$1"
    DIR_NAME=$(basename "$SUB_DIR")
    echo "[START] Processing $DIR_NAME"
    
    INPUT_FILE="$SUB_DIR/combined_image${DIR_NAME}.nii"

    if [ ! -f "$INPUT_FILE" ]; then
        INPUT_FILE=$(find "$SUB_DIR" -maxdepth 1 -name "combined_image*.nii" -print -quit)
        if [ -z "$INPUT_FILE" ]; then
            echo "[SKIP] No non-defaced file found in $DIR_NAME"
            return 0
        fi
    fi

    if ! @afni_refacer_run -input "$INPUT_FILE" -mode_all -prefix "$SUB_DIR/all_modes_image" > /dev/null 2>&1; then
        echo "[ERROR] Defacing process failed for $DIR_NAME"
        return 1
    fi

    rm -f "$SUB_DIR/all_modes_image.face_plus.nii.gz"
    rm -f "$SUB_DIR/all_modes_image.face.nii.gz"
    rm -rf "$SUB_DIR/all_modes_image_QC"
    rm -f "$INPUT_FILE"

    find "$SUB_DIR" -name "*.gz" -type f -exec gunzip {} + > /dev/null 2>&1

    OUTPUT_ZIP="$SUB_DIR/defaced_images_AFNI${DIR_NAME}.zip"
    if ! zip -j "$OUTPUT_ZIP" "$SUB_DIR"/*.nii > /dev/null 2>&1; then
        echo "[ERROR] Zipping process failed for $DIR_NAME"
        return 1
    fi

    rm -f "$SUB_DIR"/*.nii
    echo "[DONE] Processed $DIR_NAME"
    return 0
}

export -f process_directory

DIRS=$(find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d -exec sh -c 'find "$0" -maxdepth 1 -name "*.nii" -print -quit | grep -q .' {} \; -print)

echo "Number of directories to process: $(echo "$DIRS" | wc -l)"

echo "Starting parallel processing..."
echo "$DIRS" | parallel --will-cite --jobs 8 --line-buffer --joblog parallel_job.log process_directory

echo "All processing complete."
