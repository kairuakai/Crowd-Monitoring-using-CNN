
# Original Code

import cv2
from tracker import *
import numpy as np
import time
from time import ctime
import datetime
import os
import csv
import math
from openpyxl import Workbook
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment


# Hover Coordinates using mouse
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)

# Printing Coordinates and lines
# prevX,prevY = -1,-1
# def POINTS(event, x, y, flags, param):
#     global prevX,prevY
#     if event == cv2.EVENT_LBUTTONDOWN :  
#         cv2.circle(img,(x,y),3,(255,255,255),-1)
#         strXY = '(' + str(x) + ',' + str(y) + ')'
#         font = cv2.FONT_HERSHEY_PLAIN
#         cv2.putText(img,strXY,(x+10,y-10),font,1,(255,255,255))
#         if prevX == -1 and prevY == -1:
#             prevX,prevY = x,y
#         else:
#             cv2.line(img,(prevX,prevY),(x,y),(0,0,255),5)
#             prevX,prevY = -1,-1
        
#         cv2.imshow("image",img)
       

# Printing Coordinate
# def POINTS(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE :  
#         colorsBGR = [x, y]
#         print(colorsBGR)




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


# Save Excel File
def getXlsxNameWithDate(nameIn="info.xlsx"):
   
    if not nameIn.endswith(".xlsx"):
        raise ValueError("filename must end on .xlsx")

    filename = nameIn.replace(".xlsx","_{0}.xlsx").format(datetime.datetime.now().strftime("%m-%d-%Y"))

    if os.path.isfile(filename):             # if already exists
        fn2 = filename[0]+'_{0}.xlsx'          # modify pattern to include a number
        count = 1
        while os.path.isfile(fn2.format(count)): # increase number until file not exists
            count += 1
        return fn2.format(count)                 # return file with number in it

    else:                                    # filename ok, return it
        return filename


net = cv2.dnn.readNet('yolov4-tiny-custom_last.weights', 'yolov4-tiny-custom.cfg')
# net = cv2.dnn.readNet('yolov3_training_last.weights', 'yolov3_testing.cfg')
# net = cv2.dnn_DetectionModel('yolov3_training_last.weights', 'yolov3_testing.cfg')
pTime = 0
count = 0
count_down = 0
c_count = 0
frame_count= 0

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


filename = 'output_{0}.avi'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# Tracking object
tracker = Tracker()
list = []

# Polyline
# area = [(1185,855),(1185,920),(1097,916),(1093,841)]
# area = [(823,695),(884,620),(748,627),(652,675)]
# area = np.array([(938,849),(938,162),(604,121),(771,953)], np.int32)\

# Polylines for people in mall
# area = np.array([(717,493),(852,491),(876,571),(741,579)], np.int32)

# Polyline for people in school
# area = np.array([(1092,767),(1109,861),(1296,851),(1287,701)], np.int32)
# area = [(829,815),(834,843),(976,837),(969,821)]
# area = [(829,815),(844,946),(989,933),(977,836)]
area = [(3,667),(3,663),(1603,679),(1603,682)]
# area = [(3,667),(3,683),(1603,679),(1603,652)]
area_circ = set()



classes = []
with open("obj.names", "r") as f:
    classes = f.read().splitlines()

# Real time camera and video
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("rtsp://admin:Coronel_123456@192.168.1.64:554/Streaming/Channels/101")
# cap = cv2.VideoCapture('Video/walking_people.mp4')
# cap = cv2.VideoCapture('Video/person_Trim.mp4')
# cap = cv2.VideoCapture('Video/walking_Trim.mp4')
cap = cv2.VideoCapture('Video/cctv.1.avi')
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
    frame_count += 1
    # Convert grayscale
    blur = cv2.blur(img,(3,3))
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    # End of Convert grayscale

    center_points_cur_frame = []
    # Original (320,320)
    # Latest (215,215)
    blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    # Draw Line
    # cv2.line(img,(0,int(img.shape[0]/2)+3),(int(img.shape[1]), int(img.shape[0]/2)+3),(0,0,100),5)
    cv2.line(img,(0,height-400),(width,height-400),(0,128,0),2)
    # cv2.line(img,(0,height-180),(width,height-180),(0,128,0),2)
    # cv2.polylines(img,[np.array(area,np.int32)],True,(0,255,0),2)

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
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
    # print("Indexes : ", len(indexes))
    if len(indexes) >=5:
        cv2.putText(img,'Warning Crowded!', (20,200), font, 3, (0,0,255), 3)
        c_count += 1
        # print("Crowd Count : ", c_count)

        # print("CROWDED Warning")

    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            # print("Frame No.", frame_count," ", x,y,w,h)
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]

            # Center Points
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            crowd_count = cx,cy   
            center_points_cur_frame.append((cx,cy))
        

            # End of Center Points

            person = int(y+h/2)
            lineCy = height-350
            # lineCy = 3*height/6+height/30

            if(person<lineCy+6 and person>lineCy-6):
                count = count + 1
                # print(count)
                cv2.line(img,(0,height-400),(width,height-400),(255,0,0),2)
                # print(ctime())
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)

                tup1 = str(count)
                tup2 = (ctime())

                work_book = Workbook()
                work_sheet = work_book.active
                header = ["Total People","Crowd Count","Date"]
                rows = range(1, 3)
                columns = range(1, 3)
                work_sheet.append(header)
                work_sheet.append([tup1,c_count,tup2])
                for row in rows:
                    for col in columns:
                        work_sheet.cell(row, col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True,)
                       


                # work_sheet.append(header)
                # work_sheet.append([tup1,c_count,tup2])
                # work_sheet.append([tup2])
                work_book.save(f'Database/{getXlsxNameWithDate("info.xlsx")}')
            if (person>lineCy+6 and person<lineCy-6):
                 count = count - 1
            # list.append([x,y,w,h])
            # id_boxes = tracker.update(list)
            # # print("Person Id", id_boxes)

            # for id_box in id_boxes:
            #     x,y,w,h,id = id_box
                # print("Person Id", id)

            
            cv2.circle(img,(cx,cy),5,(0,255,0),-1)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)
            cv2.putText(img, label + " " + str(confidence), (x, y-15), font, 1.2, (255,255,255), 2)
            # final_result = cv2.pointPolygonTest(np.array(area,np.int32), (int(cx),int(cy)),False)
            # # print(final_result)
            # if final_result > 0:
            #    area_circ.add(id)
            #    print(ctime())

            # count_peps = len(area_circ)
            # if count_peps >=2 and count_peps <=5:
                
            #     cv2.putText(img,'(Warning!)', (280,120), font, 3, (0,234,255), 3)
            # elif count_peps >= 6 :
                
            #     cv2.putText(img,'(Danger!)', (280,120), font, 3, (0,0,255), 3)

            # with open("Database/info.csv", mode="a") as csvfile:
            #     tup1 = (count_peps,current_time)
            #     tup2 = (ctime())
                    
            #     writer = csv.writer(csvfile,delimiter='\t')
            #     writer.writerows(str(tup1))
              
            # print(len(area_circ))


    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,50), cv2.FONT_HERSHEY_PLAIN,3, (0,255,0),3)
    # cv2.putText(img,f'People: {str(count)}', (20,120), font, 3, (0,255,0), 2)
    cv2.putText(img,f'People: {str(count)}', (20,140), font, 3, (0,255,0), 3)


    resize = cv2.resize(img,(900,700))

    # cv2.imshow('Video', img)
    cv2.imshow('Video', resize)

    # cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', POINTS)

    out.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
