# Safeguarding Medical Imaging Data: The Efficacy of Defacing Techniques in Preventing Unauthorized Facial Recognition

![image](https://github.com/user-attachments/assets/4b273f19-d28e-4bf4-aa60-da969f952d26)


## Introduction
Radiographic imaging, specifically CT imaging, plays a significant role in detailed images of anatomical structures of the human body. Unfortunately, the digitalization of medical data raises a new concern for privacy, specifically cybercriminals who exploit this medical data. Recently, cybercriminals have been using facial recognition models to identify individuals from visualizations of CT scans, breaching patient privacy.

This study explores the implications with effectively anonymizing CT scan data to protect patients while also maintaining anatomical structure of the data for medical analysis. The objective of our task is to test and implement a series of different facial recognition models, visualization techniques, and defacing algorithms to ensure the face is obstructed, and the medical data is maintained.

In this GitHub repository we will walk you through how to recreate the study step by step. Beginning from downloading the original dataset of dicom images. Converting these dicom images to the NIfTI format, visualizing the NIfTI files with SimpleITK, applying the defacing algorithms to the set of NIfTI files, and then creating a matrix of original versus defaced images.

## Preparing The Data

### Downloading The Data

This step can be skipped and can be done with any set of nifti or dicom images. Just to explain a few definitions, DICOM and NIFTI are both formats to store 3D medical imaging data, so when we are converting between the 2 it is just so we can effectively use technologies later in the study. For our study we downloaded our dicom images from the academic torrents [website](https://academictorrents.com/details/d06aafd957f0c8c9b0eb4636e5c3ebdb7bdaf54f/tech&filelist=1). From this dataset we converted the images from dicom to nifti to apply visualization and defacing. 

>**IMPORTANT NOTE**: A torrent is required to download from the site above, popular torrents include [uTorrent](https://www.utorrent.com/), and [BitTorrent](https://www.bittorrent.com/).

### Converting From DICOM to NIfTI Format

Everything from this point onwards will require users to follow each step with precision. Next we will convert any DICOM medical imaging data to the NIFTI format 

The library used to convert DICOM files to NIfTI format is called `dicom2nifti`, [Click here](https://pypi.org/project/dicom2nifti/) to learn more.

This is crucial for any next steps. All defacers used require our DICOM dataset (which contain slices) be combined into one file, then converted to NIfTI format. Located in the `dicomToNifti` folder there will be a python script named `dicom2nii.py` You will need to edit your base directory to the parent folder containing all the dicom files. 

The organization scheme must remain the same, with the parent folder containing folders labelled 1-299 in consecutive order, with each folder containing the series of DICOM files for each identity. You will also be required to change your output directory to where you want the files to be stored. Once these are defined, you may run the script.

## Visualizing Original Images

1. Ensure all your medical imaging data is in the NIfTI format.
2. Use either the visualizationOfNifti.py or visualizationNiftiZoom.py python scripts to visualize the dataset to a 2D representation. The difference between these scripts is that the visualizationNiftiZoom.py will only give a front angle and will zoom in on the image. While the visualizationNiftiZoom.py's line 76 angles array can be changed to get different angles of the face. Ensure all dependencies listed are installed using pip.
3. To use either script you must change all constants in the __main__ block in the code. This will be the entry point to the script and the code will run sequentially from this point. These constants include the BASEDIR constant which will be the base directory to your project on your computer, then the SUBFOLDERDIRECTORY will be the folder that contains your NIfTI files. OUTPUTDIR represents the directory you want to output to relative to your BASEDIR. Finally, change the STARTINDEX and ENDINDEX constants to the range of NIfTI files you would like to visualize. 

> **IMPORTANT NOTE:** ensure within your subfolder you do not directly place the NIfTI files into the subfolder. Ensure it is in the form SUBFOLDERDIRECTORY/i/nifti.nii where i takes on values from STARTINDEX to ENDINDEX.

Now you should have a folder of PNG images in the form "person_{person_id}_view_frontal.png" example images can be seen in the OriginalNiftiPNGImages folder these were created by the visualizationNiftiZoom.py file.


## Defacing NIfTI Files
### FSL Deface
1. Download and install the [FSL software](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index)
2. Download the `deface_allfsl.sh` bash script
3. Edit the script with the path to the SUBFOLDERDIRECTORY with all the sub-directoreis numbered
4. Execute the `deface_allfsl.sh` script
5. The original NIfTI file should now be replaced with the defaced NIfTI file with file name format defaced_imagei.nii
### AFNI Deface/Reface/Reface Plus
1. Download the [AFNI software](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/) (check to make sure @afni_refacer_run file is downloaded)
2. Download the `deface_allafni.sh` script
3. Edit the script with the path to the SUBFOLDERDIRECTORY with all the numbered subfolder
4. Execute the `deface_allafni.sh` script
5. The original NIfTI file should now be replaced with a zip file, within the zip files is three NIfTI files for deface, reface, and reface plus
   (This is done due to the excessive storage the folder would take if it contained the the three NIfTI files instead of the zip file)
6. To unzip all the zip files and have the three NIfTI's in each subfolder:
        Download `decompress_afni.sh` script
        Edit the script with the path to the SUBFOLDERDIRECTORY with all the sub-directoreis numbered
        Execute `decompress_afni.sh`
7. You should now have 3 NIfTI files in each numbered subfolder

### Pydeface
1. Head over to [PyDeface](https://pypi.org/project/pydeface/) and install the necessary dependencies. These include the `FSL Package`, `Python 3` version, `NumPy`, `NiBabel`, and `Nipype`.
2. Ensure the `PyDeface package` is installed by running the following command.
   ```
    pip install pydeface
   ```
3. Once installed, edit the `pydeface.py` script defined in the `defacing` folder. Specifically edit the `base_dir` variable. You must make this the base directory which contains all the numbered folders.
4. Run the script `pydeface.py` once you edit the `base_dir` variable. It is important to note this process may take a while, and it is completely normal.
5. The defaced files will be outputted into the folder of each corrosponding identity. For example, if person 45 was defaced, defaced_image45 will be saved in folder 45 along side the combined_image45.

## Voxel Replacement For Defaced Images
Defacing algorithms work in a clever way by replacing specific voxels (3D pixels) with a value that supposedly represents black in 3D space. However, we notices these voxels didn't actually fade into the background and created a mask around the entire head and image. We will now be removing this mask by removing unneccessary voxels added by these algorithms. 

1. Open up the VoxelReplacement folder and download the cleanDefacedFile.py python script and install required depenencies using pip.
2. Ensure you change all the constants in this file. BASEDIR should be changed to your BASEDIR of the project. The SUBFOLDERDIR should be the folder that contains all the defaced NIfTI files in the form SUBFOLDERDIR/i/nifti.nii where i represents the number of the patient and uniquely identifies that NIfTI file. Change DEFACINGALGORITHM to the algorithm you are attempting to clean.
3. On line 21 the remove_voxels_in_range has a lower and upper bound property for the voxels we want to remove. Ensure you change these constants dependant on the algorithm and the comments above the function. If you leave it the results may be skewed. 

> **IMPORTANT NOTE:** We have defaulted to using the reface files for afni, but if you would like to try the defaced or the Reface Plus files instead you can go to line 43 of `cleanDefacedFile.py` and change the file name to `AFNI_DEFACE{i}.nii` for deface or `AFNI_REFACE_PLUS{i}.nii` for reface plus.

## Visualization Of Defaced Images
1. Ensure all your medical imaging data is in the NIfTI format.
2. Use the visualizationNiftiZoom.py python script to visualize the dataset to a 2D representation. The difference between the two scripts found in the Visualization scripts is that the visualizationNiftiZoom.py will only give a front angle and will zoom in on the image. While the visualizationNiftiZoom.py's line 76 angles array can be changed to get different angles of the face. The visualizationNiftiZoom script requires more changes in future files. If you would like to do the study from many angles ensure code is changed at all needed steps.
3. Install required depenencies using pip.
4. To use either script you must change all constants in the __main__ block in the code. This will be the entry point to the script and the code will run sequentially from this point. These constants include the BASEDIR constant which will be the base directory to your project on your computer, then the SUBFOLDERDIRECTORY will be the folder that contains your defaced NIfTI files. OUTPUTDIR represents the directory you want to output to relative to your BASEDIR ensure this is different from your original NIfTI images. Finally, change the STARTINDEX and ENDINDEX constants to the range of NIfTI files you would like to visualize. 

> **IMPORTANT NOTE:** ensure within your subfolder you do not directly place the NIfTI files into the subfolder. Ensure it is in the form SUBFOLDERDIRECTORY/i/nifti.nii where i takes on values from STARTINDEX to ENDINDEX.

Now you should have a folder of PNG images in the form "person_{person_id}_view_frontal.png" example images can be seen in the DefacedNiftiPNG folder these were created by the visualizationNiftiZoom.py file. If you take a look at the example images, many of these are incorrectly defaced or not defaced at all, keep these cases in the mind for future tests.

## Pre-detection of Images
The face recognition pipeline consists of detection, alignment, recognition and distance metrics. Each step has it's own infrasture for the case of detection we have detection algorithms to detect where a face is in an image and pass that into the recogntiion model. For our research we used the Dlib and RetinaFace detectors and had preprocessed the images so we were only required to do the detection step one time. This saves a lot of time with computation during the facial recognition task.

1. Download the FacialDetectionScript.py and install required depenencies using pip.
2. Update the constants in the file including the IMGDIR which should be the absolute file path to the folder which contains the images you are trying to detect.
3. NUMBEROFANGLES represents the number of angles for which you had visualized. If the visualizationOfNifti.py script was used ensure the consant is changed and then ensure that line 34 is changed to the filename corresponding to the saved files in the directory after visualization.
4. Update the TESTIMGCOUNT to the number of images you would like to detect.
5. Update the OUTPUTDIR to the directory you would like to save the images to.
6. Update the DETECTIONBACKEND constant to the detector you would like to use for our study we used the values 2 which corresponds to the dlib detector and 5 which corresponds to the retinaface detector. 
7. Update DEFACEDFLAG constant to True if you are detecting defaced images and False if you are detecting undefaced CT images.
8. Run the script.

After running the script make sure to put the files for a specific detector and defacing algorithms into their own respective folders in the OUTPUTDIR before running a new test. This will mitigate overriding previously detected images. Examples of detected images will be located in the DetectedImages folder.

## Sanitizing Dataset

As we mentioned earlier many of the defaced images you will notice go undetected and/or will be incorrectly defaced. These include pydeface removing the entire head, FSL deface missing the head and leaving it completely undefaced, and other similar occurrances. These cases need to be weeded out for the testing data set, you will be required to sift through and remove these bad cases. This will ensure that the test only evaluates how well the recognition models perform not the defacing algorithms

## Matrix Construction Normal Versus Defaced 30%

Now that we have a datasets of defaced images and the original dataset of the normal images. We will now create a distance matrix of the comparison of each normal image with each defaced image. This will allow us to determine the optimal threshold and determine the accuracy of the model with statistical measures.

1. Download the CompareOrigVsDefacedMatrix.py file in the DetectionAndRecognitionScripts folder and install required depenencies using pip.
2. Update the TESTIMGCOUNT constant which represents the number of images you would like to do the test with. For the first few tests make sure this value is 70% of the defaced dataset. So if we were using FSL deface ensure that TESTIMGCOUNT is set to 0.7 * Number of images in the folder.
3. Update the MODELNUMBER constant to the number of the model that you want to run the test for. In our study we did this with VGG-Face(0), Facenet-512d(2), and Dlib(7).
4. Ensure the DETECTIONBACKEND constant is set to the detector you used for the test this is due to the filename being named based on what detector used. This is used to automate the creation of the distance matrix.
5. Update METRIC to the desired metric of your choice. For our test we had used the cosine singularity metric(0) for the VGG-Face and Facenet-512d. We then used euclidean_l2 for the Dlib recognition model. 
6. Ensure the STARTIMGINDEX is set to 1 for this round of computations. 
7. Update the DEFACINGALGO constant to the name of the currently used defacing algorithm. This will be used for naming the output file.
8. Ensure that the BASEDIR is the absolute path to the folder that contains the detected normal images.
9. Ensure that the DEFACEDDIR is the absolute path to the folder that contaisn the detected defaced images for that defacing algorithm. **NOTE: the detector for both of these datasets should be the same**
10. Run the script, and wait for the results. The script will take a long time so keep your laptop running.

After this script you should have a CSV representing all the different combinations of the normal images versus the defaced images. This matrix also ensures that all matches are on the main diagonal of the CSV file and all other cells are non-matches.

## Finding The Optimal Threshold

In this step we will take out CSV which was computed and find an optimal threshold for this configuration. 

1. Download the ROC+PRC.py file in the FindingResultsAndThreshold folder and install the required dependencies with pip.
2. Update METRIC to the metrics listed in the CompareOrigVsDefacedMatrix.py file. This will be cosine for Facenet512 and VGG-Face. It will be euclidean_l2 for the Dlib recognition model.
3. Update the CSVNAME to the name of the CSV you are analyzing, exclude the extension since that is added automatically by the program.
4. Update the CSVPATH to the absolute path of where the CSV file will be stored.
5. Update OUTPUT_FOLDER to the location you would like to save the image outputted by the script.
6. Run the script and view the results in the output folder you specified. An example graph is provided in the path ResultGraphAndTable -> 

After this step we will now have an optimal threshold computed using a ROC curve (top left of the image) a PRC curve (top right of the image). And a table displaying thresholds near the optimal threshold. For our study we use the optimal threshold found by the PRC curve to determine the efficacy of the model. We also use the AU-PRC (area under precision recall curve) as a metric to judge efficacy. 

## Matrix Construction Normal Versus Defaced 30%

We want to see if our results generalized once we have picked an optimal threshold. In this computation we will use the rest of the data set the last 30% which wasn't used to determine the models efficacy at this optimal threshold.

1. Download the CompareOrigVsDefacedMatrix.py file in the DetectionAndRecognitionScripts folder and install required depenencies using pip.
2. Update the TESTIMGCOUNT constant which represents the number of images you would like to do the test with. For these tests make sure this value is 30% of the defaced dataset. So if we were using FSL deface ensure that TESTIMGCOUNT is set to 0.3 * Number of images in the folder.
3. Update the MODELNUMBER constant to the number of the model that you want to run the test for. In our study we did this with VGG-Face(0), Facenet-512d(2), and Dlib(7).
4. Ensure the DETECTIONBACKEND constant is set to the detector you used for the test this is due to the filename being named based on what detector used. This is used to automate the creation of the distance matrix.
5. Update METRIC to the desired metric of your choice. For our test we had used the cosine singularity metric(0) for the VGG-Face and Facenet-512d. We then used euclidean_l2 for the Dlib recognition model. 
6. Ensure the STARTIMGINDEX is set to the last image used in the original matrix with this configuration. This means that if you used the Dlib model, pydeface, and cosine. We would look in the matrix that had those specifications and check the patient number in the last row or column and add one to it. This will become the new STARTIMGINDEX. An example CSV can be found in the CSVToFindStart folder, for this CSV the new testing matrix will start at 156 since the last row in that CSV is 155.
7. Update the DEFACINGALGO constant to the name of the currently used defacing algorithm. This will be used for naming the output file.
8. Ensure that the BASEDIR is the absolute path to the folder that contains the detected normal images.
9. Ensure that the DEFACEDDIR is the absolute path to the folder that contaisn the detected defaced images for that defacing algorithm. **NOTE: the detector for both of these datasets should be the same**
10. Run the script, and wait for the results. The script will take a long time so keep your laptop running.

Now we will have a CSV that will be used to determine the final result.

## Create Table of Results

We will now make a table of all the results for each of the configurations. 

1. Download the GeneralizePRC.py file in the FindintResultsAndThreshold folder and install the required dependencies.
2. Update the thresholds dictionary to contain the name of each csv and the resultant optimal threshold which was found in the PRC graph from the finding optimal threshold step. This can be automated by passing in the images into ChatGPT and asking for a dictionary of the filename and the threshold from the PRC curve.
3. Update the CSVPATH to the folder that contains all the CSV that were built using 30% of the data set. Ensure all of the CSV names from the dictionary match the CSVs in the folder. 
4. Update the OUTPUT_FOLDER to the path to the folder you would like your results to be stored in.
5. Run the script and view your results in the desired folder. 

The script outputs a table of results which contains the number of true positives, false positives, and false negatives that the specific test had using the optimal threshold. True positives represent the number of people that were correctly identifies, false positives represent all the non-matches that were considered matches, and finally false negatives represent the matches that the model classified as non-matches. An example of this can be viewed by opening the ResultGraphAndTable folder and opening the nested ResultTable folder.

## Conclusion