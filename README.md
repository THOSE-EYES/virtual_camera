# Cross-Platform Virtual Camera using Python
The app is dedicated to spawn and use virtual camera on Windows and Linux

## Usage
```py
from virtual_camera import CameraApplication
import numpy as np
import sys

width = 1280
height = 720
fps = 20
image = np.zeros((height, width, 3), np.uint8)

try :
	app = CameraApplication(1, width, height, fps)
except (KeyboardInterrupt, SystemExit, RuntimeError):
	print ("Couldn't start the app")
	sys.exit(-1)

try:
	while True:
		app.show(image, 0)
except (KeyboardInterrupt, SystemExit, RuntimeError, Exception):
	print ("The app crashed")
	app.stop()
	sys.exit(-1)
```

## Installation
This package works on Windows and Linux (no version for Mac OS). Install it from PyPI with:

```sh
pip install -i https://test.pypi.org/simple/ virtual-camera
```