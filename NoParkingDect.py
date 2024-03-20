import cv2
import datetime
from time import sleep
car_cascade= cv2.CascadeClassifier('C:\\Users\\Lenovo\\OneDrive\\Desktop\\BBB\\NO-PARKING-ZONE-MONITORING-MODLE-main\\cars.xml')
cap= cv2.VideoCapture('C:\\Users\\Lenovo\\OneDrive\\Desktop\\BBB\\NO-PARKING-ZONE-MONITORING-MODLE-main\\car1.mp4')
while True:
        ret ,frame= cap.read()
        original_frame= frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 4)
        for (x,y,w,h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cars_roi=frame[y:y+h,x:x+w]
            gray_roi=frame[y:y+h,x:x+w]
            car=car_cascade.detectMultiScale(gray_roi,1.1,4)
            for x1,y1,h1,w1 in car:
                cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 2)
                time_stamp= datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                file_name=f'car-{time_stamp}.jpg'
                cv2.imwrite(file_name, original_frame)
        cv2.imshow('cam',frame)
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
