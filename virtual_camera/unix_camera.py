import pyfakewebcam
from virtual_camera.camera import Camera
import time
import cv2
import logging

'''
The class is dedicate to cover the UNIX implementation of 
the virtual camera to use the package as a cross-platform
solution. It can spawn a virtual camera and show images or
videos to the apps using this camera 
'''
class UNIXCamera(Camera):
	'''
	Constructor for a UNIX-based implementation of
	the package
	'''
	def __init__(self, width, height, fps, device):
		super().__init__(width, height, fps)

		# Set the internal fields
		self.__setDevice(device)

		# Spawn the camera
		self.__spawn()

	'''
	Spawn the camera
	'''
	def __spawn(self):
		try:
			self._camera = pyfakewebcam.FakeWebcam(self._device, self._width, self._height)
			logging.info("Camera spawned!")

		except RuntimeError:
			# Stop the thread
			self.stop()

			# Log the error
			logging.error("Camera was not spawned!")

	'''
	Show the image on the virtual camera
	'''
	def __show(self, image):
		acquire()
		# Resize the image to fit the camera
		image = cv2.resize(image, (self._width, self._height), interpolation = cv2.INTER_AREA)

		# Send the image
		self._camera.schedule_frame(image)

		# Sleep until the next frame time
		time.sleep(1 / self._fps)

	'''
	Set virtual camera's device name 
	'''
	def __setDevice(self, value):
		# Sanity check
		if not value == "":
			logging.error("Device parameter is empty")
			raise RuntimeError("Device parameter is empty")

		self._device = value

	'''
	Thread execution method
	'''
	def run(self):
		# Run while not stopped 
		while not self._stop_event.is_set(): 
			# Check if the queue is empty
			if not self._queue.empty():
				# Show the image
				self.__show(self._queue.get())