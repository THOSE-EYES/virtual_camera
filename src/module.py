import os
import argparse
import cv2

if os.name == 'nt':
	from win_camera import WinCamera as Camera
elif os.name == 'posix':
	from unix_camera import UNIXCamera as Camera
else:
    raise ImportError(
        "Sorry: no implementation for \
		 your platform ('{}') available".format(os.name))

class Application :
	_cameras = list()

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
		# Get image
		image = cv2.imread("test.png")
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		#
		while not len(self._cameras) == 0:
			for index in range(len(self._cameras)):
				self._cameras[index]._queue.put(image)

				if not self._cameras[index].is_alive():
					self._cameras.remove(self._cameras[index])

def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--number", help="number of cameras to spawn")
	parser.add_argument("-p", "--path", help="path to a folder with pictures to show")
	parser.add_argument("-w", "--width", help="width of the picture to show")
	parser.add_argument("-a", "--height", help="height of the picture to show")
	parser.add_argument("-f", "--fps", help="speed of frame change")
	if os.name == 'posix':
		parser.add_argument("-d", "--device", help="path to a spawned device")
	args = parser.parse_args()

	# Get the arguments
	number = int(args.number)
	width = int(args.width)
	height = int(args.height)
	fps = int(args.fps)
	device = args.device
	path = args.path

	# Start the app
	app = Application(number, path, width, height, fps)
	app.run()

	print("App closed!")

if __name__ == "__main__":
	main();