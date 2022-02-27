
'''
General file description.
'''
# ------------------------- DEFINE IMPORTS ---------------------------
from __future__ import print_function
from datetime import datetime
import argparse

import numpy as np
import cv2
import imutils


# ------------------------- DEFINE ARGUMENTS -------------------------
# argParser.add_argument("-a", "--min-area", type=int, default=500, help="Minimum area size before motion detection")
#argParser.add_argument('--ononly', dest='ononly', action='store_true', help="Disable turning lights off command")
#argParser.add_argument('--remote', dest='interactive', action='store_false', help="Disable Pi hardware specific functions")
#argParser.set_defaults(interactive=True)

argParser = argparse.ArgumentParser()
argParser.add_argument('--quiet', dest='quiet', action='store_true', help="Disable logging")
argParser.add_argument("-f", "--log-file", default=None, help="Specify file to log to.")
argParser.set_defaults(quiet=False)

args = vars(argParser.parse_args())
quiet = args["quiet"]
logFileName = args["log_file"]

# ------------------------- DEFINE GLOBALS ---------------------------

# ------------------------- DEFINE FUNCTIONS -------------------------
def log(text, displayWhenQuiet = False):
    if displayWhenQuiet or not quiet:
        now = datetime.now().strftime("%x %X")
        message = f"{now}: {text}"
        if logFileName is not None:
            with open(f"/home/pi/Project/{logFileName}", "a") as fout:
                fout.write(f"{message}\n")
        else:
            print(message)

def alrt(text):
    log(text, True)

# ------------------------- DEFINE INITIALIZE ------------------------
log("Initializing...", displayWhenQuiet = True)
log(f"Args: {args}", displayWhenQuiet = True)

input = cv2.VideoCapture('MantidLaserTestVideo.mp4');

laserLower = (189, 61, 145)
laserUpper = (248, 204, 245)

# Frame 220 - 224 is the laser


# ------------------------- DEFINE RUN -------------------------------
log("Initialized!", displayWhenQuiet = True)
log("Running...", displayWhenQuiet = True)

frame_count = 0

try:
    log("Run")

    if (input.isOpened() == False):
        alrt('Error opening file')

    fps = input.get(cv2.CAP_PROP_FPS)
    log("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    while (input.isOpened()):
        valid, frame = input.read()
        frame_count = frame_count + 1

        if (valid == True):
            if (frame_count > 218):    
                frame = imutils.resize(frame, width=480, height=480)
                cv2.putText(frame, f"Frame: {frame_count}", (0,720), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

                # find the colors within the specified boundaries and apply the mask
                mask = cv2.inRange(frame, laserLower, laserUpper)
                output = cv2.bitwise_and(frame, frame, mask = mask)

                cv2.imshow("images", np.hstack([frame, output]))
                cv2.imshow('Frame', frame)
                key = cv2.waitKey(0)
                if key & 0xFF == ord('q'):
                    break
                if key & 0xFF == ord('s'):
                    cv2.imwrite('laser.png', frame)
                    alrt('Image saved!')
        else:
            alrt('End reached!')
            break



    input.release()
    cv2.destroyAllWindows()
    log(f"Played {frame_count} frames")

except KeyboardInterrupt:
    log("KeyboardInterrupt caught! Cleaning up...")