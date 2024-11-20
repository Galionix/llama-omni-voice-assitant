import cv2

web_cam = cv2.VideoCapture(0)

if not web_cam.isOpened():
    print("Cannot open camera")
    exit()

path = 'webcam.jpg'
# while True:
#     ret, frame = web_cam.read()
#     cv2.imshow("WebCam", frame)

#     if cv2.waitKey(1) == 27:
#         break

ret, frame = web_cam.read()
cv2.imwrite(path, frame)
# cv2.destroyAllWindows()
web_cam.release()
