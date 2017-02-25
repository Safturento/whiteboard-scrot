import sys
from math import hypot, sqrt
import numpy as np
import cv2

calibrationPoints = []
winName = 'Whiteboard Scrot'
debugMode = True

def mouseHandler(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(calibrationPoints) < 4:
            calibrationPoints.append((x,y))
        if debugMode: print(calibrationPoints)
    elif event == cv2.EVENT_RBUTTONDOWN:pass
    elif event == cv2.EVENT_RBUTTONUP:pass
    elif event == cv2.EVENT_LBUTTONUP:pass
    elif event == cv2.EVENT_MOUSEMOVE:pass


def transformImage(image, points):
    # First lets ensure that the points are ordered correctly
    pointSums = points.sum(axis=1)
    pointDiffs = np.diff(points, axis=1)

    # Here we'll use sums and difference of points to find which end of
    # the square they belong to
    tl = points[np.argmin(pointSums)]
    tr = points[np.argmin(pointDiffs)]
    br = points[np.argmax(pointSums)]
    bl = points[np.argmax(pointDiffs)]

    # Currently skewing towards minimum side lengths,
    # need to test whether using min vs max matters for quality
    width =  int(min(hypot(tr[0]-tl[0], tr[1]-tl[1]),
                     hypot(br[0]-bl[0], br[1]-bl[1])))
    height = int(min(hypot(bl[0]-tl[0], bl[1]-tl[1]),
                     hypot(br[0]-tr[0], br[1]-tr[1])))

    return cv2.warpPerspective(
        image,
        cv2.getPerspectiveTransform(
            np.float32(
                (tl,tr,br,bl)
            ),
            np.float32((
                (0,     0),
                (width, 0),
                (width, height),
                (0,     height)
            ))
        ),
        (width,height))

def initialize(**kwargs):
    window = cv2.namedWindow(winName)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv2.setMouseCallback(winName, mouseHandler, 0)

    while(True):
        ret, frame = cap.read()

        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)
        if 'points' in kwargs:
            frame = transformImage(frame, kwargs['points'])
        elif len(calibrationPoints) == 4:
            frame = transformImage(frame, np.float32(calibrationPoints))

        cv2.imshow(winName,frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

initialize()