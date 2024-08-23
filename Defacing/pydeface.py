import os
import subprocess

# Define the base directory containing the numbered folders
base_dir = '/Users/fied/PycharmProjects/glendor/nii/thi'

def deface_nifti(nifti_file, defaced_output_file):
    # Set up FSL environment variables
    env = os.environ.copy()
    env['FSLDIR'] = '/Users/fied/fsl'
    env['PATH'] = f"{env['FSLDIR']}/bin:{env['PATH']}"
    env['FSLOUTPUTTYPE'] = 'NIFTI_GZ'

    # Deface the NIfTI image
    cmd = ['pydeface', nifti_file, '--out', defaced_output_file]
    subprocess.run(cmd, check=True, env=env)

def process_folders(base_dir, start=1, end=298):
    for i in range(start, end + 1):
        folder_path = os.path.join(base_dir, str(i))
        nifti_file = os.path.join(folder_path, f'combined_image{i}.nii')
        defaced_file = os.path.join(folder_path, f'defaced_image{i}.nii')

        if os.path.isfile(nifti_file):
            try:
                print(f"Defacing {nifti_file}...")
                deface_nifti(nifti_file, defaced_file)
                print(f"Defaced image saved to {defaced_file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to deface {nifti_file}: {e}")
        else:
            print(f"File {nifti_file} does not exist")

if __name__ == "__main__":
    process_folders(base_dir)