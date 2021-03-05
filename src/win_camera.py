import pyvirtualcam
import camera
import cv2

'''
The class is dedicate to cover the Windows implementation of 
the virtual camera to use the package as a cross-platform
solution. It can spawn a virtual camera and show images or
videos to the apps using this camera 
'''
class WinCamera(camera.Camera):
	'''
	Constructor for a Windows-based implementation of
	the package
	'''
	def __init__(self, width, height, fps):
		super().__init__(width, height, fps)

		# Spawn the camera
		self.__spawn()

	'''
	Spawn the camera
	'''
	def __spawn(self):
		self._camera = pyvirtualcam.Camera(width=self._width, height=self._height, fps=self._fps)
		print ("Camera spawned!")

	'''
	Show the image on the virtual camera
	'''
	def __show(self, image):
		# Resize the image to fit the camera
		image = cv2.resize(image, (self._width, self._height), interpolation = cv2.INTER_AREA)

		# Send the image
		self._camera.send(image)

		# Sleep until the next frame time
		self._camera.sleep_until_next_frame()

	'''
	Thread execution method
	'''
	def run(self):
		# Run while not stopped 
		while not self._isStopped :
			# Check if the queue is empty
			if not self._queue.empty():
				# Show the image
				self.__show(self._queue.get())