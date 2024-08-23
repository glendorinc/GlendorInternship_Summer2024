import nibabel as nib
import numpy as np
import os

'''
script to clean defaced files by clearing the voxels that are added by the defacing algorithms
'''
def load_nifti_file(file_path):
    image = nib.load(file_path)
    return image

def save_nifti_file(image, data, output_path):
    new_img = nib.Nifti1Image(data, image.affine, image.header)
    nib.save(new_img, output_path)

'''
pydeface: change lower_bound=-3 and upper_bound=3
fslDeface: change both lower and upper bound to 0 or define larger range around 0 if any errors are encountered
afniReface: choose lower_bound = -1 and upper_bound = 1 if you want a tighter range can extend if any errors occur
'''
def remove_voxels_in_range(image, lower_bound=-3, upper_bound=3):
    data = image.get_fdata()
    background_value = np.min(data)
    # Replace all intensities within the range with the background value
    mask = (data >= lower_bound) & (data <= upper_bound)
    data[mask] = background_value
    
    return data

def process_nifti_file(file_path, output_path):
    image = load_nifti_file(file_path)
    cleaned_data = remove_voxels_in_range(image)
    save_nifti_file(image, cleaned_data, output_path)

if __name__ == "__main__":
    STARTINDEX = 150
    ENDINDEX = 300
    DEFACINGALGORITHM = 'pydeface'
    BASEDIR = f'/Users/avnoorludhar/Desktop/uwindsor/Glendor/visualizingNiftyFiles'
    SUBFOLDERDIR = "pydeface"
    for i in range(STARTINDEX, ENDINDEX):
        #change to path of the original niftis 
        input_file = f'{BASEDIR}/{SUBFOLDERDIR}/{i}/defaced_image{i}.nii'
        #output folder path {i} represents the niftis in the folder labelled (1-300)
        output_file = f'{BASEDIR}/pyDefaceCleaned/{i}'

        if not os.path.exists(output_file):
            os.makedirs(output_file)
            output_file = os.path.join(output_file, f"combined_image_{DEFACINGALGORITHM}{i}.nii")

        process_nifti_file(input_file, output_file)
