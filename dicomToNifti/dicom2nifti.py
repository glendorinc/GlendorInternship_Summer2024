import os
import subprocess

# Define paths
dicom_dir = '/Users/fied/PycharmProjects/glendor/dicom/1'
output_dir = '/Users/fied/PycharmProjects/glendor/nii'
combined_nifti = os.path.join(output_dir, 'combined_image.nii.gz')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Step 1: Convert DICOM slices into a single NIfTI file
subprocess.run(['dcm2niix', '-o', output_dir, '-f', 'combined_image', dicom_dir], check=True)

# Step 2: Open the combined NIfTI file in FSLeyes with 3D view
subprocess.run(['fsleyes', '--scene', '3d', combined_nifti])