import cv2, time
from datetime import datetime 
import pandas

camera_port = 0
status_list = [None,None]
time = []
first_frame = None
df = pandas.DataFrame(columns = ["Start","End"])
video = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc(*"DIVX")
rec = cv2.VideoWriter("Processed_video.avi",fourcc,34.2,(640,480))
# a=0
while True:
    # a= a+1
    check, frame=video.read()
    #print(check)
    #print(frame)
    #time.sleep(3)
    status = 0
    gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_img = cv2.GaussianBlur(gray_img,(21,21),0)
    if first_frame is None:
        first_frame = gray_img
    


    delta_frame = cv2.absdiff(first_frame,gray_img)
    threshold_frame = cv2.threshold(delta_frame,40,255,cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(threshold_frame,None,iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contours in cnts:
        if cv2.contourArea(contours) < 10000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contours)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    
    status_list.append(status)
    if status_list[-1]==1 and status_list[-2]==0:
        time.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        time.append(datetime.now())


    cv2.imshow("Gray Frame",gray_img)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color",frame)
    rec.write(frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        if status == 1:
            time.append(datetime.now())
        rec.release()
        break
    print(status)


print(status_list)
print(time)

for i in range(0,len(time),2):
    df = df.append({"Start":time[i],"End":time[i+1]},ignore_index=True)
    
    
df.to_csv("Timespan.csv")

# print(a)

video.release()
cv2.destroyAllWindows()