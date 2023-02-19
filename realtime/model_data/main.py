from Detector import *
import os

def main():
    videoPath = "Video/walking_people.mp4"

    configPath = os.path.join("model_data", "yolov3_training_last.weights")
    modelPath = os.path.join("model_data", "yolov3_testing.cfg")
    classesPath = os.path.join("model_data","classes.txt")

    detector = Detector(videoPath,configPath,modelPath,classesPath)
    detector.onVideo() 

if __name__ =='__main__':
    main()