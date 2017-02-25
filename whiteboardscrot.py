import sys
from math import hypot, sqrt
import numpy as np
import cv2

class WhiteboardScrot:
	def __init__(self,winName,points=[],width=1920,height=1080):
		self.windowName = winName
		self.window = cv2.namedWindow(self.windowName)
		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
		self.width = width
		self.height = height
		self.calibrationPoints = points
		self.calibrated = False
		self.debugMode = False

		if len(self.calibrationPoints) == 4:
			self.updateCalibration()
		elif len(self.calibrationPoints) != 0:
			print('Calibration points should either be empty or have four points')

		cv2.setMouseCallback(self.windowName, self.mouseHandler, 0)

		while(True):
			ret, frame = self.cap.read()

			# frame = cv2.flip(frame, 0)
			frame = cv2.flip(frame, 1)
			if self.calibrated:
				frame = cv2.warpPerspective(
					frame,self.perspectiveMap,(self.width,self.height))

			cv2.imshow(self.windowName,frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		self.cap.release()
		cv2.destroyAllWindows()

	def updateCalibration(self):
		if len(self.calibrationPoints) != 4:
			print("Can't calibrate without four points")
			return
		else:
			if self.debugMode: print('calibrating')

		# We need to use our points as numpy floats for oru calculations
		calibrationFloats = np.float32(self.calibrationPoints)

		 # First lets ensure that the points are ordered correctly
		pointSums = calibrationFloats.sum(axis=1)
		pointDiffs = np.diff(calibrationFloats, axis=1)

		# Here we'll use sums and difference of points to find which end of
		# the square they belong to
		tl = calibrationFloats[np.argmin(pointSums)]
		tr = calibrationFloats[np.argmin(pointDiffs)]
		br = calibrationFloats[np.argmax(pointSums)]
		bl = calibrationFloats[np.argmax(pointDiffs)]

		# Currently skewing towards minimum side lengths,
		# need to test whether using min vs max matters for quality
		self.width =  int(min(hypot(tr[0]-tl[0], tr[1]-tl[1]),
						 hypot(br[0]-bl[0], br[1]-bl[1])))
		self.height = int(min(hypot(bl[0]-tl[0], bl[1]-tl[1]),
						 hypot(br[0]-tr[0], br[1]-tr[1])))

		self.perspectiveMap = cv2.getPerspectiveTransform(
			np.float32((tl,tr,br,bl)),
			np.float32(((0, 0), (self.width, 0), (self.width, self.height), (0, self.height)))
		)

		self.calibrated = True

	def mouseHandler(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			if len(self.calibrationPoints) < 4:
				self.calibrationPoints.append((x,y))
			if self.debugMode: print(self.calibrationPoints)

			if len(self.calibrationPoints) == 4:
				self.updateCalibration()
		elif event == cv2.EVENT_RBUTTONDOWN:pass
		elif event == cv2.EVENT_RBUTTONUP:pass
		elif event == cv2.EVENT_LBUTTONUP:pass
		elif event == cv2.EVENT_MOUSEMOVE:pass

ws = WhiteboardScrot('Whiteboard Scrot')