# Cross-Platform Virtual Camera using Python
The app is dedicated to spawn and use virtual camera on Windows and Linux

## Usage
```py
from virtual_camera import CameraController
import numpy as np
import sys

# Create camera controller
fps = 20
width = 1280
height = 720
app = CameraController(1, width, height, fps)
app.start()

# Create an image to test the app
image = np.zeros((height, width, 3), np.uint8)

# Run the app
while app.is_alive():
    try:
        app.show(image, 0)
    except :
        app.stop()
        break
```

## Installation
This package works on Windows and Linux (no version for Mac OS). Install it from PyPI with:

```sh
pip install -i https://test.pypi.org/simple/ virtual-camera
```