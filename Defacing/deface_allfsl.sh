#!/bin/bash

# Base directory containing the subdirectories with NIfTI files
BASE_DIR="/path/to/NII/dataset"

# Iterate through each subdirectory numbered from 1 to 297
for i in $(seq 1 298); do
  # Construct the path to the subdirectory
  folder_path="$BASE_DIR/$i"
  
  # Check if the folder exists
  if [ -d "$folder_path" ]; then
    # Check for the presence of the defaced file
    defaced_file="$folder_path/defaced_image${i}.nii"
    
    # If the defaced file does not exist, deface the original file
    if [ ! -f "$defaced_file" ]; then
      # Construct the path to the original file
      original_file="$folder_path/combined_image${i}.nii"
      
      # Check if the original file exists
      if [ -f "$original_file" ]; then
        # Define the output file for the defaced image
        defaced_output_file="$folder_path/defaced_image${i}.nii"
        
        # Run the defacing command (replace with your actual defacing command)
        echo "Defacing $original_file..."
        fsl_deface "$original_file" "$defaced_output_file"
        
        # Check if the defacing command was successful
        gz_file="$folder_path/defaced_image${i}.nii.gz"
        if [ $? -eq 0 ]; then
          echo "Successfully defaced $original_file and saved to $defaced_output_file"
          if [ -f "$gz_file" ]; then
          # Decompress the .nii.gz file
            gunzip "$gz_file"
            echo "Decompressed: $gz_file"
            rm "$gz_file"
            echo "Deleted: $gz_file"
          else
            echo "File not found: $gz_file"
          fi
   	      if [ -f "$original_file" ]; then
   	        rm "$original_file"
    	      echo "Deleted: $original_file"
   	      else
     	      echo "File not found: $original_file"
   	      fi
        else
          echo "Failed to deface $original_file"
        fi
      else
        echo "Original file not found: $original_file"
      fi
    else
      echo "Defaced file already exists: $defaced_file"
    fi
  else
    echo "Directory does not exist: $folder_path"
  fi
done
