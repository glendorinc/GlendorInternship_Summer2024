from deepface import DeepFace
import matplotlib.pyplot as plt

#script for generating the detected images and saving them using matplotlib

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
]

TESTIMGCOUNT = 299
NUMBEROFANGLES = 1
#Make sure to run the script on both retinaface and dlib and put them into 2 different folders with the same parent folder
#Example: detectedImages -> dlib and also detectedImages -> retinaface
DETECTIONBACKEND = 2
DEFACEDFLAG = False
#URL to the CT images
IMGDIR = "/Users/avnoorludhar/Desktop/uwindsor/Glendor/visualizingNiftyFiles/afniRefaceImgs"
OUTPUTDIR = "/Users/avnoorludhar/Desktop/uwindsor/Glendor/testingImages100x100/DetectedImagesFull"

IMGDIR += "/person_"

countOfNonDetectable = 0
imgs = []
for i in range(1, TESTIMGCOUNT + 1):
    for j in range(0, NUMBEROFANGLES):
        imgURL = IMGDIR + str(i) + "_view_" + "frontal" + ".png"
        try:
            currImg = DeepFace.extract_faces(imgURL, detector_backend=backends[DETECTIONBACKEND], expand_percentage=0, align=True)
            if(not DEFACEDFLAG):
                save_path = f"{OUTPUTDIR}/{str(i)}_{backends[DETECTIONBACKEND]}.png"
                plt.imsave(save_path, currImg[0]["face"])
            else:
                save_path = f"{OUTPUTDIR}/{str(i)}_d.png"
                plt.imsave(save_path, currImg[0]["face"])
        except ValueError as ve:
            countOfNonDetectable += 1
            continue
        except Exception as e:
            print(f"Exception message: {str(e)}")

print("Could not detect: " + str(countOfNonDetectable))
