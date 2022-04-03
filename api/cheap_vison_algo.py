import threading
import time
import cv2
import numpy as np

from serial_monitor import SerialMonitor

class PersonDestroyer():
    def __init__(self, serial : SerialMonitor, videoNumber : int):
        self.serial_monitor = serial

        # self.hog = cv2.HOGDescriptor()
        # self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.last_halt = 0
        self.videoNumber = videoNumber

        # open webcam video stream

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

    def start(self, showImg = False):
        self.cap = cv2.VideoCapture(self.videoNumber)

        # the output will be written to output.avi
        self.out = cv2.VideoWriter(
            'output.avi',
            cv2.VideoWriter_fourcc(*'MJPG'),
            15.,
            (640, 480))
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        while True:
            while (True):
                # Capture frame-by-frame
                ret, frame = self.cap.read()

                # resizing for faster detection
                frame = cv2.resize(frame, (640, 480))
                # using a greyscale picture, also for faster detection
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)


                faces = self.face_cascade.detectMultiScale(gray, 1.2, 3)

                cv2.line(frame, (320, 0), (320, 480), (255, 255, 0), 2)
                for (x,y,w,h) in faces:
                    xA, yA, xB, yB = x, y, x+w, y+h
                    # display the detected boxes in the colour picture
                    cv2.rectangle(frame, (xA, yA), (xB, yB),
                                  (0, 255, 0), 2)
                    # print((xA, yA), (xB, yB))

                    middleX, middleY = int((xA + xB) / 2), int((xB + yB) / 2)


                    print(middleX)
                    cv2.line(frame, (middleX, 0), (middleX, 480),  (0, 255, 255), 2)


                    shift = (middleX - 320)


                    self.__update_turret(shift)
                    break

                if len(faces) ==0:
                    if time.time() - self.last_halt >10:
                        self.serial_monitor.stop()
                        self.last_halt = time.time()


                else:
                    self.last_halt = 0
                #
                # # Write the output video
                # self.out.write(frame.astype('uint8'))
                # # Display the resulting frame
                if showImg:
                    cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            self.cap.release()
            # and release the output
            self.out.release()
            # finally, close the window
            cv2.destroyAllWindows()
            cv2.waitKey(1)
