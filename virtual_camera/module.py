import os
import argparse
import cv2
import sys
import time
import glob
import logging
import threading

# Import the suitable camera interface
if os.name == 'nt':
	from virtual_camera.win_camera import WinCamera as Camera
elif os.name == 'posix':
	from virtual_camera.unix_camera import UNIXCamera as Camera
else:
    raise ImportError(
        "Sorry: no implementation for \
		 your platform ('{}') available".format(os.name))

class CameraController(threading.Thread) :
	_cameras = list()			# List of used cameras
	_stop_event = threading.Event()
	_lock = threading.Lock()

	'''
	Constructor which takes camera parameters and the amount of the devices
	'''
	def __init__(self, number, width, height, fps, device = "/dev/video1"):
		threading.Thread.__init__(self, args=(), kwargs=None)

		for index in range(number):
			if os.name == 'nt':
				camera = Camera(width, height, fps)
			elif os.name == 'posix':
				camera = Camera(width, height, fps, device)
		
			# Add the thead to the list
			self._cameras.append(camera)

	'''
	Start the thread
	'''
	def run(self):
		try :
			# Run camera threads
			self.__startCameraThreads()

			# Main loop
			while (not self._stop_event.is_set()) and (len(self._cameras) != 0):
				# Check if cameras are running
				self.__checkCameraThreads()
		except:
			self.stop()

	'''
	Start camera threads
	'''
	def __startCameraThreads(self):
		# Start camera threads
		for index in range(len(self._cameras)):
			camera = self._cameras[index]
			camera.start()

	'''
	Check if cameras are running and remove it otherwise
	'''
	def __checkCameraThreads(self):
		for index in range(len(self._cameras)):
			camera = self._cameras[index]

			# Delete a camera if it hasn't started
			if not camera.is_alive():
				self._cameras.remove(camera)

	'''
	Show the picture on the camera
	'''
	def show(self, image, index):
		# Create a lock
		self._lock.acquire()

		try :
			# Check if the index is not out of range
			if index > len(self._cameras):
				# Stop the app
				self.stop()

				# Throw an exception
				logging.error("Camera index is out of range")
				raise RuntimeError("Camera index is out of range")

			# Send the image to the camera
			camera = self._cameras[index]
			camera._queue.put(image)

			# Release the lock
			if (self._lock.locked()):
				self._lock.release()

		# Stop all the threads after catching an exception
		except:
			# Stop the app
			self.stop()

			# Throw the exception to the main app
			logging.exception("An exception occured!")

	'''
	Stop the execution and kill all the camera threads
	'''
	def stop(self):
		logging.info("Stopping...")

		# Stop the main loop
		self._stop_event.set()

		# Stop the cameras
		for index in range(len(self._cameras)):
			logging.info("Stopping the camera : " + str(index))

			# Stop camera nodes
			self._cameras[index].stop()
			self._cameras[index].join()

		# Release the lock 
		if (self._lock.locked()):
			self._lock.release()

		logging.info("App was closed!")
	
def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--number", help="number of cameras to spawn",
						type=int, default=1, choices=[1, 2, 3, 4])
	parser.add_argument("-p", "--path", help="path to a folder with pictures to show")
	parser.add_argument("--width", help="width of the picture to show", type=int)
	parser.add_argument("--height", help="height of the picture to show", type=int)
	parser.add_argument("-f", "--fps", help="speed of frame change", type=int, default=30)
	if os.name == 'posix':
		parser.add_argument("-d", "--device", help="path to a spawned device")
	args = parser.parse_args()

	# Get the arguments
	number = args.number
	width = args.width
	height = args.height
	fps = args.fps
	path = args.path
	if os.name == 'posix':
		device = args.device

	# Start the app
	app = CameraController(number, width, height, fps)
	app.start()

	# FIXME : add the ability to show pictures here

	logging.info("App was closed!")

if __name__ == "__main__":
	main()