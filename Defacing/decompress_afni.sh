#!/bin/bash
set -euo pipefail

# Base directory containing the numbered subfolders
BASE_DIR="/path/to/AFNI_DEFACED"

for SUB_DIR in "$BASE_DIR"/*; do
    if [ -d "$SUB_DIR" ]; then
        DIR_NAME=$(basename "$SUB_DIR")
        ZIP_FILE="$SUB_DIR/defaced_images_AFNI${DIR_NAME}.zip"

        if [ -f "$ZIP_FILE" ]; then
            echo "[PROCESSING] Unzipping $ZIP_FILE..."
            unzip -q "$ZIP_FILE" -d "$SUB_DIR/unzipped"

            echo "[RENAMING] Files in $SUB_DIR..."
            mv "$SUB_DIR/unzipped/all_modes_image.deface.nii" "$SUB_DIR/AFNI_DEFACE${DIR_NAME}.nii"
            mv "$SUB_DIR/unzipped/all_modes_image.reface_plus.nii" "$SUB_DIR/AFNI_REFACE_PLUS${DIR_NAME}.nii"
            mv "$SUB_DIR/unzipped/all_modes_image.reface.nii" "$SUB_DIR/AFNI_REFACE${DIR_NAME}.nii"

            echo "[CLEANUP] Removing unneeded files and folders..."
            rm -rf "$SUB_DIR/unzipped"
            rm -f "$ZIP_FILE"

            echo "[DONE] Processed $DIR_NAME"
        else
            echo "[SKIP] No zip file found in $DIR_NAME"
        fi
    fi
done

echo "All processing complete."