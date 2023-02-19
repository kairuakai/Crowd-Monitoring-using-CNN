# import cv2
# import numpy as np
# import time

# net = cv2.dnn.readNet('yolov4-tiny-custom_last.weights', 'yolov4-tiny-custom.cfg')
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
# # net = cv2.dnn_DetectionModel('yolov3_training_last.weights', 'yolov3_testing.cfg')
# pTime = 0
# incount = 0
# total_incount = 0

# classes = []
# with open("obj.names", "r") as f:
#     classes = f.read().splitlines()

# # Real time camera and video
# # cap = cv2.VideoCapture(0)
# # cap = cv2.VideoCapture("rtsp://admin:Coronel_123456@192.168.1.64:554/Streaming/Channels/101")
# cap = cv2.VideoCapture('Video/walking_people.mp4')
# font = cv2.FONT_HERSHEY_PLAIN
# colors = np.random.uniform(0, 255, size=(100, 3))

# codec = cv2.VideoWriter_fourcc(*'XVID')
# vid_fps =int(cap.get(cv2.CAP_PROP_FPS))
# vid_width,vid_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# out = cv2.VideoWriter('Video/results.avi', codec, vid_fps, (vid_width, vid_height))



# def findObject(layerOutputs,img):
#     heightTar,weightTar,channelsTar = img.shape
#     bbox = []
#     classId = []
#     confidences = []
#     count1 = 0

#     for output in layerOutputs:
#         for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.2:
#                 center_x = int(detection[0]*weightTar)
#                 center_y = int(detection[1]*heightTar)
#                 w = int(detection[2]*weightTar)
#                 h = int(detection[3]*heightTar)

#                 x = int(center_x - w/2)
#                 y = int(center_y - h/2)

#                 bbox.append([x, y, w, h])
#                 confidences.append((float(confidence)))
#                 classId.append(class_id)
#                 if(int(img.shape[0]/2)-3) < y < (int(img.shape[0]/2)+3):
#                     if classes == 2:
#                         count1 = count1 + 1
#                 else: 
#                     continue
#     indexes = cv2.dnn.NMSBoxes(bbox, confidences, 0.2, 0.4)
#     for i in indexes:
#             i = i[0]
#             box = bbox[i]
#             x, y, w, h = box[0],box[1],box[2],box[3]
#             label = str(classes[classId[i]])
#             confidence = str(round(confidences[i],2))
#             # color = colors[i]
#             cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)
#             cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)

#             cv2.line(img,(0,int(img.shape[0]/2)+3),(int(img.shape[1]), int(img.shape[0]/2)+3),(0,0,100),5)
#             cv2.line(img,(0,int(img.shape[0]/2)-3),(int(img.shape[1]), int(img.shape[0]/2)-3),(0,0,100),5)

#             return count1

               
# while True:
#     _, img = cap.read()

#     blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0,0,0), swapRB=True, crop=False)
#     net.setInput(blob)
#     LayerNames = net.getLayerNames()

#     output_layers_names = [LayerNames[i[0]-1] for i in net.getUnconnectedOutLayersNames()]
#     layerOutputs = net.forward(output_layers_names)

#     counter1 = findObject(layerOutputs,img)

#     incount = incount + counter1
#     total_incount = total_incount + incount

#     cTime = time.time()
#     fps = 1 / (cTime-pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3, (0,255,0),2)
#     cv2.putText(img, f'People: {incount}', (20,100), cv2.FONT_HERSHEY_PLAIN,3, (0,255,0),2)
#     cv2.putText(img, f'Total: {total_incount}', (20,150), cv2.FONT_HERSHEY_PLAIN,3, (0,255,0),2)

#     cv2.imshow('Image', img)
#     out.write(img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     # key = cv2.waitKey(1)
#     # if key==27:
#     #     break

# cap.release()
# out.release()
# cv2.destroyAllWindows()
































# Original Code

import cv2
from tracker import *
import numpy as np
import time
from time import ctime
import datetime
import os
import csv


# Position
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)


# Saving Video
def getAviNameWithDate(nameIn="output.avi"):
    """Needs a file ending on .avi, inserts _<date> before .avi. 

    If file exists, it appends a additional _number after the <date> 
    ensuring filename uniqueness at this time."""
    if not nameIn.endswith(".avi"):
        raise ValueError("filename must end on .avi")

    filename = nameIn.replace(".avi","_{0}.avi").format(datetime.datetime.now().strftime("%m-%d-%Y"))

    if os.path.isfile(filename):             # if already exists
        fn2 = filename[0]+'_{0}.avi'          # modify pattern to include a number
        count = 1
        while os.path.isfile(fn2.format(count)): # increase number until file not exists
            count += 1
        return fn2.format(count)                 # return file with number in it

    else:                                    # filename ok, return it
        return filename

net = cv2.dnn.readNet('yolov4-tiny-custom_last.weights', 'yolov4-tiny-custom.cfg')
# net = cv2.dnn_DetectionModel('yolov3_training_last.weights', 'yolov3_testing.cfg')
pTime = 0
count = 0

filename = 'output_{0}.avi'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# Tracking object
tracker = Tracker()
list = []

classes = []
with open("obj.names", "r") as f:
    classes = f.read().splitlines()

# Real time camera and video
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("rtsp://admin:Coronel_123456@192.168.1.64:554/Streaming/Channels/101")
# cap = cv2.VideoCapture('Video/walking_people.mp4')
# cap = cv2.VideoCapture('Video/person_Trim.mp4')
cap = cv2.VideoCapture('Video/walking_Trim.mp4')
# cap = cv2.VideoCapture('Video/cctv.1.avi')
# cap = cv2.VideoCapture('Video/person.mp4')
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

codec = cv2.VideoWriter_fourcc(*'XVID')
vid_fps =int(cap.get(cv2.CAP_PROP_FPS))
vid_width,vid_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# out = cv2.VideoWriter(f'Video/{filename}', codec, vid_fps, (vid_width, vid_height))
out = cv2.VideoWriter(f'Video/record_vid/{getAviNameWithDate("output.avi")}', codec, vid_fps, (vid_width, vid_height))


while True:
    _, img = cap.read()
    height, width, _ = img.shape

    # Convert grayscale
    blur = cv2.blur(img,(3,3))
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    # End of Convert grayscale

    blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    # cv2.line(img,(0,int(img.shape[0]/2)+3),(int(img.shape[1]), int(img.shape[0]/2)+3),(0,0,100),5)
    cv2.line(img,(0,height-400),(width,height-400),(0,128,0),2)

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)



    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]

            person = int(y+h/2)
            lineCy = height-350
            # lineCy = 3*height/6+height/30

            # if(person<lineCy+3 and person>lineCy-3):
            #     count = count + 1

            if(person<lineCy+3 and person>lineCy-3):
                count = count + 1
                print(count)
                print(ctime())
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)

                with open("Database/info.csv", mode="a") as csvfile:
                    tup1 = (count,current_time)
                    tup2 = (ctime())
                    
                    writer = csv.writer(csvfile,delimiter='\t')
                    writer.writerows(str(tup1))
                    # writer.writerows(str(tup2))
                
                if count == 5:
                    print("Warning")
                
            list.append([x,y,w,h])
            id_boxes = tracker.update(list)
            # print("Person Id", id_boxes)
            # print("Class Id ",class_id)
            # print("Confidence: ", confidence, "Xmin: ",x, "Ymin: ",y, "Xmax",w, "Ymax", h)
            # cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)
            cv2.putText(img, label + " " + confidence, (x, y-15), font, 1.2, (255,255,255), 2)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3, (0,255,0),2)
    cv2.putText(img,f'People: {str(count)}', (20,120), font, 3, (0,255,0), 2)


    resize = cv2.resize(img,(900,700))

    # cv2.imshow('Video', img)
    cv2.imshow('Video', resize)

    # cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', POINTS)

    out.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # key = cv2.waitKey(1)
    # if key==27:
    #     break

cap.release()
cv2.destroyAllWindows()


# Image

# img = cv2.imread('Picture/sample.jpg')

# height, width, _ = img.shape

# blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0,0,0), swapRB=True, crop=False)
# net.setInput(blob)
# output_layers_names = net.getUnconnectedOutLayersNames()
# layerOutputs = net.forward(output_layers_names)

# boxes = []
# confidences = []
# class_ids = []

# for output in layerOutputs:
#     for detection in output:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.2:
#                 center_x = int(detection[0]*width)
#                 center_y = int(detection[1]*height)
#                 w = int(detection[2]*width)
#                 h = int(detection[3]*height)

#                 x = int(center_x - w/2)
#                 y = int(center_y - h/2)

#                 boxes.append([x, y, w, h])
#                 confidences.append((float(confidence)))
#                 class_ids.append(class_id)

# indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

 
# for i in indexes.flatten():
#         x, y, w, h = boxes[i]
#         label = str(classes[class_ids[i]])
#         confidence = str(round(confidences[i],2))
#         color = colors[i]
#         cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
#         cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)

# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

