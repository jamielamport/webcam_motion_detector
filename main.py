import cv2
import time
from emailing import sendEmail

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = [0, 0]

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    #cv2.imshow("My Video", gray_frame_gau)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    #cv2.imshow("my Video", delta_frame)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY_INV)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    #cv2.imshow("my Video", thresh_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in  contours:
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # Object has disappeared
        sendEmail()

    print(status_list)


    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()



