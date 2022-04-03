import threading
import time
import cv2
import numpy as np

from serial_monitor import SerialMonitor

class PersonDestroyer():
    def __init__(self, serial : SerialMonitor, videoNumber : int):
        self.serial_monitor = serial

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        cv2.startWindowThread()

        # open webcam video stream
        self.cap = cv2.VideoCapture(videoNumber)

        # the output will be written to output.avi
        self.out = cv2.VideoWriter(
            'output.avi',
            cv2.VideoWriter_fourcc(*'MJPG'),
            15.,
            (640, 480))
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    def __update_turret(self, shift):
        print(shift)
        if abs(shift) < 10:
            print("center")
            self.serial_monitor.stop()
        else:
            if shift > 0:
                self.serial_monitor.right()
                print("right")
            else:
                print("left")
                self.serial_monitor.left()

    def __start(self):
        while True:
            while (True):
                # Capture frame-by-frame
                ret, frame = self.cap.read()

                # resizing for faster detection
                frame = cv2.resize(frame, (640, 480))
                # using a greyscale picture, also for faster detection
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                lower = np.array([22, 93, 0])
                upper = np.array([80, 255, 255])

                mask = cv2.inRange(frame, lower, upper)  # modify your thresholds

                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # The black region in the mask has the value of 0,
                # so when multiplied with original image removes all non-blue regions

                result = cv2.bitwise_and(frame, frame, mask=mask)

                for cnt in contours:

                    x, y, w, h = cv2.boundingRect(cnt)
                    xA, yA, xB, yB = x, y, x + w, y + h
                    # display the detected boxes in the colour picture
                    cv2.rectangle(frame, (xA, yA), (xB, yB),
                                      (0, 255, 0), 2)
                     # print((xA, yA), (xB, yB))

                    middleX, middleY = int((xA + xB) / 2), int((xB + yB) / 2)


                    print(middleX)
                    cv2.line(frame, (middleX, 0), (middleX, 480),  (0, 255, 255), 2)

                    break;


                    # detect people in the image
                # returns the bounding boxes for the detected objects

                # faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                #
                # cv2.line(frame, (320, 0), (320, 480), (255, 255, 0), 2)
                # for (x,y,w,h) in faces:
                #     xA, yA, xB, yB = x, y, x+w, y+h
                #     # display the detected boxes in the colour picture
                #     cv2.rectangle(frame, (xA, yA), (xB, yB),
                #                   (0, 255, 0), 2)
                #     # print((xA, yA), (xB, yB))
                #
                #     middleX, middleY = int((xA + xB) / 2), int((xB + yB) / 2)
                #
                #
                #     print(middleX)
                #     cv2.line(frame, (middleX, 0), (middleX, 480),  (0, 255, 255), 2)
                #
                #
                #     shift = (middleX - 320)
                #
                #
                #     self.__update_turret(shift)
                #     break
                #
                # if len(faces) ==0:
                #     self.serial_monitor.stop()
                #
                # # Write the output video
                # self.out.write(frame.astype('uint8'))
                # # Display the resulting frame
                cv2.imshow('frame', frame)
                cv2.imshow('mask', mask)

                cv2.imshow('result', result)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            self.cap.release()
            # and release the output
            self.out.release()
            # finally, close the window
            cv2.destroyAllWindows()
            cv2.waitKey(1)
    def start(self):
        a_thread = threading.Thread(target=self.__start(), args=(1,))
        a_thread.start()