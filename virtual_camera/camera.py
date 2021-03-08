from abc import abstractmethod
import threading
import numpy
from queue import Queue
import logging

class Camera(threading.Thread) :
	_queue = Queue()
	_stop_event = threading.Event()
	_lock = threading.Lock()

	'''
	Constructor that takes the width and the height of the camera
	'''
	def __init__(self, width, height, fps):
		threading.Thread.__init__(self, args=(), kwargs=None)

		# Set camera preferences
		self.__setHeight(height)
		self.__setWidth(width)
		self.__setFPS(fps)

	'''
	A system-specific way to show image as camera's output
	'''
	@abstractmethod
	def __show(self, image):
		return

	'''
	Thread execution method
	'''
	@abstractmethod
	def run(self):
		return

	'''
	A system-specific way to spawn a camera
	'''
	@abstractmethod
	def __spawn(self):
		return

	'''
	Set the width of the camera view
	'''
	def __setWidth(self, value):
		# Sanity check
		if value <= 0:
			raise RuntimeError("Width can't be negative")

		self._width = value

	'''
	Set the height of the camera view
	'''
	def __setHeight(self, value):
		# Sanity check
		if value <= 0:
			raise RuntimeError("Height can't be negative")

		self._height = value

	'''
	Set the desired FPS value
	'''
	def __setFPS(self, value):
		# Sanity check
		if value <= 0:
			raise RuntimeError("FPS can't be negative")

		self._fps = value

	'''
	Stop thread's execution
	'''
	def stop(self):
		self._stop_event.set()