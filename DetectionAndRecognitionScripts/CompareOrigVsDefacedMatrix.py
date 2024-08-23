from deepface import DeepFace
import csv
import os
from multiprocessing import Pool, cpu_count

imagesVerified = 0

# Function to process a single pair of images
def process_pair(args):
    global imagesVerified

    img1_path, img2_path, model_name, detection_backend, metric = args
    result = DeepFace.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend='skip',
        distance_metric=metric
    )

    imagesVerified += 1
    if(imagesVerified % 1000 == 0):
        print(f"{imagesVerified} images verified")
    
    return round(result['distance'], 2)

# Function to create argument list for parrallel processing
def create_args_list(imgs, angleImgs, model_name, detection_backend, metric):
    args_list = []
    for i in range(len(imgs)):
        if(imgs[i] is None):
            continue
        for j in range(len(angleImgs)):
            if (imgs[i] is not None and angleImgs[j] is not None):
                #creates a tuple of the parameters for the verify function
                args_list.append((imgs[i], angleImgs[j], model_name, detection_backend, metric))
    return args_list

# Main script
if __name__ == "__main__":
    backends = [
        'opencv', 
        'ssd', 
        'dlib', 
        'mtcnn', 
        'fastmtcnn',
        'retinaface', 
        'mediapipe',
        'yolov8',
        'yunet',
        'centerface',
        'skip'
    ]

    models = [
        "VGG-Face", 
        "Facenet", 
        "Facenet512", 
        "OpenFace", 
        "DeepFace", 
        "DeepID", 
        "ArcFace", 
        "Dlib", 
        "SFace",
        "GhostFaceNet",
    ]

    metrics = ["cosine", "euclidean", "euclidean_l2"]

    
    TESTIMGCOUNT = 40   #matrix size
    MODELNUMBER = 2   #Change the number to test different models(currently only Dlib, VGG-Face, Facenet512)
    DETECTIONBACKEND = 2   #When using Dlib recognition model use dlib detector when using other recognition models use retinaface
    METRIC = 0   # Only use cosine and euclidean_l2
    STARTIMGINDEX = 105
    DEFACINGALGO = "fsl"

    #URL to the pre-detected images
    BASEDIR = "/Users/avnoorludhar/Desktop/NormalDetectedDlib"
    DEFACEDDIR = "/Users/avnoorludhar/Desktop/fslDetectedViaDlib"
    #matrix of imgs
    imgs = []
    angleImgs = []
    #matrix of img file names for the CSV file
    imgFilesForRow = [""]
    imgFilesForCol = [""]
    #URL to directory with MRI images

    #change this to the last value in the CSVs you are copying from(in google drive)
    currImage = STARTIMGINDEX
    while(len(imgs) < TESTIMGCOUNT and currImage < 300):
        for f in os.listdir(BASEDIR):
            imgNumber = int(f.split('_')[0])

            if(f.endswith(f'_{backends[DETECTIONBACKEND]}.png') and imgNumber == currImage):
                imgPath = os.path.join(BASEDIR, f)
                imgDefacedPath = os.path.join(DEFACEDDIR, f.replace(f'{backends[DETECTIONBACKEND]}', 'd'))

                if(os.path.exists(imgPath) and os.path.exists(imgDefacedPath)):
                    imgs.append(imgPath)
                    imgFilesForRow.append(f"{imgNumber}_n")

                    angleImgs.append(imgDefacedPath)
                    imgFilesForCol.append(f"{imgNumber}_d")
                    break

        currImage += 1

    print("passed building comparision arrays")
    
    # Create argument list for multiprocessing
    args_list = create_args_list(imgs, angleImgs, models[MODELNUMBER], backends[DETECTIONBACKEND], metrics[METRIC])

    with Pool(cpu_count()//2) as pool:
        results = pool.map(process_pair, args_list)

    print("done verifying with deepface")
    # Reshape results from the dictionary(1D list) created to a 2D list
    results_matrix = []
    index = 0
    row = -1
    rowFlag = False
    for i in range(TESTIMGCOUNT):
        #lets us know we need a new row added
        if(imgs[i] is not None):
            row += 1
            rowFlag = True
        
        for j in range(TESTIMGCOUNT):
            if (imgs[i] is not None and angleImgs[j] is not None):
                #states to add a new row if we are looking at the first element
                if(rowFlag):
                    results_matrix.append([results[index]])
                    rowFlag = False
                else:
                    results_matrix[row].append(results[index])

                index += 1

    # Save results to CSV
    file_name = models[MODELNUMBER] + f"_{DEFACINGALGO}Defaced_" + metrics[METRIC]  + ".csv"

    #writes out the data to a csv file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(imgFilesForCol)
        for i in range(len(results_matrix)):
            writer.writerow([imgFilesForRow[i + 1]] + results_matrix[i])
