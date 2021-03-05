import os
import argparse
import cv2
import sys
import time

# Import the suitable camera interface
if os.name == 'nt':
	from win_camera import WinCamera as Camera
elif os.name == 'posix':
	from unix_camera import UNIXCamera as Camera
else:
    raise ImportError(
        "Sorry: no implementation for \
		 your platform ('{}') available".format(os.name))

class Application :
	_cameras = list()			# List of used cameras

	'''
	Constructor which takes camera parameters and the amount of the devices
	'''
	def __init__(self, number, path, width, height, fps, device = "/dev/video1"):
		for index in range(number):
			if os.name == 'nt':
				camera = Camera(width, height, fps)
			elif os.name == 'posix':
				camera = Camera(width, height, fps, device)

			# Start the thread
			camera.start()

			# Add the thead to the list
			self._cameras.append(camera)

	def run(self):
		# Read the image
		try :
			pass
			#image = cv2.imread( # FIXME )
			#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
		except cv2.error:
			print("Image not found. Closing the app...")
			self.stop()

		# Send images to cameras' queues
		try : 
			for index in range(len(self._cameras)):
				camera = self._cameras[index]

				# Send the image to the camera
				camera._queue.put(image)

				# Remove the cameras which are stopped
				if not camera.is_alive():
					self._cameras.remove(camera)
		
		except (KeyboardInterrupt, SystemExit):
			self.stop()

		'''
		Stop the execution and kill all the camera threads
		'''
	def stop(self):
		for index in range(len(self._cameras)):
			self._cameras[index].stop()

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
	app = Application(number, path, width, height, fps)
	try :
		app.run()
	
	# Stop all the threads after catching an exception in the main thread
	except Exception as e :
		print("An exception occured : " + str(e))
		app.stop()

	print("App closed!")

if __name__ == "__main__":
	main()